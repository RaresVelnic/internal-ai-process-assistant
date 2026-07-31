import pytest

from internal_ai_process_assistant.rag.embeddings import (
    EmbeddingVector,
    create_deterministic_embedding,
    embed_chunks,
)
from internal_ai_process_assistant.rag.text_chunking import DocumentChunk
from internal_ai_process_assistant.rag.vector_store import (
    InMemoryVectorStore,
    VectorSearchResult,
    cosine_similarity,
)


def test_cosine_similarity_returns_one_for_identical_vectors() -> None:
    vector = EmbeddingVector(values=(1.0, 0.0, 0.0))

    assert cosine_similarity(vector, vector) == pytest.approx(1.0)


def test_cosine_similarity_returns_zero_for_orthogonal_vectors() -> None:
    first = EmbeddingVector(values=(1.0, 0.0))
    second = EmbeddingVector(values=(0.0, 1.0))

    assert cosine_similarity(first, second) == pytest.approx(0.0)


def test_cosine_similarity_rejects_dimension_mismatch() -> None:
    first = EmbeddingVector(values=(1.0, 0.0))
    second = EmbeddingVector(values=(1.0, 0.0, 0.0))

    with pytest.raises(ValueError, match="embedding dimensions must match"):
        cosine_similarity(first, second)


def test_cosine_similarity_rejects_zero_vector() -> None:
    first = EmbeddingVector(values=(0.0, 0.0))
    second = EmbeddingVector(values=(1.0, 0.0))

    with pytest.raises(ValueError, match="embedding vectors must not be zero vectors"):
        cosine_similarity(first, second)


def test_in_memory_vector_store_adds_items() -> None:
    chunk = DocumentChunk(
        text="Internal assistant processing notes",
        chunk_index=0,
        source_filename="sample.pdf",
        source_type="pdf",
        page_number=1,
    )
    embedded_chunk = embed_chunks([chunk])[0]

    store = InMemoryVectorStore()
    store.add(embedded_chunk)

    assert store.count == 1


def test_in_memory_vector_store_search_returns_ranked_results() -> None:
    chunks = [
        DocumentChunk(
            text="internal assistant document processing",
            chunk_index=0,
            source_filename="sample.pdf",
            source_type="pdf",
            page_number=1,
        ),
        DocumentChunk(
            text="quarterly finance report",
            chunk_index=1,
            source_filename="sample.pdf",
            source_type="pdf",
            page_number=2,
        ),
    ]

    store = InMemoryVectorStore()
    store.add_many(embed_chunks(chunks, dimensions=8))

    query_embedding = create_deterministic_embedding("assistant processing", dimensions=8)
    results = store.search(query_embedding, top_k=1)

    assert len(results) == 1
    assert isinstance(results[0], VectorSearchResult)
    assert results[0].embedded_chunk.chunk.chunk_index == 0
    assert results[0].score > 0


def test_in_memory_vector_store_search_respects_top_k() -> None:
    chunks = [
        DocumentChunk(
            text=f"document chunk {index}",
            chunk_index=index,
            source_filename="sample.pdf",
            source_type="pdf",
            page_number=1,
        )
        for index in range(5)
    ]

    store = InMemoryVectorStore()
    store.add_many(embed_chunks(chunks, dimensions=8))

    query_embedding = create_deterministic_embedding("document", dimensions=8)
    results = store.search(query_embedding, top_k=2)

    assert len(results) == 2


def test_in_memory_vector_store_search_rejects_invalid_top_k() -> None:
    store = InMemoryVectorStore()
    query_embedding = EmbeddingVector(values=(1.0, 0.0))

    with pytest.raises(ValueError, match="top_k must be at least 1"):
        store.search(query_embedding, top_k=0)
