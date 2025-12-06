"""Claude multi-pdf analyser, written by Claude AI"""

# pylint: disable=line-too-long
# pylint: disable=ungrouped-imports
# pylint: disable=no-name-in-module
# pylint: disable=trailing-whitespace
# pylint: disable=broad-exception-caught

# multi_pdf_analyzer.py
import warnings
import logging
warnings.filterwarnings('ignore', category=UserWarning, module='torch')
# Suppress Streamlit threading warnings
logging.getLogger('streamlit.runtime.scriptrunner.script_runner').setLevel(logging.ERROR)

import os
import time
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
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
Per-Document Metadata - Track source files for each chunk of text"""
    def __init__(self, api_key: str = None):
        """Initialize the multi-PDF analyzer."""
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
        
    def load_single_pdf(self, pdf_path: str, progress_callback=None) -> Dict:
        """Load and process a single PDF."""
        filename = os.path.basename(pdf_path)
        
        try:
            if progress_callback:
                progress_callback(f"Loading {filename}...")
            
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            if progress_callback:
                progress_callback(f"Splitting {filename} into chunks...")
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_documents(documents)
            
            # Add source metadata
            for chunk in chunks:
                chunk.metadata['source_file'] = filename
            
            if progress_callback:
                progress_callback(f"Creating vector store for {filename}...")
            
            vectorstore = FAISS.from_documents(chunks, self.embeddings)
            
            self.documents[filename] = documents
            self.vectorstores[filename] = vectorstore
            
            return {
                'filename': filename,
                'status': 'success',
                'pages': len(documents),
                'chunks': len(chunks)
            }
            
        except Exception as e:
            return {
                'filename': filename,
                'status': 'error',
                'error': str(e)
            }
    
    def load_multiple_pdfs(self, pdf_paths: List[str], progress_callback=None) -> List[Dict]:
        """Load multiple PDFs in parallel."""
        results = []
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self.load_single_pdf, path, progress_callback): path 
                for path in pdf_paths
            }
            
            for future in as_completed(futures):
                results.append(future.result())
        
        # Create combined vectorstore
        if self.vectorstores:
            if progress_callback:
                progress_callback("Creating combined search index...")
            
            all_vectorstores = list(self.vectorstores.values())
            self.combined_vectorstore = all_vectorstores[0]
            
            for vs in all_vectorstores[1:]:
                self.combined_vectorstore.merge_from(vs)
        
        return results
    
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
    
    def query_all_documents(self, question: str) -> Dict:
        """Query across all loaded documents."""
        if not self.combined_vectorstore:
            return {'error': 'No documents loaded'}
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.combined_vectorstore.as_retriever(
                search_kwargs={"k": 6}
            ),
            return_source_documents=True
        )
        
        result = qa_chain.invoke({"query": question})
        
        # Group sources by document
        sources_by_doc = {}
        for doc in result['source_documents']:
            source = doc.metadata.get('source_file', 'Unknown')
            if source not in sources_by_doc:
                sources_by_doc[source] = []
            sources_by_doc[source].append(doc.page_content[:200])
        
        return {
            'answer': result['result'],
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
