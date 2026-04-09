"""
Concrete BaseRAG implementation using Anthropic Claude, sentence-transformers,
FAISS, and pdfplumber.
"""

import json
import os
import re
from typing import Dict, List, Optional

import anthropic
import faiss
import numpy as np
import pdfplumber
from sentence_transformers import SentenceTransformer

from baserag import BaseRAG, IngestionResult, LLMConfig, RAGConfig


class AnthropicRAG(BaseRAG):
    """
    BaseRAG implementation using:
      - Anthropic Claude SDK  (LLM inference)
      - sentence-transformers (embeddings)
      - FAISS                 (vector store — combined + per-source indices)
      - pdfplumber            (PDF text extraction)

    Example
    -------
    rag = AnthropicRAG(
        llm_config=LLMConfig(model="claude-sonnet-4-20250514", temperature=0.0),
        rag_config=RAGConfig(embedding_model="all-MiniLM-L6-v2", chunk_size=1000, chunk_overlap=200),
    )
    rag.ingest_pdf("report.pdf")
    print(rag.query("What are the key findings?"))
    """

    # ------------------------------------------------------------------
    # Embedding
    # ------------------------------------------------------------------

    def _init_embedding_model(self) -> None:
        self._st_model = SentenceTransformer(self.rag.embedding_model)

    def _embed(self, texts: List[str]) -> List[List[float]]:
        return self._st_model.encode(texts, show_progress_bar=False).tolist()

    # ------------------------------------------------------------------
    # Vector store (FAISS)
    # ------------------------------------------------------------------

    def _init_vector_store(self) -> None:
        self._dim: Optional[int] = None
        self._index: Optional[faiss.IndexFlatIP] = None
        self._source_indices: Dict[str, faiss.IndexFlatIP] = {}

    def _upsert(
        self,
        embeddings: List[List[float]],
        texts: List[str],
        source_id: str,
    ) -> None:
        arr = np.array(embeddings, dtype=np.float32)
        if self._index is None:
            self._dim = arr.shape[1]
            self._index = faiss.IndexFlatIP(self._dim)
        self._index.add(arr)

        if source_id not in self._source_indices:
            self._source_indices[source_id] = faiss.IndexFlatIP(self._dim)
        self._source_indices[source_id].add(arr)

    def _search(self, query_embedding: List[float], k: int) -> List[str]:
        if self._index is None or self._index.ntotal == 0:
            return []
        q = np.array([query_embedding], dtype=np.float32)
        safe_k = min(k, self._index.ntotal)
        _, indices = self._index.search(q, safe_k)
        return [
            self.chunks[i]
            for i in indices[0]
            if 0 <= i < len(self.chunks)
        ]

    def _search_in_source(
        self, query_embedding: List[float], source_id: str, k: int
    ) -> List[str]:
        index = self._source_indices.get(source_id)
        source_chunks = self.chunks_by_source.get(source_id, [])
        if index is None or index.ntotal == 0:
            return []
        q = np.array([query_embedding], dtype=np.float32)
        safe_k = min(k, index.ntotal)
        _, indices = index.search(q, safe_k)
        return [
            source_chunks[i]
            for i in indices[0]
            if 0 <= i < len(source_chunks)
        ]

    def save_vector_store(self, path: str) -> None:
        """Save FAISS indices and chunk metadata to a directory."""
        os.makedirs(path, exist_ok=True)

        if self._index is not None:
            faiss.write_index(self._index, os.path.join(path, "_combined.faiss"))

        for sid, idx in self._source_indices.items():
            safe = sid.replace("/", "_").replace("\\", "_")
            faiss.write_index(idx, os.path.join(path, f"{safe}.faiss"))

        meta = {
            "chunks": self.chunks,
            "chunks_by_source": self.chunks_by_source,
            "dim": self._dim,
        }
        with open(os.path.join(path, "_meta.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f)

    def load_vector_store(self, path: str) -> bool:
        """Load FAISS indices and chunk metadata from a directory."""
        meta_path = os.path.join(path, "_meta.json")
        if not os.path.exists(meta_path):
            return False

        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)

        self.chunks = meta["chunks"]
        self.chunks_by_source = meta["chunks_by_source"]
        self._dim = meta["dim"]

        combined_path = os.path.join(path, "_combined.faiss")
        if os.path.exists(combined_path):
            self._index = faiss.read_index(combined_path)

        for sid in self.chunks_by_source:
            safe = sid.replace("/", "_").replace("\\", "_")
            idx_path = os.path.join(path, f"{safe}.faiss")
            if os.path.exists(idx_path):
                self._source_indices[sid] = faiss.read_index(idx_path)

        return True

    # ------------------------------------------------------------------
    # PDF extraction
    # ------------------------------------------------------------------

    def _extract_text_from_pdf(self, file_path: str) -> str:
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

    # ------------------------------------------------------------------
    # LLM (Anthropic Claude)
    # ------------------------------------------------------------------

    def _client(self) -> anthropic.Anthropic:
        return anthropic.Anthropic(
            api_key=self.llm.api_key or os.getenv("ANTHROPIC_API_KEY")
        )

    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        response = self._client().messages.create(
            model=self.llm.model,
            max_tokens=self.llm.max_tokens,
            temperature=self.llm.temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return response.content[0].text

    def _extract_structured(self, texts: List[str], instructions: str) -> dict:
        """
        Use Claude to extract structured JSON data from texts.

        instructions: describes what to extract and the expected field names/schema.
        Returns a dict parsed from the model's JSON response.
        """
        combined = "\n\n".join(texts)
        user_prompt = (
            f"{instructions}\n\n"
            f"Text:\n{combined}\n\n"
            "Respond with valid JSON only. No explanation or markdown."
        )
        system = (
            "You are a precise data-extraction assistant. "
            "Output only valid, well-formed JSON with no surrounding text."
        )
        raw = self._call_llm(system, user_prompt)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                return json.loads(match.group())
            return {"raw": raw}


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
def main():
    """Demonstrate AnthropicRAG with a local PDF."""
    rag = AnthropicRAG(
        llm_config=LLMConfig(
            model="claude-sonnet-4-20250514",
            temperature=0.0,
        ),
        rag_config=RAGConfig(
            embedding_model="all-MiniLM-L6-v2",
            chunk_size=1000,
            chunk_overlap=200,
            top_k=4,
        ),
    )

    pdf_path = "Transition-Plan-2025.pdf"
    result = rag.ingest_pdf(pdf_path, progress_callback=print)
    print(f"\nIngested '{result.source_id}': {result.chunks} chunks ({result.status})")

    answer = rag.query("What are the key objectives?")
    print(f"\nAnswer:\n{answer}")

    summary = rag.summarize_document(result.source_id)
    print(f"\nSummary:\n{summary}")


if __name__ == "__main__":
    main()
