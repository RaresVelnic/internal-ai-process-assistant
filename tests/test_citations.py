from internal_ai_process_assistant.rag.citations import (
    format_chunk_citation,
    format_search_result_citations,
)
from internal_ai_process_assistant.rag.keyword_search import ChunkSearchResult
from internal_ai_process_assistant.rag.text_chunking import DocumentChunk


def make_chunk(
    source_filename: str = "sample.pdf",
    source_type: str = "pdf",
    page_number: int | None = 1,
    chunk_index: int = 0,
) -> DocumentChunk:
    return DocumentChunk(
        text="Example chunk text",
        chunk_index=chunk_index,
        source_filename=source_filename,
        source_type=source_type,
        page_number=page_number,
    )


def test_format_chunk_citation_includes_filename_page_and_chunk() -> None:
    citation = format_chunk_citation(make_chunk())

    assert citation == "sample.pdf, page 1, chunk 0"


def test_format_chunk_citation_omits_missing_page_number() -> None:
    citation = format_chunk_citation(
        make_chunk(
            source_filename="notes.txt",
            source_type="text",
            page_number=None,
            chunk_index=3,
        )
    )

    assert citation == "notes.txt, chunk 3"


def test_format_search_result_citations_formats_all_results() -> None:
    results = [
        ChunkSearchResult(chunk=make_chunk(chunk_index=0), match_count=2),
        ChunkSearchResult(chunk=make_chunk(chunk_index=1, page_number=2), match_count=1),
    ]

    citations = format_search_result_citations(results)

    assert citations == [
        "sample.pdf, page 1, chunk 0",
        "sample.pdf, page 2, chunk 1",
    ]


def test_format_search_result_citations_returns_empty_list_for_no_results() -> None:
    citations = format_search_result_citations([])

    assert citations == []
