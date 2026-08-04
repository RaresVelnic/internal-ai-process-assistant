"""Tests for the OpenAI embedding provider placeholder."""

import pytest

from internal_ai_process_assistant.rag.openai_embeddings import OpenAIEmbeddingProvider


def test_openai_embedding_provider_stores_configuration() -> None:
    provider = OpenAIEmbeddingProvider(
        api_key="test-key",
        model="text-embedding-3-small",
    )

    assert provider.api_key == "test-key"
    assert provider.model == "text-embedding-3-small"
    assert provider.allow_paid_embedding_calls is False


def test_openai_embedding_provider_rejects_empty_api_key() -> None:
    with pytest.raises(ValueError, match="API key"):
        OpenAIEmbeddingProvider(api_key="   ", model="text-embedding-3-small")


def test_openai_embedding_provider_rejects_empty_model() -> None:
    with pytest.raises(ValueError, match="model"):
        OpenAIEmbeddingProvider(api_key="test-key", model="   ")


def test_openai_embedding_provider_rejects_empty_text_before_api_call() -> None:
    provider = OpenAIEmbeddingProvider(
        api_key="test-key",
        model="text-embedding-3-small",
    )

    with pytest.raises(ValueError, match="text"):
        provider.embed_text("   ")


def test_openai_embedding_provider_blocks_paid_calls_by_default() -> None:
    provider = OpenAIEmbeddingProvider(
        api_key="test-key",
        model="text-embedding-3-small",
    )

    with pytest.raises(PermissionError, match="Paid embedding calls are disabled"):
        provider.embed_text("hello world")


def test_openai_embedding_provider_does_not_call_api_yet_when_paid_calls_are_allowed() -> None:
    provider = OpenAIEmbeddingProvider(
        api_key="test-key",
        model="text-embedding-3-small",
        allow_paid_embedding_calls=True,
    )

    with pytest.raises(NotImplementedError, match="not implemented"):
        provider.embed_text("hello world")
