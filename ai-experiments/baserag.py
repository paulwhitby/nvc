"""Abstract base class for PDF RAG systems."""

import multiprocessing
import os
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from threading import Lock
from typing import Callable, Dict, List, Optional


@dataclass
class LLMConfig:
    """All parameters that govern LLM behaviour."""
    model: str
    api_key: Optional[str] = None
    temperature: float = 0.0
    max_tokens: int = 2048
    system_prompt: str = (
        "You are a helpful assistant that answers questions based solely "
        "on the provided context. If the context does not contain enough "
        "information, say so."
    )
    user_prompt_template: str = (
        "Context:\n{context}\n\n"
        "Question: {query}\n\n"
        "Answer:"
    )
    summarize_prompt_template: str = (
        "Write a concise summary of the following text:\n\n{text}\n\nSUMMARY:"
    )
    compare_prompt_template: str = (
        "Compare how the following document excerpts address the topic: {topic}\n\n"
        "Analyse the different perspectives and information provided by each source.\n\n"
        "{text}\n\nCOMPARISON:"
    )


@dataclass
class RAGConfig:
    """Parameters that govern ingestion and retrieval."""
    embedding_model: str
    chunk_size: int = 512
    chunk_overlap: int = 64
    top_k: int = 3


@dataclass
class IngestionResult:
    """Result returned by every ingest_* method."""
    source_id: str
    status: str           # 'success' | 'error'
    chunks: int = 0
    error: Optional[str] = None


class BaseRAG(ABC):
    """
    Abstract base class for multi-document PDF RAG systems.

    Provider-specific (must be implemented by subclasses):
      _init_embedding_model, _embed
      _init_vector_store, _upsert, _search, _search_in_source,
      save_vector_store, load_vector_store
      _extract_text_from_pdf, _call_llm, _extract_structured

    Shared orchestration (concrete, inherited):
      chunk_text, ingest_pdf, ingest_pdfs, ingest_text
      retrieve_context, generate_response, query, query_document
      summarize_document, summarize_all_documents, compare_documents
      get_loaded_documents, get_document_info
    """

    def __init__(self, llm_config: LLMConfig, rag_config: RAGConfig):
        self.llm = llm_config
        self.rag = rag_config
        self.chunks: List[str] = []
        self.chunks_by_source: Dict[str, List[str]] = {}
        self._lock = Lock()
        self._init_embedding_model()
        self._init_vector_store()

    # ------------------------------------------------------------------
    # Abstract: embedding
    # ------------------------------------------------------------------

    @abstractmethod
    def _init_embedding_model(self) -> None:
        """Load or connect to the embedding model."""

    @abstractmethod
    def _embed(self, texts: List[str]) -> List[List[float]]:
        """Return a list of embedding vectors, one per input text."""

    # ------------------------------------------------------------------
    # Abstract: vector store
    # ------------------------------------------------------------------

    @abstractmethod
    def _init_vector_store(self) -> None:
        """Initialise (or connect to) the vector store."""

    @abstractmethod
    def _upsert(
        self,
        embeddings: List[List[float]],
        texts: List[str],
        source_id: str,
    ) -> None:
        """Persist embeddings and source texts; maintain per-source indexing."""

    @abstractmethod
    def _search(self, query_embedding: List[float], k: int) -> List[str]:
        """Return the k most similar texts across all ingested sources."""

    @abstractmethod
    def _search_in_source(
        self, query_embedding: List[float], source_id: str, k: int
    ) -> List[str]:
        """Return the k most similar texts from a single named source."""

    @abstractmethod
    def save_vector_store(self, path: str) -> None:
        """Persist the vector store and metadata to disk."""

    @abstractmethod
    def load_vector_store(self, path: str) -> bool:
        """Load a previously saved vector store. Returns True on success."""

    # ------------------------------------------------------------------
    # Abstract: PDF extraction and LLM
    # ------------------------------------------------------------------

    @abstractmethod
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract raw text from a PDF file."""

    @abstractmethod
    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Send a prompt to the LLM and return its text response."""

    @abstractmethod
    def _extract_structured(self, texts: List[str], instructions: str) -> dict:
        """
        Extract structured data from texts and return as a dict.

        instructions: natural-language description of what to extract
        and the expected JSON schema/field names.
        """

    # ------------------------------------------------------------------
    # Concrete: chunking (overridable)
    # ------------------------------------------------------------------

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping fixed-size character chunks.
        Override to use sentence-aware or token-aware chunking.
        """
        size, overlap = self.rag.chunk_size, self.rag.chunk_overlap
        step = size - overlap
        return [
            text[i: i + size]
            for i in range(0, len(text), step)
            if text[i: i + size].strip()
        ]

    # ------------------------------------------------------------------
    # Concrete: ingestion pipeline
    # ------------------------------------------------------------------

    def ingest_pdf(
        self,
        file_path: str,
        source_id: Optional[str] = None,
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> IngestionResult:
        """
        Full ingestion pipeline for one PDF: extract → chunk → embed → store.
        source_id defaults to the file's basename.
        """
        sid = source_id or os.path.basename(file_path)
        try:
            if progress_callback:
                progress_callback(f"Extracting text from {sid}...")
            text = self._extract_text_from_pdf(file_path)

            if progress_callback:
                progress_callback(f"Chunking {sid}...")
            new_chunks = self.chunk_text(text)
            if not new_chunks:
                return IngestionResult(source_id=sid, status="success", chunks=0)

            if progress_callback:
                progress_callback(f"Embedding and storing {sid}...")
            embeddings = self._embed(new_chunks)

            with self._lock:
                self._upsert(embeddings, new_chunks, sid)
                self.chunks.extend(new_chunks)
                self.chunks_by_source.setdefault(sid, []).extend(new_chunks)

            return IngestionResult(source_id=sid, status="success", chunks=len(new_chunks))
        except Exception as exc:  # pylint: disable=broad-exception-caught
            return IngestionResult(source_id=sid, status="error", error=str(exc))

    def ingest_pdfs(
        self,
        file_paths: List[str],
        source_ids: Optional[List[str]] = None,
        progress_callback: Optional[Callable[[str], None]] = None,
        max_workers: Optional[int] = None,
    ) -> List[IngestionResult]:
        """Ingest multiple PDFs in parallel using a thread pool."""
        sid_map = dict(zip(file_paths, source_ids or file_paths))
        workers = max_workers or min(10, multiprocessing.cpu_count(), len(file_paths))
        results: List[IngestionResult] = []

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(self.ingest_pdf, path, sid_map.get(path), None): path
                for path in file_paths
            }
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                if progress_callback:
                    done = sum(1 for r in results if r.status == "success")
                    progress_callback(f"Ingested {done}/{len(file_paths)} documents")

        return results

    def ingest_text(
        self, text: str, source_id: str = "inline"
    ) -> IngestionResult:
        """Ingest pre-extracted text directly (useful for testing or non-PDF sources)."""
        try:
            new_chunks = self.chunk_text(text)
            if not new_chunks:
                return IngestionResult(source_id=source_id, status="success", chunks=0)
            embeddings = self._embed(new_chunks)
            with self._lock:
                self._upsert(embeddings, new_chunks, source_id)
                self.chunks.extend(new_chunks)
                self.chunks_by_source.setdefault(source_id, []).extend(new_chunks)
            return IngestionResult(source_id=source_id, status="success", chunks=len(new_chunks))
        except Exception as exc:  # pylint: disable=broad-exception-caught
            return IngestionResult(source_id=source_id, status="error", error=str(exc))

    # ------------------------------------------------------------------
    # Concrete: retrieval and generation
    # ------------------------------------------------------------------

    def retrieve_context(
        self, query: str, source_id: Optional[str] = None
    ) -> List[str]:
        """
        Return top-k relevant chunks.
        If source_id is given, search only within that document.
        """
        q_emb = self._embed([query])[0]
        if source_id:
            return self._search_in_source(q_emb, source_id, self.rag.top_k)
        return self._search(q_emb, self.rag.top_k)

    def generate_response(self, query: str, context: List[str]) -> str:
        """Build prompts from config templates and call the LLM."""
        context_str = "\n\n".join(context)
        user_prompt = self.llm.user_prompt_template.format(
            context=context_str, query=query
        )
        return self._call_llm(self.llm.system_prompt, user_prompt)

    def query(self, query: str) -> str:
        """Full RAG pipeline across all ingested documents."""
        context = self.retrieve_context(query)
        if not context:
            return "No relevant documents found in the knowledge base."
        return self.generate_response(query, context)

    def query_document(self, source_id: str, query: str) -> str:
        """Full RAG pipeline scoped to a single named document."""
        if source_id not in self.chunks_by_source:
            return f"Document '{source_id}' has not been ingested."
        context = self.retrieve_context(query, source_id=source_id)
        if not context:
            return "No relevant passages found in that document."
        return self.generate_response(query, context)

    # ------------------------------------------------------------------
    # Concrete: summarisation and comparison
    # ------------------------------------------------------------------

    def summarize_document(self, source_id: str) -> str:
        """Summarise a single ingested document using the LLM."""
        chunks = self.chunks_by_source.get(source_id)
        if not chunks:
            return f"Document '{source_id}' has not been ingested."
        # Sample up to top_k * 5 chunks as a representative slice
        sample = chunks[: max(1, self.rag.top_k * 5)]
        prompt = self.llm.summarize_prompt_template.format(text="\n\n".join(sample))
        return self._call_llm(self.llm.system_prompt, prompt)

    def summarize_all_documents(self) -> Dict[str, str]:
        """Return LLM summaries keyed by source_id for all ingested documents."""
        return {sid: self.summarize_document(sid) for sid in self.chunks_by_source}

    def compare_documents(self, topic: str) -> str:
        """Compare how all ingested documents address a given topic."""
        if not self.chunks_by_source:
            return "No documents have been ingested."
        q_emb = self._embed([topic])[0]
        excerpts: Dict[str, List[str]] = {}
        for sid in self.chunks_by_source:
            hits = self._search_in_source(q_emb, sid, k=2)
            if hits:
                excerpts[sid] = hits
        if not excerpts:
            return "No relevant content found across documents."
        structured_text = ""
        for sid, passages in excerpts.items():
            structured_text += f"\n\n--- {sid} ---\n" + "\n\n".join(passages)
        prompt = self.llm.compare_prompt_template.format(
            topic=topic, text=structured_text
        )
        return self._call_llm(self.llm.system_prompt, prompt)

    # ------------------------------------------------------------------
    # Concrete: utilities
    # ------------------------------------------------------------------

    def get_loaded_documents(self) -> List[str]:
        """Return the source_ids of all ingested documents."""
        return list(self.chunks_by_source.keys())

    def get_document_info(self, source_id: str) -> Dict:
        """Return chunk count and status for a named document."""
        if source_id not in self.chunks_by_source:
            return {"error": f"Document '{source_id}' not found"}
        return {
            "source_id": source_id,
            "chunks": len(self.chunks_by_source[source_id]),
        }
