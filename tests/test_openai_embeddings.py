"""Tests for the OpenAI embedding provider."""

from dataclasses import dataclass

import pytest

from internal_ai_process_assistant.rag.embeddings import EmbeddingVector
from internal_ai_process_assistant.rag.openai_embeddings import OpenAIEmbeddingProvider


@dataclass(frozen=True)
class FakeEmbedding:
    embedding: list[float]


@dataclass(frozen=True)
class FakeEmbeddingResponse:
    data: list[FakeEmbedding]


class FakeEmbeddingsResource:
    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []

    def create(
        self,
        *,
        input: str,
        model: str,
        encoding_format: str,
    ) -> FakeEmbeddingResponse:
        self.calls.append(
            {
                "input": input,
                "model": model,
                "encoding_format": encoding_format,
            }
        )
        return FakeEmbeddingResponse(data=[FakeEmbedding(embedding=[0.1, 0.2, 0.3])])


class FakeOpenAIClient:
    def __init__(self) -> None:
        self.embeddings = FakeEmbeddingsResource()


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
    client = FakeOpenAIClient()
    provider = OpenAIEmbeddingProvider(
        api_key="test-key",
        model="text-embedding-3-small",
        client=client,
    )

    with pytest.raises(PermissionError, match="Paid embedding calls are disabled"):
        provider.embed_text("hello world")

    assert client.embeddings.calls == []


def test_openai_embedding_provider_uses_injected_client_when_paid_calls_are_allowed() -> None:
    client = FakeOpenAIClient()
    provider = OpenAIEmbeddingProvider(
        api_key="test-key",
        model="text-embedding-3-small",
        allow_paid_embedding_calls=True,
        client=client,
    )

    embedding = provider.embed_text("  hello world  ")

    assert isinstance(embedding, EmbeddingVector)
    assert embedding.values == (0.1, 0.2, 0.3)
    assert client.embeddings.calls == [
        {
            "input": "hello world",
            "model": "text-embedding-3-small",
            "encoding_format": "float",
        }
    ]


def test_openai_embedding_provider_rejects_response_without_data() -> None:
    class EmptyEmbeddingsResource:
        def create(
            self,
            *,
            input: str,
            model: str,
            encoding_format: str,
        ) -> FakeEmbeddingResponse:
            return FakeEmbeddingResponse(data=[])

    class EmptyClient:
        embeddings = EmptyEmbeddingsResource()

    provider = OpenAIEmbeddingProvider(
        api_key="test-key",
        model="text-embedding-3-small",
        allow_paid_embedding_calls=True,
        client=EmptyClient(),
    )

    with pytest.raises(ValueError, match="did not contain data"):
        provider.embed_text("hello world")


def test_openai_embedding_provider_rejects_response_without_embedding() -> None:
    @dataclass(frozen=True)
    class EmptyEmbedding:
        embedding: list[float]

    class EmptyEmbeddingResource:
        def create(
            self,
            *,
            input: str,
            model: str,
            encoding_format: str,
        ) -> FakeEmbeddingResponse:
            return FakeEmbeddingResponse(data=[EmptyEmbedding(embedding=[])])

    class EmptyEmbeddingClient:
        embeddings = EmptyEmbeddingResource()

    provider = OpenAIEmbeddingProvider(
        api_key="test-key",
        model="text-embedding-3-small",
        allow_paid_embedding_calls=True,
        client=EmptyEmbeddingClient(),
    )

    with pytest.raises(ValueError, match="did not contain an embedding"):
        provider.embed_text("hello world")
