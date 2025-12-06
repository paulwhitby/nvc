# Large Document Collection Guide (286+ Documents)

This guide explains how to use the Multi-PDF Analyzer with large document collections (100+ documents).

## Key Improvements for 286 Documents

### 1. Persistent Storage
The analyzer now supports saving and loading vectorstores to disk, avoiding the need to reprocess all PDFs on each session.

```python
# Initialize with persistent storage
analyzer = MultiPDFAnalyzer(
    api_key="your-api-key",
    vectorstore_path="./vectorstore_cache"
)

# Load existing vectorstores (if any)
analyzer.load_vectorstores()

# Process new documents
results = analyzer.load_multiple_pdfs(pdf_paths)

# Save vectorstores for next time
analyzer.save_vectorstores()
```

### 2. Optimized Parallel Processing
- Automatically scales workers based on CPU count and collection size
- Default: `min(10, cpu_count, num_documents)` workers
- For 286 documents: Uses 10 parallel workers for faster processing

### 3. Incremental Updates
- First load: Builds combined vectorstore from all documents
- Subsequent loads: Incrementally merges new documents without rebuilding
- Significantly faster when adding documents to existing collection

### 4. Adaptive Query Strategy
The system now uses different strategies based on collection size:

| Documents | Chunks per Doc | Total Chunks | Strategy |
|-----------|----------------|--------------|----------|
| 1-10      | 4-12           | 20           | Balanced per-document sampling |
| 11-50     | 2-4            | 20           | Moderate per-document sampling |
| 51-286+   | 1-2            | 20           | Sparse sampling or top-k from combined store |

## Workflow for 286 Documents

### Initial Setup (First Time)

1. **Create vectorstore directory:**
```bash
mkdir -p ai-experiments/vectorstore_cache
```

2. **Batch process all 286 PDFs:**
```python
import os
from claude_multi_pdf_analyzer import MultiPDFAnalyzer

# Initialize with persistence
analyzer = MultiPDFAnalyzer(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    vectorstore_path="./vectorstore_cache"
)

# Get all PDF paths
pdf_dir = "/path/to/your/286/pdfs"
pdf_paths = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

print(f"Processing {len(pdf_paths)} PDFs...")

# Process in batches to monitor progress
batch_size = 50
for i in range(0, len(pdf_paths), batch_size):
    batch = pdf_paths[i:i+batch_size]
    print(f"\nProcessing batch {i//batch_size + 1}: {len(batch)} files")

    results = analyzer.load_multiple_pdfs(batch, max_workers=10)

    # Show progress
    success = sum(1 for r in results if r['status'] == 'success')
    print(f"Batch complete: {success}/{len(batch)} successful")

    # Save after each batch
    analyzer.save_vectorstores()
    print(f"Saved progress. Total documents: {len(analyzer.documents)}")

print(f"\n✅ All documents processed: {len(analyzer.documents)}")
```

**Expected Processing Time:**
- ~2-5 seconds per document (loading + embedding)
- 286 documents with 10 workers: **~5-10 minutes total**

### Subsequent Sessions (Load from Cache)

```python
# Initialize and load from cache
analyzer = MultiPDFAnalyzer(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    vectorstore_path="./vectorstore_cache"
)

# Load existing vectorstores - takes seconds instead of minutes!
loaded = analyzer.load_vectorstores()

if loaded:
    print(f"✅ Loaded {len(analyzer.documents)} documents from cache")

    # Ready to query immediately
    result = analyzer.query_all_documents("What is Nonviolent Communication?")
    print(result['answer'])
else:
    print("No cache found, need to process PDFs")
```

**Load Time from Cache:** ~10-30 seconds for 286 documents

## Performance Optimization Tips

### 1. Memory Management
- Expected memory usage: ~200-500 MB for 286 documents
- Close other applications if running on systems with <8GB RAM

### 2. Query Performance
For 286 documents, queries take ~15-30 seconds:
- 5-10s: Retrieving relevant chunks
- 10-20s: Claude API processing

### 3. Batch Processing Strategy
When processing 286 documents initially:
- **Option A:** Process all at once (10-15 minutes)
- **Option B:** Process in batches of 50 (5 batches × 2-3 minutes)
  - Advantage: Can stop/resume, see progress, save incrementally

### 4. Storage Requirements
Vectorstore cache size:
- ~1-2 MB per document
- 286 documents ≈ **300-600 MB** disk space

## Troubleshooting

### Out of Memory
If you encounter memory errors:
1. Process in smaller batches (25-30 at a time)
2. Save and clear between batches:
```python
analyzer.save_vectorstores()
analyzer.documents.clear()
analyzer.vectorstores.clear()
analyzer.combined_vectorstore = None
analyzer.load_vectorstores()  # Reload to continue
```

### Slow Queries
If queries are taking too long:
1. Reduce `max_chunks` parameter:
```python
result = analyzer.query_all_documents(question, max_chunks=15)
```

2. Query specific documents instead of all:
```python
result = analyzer.query_single_document("workshop_1.pdf", question)
```

### Cache Corruption
If vectorstore cache becomes corrupted:
```bash
rm -rf vectorstore_cache/
# Then reprocess all documents
```

## Streamlit UI Considerations

For the Streamlit interface with 286 documents:

1. **Document Selection:** Add search/filter for document names
2. **Progress Indication:** Show real-time progress during batch processing
3. **Selective Loading:** Option to load subset of documents
4. **Cache Management:** UI button to clear/rebuild cache

Example additions to [claude_nvc_chatbot.py](claude_nvc_chatbot.py):
```python
# Add to sidebar
if st.button("💾 Save Vectorstores"):
    if analyzer:
        analyzer.save_vectorstores("./vectorstore_cache")
        st.success("Vectorstores saved!")

if st.button("📂 Load from Cache"):
    analyzer = get_analyzer(api_key)
    loaded = analyzer.load_vectorstores("./vectorstore_cache")
    if loaded:
        st.success(f"Loaded {len(analyzer.documents)} documents!")
```

## Recommended Workflow Summary

1. **First Time:**
   - Process all 286 PDFs in batches
   - Save vectorstores after each batch
   - Total time: ~10-15 minutes

2. **Daily Use:**
   - Load vectorstores from cache (~30 seconds)
   - Query across all documents
   - Add new documents incrementally if needed

3. **Maintenance:**
   - Rebuild cache monthly or when adding many new documents
   - Monitor cache size (should be ~500MB)
   - Test queries periodically to ensure accuracy

## Next Steps for Further Scaling (1000+ documents)

If you need to scale beyond 286 documents:
1. Consider vector databases (Pinecone, Weaviate, Qdrant)
2. Implement document filtering/categorization
3. Use hybrid search (keyword + semantic)
4. Add re-ranking for better result quality
5. Consider document summarization for overview queries
