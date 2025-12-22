"""Claude multi-pdf analyser, written by Claude AI"""

# pylint: disable=line-too-long
# pylint: disable=ungrouped-imports
# pylint: disable=no-name-in-module
# pylint: disable=trailing-whitespace
# pylint: disable=broad-exception-caught
# pylint: disable=unused-import

# multi_pdf_analyzer.py
import os
import sys
import traceback
import warnings
import logging
import time
import multiprocessing
import json
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor


# Set environment variables before any torch/transformers imports
os.environ['TOKENIZERS_PARALLELISM'] = 'false'


# Suppress all warnings before imports
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Suppress Streamlit threading warnings
logging.getLogger('streamlit.runtime.scriptrunner.script_runner').setLevel(logging.ERROR)

load_dotenv()

class ContactInfo(BaseModel):
    """Contact information extracted from document."""
    names: List[str] = Field(description="Names mentioned in the document")
    emails: List[str] = Field(description="Email addresses found")
    phone_numbers: List[str] = Field(description="Phone numbers found")

class DocumentMetadata(BaseModel):
    """Metadata about the document."""
    title: str = Field(description="Document title")
    author: str = Field(description="Document author or organization")
    document_type: str = Field(description="Type of document")

class MultiPDFAnalyzer:
    """Multi-PDF Capabilities:
Parallel Processing - Load multiple PDFs simultaneously using ThreadPoolExecutor
Individual & Combined Querying - Query specific documents or search across all
Document Comparison - Compare how different documents address the same topic
Batch Summaries - Generate summaries for all documents at once
Per-Document Metadata - Track source files for each chunk of text
Persistent Storage - Save and load vectorstores to disk for large collections"""
    def __init__(self, api_key: str = None, vectorstore_path: str = None):
        """Initialize the multi-PDF analyzer.

        Args:
            api_key: Anthropic API key
            vectorstore_path: Directory to save/load persistent vectorstores (for large collections)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key is required")

        self.llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            anthropic_api_key=self.api_key,
            temperature=0
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.documents = {}  # Store documents by filename
        self.vectorstores = {}  # Store vectorstores by filename
        self.combined_vectorstore = None
        self._lock = Lock()  # Thread lock for safe dictionary access
        self.vectorstore_path = vectorstore_path  # Path for persistent storage
        
    def load_single_pdf(self, pdf_path: str, progress_callback=None, original_filename=None) -> Dict:
        """Load and process a single PDF."""
        filename = original_filename or os.path.basename(pdf_path)

        try:
            print(f"[PDF LOADER] Starting to load {filename}")
            if progress_callback:
                progress_callback(f"Loading {filename}...")

            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            print(f"[PDF LOADER] Loaded {len(documents)} pages from {filename}")

            if progress_callback:
                progress_callback(f"Splitting {filename} into chunks...")

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_documents(documents)
            print(f"[PDF LOADER] Split into {len(chunks)} chunks")

            # Add source metadata
            for chunk in chunks:
                chunk.metadata['source_file'] = filename

            if progress_callback:
                progress_callback(f"Creating vector store for {filename}...")

            print(f"[PDF LOADER] Creating vector store for {filename}...")
            vectorstore = FAISS.from_documents(chunks, self.embeddings)
            print(f"[PDF LOADER] Vector store created for {filename}")

            # Use lock to ensure thread-safe dictionary updates
            with self._lock:
                self.documents[filename] = documents
                self.vectorstores[filename] = vectorstore
                print(f"[PDF LOADER] Stored {filename}. Total docs: {len(self.documents)}")
                print(f"[PDF LOADER] Vectorstore keys: {list(self.vectorstores.keys())}")

            return {
                'filename': filename,
                'status': 'success',
                'pages': len(documents),
                'chunks': len(chunks)
            }

        except Exception as e:
            print(f"[PDF LOADER ERROR] {filename}: {str(e)}")
            traceback.print_exc()
            return {
                'filename': filename,
                'status': 'error',
                'error': str(e)
            }
    
    def load_multiple_pdfs(self, pdf_paths: List[str], filename_mapping=None, progress_callback=None, max_workers=None) -> List[Dict]:
        """Load multiple PDFs in parallel.

        Args:
            pdf_paths: List of PDF file paths to load
            filename_mapping: Optional mapping of temp paths to original filenames
            progress_callback: Optional callback for progress updates
            max_workers: Number of parallel workers (default: min(10, cpu_count))
        """
        results = []
        filename_mapping = filename_mapping or {}

        # Scale workers based on collection size
        if max_workers is None:
            max_workers = min(10, multiprocessing.cpu_count(), len(pdf_paths))

        print(f"[PDF LOADER] Loading {len(pdf_paths)} PDFs with {max_workers} workers")

        # Don't pass progress_callback to threads - causes NoSessionContext error
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    self.load_single_pdf,
                    path,
                    None,
                    filename_mapping.get(path)  # Pass original filename
                ): path
                for path in pdf_paths
            }

            for future in as_completed(futures):
                results.append(future.result())

        # Create combined vectorstore - ALWAYS rebuild to avoid metadata corruption
        # Thread-safe: All individual vectorstores are complete at this point
        if self.vectorstores:
            with self._lock:  # Lock to prevent concurrent reads during rebuild
                print(f"[PDF LOADER] Building combined vectorstore from {len(self.vectorstores)} stores")
                print(f"[PDF LOADER] Documents in vectorstores: {list(self.vectorstores.keys())}")

                # Get all documents from all vectorstores
                all_docs = []
                for filename, vs in self.vectorstores.items():
                    docs = vs.docstore._dict.values() if hasattr(vs.docstore, '_dict') else []
                    print(f"[PDF LOADER] Extracting {len(docs)} docs from {filename}")
                    all_docs.extend(docs)

                print(f"[PDF LOADER] Creating new combined vectorstore with {len(all_docs)} total documents")
                # Create completely new vectorstore to ensure clean metadata
                self.combined_vectorstore = FAISS.from_documents(
                    all_docs,
                    self.embeddings
                )

                print(f"[PDF LOADER] Combined vectorstore ready with {len(self.documents)} documents")

        return results

    def save_vectorstores(self, path: str = None):
        """Save all vectorstores to disk for persistence."""
        save_path = path or self.vectorstore_path
        if not save_path:
            raise ValueError("No vectorstore_path specified")

        os.makedirs(save_path, exist_ok=True)

        print(f"[PERSISTENCE] Saving {len(self.vectorstores)} vectorstores to {save_path}")

        for filename, vs in self.vectorstores.items():
            # Sanitize filename for filesystem
            safe_filename = filename.replace('/', '_').replace('\\', '_')
            vs_path = os.path.join(save_path, safe_filename)
            vs.save_local(vs_path)
            print(f"[PERSISTENCE] Saved {filename}")

        # Save combined vectorstore if it exists
        if self.combined_vectorstore:
            combined_path = os.path.join(save_path, "_combined")
            self.combined_vectorstore.save_local(combined_path)
            print(f"[PERSISTENCE] Saved combined vectorstore")

        # Save document metadata
        metadata_path = os.path.join(save_path, "_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump({
                'documents': list(self.documents.keys()),
                'vectorstores': list(self.vectorstores.keys())
            }, f)
        print(f"[PERSISTENCE] Saved metadata")

    def load_vectorstores(self, path: str = None):
        """Load vectorstores from disk."""
        load_path = path or self.vectorstore_path
        if not load_path or not os.path.exists(load_path):
            print(f"[PERSISTENCE] No saved vectorstores found at {load_path}")
            return False

        print(f"[PERSISTENCE] Loading vectorstores from {load_path}")

        # Load metadata
        metadata_path = os.path.join(load_path, "_metadata.json")
        if not os.path.exists(metadata_path):
            print(f"[PERSISTENCE] No metadata file found")
            return False

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        # Load individual vectorstores
        for filename in metadata['vectorstores']:
            safe_filename = filename.replace('/', '_').replace('\\', '_')
            vs_path = os.path.join(load_path, safe_filename)
            if os.path.exists(vs_path):
                self.vectorstores[filename] = FAISS.load_local(
                    vs_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                self.documents[filename] = True  # Mark as loaded
                print(f"[PERSISTENCE] Loaded {filename}")

        # Load combined vectorstore
        combined_path = os.path.join(load_path, "_combined")
        if os.path.exists(combined_path):
            self.combined_vectorstore = FAISS.load_local(
                combined_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"[PERSISTENCE] Loaded combined vectorstore")

        print(f"[PERSISTENCE] Loaded {len(self.vectorstores)} vectorstores")
        return True

    def query_single_document(self, filename: str, question: str) -> Dict:
        """Query a specific document."""
        if filename not in self.vectorstores:
            return {'error': f'Document {filename} not found'}
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstores[filename].as_retriever(
                search_kwargs={"k": 4}
            ),
            return_source_documents=True
        )
        
        result = qa_chain.invoke({"query": question})
        
        return {
            'answer': result['result'],
            'source_documents': result['source_documents']
        }
    
    def query_all_documents(self, question: str, max_chunks=20) -> Dict:
        """Query across all loaded documents using a contextual compression retriever
        to maximize accuracy and completeness.

        Args:
            question: Question to ask
            max_chunks: (Not directly used, but kept for signature consistency)
                        The base retriever will fetch a fixed number of documents (25).
        """
        if not self.combined_vectorstore:
            return {'error': 'No documents loaded or combined vectorstore not created.'}

        print(f"[QUERY] Starting query with ContextualCompressionRetriever.")

        # 1. Create a compressor that uses the LLM to extract relevant parts
        compressor = LLMChainExtractor.from_llm(self.llm)

        # 2. Set up the base retriever to fetch a larger number of documents
        base_retriever = self.combined_vectorstore.as_retriever(
            search_kwargs={"k": 25}
        )

        # 3. Create the ContextualCompressionRetriever
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )

        # 4. Retrieve and compress documents. This returns only the relevant, compressed parts.
        print("[QUERY] Retrieving and compressing relevant documents...")
        compressed_docs = compression_retriever.invoke(question)
        print(f"[QUERY] Retrieved {len(compressed_docs)} compressed, relevant chunks.")

        # 5. Build context from the compressed documents
        context = "\n\n".join([doc.page_content for doc in compressed_docs])

        # 6. Use LLM to answer based on the focused, compressed context
        prompt = f"""Based *only* on the following context from multiple documents, please provide a comprehensive answer to the question. If the context does not contain the answer, state that clearly.

Context:
{context}

Question: {question}

Answer:"""

        answer = self.llm.invoke(prompt).content

        # 7. Group sources by document for traceability
        sources_by_doc = {}
        for doc in compressed_docs:
            source = doc.metadata.get('source_file', 'Unknown')
            if source not in sources_by_doc:
                sources_by_doc[source] = []
            # Store the compressed content that was used for the answer
            sources_by_doc[source].append(doc.page_content)

        print(f"[QUERY] Total chunks used for answer: {len(compressed_docs)}")
        print(f"[QUERY] Documents represented: {list(sources_by_doc.keys())}")

        return {
            'answer': answer,
            'sources_by_document': sources_by_doc
        }
    
    def summarize_document(self, filename: str) -> str:
        """Summarize a specific document."""
        if filename not in self.vectorstores:
            return f'Error: Document {filename} not found'
        
        docs = self.vectorstores[filename].similarity_search("", k=50)
        
        prompt_template = """Write a concise summary of the following text:

{text}

SUMMARY:"""
        
        chain = load_summarize_chain(
            self.llm,
            chain_type="map_reduce",
            map_prompt=PromptTemplate.from_template(prompt_template),
            combine_prompt=PromptTemplate.from_template(prompt_template)
        )
        
        summary = chain.invoke(docs)
        return summary['output_text']
    
    def summarize_all_documents(self) -> Dict[str, str]:
        """Generate summaries for all documents."""
        summaries = {}
        for filename in self.documents.keys():
            summaries[filename] = self.summarize_document(filename)
        return summaries
    
    def compare_documents(self, topic: str) -> str:
        """Compare how different documents address a topic."""
        if not self.combined_vectorstore:
            return "No documents loaded"
        
        prompt = f"""Compare how the following documents address the topic: {topic}

Analyze the different perspectives, approaches, or information provided by each source.

Documents:
{{text}}

COMPARISON:"""
        
        docs = self.combined_vectorstore.similarity_search(topic, k=8)
        
        # Group by source
        docs_by_source = {}
        for doc in docs:
            source = doc.metadata.get('source_file', 'Unknown')
            if source not in docs_by_source:
                docs_by_source[source] = []
            docs_by_source[source].append(doc.page_content)
        
        # Create structured input
        structured_text = ""
        for source, contents in docs_by_source.items():
            structured_text += f"\n\n--- {source} ---\n"
            structured_text += "\n\n".join(contents[:2])
        
        response = self.llm.invoke(prompt.format(text=structured_text))
        return response.content
    
    def extract_contacts_from_document(self, filename: str) -> Optional[ContactInfo]:
        """Extract contact information from a specific document."""
        if filename not in self.vectorstores:
            return None
        
        parser = PydanticOutputParser(pydantic_object=ContactInfo)
        
        prompt = PromptTemplate(
            template="""Extract all contact information from the following text.
            
{format_instructions}

Text: {text}

Output:""",
            input_variables=["text"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        
        docs = self.vectorstores[filename].similarity_search("contact email phone name", k=10)
        combined_text = "\n\n".join([doc.page_content for doc in docs])
        
        try:
            chain = prompt | self.llm | parser
            result = chain.invoke({"text": combined_text})
            return result
        except:
            return None
    
    def get_loaded_documents(self) -> List[str]:
        """Get list of loaded document filenames."""
        return list(self.documents.keys())
    
    def get_document_info(self, filename: str) -> Dict:
        """Get information about a specific document."""
        if filename not in self.documents:
            return {'error': 'Document not found'}
        
        return {
            'filename': filename,
            'pages': len(self.documents[filename]),
            'chunks': len(self.vectorstores[filename].docstore._dict)
        }
