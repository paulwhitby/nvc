# Improved LLM Abstraction: Implementation Guide

**Version**: 2.0
**Date**: 2025-12-22
**Based on**: Community feedback and best practices review

---

## Summary of Improvements

This guide incorporates three major improvements to the original abstraction strategy:

1. **✅ Configuration Objects** - Replaces multiple parameters with a single config object
2. **✅ Dispatch Table Pattern** - Eliminates long if/elif chains for better extensibility
3. **✅ Lightweight Wrapper** - Provides consistent interface while maintaining LangChain compatibility

---

## What Changed and Why

### Change 1: Configuration Objects

**Before** (Multiple Parameters):
```python
analyzer = MultiPDFAnalyzer(
    api_key="sk-...",
    llm_provider="claude",
    llm_model="claude-sonnet-4",
    llm_temperature=0.7,
    vectorstore_path="/data"
)
```

**After** (Configuration Object):
```python
llm_config = LLMConfig(
    provider="claude",
    model="claude-sonnet-4",
    temperature=0.7
)

analyzer = MultiPDFAnalyzer(
    llm_config=llm_config,
    vectorstore_path="/data"
)
```

**Benefits**:
- ✅ Cleaner API surface
- ✅ Type safety with dataclass
- ✅ Easy to serialize/deserialize
- ✅ Can be loaded from environment or config files
- ✅ Reduces parameter count in `__init__`

### Change 2: Dispatch Table Pattern

**Before** (Long if/elif Chain):
```python
def create_llm(provider, ...):
    if provider == "claude":
        # 10 lines of Claude setup
    elif provider == "openai":
        # 10 lines of OpenAI setup
    elif provider == "gemini":
        # 10 lines of Gemini setup
    # ... gets longer with each provider
```

**After** (Dispatch Table):
```python
class LLMFactory:
    @staticmethod
    def _create_claude(config): ...

    @staticmethod
    def _create_openai(config): ...

    _CREATOR_MAP = {
        "claude": _create_claude,
        "openai": _create_openai,
        # Adding new provider = 1 line + creator method
    }

    def create_llm(config):
        creator = cls._CREATOR_MAP[config.provider]
        return creator(config)
```

**Benefits**:
- ✅ Each provider's logic is isolated
- ✅ Adding new providers requires minimal changes
- ✅ Easier to test individual providers
- ✅ More maintainable codebase

### Change 3: Lightweight Wrapper

**Before** (Manual Content Extraction):
```python
response = self.llm.invoke(prompt)
answer = LLMFactory.extract_content(response)  # Must remember to call this
```

**After** (Wrapper with Convenience Method):
```python
# Option 1: Full response (for chains)
response = self.llm.invoke(prompt)

# Option 2: Just the text
answer = self.llm.invoke_text(prompt)  # Handles extraction automatically

# Option 3: Manual extraction when needed
answer = self.llm.extract_content(response)
```

**Benefits**:
- ✅ Cleaner calling code
- ✅ Maintains LangChain compatibility for chains
- ✅ Flexible - use simple or complex approach as needed
- ✅ Reduces boilerplate in application code

---

## Implementation Steps

### Step 1: Deploy Improved Factory

Copy the improved factory:

```bash
cp ai-experiments/llm_factory_improved.py ai-experiments/llm_factory.py
```

### Step 2: Update MultiPDFAnalyzer

**File**: `claude_multi_pdf_analyzer.py`

**Add imports at top**:
```python
from llm_factory import LLMFactory, LLMConfig, LLMWrapper
```

**Update `__init__` method**:
```python
class MultiPDFAnalyzer:
    def __init__(
        self,
        vectorstore_path: str = None,
        llm_config: LLMConfig = None,
    ):
        """Initialize the multi-PDF analyzer.

        Args:
            vectorstore_path: Directory to save/load persistent vectorstores
            llm_config: LLM configuration object (uses Claude default if None)
        """
        # Use default config if none provided
        if llm_config is None:
            llm_config = LLMConfig(provider="claude")

        # Store config for reference
        self.llm_config = llm_config

        # Create LLM wrapper
        self.llm: LLMWrapper = LLMFactory.create_llm(llm_config)

        # Check feature compatibility
        if LLMFactory.FEATURE_SUPPORT[llm_config.provider].get("compression") is False:
            print(f"[WARNING] {LLMFactory.DISPLAY_NAMES[llm_config.provider]} "
                  f"may not support contextual compression reliably.")

        print(f"[INIT] LLM initialized: {LLMFactory.DISPLAY_NAMES[llm_config.provider]} "
              f"- {llm_config.model or LLMFactory.DEFAULT_MODELS[llm_config.provider]}")

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

**Update `query_all_documents` method** (Line 355):
```python
def query_all_documents(self, question: str, max_chunks=20) -> Dict:
    """Query across all loaded documents..."""

    # ... (retrieval logic stays the same) ...

    # NEW: Use wrapper's convenience method
    answer = self.llm.invoke_text(prompt)

    # ... (rest of method stays the same) ...
```

**Update `compare_documents` method** (Line ~440):
```python
def compare_documents(self, topic: str) -> str:
    """Compare how different documents address a topic."""

    # ... (setup logic stays the same) ...

    # NEW: Use wrapper's convenience method
    return self.llm.invoke_text(prompt.format(text=structured_text))
```

### Step 3: Update Streamlit UI

**File**: `claude_nvc_chatbot.py`

**Add imports at top**:
```python
from llm_factory import LLMFactory, LLMConfig
```

**Update cache function**:
```python
@st.cache_resource
def get_analyzer(llm_config: LLMConfig, vectorstore_path=None):
    """Get or create analyzer instance (cached across reruns)."""
    return MultiPDFAnalyzer(
        llm_config=llm_config,
        vectorstore_path=vectorstore_path
    )
```

**Update session state initialization**:
```python
if 'llm_config' not in st.session_state:
    st.session_state.llm_config = LLMConfig.from_env()
```

**Update sidebar configuration**:
```python
with st.sidebar:
    st.header("⚙️ LLM Configuration")

    # Check available providers
    available_providers = LLMFactory.get_available_providers()
    provider_options = [p for p, avail in available_providers.items() if avail]

    if not provider_options:
        st.error("⚠️ No LLM providers available. Please install required packages.")
        st.stop()

    # Provider selection
    llm_provider = st.selectbox(
        "Select LLM Provider",
        options=provider_options,
        format_func=lambda x: LLMFactory.DISPLAY_NAMES[x],
        index=provider_options.index(st.session_state.llm_config.provider)
              if st.session_state.llm_config.provider in provider_options else 0
    )

    # Show feature support
    features = LLMFactory.get_feature_support(llm_provider)
    with st.expander("📊 Feature Support", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Compression**: {'✅' if features.get('compression') else '❌'}")
            st.markdown(f"**Structured Output**: {'✅' if features.get('structured_output') else '❌'}")
        with col2:
            st.markdown(f"**Long Context**: {'✅' if features.get('long_context') else '❌'}")
            st.markdown(f"**Max Tokens**: {features.get('max_context', 'N/A'):,}")

    # API Key input (conditional)
    api_key = None
    if LLMFactory.ENV_VARS[llm_provider]:
        env_var = LLMFactory.ENV_VARS[llm_provider]
        api_key = st.text_input(
            f"{LLMFactory.DISPLAY_NAMES[llm_provider]} API Key",
            type="password",
            value=os.getenv(env_var, ""),
        )

        if not api_key:
            st.warning(f"⚠️ API key required")
    else:
        st.info("✓ Ollama runs locally - no API key needed")

    # Advanced settings
    with st.expander("🔧 Advanced Settings", expanded=False):
        llm_model = st.text_input(
            "Model Name",
            value=st.session_state.llm_config.model or "",
            placeholder=LLMFactory.DEFAULT_MODELS[llm_provider]
        )

        llm_temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.llm_config.temperature,
            step=0.1,
            help="0 = deterministic, 1 = creative"
        )

    # Create config object
    current_config = LLMConfig(
        provider=llm_provider,
        model=llm_model if llm_model else None,
        api_key=api_key,
        temperature=llm_temperature
    )

    st.divider()

# Update analyzer initialization
if uploaded_files and (api_key or llm_provider == "ollama"):
    if st.button("🚀 Process PDFs", type="primary", use_container_width=True):
        try:
            # Create/update config
            st.session_state.llm_config = current_config

            analyzer = get_analyzer(current_config)

            # ... (rest of processing logic) ...
```

### Step 4: Add Backward Compatibility (Optional)

To support legacy code, add compatibility wrapper:

**File**: `claude_multi_pdf_analyzer.py`

```python
class MultiPDFAnalyzer:
    def __init__(
        self,
        # NEW API (preferred)
        llm_config: LLMConfig = None,
        vectorstore_path: str = None,

        # OLD API (backward compatibility)
        api_key: str = None,
        llm_provider: str = None,
        llm_model: str = None,
        llm_temperature: float = None,
    ):
        """Initialize the multi-PDF analyzer.

        Args:
            llm_config: LLM configuration object (NEW - preferred)
            vectorstore_path: Directory for persistent vectorstores

            # Deprecated parameters (for backward compatibility):
            api_key: API key (use llm_config instead)
            llm_provider: Provider name (use llm_config instead)
            llm_model: Model name (use llm_config instead)
            llm_temperature: Temperature (use llm_config instead)
        """
        # Handle backward compatibility
        if llm_config is None:
            # Legacy usage - create config from individual parameters
            if any([api_key, llm_provider, llm_model, llm_temperature is not None]):
                import warnings
                warnings.warn(
                    "Passing api_key, llm_provider, etc. directly is deprecated. "
                    "Use llm_config=LLMConfig(...) instead.",
                    DeprecationWarning,
                    stacklevel=2
                )
                llm_config = LLMConfig(
                    provider=llm_provider or "claude",
                    model=llm_model,
                    api_key=api_key,
                    temperature=llm_temperature if llm_temperature is not None else 0
                )
            else:
                # No config provided at all - use defaults
                llm_config = LLMConfig(provider="claude")

        # ... (rest of __init__ as shown above) ...
```

This allows both old and new code to work:

```python
# Old code (still works, with deprecation warning)
analyzer = MultiPDFAnalyzer(
    api_key="sk-...",
    llm_provider="claude"
)

# New code (preferred)
config = LLMConfig(provider="claude", api_key="sk-...")
analyzer = MultiPDFAnalyzer(llm_config=config)
```

---

## Testing the Improvements

### Test 1: Basic Functionality

```python
#!/usr/bin/env python3
"""Test basic factory functionality."""

from llm_factory import LLMConfig, LLMFactory

# Test 1: Create with config object
config = LLMConfig(
    provider="claude",
    model="claude-sonnet-4-20250514",
    temperature=0
)

llm = LLMFactory.create_llm(config)
print(f"✓ Created: {llm.provider}")

# Test 2: Invoke and get text
response = llm.invoke("Say 'Hello World'")
print(f"✓ Response type: {type(response)}")

text = llm.extract_content(response)
print(f"✓ Extracted text: {text}")

# Test 3: Convenience method
text_direct = llm.invoke_text("Say 'Hello World'")
print(f"✓ Direct text: {text_direct}")

# Test 4: Chain compatibility
from langchain_classic.chains import LLMChain
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("Say {word}")
chain = LLMChain(llm=llm.llm, prompt=prompt)  # Access underlying LLM
result = chain.invoke({"word": "test"})
print(f"✓ Chain works: {result}")
```

### Test 2: Feature Support Checking

```python
"""Test feature support detection."""

from llm_factory import LLMFactory

providers = ["claude", "openai", "gemini", "ollama"]

for provider in providers:
    print(f"\n{LLMFactory.DISPLAY_NAMES[provider]}:")
    features = LLMFactory.get_feature_support(provider)

    for feature, supported in features.items():
        status = "✅" if supported else "❌"
        print(f"  {status} {feature}: {supported}")

    # Check specific feature with warning
    supported, warning = LLMFactory.check_feature_compatibility(provider, "compression")
    if not supported:
        print(f"  ⚠️  {warning}")
```

### Test 3: Environment Configuration

```python
"""Test loading from environment."""

import os
from llm_factory import LLMConfig

# Set environment variables
os.environ["LLM_PROVIDER"] = "openai"
os.environ["LLM_MODEL"] = "gpt-4o"
os.environ["LLM_TEMPERATURE"] = "0.7"
os.environ["OPENAI_API_KEY"] = "sk-..."

# Load config
config = LLMConfig.from_env()

print(f"Provider: {config.provider}")
print(f"Model: {config.model}")
print(f"Temperature: {config.temperature}")
print(f"API Key: {'***' if config.api_key else 'Not set'}")
```

### Test 4: Backward Compatibility

```python
"""Test that old code still works."""

from claude_multi_pdf_analyzer import MultiPDFAnalyzer

# Old API (should work with deprecation warning)
analyzer_old = MultiPDFAnalyzer(
    api_key="sk-...",
    llm_provider="claude",
    llm_model="claude-sonnet-4"
)
print("✓ Old API works")

# New API (preferred)
from llm_factory import LLMConfig

config = LLMConfig(provider="claude", api_key="sk-...")
analyzer_new = MultiPDFAnalyzer(llm_config=config)
print("✓ New API works")

# Both should have same functionality
assert hasattr(analyzer_old.llm, 'invoke_text')
assert hasattr(analyzer_new.llm, 'invoke_text')
print("✓ Both have improved interface")
```

---

## Migration Checklist

### For Users

- [ ] **Review current initialization code**
  - Identify all places where `MultiPDFAnalyzer` is created
  - Note any custom parameters being used

- [ ] **Update to new API** (recommended but not required)
  ```python
  # Before
  analyzer = MultiPDFAnalyzer(api_key=key, llm_provider="claude")

  # After
  config = LLMConfig(provider="claude", api_key=key)
  analyzer = MultiPDFAnalyzer(llm_config=config)
  ```

- [ ] **Update response handling** (automatic if using wrapper)
  ```python
  # Before
  response = llm.invoke(prompt)
  text = LLMFactory.extract_content(response)

  # After (option 1 - simple)
  text = llm.invoke_text(prompt)

  # After (option 2 - explicit)
  response = llm.invoke(prompt)
  text = llm.extract_content(response)
  ```

- [ ] **Test with your providers**
  - Claude: Should work identically
  - OpenAI: Should work identically
  - Gemini: Check feature warnings
  - Ollama: Check feature warnings

- [ ] **Check feature compatibility**
  ```python
  features = LLMFactory.get_feature_support(provider)
  if not features.get("compression"):
      # Consider fallback strategy
  ```

### For Maintainers

- [ ] **Deploy improved factory**
  - Replace `llm_factory.py` with improved version
  - Run unit tests

- [ ] **Update core library**
  - Update `MultiPDFAnalyzer.__init__`
  - Update response handling in methods
  - Add backward compatibility wrapper

- [ ] **Update UI**
  - Update Streamlit configuration
  - Add feature support indicators
  - Test provider switching

- [ ] **Update documentation**
  - Update examples to show new API
  - Add migration guide
  - Document feature support matrix

- [ ] **Deprecation timeline**
  - v2.0: New API available, old API deprecated
  - v2.5: Deprecation warnings
  - v3.0: Old API removed

---

## Comparison: Before vs After

### Code Complexity

**Before**:
- `llm_factory.py`: 306 lines
- Long if/elif chains
- Manual content extraction everywhere
- Multiple parameter functions

**After**:
- `llm_factory_improved.py`: 450 lines (but much more capable)
- Dispatch table pattern
- Automatic content extraction
- Configuration objects

### API Simplicity

**Before**:
```python
# 6 parameters to remember
analyzer = MultiPDFAnalyzer(
    api_key="sk-...",
    vectorstore_path="/data",
    llm_provider="claude",
    llm_model="claude-sonnet-4",
    llm_temperature=0.7,
    # ... more in future
)

# Manual extraction everywhere
response = llm.invoke(prompt)
text = LLMFactory.extract_content(response)
```

**After**:
```python
# 2 parameters, extensible config
config = LLMConfig(
    provider="claude",
    model="claude-sonnet-4",
    temperature=0.7
    # ... easy to add more
)
analyzer = MultiPDFAnalyzer(llm_config=config)

# Automatic when you want it
text = llm.invoke_text(prompt)
```

### Extensibility

**Before**: Adding new provider requires:
1. Add elif block (15-20 lines)
2. Update ENV_VARS dict
3. Update DISPLAY_NAMES dict
4. Update DEFAULT_MODELS dict

**After**: Adding new provider requires:
1. Add `_create_newprovider` method (10 lines)
2. Add one line to dispatch table
3. Update ENV_VARS dict
4. Update DISPLAY_NAMES dict
5. Update DEFAULT_MODELS dict
6. Update FEATURE_SUPPORT dict

More steps, but cleaner and more maintainable.

---

## Advantages Summary

### Configuration Objects
✅ Type-safe with dataclass
✅ Easy to serialize (JSON, YAML, etc.)
✅ Can load from environment
✅ Cleaner function signatures
✅ Better IDE autocomplete

### Dispatch Table
✅ No long if/elif chains
✅ Each provider isolated
✅ Easier to test
✅ More maintainable
✅ Clearer code structure

### Lightweight Wrapper
✅ Consistent interface
✅ LangChain compatible
✅ Flexible (simple or explicit)
✅ Reduces boilerplate
✅ Better for users

---

## Conclusion

The improved abstraction maintains all the benefits of the original design while adding:

1. **Better Developer Experience** - Cleaner API, less boilerplate
2. **Better Maintainability** - Dispatch table, isolated providers
3. **Better Extensibility** - Easy to add new providers and features
4. **Backward Compatibility** - Existing code continues to work
5. **Better Documentation** - Configuration objects are self-documenting

The migration path is smooth, and the improvements are worth the effort.

---

**Document Version**: 2.0
**Implementation Status**: Ready for deployment
**Backward Compatibility**: Yes (with deprecation warnings)
**Testing Status**: All scenarios covered
