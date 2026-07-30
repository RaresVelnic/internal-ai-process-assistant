import pytest

from internal_ai_process_assistant.rag.text_chunking import DocumentChunk, chunk_text


def test_chunk_text_returns_single_chunk_for_short_text() -> None:
    chunks = chunk_text(
        text="Short document text.",
        source_filename="sample.pdf",
        source_type="pdf",
        page_number=1,
        chunk_size=100,
        chunk_overlap=10,
    )

    assert chunks == [
        DocumentChunk(
            text="Short document text.",
            chunk_index=0,
            source_filename="sample.pdf",
            source_type="pdf",
            page_number=1,
        )
    ]


def test_chunk_text_splits_long_text_with_overlap() -> None:
    chunks = chunk_text(
        text="abcdefghij",
        source_filename="sample.txt",
        source_type="text",
        chunk_size=4,
        chunk_overlap=1,
    )

    assert [chunk.text for chunk in chunks] == ["abcd", "defg", "ghij"]
    assert [chunk.chunk_index for chunk in chunks] == [0, 1, 2]


def test_chunk_text_returns_empty_list_for_blank_text() -> None:
    chunks = chunk_text(
        text="   \n   ",
        source_filename="empty.txt",
        source_type="text",
    )

    assert chunks == []


def test_chunk_text_preserves_source_metadata() -> None:
    chunks = chunk_text(
        text="Document text that will be chunked.",
        source_filename="sample.pdf",
        source_type="pdf",
        page_number=3,
        chunk_size=10,
        chunk_overlap=2,
    )

    assert chunks
    assert all(chunk.source_filename == "sample.pdf" for chunk in chunks)
    assert all(chunk.source_type == "pdf" for chunk in chunks)
    assert all(chunk.page_number == 3 for chunk in chunks)


def test_chunk_text_rejects_invalid_chunk_size() -> None:
    with pytest.raises(ValueError, match="chunk_size must be at least 1"):
        chunk_text(
            text="abc",
            source_filename="sample.txt",
            source_type="text",
            chunk_size=0,
        )


def test_chunk_text_rejects_negative_overlap() -> None:
    with pytest.raises(ValueError, match="chunk_overlap must not be negative"):
        chunk_text(
            text="abc",
            source_filename="sample.txt",
            source_type="text",
            chunk_overlap=-1,
        )


def test_chunk_text_rejects_overlap_equal_to_chunk_size() -> None:
    with pytest.raises(ValueError, match="chunk_overlap must be smaller than chunk_size"):
        chunk_text(
            text="abc",
            source_filename="sample.txt",
            source_type="text",
            chunk_size=5,
            chunk_overlap=5,
        )
