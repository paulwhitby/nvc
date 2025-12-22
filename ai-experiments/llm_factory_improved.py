"""Improved LLM Factory with Configuration Objects and Dispatch Pattern

This module provides a clean abstraction for working with multiple LLM providers
through a unified interface.
"""

import os
from typing import Literal, Optional, Dict, Any, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# LangChain imports - conditional to avoid errors if packages not installed
try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    ChatAnthropic = None

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

try:
    from langchain_community.llms import Ollama
except ImportError:
    Ollama = None


LLMProvider = Literal["claude", "openai", "gemini", "ollama"]


@dataclass
class LLMConfig:
    """Configuration for LLM provider.

    Args:
        provider: LLM provider name (claude, openai, gemini, ollama)
        model: Model name (uses provider default if None)
        api_key: API key (uses environment variable if None)
        temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative)
        max_tokens: Maximum tokens in response (None = provider default)
        streaming: Enable streaming responses
        extra_params: Additional provider-specific parameters
    """
    provider: LLMProvider
    model: Optional[str] = None
    api_key: Optional[str] = None
    temperature: float = 0
    max_tokens: Optional[int] = None
    streaming: bool = False
    extra_params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_env(cls, provider: Optional[LLMProvider] = None) -> "LLMConfig":
        """Create configuration from environment variables.

        Args:
            provider: Provider name (uses LLM_PROVIDER env var if None)

        Returns:
            LLMConfig instance populated from environment
        """
        provider = provider or os.getenv("LLM_PROVIDER", "claude")

        return cls(
            provider=provider,
            model=os.getenv("LLM_MODEL"),
            api_key=None,  # Will be loaded by factory from provider-specific env var
            temperature=float(os.getenv("LLM_TEMPERATURE", "0")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS")) if os.getenv("LLM_MAX_TOKENS") else None,
            streaming=os.getenv("LLM_STREAMING", "false").lower() == "true"
        )


class LLMWrapper(ABC):
    """Lightweight wrapper for LLM instances providing consistent interface.

    This wrapper maintains LangChain compatibility while providing
    a standardized response format.
    """

    def __init__(self, llm_instance, provider: LLMProvider):
        """Initialize wrapper.

        Args:
            llm_instance: Underlying LangChain LLM instance
            provider: Provider name for this instance
        """
        self._llm = llm_instance
        self.provider = provider

    def invoke(self, prompt: str, **kwargs) -> Any:
        """Invoke the LLM with standardized response handling.

        Args:
            prompt: Input prompt
            **kwargs: Additional parameters for invoke

        Returns:
            Response from LLM (preserves LangChain format for chain compatibility)
        """
        return self._llm.invoke(prompt, **kwargs)

    def extract_content(self, response: Any) -> str:
        """Extract text content from LLM response.

        Args:
            response: LLM response object

        Returns:
            String content from response
        """
        # Handle AIMessage objects (most LangChain LLMs)
        if hasattr(response, 'content'):
            return response.content

        # Handle string responses (some Ollama configurations)
        if isinstance(response, str):
            return response

        # Fallback
        return str(response)

    def invoke_text(self, prompt: str, **kwargs) -> str:
        """Invoke and return text content directly.

        This is a convenience method for when you just want the text response.

        Args:
            prompt: Input prompt
            **kwargs: Additional parameters for invoke

        Returns:
            String content from response
        """
        response = self.invoke(prompt, **kwargs)
        return self.extract_content(response)

    @property
    def llm(self):
        """Access underlying LLM instance for chain operations."""
        return self._llm

    def __getattr__(self, name):
        """Delegate attribute access to underlying LLM for chain compatibility."""
        return getattr(self._llm, name)


class LLMFactory:
    """Factory for creating LLM instances across different providers.

    This factory uses a dispatch table pattern for extensibility.
    """

    # Default models for each provider
    DEFAULT_MODELS = {
        "claude": "claude-sonnet-4-20250514",
        "openai": "gpt-4o",
        "gemini": "gemini-2.0-flash-exp",
        "ollama": "llama3.1"
    }

    # Environment variable mapping
    ENV_VARS = {
        "claude": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
        "gemini": "GOOGLE_API_KEY",
        "ollama": None  # No API key needed
    }

    # Provider display names
    DISPLAY_NAMES = {
        "claude": "Claude (Anthropic)",
        "openai": "ChatGPT (OpenAI)",
        "gemini": "Gemini (Google)",
        "ollama": "Ollama (Local)"
    }

    # Feature support matrix
    FEATURE_SUPPORT = {
        "claude": {
            "compression": True,
            "structured_output": True,
            "long_context": True,
            "max_context": 200000
        },
        "openai": {
            "compression": True,
            "structured_output": True,
            "long_context": True,
            "max_context": 128000
        },
        "gemini": {
            "compression": True,  # But slower
            "structured_output": False,  # Limited support
            "long_context": True,
            "max_context": 1000000
        },
        "ollama": {
            "compression": False,  # Resource intensive, may fail
            "structured_output": False,  # Unreliable with smaller models
            "long_context": False,
            "max_context": 4096  # Typical for 8B models
        }
    }

    # --- Private creator methods for each provider ---

    @staticmethod
    def _create_claude(config: LLMConfig) -> Any:
        """Create Claude LLM instance."""
        if ChatAnthropic is None:
            raise ImportError(
                "langchain-anthropic is not installed. "
                "Install it with: pip install langchain-anthropic"
            )
        if not config.api_key:
            raise ValueError("Anthropic API key is required for Claude")

        kwargs = {
            "model": config.model,
            "anthropic_api_key": config.api_key,
            "temperature": config.temperature,
        }

        if config.max_tokens:
            kwargs["max_tokens"] = config.max_tokens
        if config.streaming:
            kwargs["streaming"] = config.streaming

        kwargs.update(config.extra_params)

        return ChatAnthropic(**kwargs)

    @staticmethod
    def _create_openai(config: LLMConfig) -> Any:
        """Create OpenAI LLM instance."""
        if ChatOpenAI is None:
            raise ImportError(
                "langchain-openai is not installed. "
                "Install it with: pip install langchain-openai"
            )
        if not config.api_key:
            raise ValueError("OpenAI API key is required for ChatGPT")

        kwargs = {
            "model": config.model,
            "api_key": config.api_key,
            "temperature": config.temperature,
        }

        if config.max_tokens:
            kwargs["max_tokens"] = config.max_tokens
        if config.streaming:
            kwargs["streaming"] = config.streaming

        kwargs.update(config.extra_params)

        return ChatOpenAI(**kwargs)

    @staticmethod
    def _create_gemini(config: LLMConfig) -> Any:
        """Create Gemini LLM instance."""
        if ChatGoogleGenerativeAI is None:
            raise ImportError(
                "langchain-google-genai is not installed. "
                "Install it with: pip install langchain-google-genai"
            )
        if not config.api_key:
            raise ValueError("Google API key is required for Gemini")

        kwargs = {
            "model": config.model,
            "google_api_key": config.api_key,
            "temperature": config.temperature,
        }

        if config.max_tokens:
            kwargs["max_output_tokens"] = config.max_tokens

        kwargs.update(config.extra_params)

        return ChatGoogleGenerativeAI(**kwargs)

    @staticmethod
    def _create_ollama(config: LLMConfig) -> Any:
        """Create Ollama LLM instance."""
        if Ollama is None:
            raise ImportError(
                "langchain-community is not installed. "
                "Install it with: pip install langchain-community"
            )

        kwargs = {
            "model": config.model,
            "temperature": config.temperature,
        }

        # Ollama-specific parameters
        if config.max_tokens:
            kwargs["num_predict"] = config.max_tokens

        kwargs.update(config.extra_params)

        return Ollama(**kwargs)

    # --- Dispatch table mapping provider to creator function ---
    _CREATOR_MAP: Dict[LLMProvider, Callable[[LLMConfig], Any]] = {
        "claude": _create_claude.__func__,
        "openai": _create_openai.__func__,
        "gemini": _create_gemini.__func__,
        "ollama": _create_ollama.__func__,
    }

    @classmethod
    def create_llm(cls, config: LLMConfig) -> LLMWrapper:
        """Create LLM instance from a configuration object.

        Args:
            config: LLMConfig object with provider settings

        Returns:
            LLMWrapper instance wrapping the provider's LLM

        Raises:
            ValueError: If provider is unsupported or configuration is invalid
            ImportError: If required package is not installed
        """

        # 1. Get the creator function from dispatch table
        creator_func = cls._CREATOR_MAP.get(config.provider)
        if not creator_func:
            raise ValueError(f"Unsupported LLM provider: {config.provider}")

        # 2. Fill in missing configuration details
        if not config.model:
            config.model = cls.DEFAULT_MODELS[config.provider]

        if not config.api_key:
            env_var = cls.ENV_VARS.get(config.provider)
            if env_var:
                config.api_key = os.getenv(env_var)

        # 3. Validate configuration
        is_valid, error_msg = cls.validate_config(config.provider, config.api_key)
        if not is_valid:
            raise ValueError(error_msg)

        # 4. Create the LLM instance
        llm_instance = creator_func(config)

        # 5. Wrap in our abstraction layer
        return LLMWrapper(llm_instance, config.provider)

    @classmethod
    def get_available_providers(cls) -> Dict[str, bool]:
        """Check which providers are available (packages installed).

        Returns:
            Dict mapping provider name to availability status
        """
        return {
            "claude": ChatAnthropic is not None,
            "openai": ChatOpenAI is not None,
            "gemini": ChatGoogleGenerativeAI is not None,
            "ollama": Ollama is not None
        }

    @classmethod
    def validate_config(cls, provider: LLMProvider, api_key: Optional[str] = None) -> tuple[bool, str]:
        """Validate configuration for a provider.

        Args:
            provider: Provider name
            api_key: API key to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if package is installed
        available = cls.get_available_providers()
        if not available.get(provider):
            return False, f"Package for {cls.DISPLAY_NAMES[provider]} is not installed"

        # Check API key if required
        env_var = cls.ENV_VARS.get(provider)
        if env_var:
            key = api_key or os.getenv(env_var)
            if not key:
                return False, f"API key required for {cls.DISPLAY_NAMES[provider]}"

        return True, ""

    @classmethod
    def get_feature_support(cls, provider: LLMProvider) -> Dict[str, Any]:
        """Get feature support information for a provider.

        Args:
            provider: Provider name

        Returns:
            Dict with feature support flags and limits
        """
        return cls.FEATURE_SUPPORT.get(provider, {})

    @classmethod
    def check_feature_compatibility(cls, provider: LLMProvider, feature: str) -> tuple[bool, str]:
        """Check if provider supports a specific feature.

        Args:
            provider: Provider name
            feature: Feature name (e.g., 'compression', 'structured_output')

        Returns:
            Tuple of (is_supported, warning_message)
        """
        support = cls.get_feature_support(provider)

        if feature not in support:
            return True, ""  # Unknown feature, assume supported

        if not support[feature]:
            warnings = {
                "compression": (
                    f"{cls.DISPLAY_NAMES[provider]} may not support contextual compression reliably. "
                    "Consider using a simpler retrieval strategy."
                ),
                "structured_output": (
                    f"{cls.DISPLAY_NAMES[provider]} has limited structured output support. "
                    "Pydantic parsing may fail or produce inconsistent results."
                ),
                "long_context": (
                    f"{cls.DISPLAY_NAMES[provider]} has limited context window. "
                    "Consider reducing chunk count or using summarization."
                )
            }
            return False, warnings.get(feature, f"Feature '{feature}' not supported")

        return True, ""


# Convenience functions for backward compatibility

def create_llm(provider: LLMProvider, **kwargs) -> LLMWrapper:
    """Convenience function to create LLM instance from individual parameters.

    This is maintained for backward compatibility but using LLMConfig directly
    is preferred.

    Args:
        provider: Provider name
        **kwargs: Parameters matching LLMConfig fields

    Returns:
        LLMWrapper instance
    """
    config = LLMConfig(provider=provider, **kwargs)
    return LLMFactory.create_llm(config)


def create_llm_from_env() -> LLMWrapper:
    """Create LLM instance from environment variables.

    Reads configuration from:
    - LLM_PROVIDER (default: claude)
    - LLM_MODEL (default: provider-specific)
    - LLM_TEMPERATURE (default: 0)
    - Provider-specific API key env vars

    Returns:
        LLMWrapper instance
    """
    config = LLMConfig.from_env()
    return LLMFactory.create_llm(config)
