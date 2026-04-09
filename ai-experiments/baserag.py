"""Abstract base class for PDF RAG systems."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class LLMConfig:
    """All parameters that govern LLM behaviour."""
    model: str
    api_key: Optional[str] = None
    temperature: float = 0.7
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


@dataclass
class RAGConfig:
    """Parameters that govern ingestion and retrieval."""
    embedding_model: str
    chunk_size: int = 512
    chunk_overlap: int = 64
    top_k: int = 3


class BaseRAG(ABC):
    """
    Abstract base class for PDF ingestion, embedding, vector storage, and
    retrieval-augmented generation.

    Subclasses must implement the provider-specific operations:
      - PDF text extraction
      - Embedding generation
      - Vector store initialisation, upsert, and search
      - LLM inference

    The orchestration logic (chunking, ingestion pipeline, query pipeline)
    is implemented here and shared by all subclasses.
    """

    def __init__(self, llm_config: LLMConfig, rag_config: RAGConfig):
        self.llm = llm_config
        self.rag = rag_config
        self.chunks: List[str] = []          # flat store of all ingested chunks
        self._init_embedding_model()
        self._init_vector_store()

    # ------------------------------------------------------------------
    # Abstract: provider-specific — must be implemented by subclasses
    # ------------------------------------------------------------------

    @abstractmethod
    def _init_embedding_model(self) -> None:
        """Load or connect to the embedding model."""

    @abstractmethod
    def _embed(self, texts: List[str]) -> List[List[float]]:
        """Return a list of embedding vectors, one per input text."""

    @abstractmethod
    def _init_vector_store(self) -> None:
        """Initialise (or connect to) the vector store."""

    @abstractmethod
    def _upsert(self, embeddings: List[List[float]], texts: List[str]) -> None:
        """Persist embeddings and their source texts to the vector store."""

    @abstractmethod
    def _search(self, query_embedding: List[float], k: int) -> List[str]:
        """Return the k most similar texts for a given query embedding."""

    @abstractmethod
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract raw text from a PDF file."""

    @abstractmethod
    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Send a prompt to the LLM and return its text response."""

    # ------------------------------------------------------------------
    # Concrete: shared orchestration logic
    # ------------------------------------------------------------------

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping fixed-size chunks.
        Override this method to use a different chunking strategy
        (e.g. sentence-aware, token-based).
        """
        size, overlap = self.rag.chunk_size, self.rag.chunk_overlap
        step = size - overlap
        return [text[i : i + size] for i in range(0, len(text), step) if text[i : i + size].strip()]

    def ingest_pdf(self, file_path: str) -> int:
        """
        Full ingestion pipeline: extract → chunk → embed → store.
        Returns the number of chunks added.
        """
        text = self._extract_text_from_pdf(file_path)
        new_chunks = self.chunk_text(text)
        if not new_chunks:
            return 0
        embeddings = self._embed(new_chunks)
        self._upsert(embeddings, new_chunks)
        self.chunks.extend(new_chunks)
        return len(new_chunks)

    def ingest_text(self, text: str) -> int:
        """Ingest pre-extracted text directly (useful for testing or non-PDF sources)."""
        new_chunks = self.chunk_text(text)
        if not new_chunks:
            return 0
        embeddings = self._embed(new_chunks)
        self._upsert(embeddings, new_chunks)
        self.chunks.extend(new_chunks)
        return len(new_chunks)

    def retrieve_context(self, query: str) -> List[str]:
        """Embed the query and return the top-k most relevant chunks."""
        query_embedding = self._embed([query])[0]
        return self._search(query_embedding, self.rag.top_k)

    def generate_response(self, query: str, context: List[str]) -> str:
        """Build prompts from templates and call the LLM."""
        context_str = "\n\n".join(context)
        user_prompt = self.llm.user_prompt_template.format(
            context=context_str, query=query
        )
        return self._call_llm(self.llm.system_prompt, user_prompt)

    def query(self, query: str) -> str:
        """Full RAG pipeline: retrieve context then generate a response."""
        context = self.retrieve_context(query)
        if not context:
            return "No relevant documents found in the knowledge base."
        return self.generate_response(query, context)
