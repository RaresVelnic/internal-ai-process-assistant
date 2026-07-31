"""Deterministic embedding utilities for the RAG foundation."""

from dataclasses import dataclass
import hashlib
import math
from collections.abc import Sequence

from internal_ai_process_assistant.rag.text_chunking import DocumentChunk


DEFAULT_EMBEDDING_DIMENSIONS = 16


@dataclass(frozen=True)
class EmbeddingVector:
    """A numeric vector representation of text."""

    values: tuple[float, ...]

    @property
    def dimensions(self) -> int:
        """Return the number of vector dimensions."""
        return len(self.values)


@dataclass(frozen=True)
class EmbeddedChunk:
    """A document chunk with its embedding vector."""

    chunk: DocumentChunk
    embedding: EmbeddingVector


def create_deterministic_embedding(
    text: str,
    dimensions: int = DEFAULT_EMBEDDING_DIMENSIONS,
) -> EmbeddingVector:
    """Create a deterministic test embedding for text.

    This is not a semantic embedding model. It is a stable local stand-in used
    to test embedding and vector store infrastructure without external APIs.
    """
    if dimensions < 1:
        raise ValueError("dimensions must be at least 1")

    normalized_text = " ".join(text.casefold().split())
    if not normalized_text:
        raise ValueError("text must not be empty")

    values = [0.0 for _ in range(dimensions)]

    for token in normalized_text.split():
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
        vector_index = int.from_bytes(digest[:4], byteorder="big") % dimensions
        weight = 1.0 + int.from_bytes(digest[4:], byteorder="big") / (2**32 - 1)
        values[vector_index] += weight

    norm = math.sqrt(sum(value * value for value in values))
    normalized_values = tuple(value / norm for value in values)

    return EmbeddingVector(values=normalized_values)


def embed_chunks(
    chunks: Sequence[DocumentChunk],
    dimensions: int = DEFAULT_EMBEDDING_DIMENSIONS,
) -> list[EmbeddedChunk]:
    """Create deterministic embeddings for document chunks."""
    return [
        EmbeddedChunk(
            chunk=chunk,
            embedding=create_deterministic_embedding(chunk.text, dimensions=dimensions),
        )
        for chunk in chunks
    ]
