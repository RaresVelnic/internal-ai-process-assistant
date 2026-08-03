"""Embedding provider selection helpers."""

from internal_ai_process_assistant.config import AppConfig
from internal_ai_process_assistant.rag.embeddings import (
    DeterministicEmbeddingProvider,
    EmbeddingProvider,
)


def get_embedding_provider(config: AppConfig) -> EmbeddingProvider:
    """Return the configured embedding provider.

    The OpenAI provider is intentionally not implemented yet. This keeps
    provider selection explicit without introducing paid API calls too early.
    """
    if config.embedding_provider == "deterministic":
        return DeterministicEmbeddingProvider()

    if config.embedding_provider == "openai":
        raise NotImplementedError(
            "OpenAI embedding provider is configured but not implemented yet."
        )

    raise ValueError(f"Unsupported embedding provider: {config.embedding_provider}")
