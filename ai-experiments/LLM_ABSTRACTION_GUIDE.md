# LLM Abstraction Guide: Claude AI Dependencies

This document identifies all Claude AI-specific dependencies and how to abstract them for using different LLMs (OpenAI, Google Gemini, local models, etc.).

---

## Claude AI Dependencies Summary

### 1. **Import Statement** (Line 33)
```python
from langchain_anthropic import ChatAnthropic
```

**Required for:** Initializing Claude AI model
**Change needed:** Import different LangChain LLM wrapper

---

### 2. **Environment Variable** (Line 72)
```python
self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
```

**Required for:** API authentication
**Change needed:** Different environment variable name

---

### 3. **API Key Validation** (Line 73-74)
```python
if not self.api_key:
    raise ValueError("Anthropic API key is required")
```

**Required for:** Error handling
**Change needed:** Generic error message

---

### 4. **LLM Initialization** (Lines 76-80)
```python
self.llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    anthropic_api_key=self.api_key,
    temperature=0
)
```

**Required for:** All LLM operations
**Change needed:** Different LLM class and parameters

---

### 5. **LLM Usage Locations**

The `self.llm` object is used in these methods:

| Line | Method | Usage | Type |
|------|--------|-------|------|
| 294 | `query_single_document()` | Via RetrievalQA chain | Chain |
| 362 | `query_all_documents()` | Direct `.invoke()` call | Direct |
| 394 | `summarize_document()` | Via summarization chain | Chain |
| 440 | `compare_documents()` | Direct `.invoke()` call | Direct |
| 466 | `extract_contacts_from_document()` | Via prompt chain | Chain |

---

## Refactoring Strategy: LLM Abstraction Layer

### Option 1: Factory Pattern (Recommended for Multiple LLMs)

Create an LLM factory that returns the appropriate LLM instance:

```python
# llm_factory.py
from typing import Literal
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama

LLMProvider = Literal["claude", "openai", "gemini", "ollama"]

class LLMFactory:
    @staticmethod
    def create_llm(
        provider: LLMProvider,
        api_key: str = None,
        model: str = None,
        temperature: float = 0,
        **kwargs
    ):
        """Create LLM instance based on provider."""

        if provider == "claude":
            return ChatAnthropic(
                model=model or "claude-sonnet-4-20250514",
                anthropic_api_key=api_key or os.getenv("ANTHROPIC_API_KEY"),
                temperature=temperature
            )

        elif provider == "openai":
            return ChatOpenAI(
                model=model or "gpt-4o",
                api_key=api_key or os.getenv("OPENAI_API_KEY"),
                temperature=temperature
            )

        elif provider == "gemini":
            return ChatGoogleGenerativeAI(
                model=model or "gemini-2.0-flash-exp",
                google_api_key=api_key or os.getenv("GOOGLE_API_KEY"),
                temperature=temperature
            )

        elif provider == "ollama":
            return Ollama(
                model=model or "llama3.1",
                temperature=temperature
            )

        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    @staticmethod
    def get_default_env_var(provider: LLMProvider) -> str:
        """Get default environment variable name for provider."""
        mapping = {
            "claude": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "gemini": "GOOGLE_API_KEY",
            "ollama": None  # No API key needed
        }
        return mapping.get(provider)
```

### Option 2: Configuration-Based (Recommended for Single Deployment)

Use a configuration file to specify LLM settings:

```python
# config.py
import os
from dataclasses import dataclass

@dataclass
class LLMConfig:
    provider: str = "claude"  # claude, openai, gemini, ollama
    model: str = None
    api_key: str = None
    temperature: float = 0

    @classmethod
    def from_env(cls):
        """Load config from environment variables."""
        provider = os.getenv("LLM_PROVIDER", "claude")

        # Map provider to default model
        default_models = {
            "claude": "claude-sonnet-4-20250514",
            "openai": "gpt-4o",
            "gemini": "gemini-2.0-flash-exp",
            "ollama": "llama3.1"
        }

        # Map provider to env var
        api_key_vars = {
            "claude": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "gemini": "GOOGLE_API_KEY",
            "ollama": None
        }

        return cls(
            provider=provider,
            model=os.getenv("LLM_MODEL", default_models.get(provider)),
            api_key=os.getenv(api_key_vars[provider]) if api_key_vars[provider] else None,
            temperature=float(os.getenv("LLM_TEMPERATURE", "0"))
        )
```

---

## Modified `MultiPDFAnalyzer.__init__()` (Using Factory)

```python
def __init__(
    self,
    api_key: str = None,
    vectorstore_path: str = None,
    llm_provider: str = "claude",
    llm_model: str = None
):
    """Initialize the multi-PDF analyzer.

    Args:
        api_key: API key for the LLM provider (if required)
        vectorstore_path: Directory to save/load persistent vectorstores
        llm_provider: LLM provider to use (claude, openai, gemini, ollama)
        llm_model: Specific model name (uses provider default if None)
    """
    from llm_factory import LLMFactory

    # Create LLM instance using factory
    self.llm = LLMFactory.create_llm(
        provider=llm_provider,
        api_key=api_key,
        model=llm_model,
        temperature=0
    )

    # Embeddings are LLM-independent
    self.embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    self.documents = {}
    self.vectorstores = {}
    self.combined_vectorstore = None
    self._lock = Lock()
    self.vectorstore_path = vectorstore_path
```

---

## LangChain Compatibility Notes

### ✅ Compatible Methods (No Changes Needed)

All these methods work identically across LLM providers because they use LangChain's standard interfaces:

1. **`query_single_document()`** (line 294)
   - Uses `RetrievalQA.from_chain_type()`
   - Works with any LangChain LLM

2. **`summarize_document()`** (line 394)
   - Uses `load_summarize_chain()`
   - Works with any LangChain LLM

3. **`extract_contacts_from_document()`** (line 466)
   - Uses `prompt | self.llm | parser` (LCEL)
   - Works with any LangChain LLM

### ⚠️ Methods Requiring Attention

1. **`query_all_documents()`** (line 362)
   ```python
   answer = self.llm.invoke(prompt).content
   ```
   **Issue:** Direct `.invoke()` assumes response has `.content` attribute

   **Fix:** Use standard LangChain response handling
   ```python
   response = self.llm.invoke(prompt)
   answer = response.content if hasattr(response, 'content') else str(response)
   ```

2. **`compare_documents()`** (line 440)
   ```python
   response = self.llm.invoke(prompt.format(text=structured_text))
   return response.content
   ```
   **Same issue:** Assumes `.content` attribute

   **Fix:** Same as above

---

## Testing Different LLMs

### Claude (Current)
```python
analyzer = MultiPDFAnalyzer(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    llm_provider="claude",
    llm_model="claude-sonnet-4-20250514"
)
```

### OpenAI GPT-4
```python
analyzer = MultiPDFAnalyzer(
    api_key=os.getenv("OPENAI_API_KEY"),
    llm_provider="openai",
    llm_model="gpt-4o"
)
```

### Google Gemini
```python
analyzer = MultiPDFAnalyzer(
    api_key=os.getenv("GOOGLE_API_KEY"),
    llm_provider="gemini",
    llm_model="gemini-2.0-flash-exp"
)
```

### Local Ollama (No API Key)
```python
analyzer = MultiPDFAnalyzer(
    llm_provider="ollama",
    llm_model="llama3.1"
)
```

---

## Streamlit UI Changes

Update [claude_nvc_chatbot.py](claude_nvc_chatbot.py) to support LLM selection:

```python
# In sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    # LLM Provider selection
    llm_provider = st.selectbox(
        "LLM Provider",
        ["claude", "openai", "gemini", "ollama"],
        help="Select which LLM to use"
    )

    # Conditional API key input
    if llm_provider != "ollama":
        api_key_label = {
            "claude": "Anthropic API Key",
            "openai": "OpenAI API Key",
            "gemini": "Google API Key"
        }[llm_provider]

        env_var = {
            "claude": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "gemini": "GOOGLE_API_KEY"
        }[llm_provider]

        api_key = st.text_input(
            api_key_label,
            type="password",
            value=os.getenv(env_var, ""),
            help=f"Enter your {api_key_label}"
        )
    else:
        api_key = None
        st.info("Ollama runs locally - no API key needed")

    # Model selection (optional)
    model = st.text_input(
        "Model (optional)",
        help="Leave blank for default"
    )

# Update analyzer initialization
@st.cache_resource
def get_analyzer(api_key, vectorstore_path=None, llm_provider="claude", llm_model=None):
    """Get or create analyzer instance (cached across reruns)."""
    return MultiPDFAnalyzer(
        api_key=api_key,
        vectorstore_path=vectorstore_path,
        llm_provider=llm_provider,
        llm_model=llm_model
    )

# Use it
analyzer = get_analyzer(api_key, vectorstore_path, llm_provider, model)
```

---

## Cost Comparison (286 Documents, 10 Queries/Day)

| Provider | Model | Input Cost | Output Cost | Est. Monthly Cost |
|----------|-------|------------|-------------|-------------------|
| Claude | Sonnet 4.5 | $3/MTok | $15/MTok | $15-30 |
| OpenAI | GPT-4o | $2.50/MTok | $10/MTok | $12-25 |
| Google | Gemini 2.0 Flash | Free (rate limited) | Free | $0 |
| Ollama | Llama 3.1 | Free (local) | Free | $0 |

**Notes:**
- Estimates based on ~50k input tokens/query, ~500 output tokens/query
- Gemini Flash has daily limits (1500 requests/day)
- Ollama requires local GPU/CPU resources

---

## Performance Considerations

### Response Speed (Typical)
- **Claude Sonnet 4.5**: 5-10 seconds
- **GPT-4o**: 4-8 seconds
- **Gemini Flash**: 3-6 seconds
- **Ollama (local)**: 10-30 seconds (depends on hardware)

### Quality Ranking (Subjective)
1. Claude Sonnet 4.5 / GPT-4o (tie)
2. Gemini 2.0 Flash
3. Llama 3.1 (depends on size: 8B < 70B)

### Best Use Cases
- **Claude**: Best for complex reasoning, nuanced understanding
- **OpenAI**: Best API ecosystem, most tooling support
- **Gemini**: Best for high-volume, cost-sensitive workloads
- **Ollama**: Best for privacy, offline use, no API costs

---

## Migration Checklist

- [ ] Create `llm_factory.py` with factory pattern
- [ ] Update `MultiPDFAnalyzer.__init__()` to accept `llm_provider` parameter
- [ ] Fix `.content` attribute access in `query_all_documents()` and `compare_documents()`
- [ ] Update Streamlit UI to include LLM provider selection
- [ ] Update `get_analyzer()` cache function signature
- [ ] Test with all supported LLM providers
- [ ] Update environment variable documentation
- [ ] Update [LARGE_COLLECTION_GUIDE.md](LARGE_COLLECTION_GUIDE.md) with multi-LLM instructions
- [ ] Add requirements for different LLM providers to `requirements.txt`:
  ```
  # Claude (current)
  langchain-anthropic>=0.1.0

  # OpenAI (add these)
  langchain-openai>=0.1.0

  # Google Gemini (add these)
  langchain-google-genai>=0.0.5

  # Ollama (add these)
  langchain-community>=0.0.20  # Already included
  ```

---

## Summary

**Total Changes Required:** 5 locations

1. ✅ Import statement (1 new factory file)
2. ✅ `__init__()` method (use factory)
3. ✅ Fix `.content` access (2 methods)
4. ✅ Update Streamlit UI (provider selection)
5. ✅ Add new dependencies to requirements

**Effort:** ~2-3 hours for complete migration with testing

**Benefit:** Support for multiple LLM providers with ~90% code reuse
