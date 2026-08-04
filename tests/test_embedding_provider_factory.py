"""Tests for embedding provider selection."""

import pytest

from internal_ai_process_assistant.config import AppConfig, load_config
from internal_ai_process_assistant.rag.embedding_provider_factory import get_embedding_provider
from internal_ai_process_assistant.rag.embeddings import DeterministicEmbeddingProvider
from internal_ai_process_assistant.rag.openai_embeddings import OpenAIEmbeddingProvider


def test_get_embedding_provider_returns_deterministic_provider_by_default() -> None:
    config = load_config({})

    provider = get_embedding_provider(config)

    assert isinstance(provider, DeterministicEmbeddingProvider)


def test_get_embedding_provider_returns_openai_provider_placeholder() -> None:
    config = load_config(
        {
            "IAPA_EMBEDDING_PROVIDER": "openai",
            "OPENAI_API_KEY": "test-key",
        }
    )

    provider = get_embedding_provider(config)

    assert isinstance(provider, OpenAIEmbeddingProvider)
    assert provider.api_key == "test-key"
    assert provider.model == "text-embedding-3-small"


def test_get_embedding_provider_rejects_unknown_provider_defensively() -> None:
    config = AppConfig(
        embedding_provider="unknown",
        openai_api_key=None,
        openai_embedding_model="text-embedding-3-small",
        max_embedding_chunks_per_run=20,
        max_estimated_embedding_tokens_per_run=20_000,
        allow_paid_embedding_calls=False,
    )

    with pytest.raises(ValueError, match="Unsupported embedding provider"):
        get_embedding_provider(config)
