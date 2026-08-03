"""OpenAI embedding provider placeholder.

This module defines the boundary for future OpenAI embedding integration.
It intentionally does not call the OpenAI API yet.
"""

from dataclasses import dataclass

from internal_ai_process_assistant.rag.embeddings import EmbeddingVector


@dataclass(frozen=True)
class OpenAIEmbeddingProvider:
    """Placeholder OpenAI embedding provider.

    The class stores the configuration needed for the future implementation,
    but embed_text intentionally raises NotImplementedError until the project
    is ready to make explicit paid API calls.
    """

    api_key: str
    model: str

    def __post_init__(self) -> None:
        """Validate provider configuration."""
        if not self.api_key.strip():
            raise ValueError("OpenAI API key must not be empty")

        if not self.model.strip():
            raise ValueError("OpenAI embedding model must not be empty")

    def embed_text(self, text: str) -> EmbeddingVector:
        """Create an embedding vector for text.

        Real OpenAI API calls are intentionally not implemented yet.
        """
        if not text.strip():
            raise ValueError("text must not be empty")

        raise NotImplementedError(
            "OpenAI embedding API calls are not implemented yet."
        )
