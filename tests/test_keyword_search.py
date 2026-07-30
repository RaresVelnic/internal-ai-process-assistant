from internal_ai_process_assistant.rag.keyword_search import (
    ChunkSearchResult,
    search_chunks_by_keyword,
)
from internal_ai_process_assistant.rag.text_chunking import DocumentChunk


def make_chunk(text: str, chunk_index: int, page_number: int | None = None) -> DocumentChunk:
    return DocumentChunk(
        text=text,
        chunk_index=chunk_index,
        source_filename="sample.pdf",
        source_type="pdf",
        page_number=page_number,
    )


def test_search_chunks_by_keyword_returns_matching_chunks() -> None:
    chunks = [
        make_chunk("Internal AI Process Assistant overview", 0, page_number=1),
        make_chunk("Processing notes for controlled input files", 1, page_number=2),
    ]

    results = search_chunks_by_keyword(chunks, "assistant")

    assert results == [
        ChunkSearchResult(
            chunk=chunks[0],
            match_count=1,
        )
    ]


def test_search_chunks_by_keyword_is_case_insensitive() -> None:
    chunks = [make_chunk("Internal AI Process Assistant", 0)]

    results = search_chunks_by_keyword(chunks, "assistant")

    assert len(results) == 1
    assert results[0].chunk == chunks[0]


def test_search_chunks_by_keyword_sorts_by_match_count_then_chunk_index() -> None:
    chunks = [
        make_chunk("assistant", 0),
        make_chunk("assistant assistant assistant", 1),
        make_chunk("assistant assistant", 2),
    ]

    results = search_chunks_by_keyword(chunks, "assistant")

    assert [result.chunk.chunk_index for result in results] == [1, 2, 0]
    assert [result.match_count for result in results] == [3, 2, 1]


def test_search_chunks_by_keyword_returns_empty_list_for_blank_query() -> None:
    chunks = [make_chunk("Internal AI Process Assistant", 0)]

    results = search_chunks_by_keyword(chunks, "   ")

    assert results == []


def test_search_chunks_by_keyword_returns_empty_list_when_no_match() -> None:
    chunks = [make_chunk("Internal AI Process Assistant", 0)]

    results = search_chunks_by_keyword(chunks, "invoice")

    assert results == []


def test_search_chunks_by_keyword_preserves_source_metadata() -> None:
    chunks = [make_chunk("privacy policy document", 3, page_number=5)]

    results = search_chunks_by_keyword(chunks, "privacy")

    assert results[0].chunk.source_filename == "sample.pdf"
    assert results[0].chunk.source_type == "pdf"
    assert results[0].chunk.page_number == 5
    assert results[0].chunk.chunk_index == 3
