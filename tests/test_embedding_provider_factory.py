"""Tests for embedding provider selection."""

import pytest

from internal_ai_process_assistant.config import AppConfig, load_config
from internal_ai_process_assistant.rag.embedding_provider_factory import get_embedding_provider
from internal_ai_process_assistant.rag.embeddings import DeterministicEmbeddingProvider


def test_get_embedding_provider_returns_deterministic_provider_by_default() -> None:
    config = load_config({})

    provider = get_embedding_provider(config)

    assert isinstance(provider, DeterministicEmbeddingProvider)


def test_get_embedding_provider_rejects_openai_until_provider_is_implemented() -> None:
    config = load_config(
        {
            "IAPA_EMBEDDING_PROVIDER": "openai",
            "OPENAI_API_KEY": "test-key",
        }
    )

    with pytest.raises(NotImplementedError, match="OpenAI embedding provider"):
        get_embedding_provider(config)


def test_get_embedding_provider_rejects_unknown_provider_defensively() -> None:
    config = AppConfig(
        embedding_provider="unknown",
        openai_api_key=None,
        openai_embedding_model="text-embedding-3-small",
        max_embedding_chunks_per_run=20,
        max_estimated_embedding_tokens_per_run=20_000,
    )

    with pytest.raises(ValueError, match="Unsupported embedding provider"):
        get_embedding_provider(config)
