import numpy as np
import faiss
import ollama
from sentence_transformers import SentenceTransformer
import pdfplumber   # or PyMuPDF / PyPDF2
from baserag import BaseRAG, LLMConfig, RAGConfig
from typing import List, Optional



class OllamaFaissRAG(BaseRAG):

    def _init_embedding_model(self):
        self._st_model = SentenceTransformer(self.rag.embedding_model)

    def _embed(self, texts):
        return self._st_model.encode(texts).tolist()

    def _init_vector_store(self):
        self._index = None   # lazy-init on first upsert

    def _upsert(self, embeddings, texts):
        arr = np.array(embeddings, dtype=np.float32)
        if self._index is None:
            self._index = faiss.IndexFlatIP(arr.shape[1])
        self._index.add(arr)

    def _search(self, query_embedding, k):
        if self._index is None:
            return []
        q = np.array([query_embedding], dtype=np.float32)
        _, indices = self._index.search(q, k)
        return [self.chunks[i] for i in indices[0] if i < len(self.chunks)]

    def _extract_text_from_pdf(self, file_path):
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages)

    def _call_llm(self, system_prompt, user_prompt):
        response = ollama.chat(
            model=self.llm.model,
            options={"temperature": self.llm.temperature},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
        )
        return response["message"]["content"]


# Instantiation
rag = OllamaFaissRAG(
    llm_config=LLMConfig(model="qwen3:30b", temperature=0.2),
    rag_config=RAGConfig(embedding_model="all-MiniLM-L6-v2", chunk_size=400, chunk_overlap=50),
)
rag.ingest_pdf("my_document.pdf")
print(rag.query("What is the key finding?"))
