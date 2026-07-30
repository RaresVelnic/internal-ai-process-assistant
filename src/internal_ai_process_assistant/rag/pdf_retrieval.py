"""Local PDF retrieval workflow for the RAG foundation."""

from dataclasses import dataclass
from pathlib import Path

from internal_ai_process_assistant.rag.citations import format_search_result_citations
from internal_ai_process_assistant.rag.keyword_search import ChunkSearchResult, search_chunks_by_keyword
from internal_ai_process_assistant.rag.pdf_chunking import chunk_pdf_text


@dataclass(frozen=True)
class PdfRetrievalResult:
    """Structured result returned by local PDF retrieval."""

    filename: str
    query: str
    match_count: int
    matches: list[ChunkSearchResult]
    citations: list[str]


def search_pdf_text(
    filename: str,
    query: str,
    project_root: Path,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> PdfRetrievalResult:
    """Search a controlled PDF file with local keyword retrieval."""
    normalized_query = query.strip()

    if not normalized_query:
        return PdfRetrievalResult(
            filename=filename,
            query=query,
            match_count=0,
            matches=[],
            citations=[],
        )

    chunks = chunk_pdf_text(
        filename=filename,
        project_root=project_root,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    matches = search_chunks_by_keyword(chunks=chunks, query=normalized_query)
    citations = format_search_result_citations(matches)

    return PdfRetrievalResult(
        filename=filename,
        query=normalized_query,
        match_count=len(matches),
        matches=matches,
        citations=citations,
    )
