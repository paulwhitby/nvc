"""sample code written by qwen3-coder:30b run from Ollama for RAG pattern application"""
# Sample Python program to interact with Ollama using RAG pattern
import os
import json
from typing import List, Dict, Any
import numpy as np
import ollama
from sentence_transformers import SentenceTransformer
import faiss

class OllamaRAG:
    """OllamaRAG class to handle retrieval-augmented generation using Ollama and sentence-transformers"""
    def __init__(self, model_name: str = "qwen3-coder:30b", embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize Ollama RAG system
        """
        self.model_name = model_name
        self.embedding_model_name = embedding_model
        self.embedding_model = SentenceTransformer(embedding_model)
        self.vector_db = None
        self.documents = []
        
    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using sentence-transformers
        """
        return self.embedding_model.encode(text).tolist()
    
    def add_documents(self, documents: List[str]):
        """
        Add documents to the vector database
        """
        self.documents.extend(documents)
        
        # Create embeddings for all documents
        embeddings = [self.get_embedding(doc) for doc in documents]
        
        # Create FAISS index
        dimension = len(embeddings[0])
        self.vector_db = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        
        # Add embeddings to index
        embeddings_array = np.array(embeddings, dtype=np.float32)
        self.vector_db.add(embeddings_array)
        
        print(f"Added {len(documents)} documents to vector database")
    
    def retrieve_context(self, query: str, k: int = 3) -> List[str]:
        """
        Retrieve relevant documents based on query
        """
        if self.vector_db is None:
            return []
            
        query_embedding = self.get_embedding(query)
        query_array = np.array([query_embedding], dtype=np.float32)
        
        # Search for similar embeddings
        distances, indices = self.vector_db.search(query_array, k)
        
        # Return relevant documents
        relevant_docs = [self.documents[i] for i in indices[0] if i < len(self.documents)]
        return relevant_docs
    
    def generate_response(self, query: str, context: List[str]) -> str:
        """
        Generate response using Ollama with retrieved context
        """
        # Format context
        context_str = "\n\n".join(context)
        
        # Create prompt with context
        prompt = f"""
        You are an assistant that answers questions based on the provided context.
        Context:
        {context_str}
        
        Question: {query}
        
        Please provide a helpful and accurate answer based only on the context provided.
        """
        
        # Call Ollama model
        response = ollama.generate(
            model=self.model_name,
            prompt=prompt,
            stream=False
        )
        
        return response['response']
    
    def rag_query(self, query: str, k: int = 3) -> str:
        """
        Complete RAG pipeline: retrieve + generate
        """
        # Retrieve relevant documents
        context = self.retrieve_context(query, k)
        
        if not context:
            return "No relevant documents found."
        
        # Generate response
        response = self.generate_response(query, context)
        return response

# Example usage
def main():
    # Initialize RAG system
    rag_system = OllamaRAG(model_name="llama3", embedding_model="all-MiniLM-L6-v2")
    
    # Sample documents
    documents = [
        "The capital of France is Paris. Paris is located in northern central France.",
        "The Eiffel Tower is a famous landmark in Paris, France. It was built in 1889.",
        "Climate change refers to long-term shifts in global or regional climate patterns.",
        "Machine learning is a subset of artificial intelligence that focuses on algorithms.",
        "Python is a popular programming language used in data science and AI."
    ]
    
    # Add documents to system
    rag_system.add_documents(documents)
    
    # Example queries
    queries = [
        "What is the capital of France?",
        "When was the Eiffel Tower built?",
        "What is climate change?",
        "What is machine learning?"
    ]
    
    # Run queries
    for query in queries:
        print(f"\nQuery: {query}")
        response = rag_system.rag_query(query, k=2)
        print(f"Response: {response}")
        print("-" * 50)

if __name__ == "__main__":
    main()
