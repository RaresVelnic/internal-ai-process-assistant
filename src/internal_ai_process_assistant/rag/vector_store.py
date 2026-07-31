"""In-memory vector store utilities for local RAG infrastructure."""

from dataclasses import dataclass

from internal_ai_process_assistant.rag.embeddings import EmbeddedChunk, EmbeddingVector


@dataclass(frozen=True)
class VectorSearchResult:
    """A vector search match with similarity score."""

    embedded_chunk: EmbeddedChunk
    score: float


class InMemoryVectorStore:
    """A small in-memory vector store for deterministic local retrieval."""

    def __init__(self) -> None:
        self._items: list[EmbeddedChunk] = []

    def add(self, embedded_chunk: EmbeddedChunk) -> None:
        """Add one embedded chunk to the store."""
        self._items.append(embedded_chunk)

    def add_many(self, embedded_chunks: list[EmbeddedChunk]) -> None:
        """Add multiple embedded chunks to the store."""
        self._items.extend(embedded_chunks)

    def search(
        self,
        query_embedding: EmbeddingVector,
        top_k: int = 3,
    ) -> list[VectorSearchResult]:
        """Return the most similar chunks by cosine similarity."""
        if top_k < 1:
            raise ValueError("top_k must be at least 1")

        results = [
            VectorSearchResult(
                embedded_chunk=embedded_chunk,
                score=cosine_similarity(query_embedding, embedded_chunk.embedding),
            )
            for embedded_chunk in self._items
        ]

        return sorted(results, key=lambda result: result.score, reverse=True)[:top_k]

    @property
    def count(self) -> int:
        """Return the number of stored embedded chunks."""
        return len(self._items)


def cosine_similarity(first: EmbeddingVector, second: EmbeddingVector) -> float:
    """Calculate cosine similarity between two embedding vectors."""
    if first.dimensions != second.dimensions:
        raise ValueError("embedding dimensions must match")

    first_norm = _vector_norm(first)
    second_norm = _vector_norm(second)

    if first_norm == 0 or second_norm == 0:
        raise ValueError("embedding vectors must not be zero vectors")

    dot_product = sum(
        first_value * second_value
        for first_value, second_value in zip(first.values, second.values, strict=True)
    )

    return dot_product / (first_norm * second_norm)


def _vector_norm(vector: EmbeddingVector) -> float:
    return sum(value * value for value in vector.values) ** 0.5
