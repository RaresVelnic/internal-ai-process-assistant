import math
from dataclasses import dataclass

import pytest

from internal_ai_process_assistant.rag.embeddings import (
    DEFAULT_EMBEDDING_DIMENSIONS,
    DeterministicEmbeddingProvider,
    EmbeddedChunk,
    EmbeddingVector,
    create_deterministic_embedding,
    embed_chunks,
)
from internal_ai_process_assistant.rag.text_chunking import DocumentChunk


@dataclass(frozen=True)
class FakeEmbeddingProvider:
    embedding: EmbeddingVector

    def embed_text(self, text: str) -> EmbeddingVector:
        if not text:
            raise ValueError("text must not be empty")
        return self.embedding


def test_create_deterministic_embedding_returns_expected_dimensions() -> None:
    embedding = create_deterministic_embedding("Internal assistant processing notes")

    assert isinstance(embedding, EmbeddingVector)
    assert embedding.dimensions == DEFAULT_EMBEDDING_DIMENSIONS


def test_create_deterministic_embedding_is_stable_for_same_text() -> None:
    first = create_deterministic_embedding("Internal assistant")
    second = create_deterministic_embedding("  internal   assistant  ")

    assert first == second


def test_create_deterministic_embedding_changes_for_different_text() -> None:
    first = create_deterministic_embedding("internal assistant")
    second = create_deterministic_embedding("financial report")

    assert first != second


def test_create_deterministic_embedding_is_normalized() -> None:
    embedding = create_deterministic_embedding("internal assistant processing notes")
    norm = math.sqrt(sum(value * value for value in embedding.values))

    assert norm == pytest.approx(1.0)


def test_create_deterministic_embedding_supports_custom_dimensions() -> None:
    embedding = create_deterministic_embedding("internal assistant", dimensions=8)

    assert embedding.dimensions == 8


def test_create_deterministic_embedding_rejects_invalid_dimensions() -> None:
    with pytest.raises(ValueError, match="dimensions must be at least 1"):
        create_deterministic_embedding("internal assistant", dimensions=0)


def test_create_deterministic_embedding_rejects_empty_text() -> None:
    with pytest.raises(ValueError, match="text must not be empty"):
        create_deterministic_embedding("   ")


def test_deterministic_embedding_provider_embeds_text() -> None:
    provider = DeterministicEmbeddingProvider(dimensions=8)

    embedding = provider.embed_text("Internal assistant")

    assert isinstance(embedding, EmbeddingVector)
    assert embedding.dimensions == 8


def test_embed_chunks_preserves_chunk_metadata() -> None:
    chunks = [
        DocumentChunk(
            text="Internal assistant processing notes",
            chunk_index=0,
            source_filename="sample.pdf",
            source_type="pdf",
            page_number=1,
        ),
        DocumentChunk(
            text="Controlled input files only",
            chunk_index=1,
            source_filename="sample.pdf",
            source_type="pdf",
            page_number=2,
        ),
    ]

    embedded_chunks = embed_chunks(chunks, dimensions=8)

    assert len(embedded_chunks) == 2
    assert all(isinstance(item, EmbeddedChunk) for item in embedded_chunks)
    assert embedded_chunks[0].chunk.source_filename == "sample.pdf"
    assert embedded_chunks[0].chunk.page_number == 1
    assert embedded_chunks[0].embedding.dimensions == 8
    assert embedded_chunks[1].chunk.chunk_index == 1


def test_embed_chunks_accepts_custom_provider() -> None:
    chunks = [
        DocumentChunk(
            text="Internal assistant processing notes",
            chunk_index=0,
            source_filename="sample.pdf",
            source_type="pdf",
            page_number=1,
        )
    ]
    provider = FakeEmbeddingProvider(embedding=EmbeddingVector(values=(1.0, 0.0, 0.0)))

    embedded_chunks = embed_chunks(chunks, provider=provider)

    assert embedded_chunks[0].embedding == EmbeddingVector(values=(1.0, 0.0, 0.0))
