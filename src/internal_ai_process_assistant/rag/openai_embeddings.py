"""OpenAI embedding provider implementation."""

from dataclasses import dataclass
from typing import Protocol

from openai import OpenAI

from internal_ai_process_assistant.rag.embeddings import EmbeddingVector


class OpenAIEmbeddingsResource(Protocol):
    """Small protocol for the OpenAI embeddings resource."""

    def create(
        self,
        *,
        input: str,
        model: str,
        encoding_format: str,
    ) -> object:
        """Create an embedding response."""


class OpenAIEmbeddingsClient(Protocol):
    """Small protocol for the OpenAI client used by this provider."""

    embeddings: OpenAIEmbeddingsResource


@dataclass(frozen=True)
class OpenAIEmbeddingProvider:
    """OpenAI embedding provider with explicit paid-call opt-in."""

    api_key: str
    model: str
    allow_paid_embedding_calls: bool = False
    client: OpenAIEmbeddingsClient | None = None

    def __post_init__(self) -> None:
        """Validate provider configuration."""
        if not self.api_key.strip():
            raise ValueError("OpenAI API key must not be empty")

        if not self.model.strip():
            raise ValueError("OpenAI embedding model must not be empty")

    def embed_text(self, text: str) -> EmbeddingVector:
        """Create an embedding vector for text."""
        normalized_text = text.strip()
        if not normalized_text:
            raise ValueError("text must not be empty")

        if not self.allow_paid_embedding_calls:
            raise PermissionError(
                "Paid embedding calls are disabled. Set "
                "IAPA_ALLOW_PAID_EMBEDDING_CALLS=true to enable them."
            )

        client = self.client or OpenAI(api_key=self.api_key)
        response = client.embeddings.create(
            input=normalized_text,
            model=self.model,
            encoding_format="float",
        )

        values = _extract_embedding_values(response)
        return EmbeddingVector(values=tuple(float(value) for value in values))


def _extract_embedding_values(response: object) -> list[float]:
    """Extract embedding values from an OpenAI embeddings response."""
    data = getattr(response, "data", None)
    if not data:
        raise ValueError("OpenAI embedding response did not contain data")

    first_embedding = data[0]
    values = getattr(first_embedding, "embedding", None)
    if not values:
        raise ValueError("OpenAI embedding response did not contain an embedding")

    return list(values)
