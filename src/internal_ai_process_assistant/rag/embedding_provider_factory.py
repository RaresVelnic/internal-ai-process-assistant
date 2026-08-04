"""Embedding provider selection helpers."""

from internal_ai_process_assistant.config import AppConfig
from internal_ai_process_assistant.rag.embeddings import (
    DeterministicEmbeddingProvider,
    EmbeddingProvider,
)
from internal_ai_process_assistant.rag.openai_embeddings import OpenAIEmbeddingProvider


def get_embedding_provider(config: AppConfig) -> EmbeddingProvider:
    """Return the configured embedding provider.

    OpenAI API calls are intentionally not implemented yet. This keeps
    provider selection explicit without introducing paid API calls too early.
    """
    if config.embedding_provider == "deterministic":
        return DeterministicEmbeddingProvider()

    if config.embedding_provider == "openai":
        if config.openai_api_key is None:
            raise ValueError("OPENAI_API_KEY is required for OpenAI embeddings")

        return OpenAIEmbeddingProvider(
            api_key=config.openai_api_key,
            model=config.openai_embedding_model,
            allow_paid_embedding_calls=config.allow_paid_embedding_calls,
        )

    raise ValueError(f"Unsupported embedding provider: {config.embedding_provider}")
