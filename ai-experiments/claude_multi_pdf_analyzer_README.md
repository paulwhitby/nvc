# `claude_multi_pdf_analyzer.py` - Code Description

## 1. Overview

The `claude_multi_pdf_analyzer.py` script provides a robust framework for analyzing a collection of PDF documents using a Retrieval-Augmented Generation (RAG) architecture. It is built using Python and leverages several key libraries, most notably `langchain`, `langchain-anthropic` for LLM interaction, `langchain-huggingface` for embeddings, and `FAISS` for efficient vector storage and retrieval.

The script defines a `MultiPDFAnalyzer` class that encapsulates all the functionality. It can load multiple PDFs in parallel, process them into a queryable vector-based index, and use this index to answer questions, generate summaries, and compare information across documents. The primary LLM used for generation is Anthropic's Claude, specifically the `claude-sonnet-4-20250514` model.

Key capabilities include:
- Parallel processing of multiple PDFs.
- Creation of individual and combined vector stores.
- Persistent storage and loading of vector stores to disk.
- Querying individual or all documents.
- Summarization and cross-document comparison.
- Structured data extraction (e.g., contact information).

---

## 2. Document Ingestion

Document ingestion is the first step, where the PDF files are read and their content is loaded into memory.

- **Tooling:** The script uses `PyPDFLoader` from the `langchain_community.document_loaders` library.
- **Process:** The `load_single_pdf` method is the core of the ingestion process.
    1.  It takes a path to a PDF file as input.
    2.  An instance of `PyPDFLoader` is created with the file path.
    3.  The `loader.load()` method is called, which reads the PDF and splits it into a list of `Document` objects, where each `Document` typically corresponds to a page. The content of the page is stored in `page_content`, and metadata (like the page number) is also attached.
- **Parallelism:** The `load_multiple_pdfs` method orchestrates the loading of several PDFs concurrently using Python's `ThreadPoolExecutor`. This significantly speeds up the process for large collections by distributing the `load_single_pdf` calls across multiple threads.

---

## 3. Chunking

Once the documents are loaded, their text needs to be split into smaller, manageable chunks. This is crucial for the embedding model, which has a limited input token length, and for creating a granular index for retrieval.

- **Tooling:** The script employs the `RecursiveCharacterTextSplitter` from `langchain_text_splitters`.
- **Process:** Within the `load_single_pdf` method, after loading the pages:
    1.  An instance of `RecursiveCharacterTextSplitter` is created with a `chunk_size` of 1000 characters and a `chunk_overlap` of 200 characters. The overlap ensures semantic continuity between chunks.
    2.  The `text_splitter.split_documents()` method is called on the list of `Document` objects (pages). This method iterates through the documents, splits the text according to the specified parameters, and returns a new list of `Document` objects, where each object is now a chunk.
    3.  Crucially, the script then iterates through these chunks to add `source_file` metadata to each one, allowing the system to trace any retrieved chunk back to its original PDF.

---

## 4. Embedding

Embedding is the process of converting the text chunks into numerical vectors. These vectors capture the semantic meaning of the text, allowing for similarity-based searches.

- **Tooling:** The `HuggingFaceEmbeddings` class from `langchain_huggingface` is used, specifically with the `sentence-transformers/all-MiniLM-L6-v2` model. This is a popular and efficient model that runs locally.
- **Process:**
    1.  In the `MultiPDFAnalyzer`'s `__init__` method, an instance of `HuggingFaceEmbeddings` is created and stored as `self.embeddings`.
    2.  This embedding object is then passed to the vector store creation step. When `FAISS.from_documents()` is called, it internally uses the provided embedding object to convert each chunk's `page_content` into a vector.

---

## 5. RAG Generation (Vector Store Creation)

The "RAG Generation" step involves creating the index that the retrieval system will use. This index, known as a vector store, stores the embeddings of all chunks and provides a fast way to find the chunks most relevant to a query.

- **Tooling:** The script uses `FAISS` (Facebook AI Similarity Search) from the `langchain_community.vectorstores` library, which is a highly efficient library for vector similarity search.
- **Process:**
    1.  **Individual Vector Stores:** In `load_single_pdf`, after chunking, `FAISS.from_documents(chunks, self.embeddings)` is called. This takes the list of chunked `Document` objects, computes embeddings for each, and builds a FAISS index. This index is stored in a dictionary `self.vectorstores`, keyed by the original filename.
    2.  **Combined Vector Store:** In `load_multiple_pdfs`, after all individual PDFs have been processed, the script creates a single, unified vector store named `self.combined_vectorstore`. It does this by extracting all the document chunks from each individual vector store and then creating a new `FAISS` index from this aggregated list. This allows for querying across the entire document collection simultaneously.
    3.  **Persistence:** The `save_vectorstores` and `load_vectorstores` methods allow the created FAISS indexes to be saved to and loaded from disk. This is a critical feature for large collections, as it avoids the need to re-process the PDFs every time the script is run.

---

## 6. Querying the RAG with the LLM

This is where the system answers user questions by retrieving relevant information and synthesizing an answer.

- **Tooling:** The primary components are:
    - The `FAISS` vector store, which acts as the **Retriever**.
    - The `ChatAnthropic` LLM (`claude-sonnet-4-20250514`), which acts as the **Generator**.
    - `RetrievalQA` and `load_summarize_chain` chains from `langchain_classic.chains` to orchestrate the process.
- **Process (for querying):**
    1.  **Retrieval:** When a question is asked (e.g., in `query_single_document` or `query_all_documents`), the relevant vector store is used to find the most similar document chunks to the query string. The `as_retriever()` method is called on the FAISS object, which returns a retriever that can be invoked with the query. The retriever finds the top `k` most relevant chunks.
    2.  **Context Augmentation:** The content of these retrieved chunks is collected and formatted into a "context".
    3.  **Generation:** This context, along with the original question, is passed to the `ChatAnthropic` LLM within a structured prompt. The prompt instructs the LLM to answer the question *based on the provided context*.
    4.  **Chaining:** The `RetrievalQA` chain elegantly wraps these steps. It takes the retriever and the LLM as inputs and handles the process of retrieving documents, stuffing them into a prompt (using the `"stuff"` chain type), and getting the final answer from the LLM. The `query_all_documents` method implements a more manual but balanced retrieval strategy to ensure chunks are drawn from all documents before sending them to the LLM for the final answer.

---

## 7. LangChain-Derived Functions and Classes

This script is heavily based on the LangChain library, adopting its modular and chainable architecture.

- **`PyPDFLoader`:** A standard LangChain document loader for reading and parsing PDF files.
- **`RecursiveCharacterTextSplitter`:** A core LangChain component for splitting documents into chunks. It is configured with `chunk_size` and `chunk_overlap`.
- **`HuggingFaceEmbeddings`:** A standard LangChain wrapper for using Hugging Face's sentence-transformer models to create text embeddings locally.
- **`FAISS`:** A LangChain vector store integration. The script uses `FAISS.from_documents()` to create the index and `as_retriever()` to use it for searching. It also uses the `save_local` and `load_local` methods for persistence.
- **`ChatAnthropic`:** The LangChain integration for Anthropic's chat models, used here as the core LLM for generation.
- **`RetrievalQA`:** A classic LangChain "chain" that combines a retriever and an LLM to perform question-answering. The script uses the `"stuff"` chain type, which simply "stuffs" all retrieved context into a single prompt.
- **`load_summarize_chain`:** A specialized LangChain chain for summarization tasks. The script uses the `"map_reduce"` type, which generates a summary for each chunk (`map` step) and then recursively combines those summaries into a final one (`reduce` step).
- **`PromptTemplate`:** Used to create structured, reusable prompts for the LLM, clearly defining input variables and instructions.
- **`PydanticOutputParser`:** A powerful tool for getting structured (JSON/Pydantic) output from the LLM. The script uses it in `extract_contacts_from_document` to force the LLM's output into a `ContactInfo` Pydantic model, making the result reliable and easy to work with. The chain is constructed with `prompt | llm | parser`, which is a modern LangChain Expression Language (LCEL) syntax.
