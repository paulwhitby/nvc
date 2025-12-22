"""Claude NVC chatbot with streamlit interface, written by Claude AI"""

# pylint: disable=line-too-long
# pylint: disable=ungrouped-imports
# pylint: disable=no-name-in-module
# pylint: disable=trailing-whitespace
# pylint: disable=broad-exception-caught
# pylint: disable=unused-import

# app.py
import os
import sys
import warnings
import logging
import tempfile
import time
import streamlit as st
from claude_multi_pdf_analyzer import MultiPDFAnalyzer

# Set environment variables before any imports
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Suppress all warnings
warnings.filterwarnings('ignore')
logging.getLogger('streamlit.runtime.scriptrunner.script_runner').setLevel(logging.ERROR)


# Page configuration
st.set_page_config(
    page_title="Multi-PDF Analyzer",
    page_icon="📚",
    layout="wide"
)

# Use cache_resource for non-serializable analyzer object
@st.cache_resource
def get_analyzer(api_key, vectorstore_path=None):
    """Get or create analyzer instance (cached across reruns)."""
    return MultiPDFAnalyzer(api_key=api_key, vectorstore_path=vectorstore_path)

# Initialize session state
if 'analyzer_key' not in st.session_state:
    st.session_state.analyzer_key = None
if 'loaded_files' not in st.session_state:
    st.session_state.loaded_files = []
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📚 Multi-PDF Analyzer</div>', unsafe_allow_html=True)
st.markdown("Analyze multiple PDF documents simultaneously using Claude AI")

# Sidebar for API key and file upload
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        help="Enter your Anthropic API key"
    )
    
    st.divider()
    
    st.header("📁 Upload PDFs")
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
    )
    
    if uploaded_files and api_key:
        if st.button("🚀 Process PDFs", type="primary", use_container_width=True):
            st.session_state.processing = True

            # Initialize analyzer
            try:
                analyzer = get_analyzer(api_key)
                st.session_state.analyzer_key = api_key

                # Clear existing documents to start fresh
                analyzer.documents.clear()
                analyzer.vectorstores.clear()
                analyzer.combined_vectorstore = None

                # Save uploaded files to temp directory
                temp_to_original = {}
                with st.spinner("Saving uploaded files..."):
                    for uploaded_file in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            temp_to_original[tmp_file.name] = uploaded_file.name

                # Process PDFs
                with st.spinner("Processing PDFs..."):
                    results = analyzer.load_multiple_pdfs(list(temp_to_original.keys()), temp_to_original)

                # Clean up temp files
                for path in temp_to_original.keys():
                    os.unlink(path)

                # Store results
                st.session_state.loaded_files = [
                    r for r in results if r['status'] == 'success'
                ]

                # Show results
                success_count = sum(1 for r in results if r['status'] == 'success')
                if success_count > 0:
                    st.success(f"✅ Successfully processed {success_count} document(s)!")

                error_count = sum(1 for r in results if r['status'] == 'error')
                if error_count > 0:
                    st.error(f"❌ Failed to process {error_count} document(s)")
                    for r in results:
                        if r['status'] == 'error':
                            st.error(f"**{r['filename']}**: {r.get('error', 'Unknown error')}")

                st.session_state.processing = False
                st.rerun()

            except Exception as e:
                st.error(f"Error: {str(e)}")
                import traceback
                st.error(traceback.format_exc())
                st.session_state.processing = False
    
    # Show loaded documents
    if st.session_state.loaded_files:
        st.divider()
        st.header("📄 Loaded Documents")
        for file_info in st.session_state.loaded_files:
            with st.expander(f"📄 {file_info['filename']}"):
                st.write(f"**Pages:** {file_info['pages']}")
                st.write(f"**Chunks:** {file_info['chunks']}")

# Main content area
# Get analyzer if we have an API key
analyzer = None
if st.session_state.analyzer_key:
    analyzer = get_analyzer(st.session_state.analyzer_key)

# Debug info (can be removed later)
with st.sidebar:
    if analyzer:
        st.success(f"✓ Analyzer active")
        loaded_docs = analyzer.get_loaded_documents()
        st.write(f"Documents in analyzer: {len(loaded_docs)}")
        if loaded_docs:
            for doc in loaded_docs:
                st.write(f"  - {doc}")
    else:
        st.warning("⚠ No analyzer")
    st.write(f"Loaded files in state: {len(st.session_state.loaded_files)}")

if not analyzer:
    st.info("👈 Upload PDF files using the sidebar to get started")
    
    # Feature showcase
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔍 Query Documents")
        st.write("Ask questions across all documents or query specific files")
    
    with col2:
        st.markdown("### 📊 Compare & Analyze")
        st.write("Compare how different documents address the same topics")
    
    with col3:
        st.markdown("### 📝 Summarize")
        st.write("Generate concise summaries of individual or all documents")

else:
    # Create tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Query", "📝 Summarize", "📊 Compare", "📇 Extract"])
    
    # Query Tab
    with tab1:
        st.header("Query Documents")
        
        query_scope = st.radio(
            "Query scope:",
            ["All Documents", "Specific Document"],
            horizontal=True
        )
        
        selected_doc = None
        if query_scope == "Specific Document":
            selected_doc = st.selectbox(
                "Select document:",
                analyzer.get_loaded_documents()
            )
        
        question = st.text_area(
            "Ask a question:",
            # type="default",
            width="stretch",
            placeholder="What are the main findings discussed in these documents?"
        )
        
        if st.button("🔍 Search", type="primary"):
            if question:
                with st.spinner("Searching documents..."):
                    if query_scope == "All Documents":
                        result = analyzer.query_all_documents(question)
                        
                        if 'error' not in result:
                            st.markdown("### 💬 Answer")
                            st.write(result['answer'])
                            
                            st.markdown("### 📚 Sources")
                            for doc_name, excerpts in result['sources_by_document'].items():
                                with st.expander(f"📄 {doc_name}"):
                                    for i, excerpt in enumerate(excerpts, 1):
                                        st.markdown(f"**Excerpt {i}:**")
                                        st.text(excerpt + "...")
                                        st.divider()
                        else:
                            st.error(result['error'])
                    else:
                        result = analyzer.query_single_document(
                            selected_doc,
                            question
                        )
                        
                        if 'error' not in result:
                            st.markdown("### 💬 Answer")
                            st.write(result['answer'])
                            
                            st.markdown("### 📚 Source Excerpts")
                            for i, doc in enumerate(result['source_documents'], 1):
                                with st.expander(f"Source {i} - Page {doc.metadata.get('page', 'Unknown')}"):
                                    st.text(doc.page_content)
                        else:
                            st.error(result['error'])
            else:
                st.warning("Please enter a question")
    
    # Summarize Tab
    with tab2:
        st.header("Document Summaries")
        
        summary_option = st.radio(
            "Summarize:",
            ["All Documents", "Specific Document"],
            horizontal=True
        )
        
        if summary_option == "Specific Document":
            doc_to_summarize = st.selectbox(
                "Select document:",
                analyzer.get_loaded_documents(),
                key="summarize_select"
            )
            
            if st.button("📝 Generate Summary", type="primary"):
                with st.spinner(f"Summarizing {doc_to_summarize}..."):
                    summary = analyzer.summarize_document(doc_to_summarize)
                    
                    st.markdown(f"### Summary of {doc_to_summarize}")
                    st.write(summary)
        else:
            if st.button("📝 Generate All Summaries", type="primary"):
                with st.spinner("Generating summaries for all documents..."):
                    summaries = analyzer.summarize_all_documents()
                    
                    for filename, summary in summaries.items():
                        with st.expander(f"📄 {filename}", expanded=True):
                            st.write(summary)
    
    # Compare Tab
    with tab3:
        st.header("Compare Documents")
        
        st.write("Compare how different documents address a specific topic or question")
        
        comparison_topic = st.text_input(
            "Enter topic or question to compare:",
            placeholder="e.g., What are the proposed solutions to climate change?"
        )
        
        if st.button("🔄 Compare", type="primary"):
            if comparison_topic:
                with st.spinner("Analyzing and comparing documents..."):
                    comparison = analyzer.compare_documents(comparison_topic)
                    
                    st.markdown("### 📊 Comparison Results")
                    st.write(comparison)
            else:
                st.warning("Please enter a topic to compare")
    
    # Extract Tab
    with tab4:
        st.header("Extract Information")
        
        st.write("Extract structured information like contact details from documents")
        
        extract_doc = st.selectbox(
            "Select document:",
            analyzer.get_loaded_documents(),
            key="extract_select"
        )
        
        if st.button("📇 Extract Contacts", type="primary"):
            with st.spinner(f"Extracting contacts from {extract_doc}..."):
                contacts = analyzer.extract_contacts_from_document(extract_doc)
                
                if contacts:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 👤 Names")
                        if contacts.names:
                            for name in contacts.names:
                                st.write(f"• {name}")
                        else:
                            st.write("No names found")
                        
                        st.markdown("### 📞 Phone Numbers")
                        if contacts.phone_numbers:
                            for phone in contacts.phone_numbers:
                                st.write(f"• {phone}")
                        else:
                            st.write("No phone numbers found")
                    
                    with col2:
                        st.markdown("### 📧 Emails")
                        if contacts.emails:
                            for email in contacts.emails:
                                st.write(f"• {email}")
                        else:
                            st.write("No emails found")
                else:
                    st.warning("Could not extract contact information from this document")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        Built with Streamlit and Claude AI | Multi-PDF Document Analyzer
    </div>
    """,
    unsafe_allow_html=True
)
