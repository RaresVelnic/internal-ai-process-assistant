"""Citation formatting helpers for retrieval results."""

from internal_ai_process_assistant.rag.keyword_search import ChunkSearchResult
from internal_ai_process_assistant.rag.text_chunking import DocumentChunk


def format_chunk_citation(chunk: DocumentChunk) -> str:
    """Format a human-readable source citation for one document chunk."""
    parts = [chunk.source_filename]

    if chunk.page_number is not None:
        parts.append(f"page {chunk.page_number}")

    parts.append(f"chunk {chunk.chunk_index}")

    return ", ".join(parts)


def format_search_result_citations(results: list[ChunkSearchResult]) -> list[str]:
    """Format citations for keyword search results."""
    return [format_chunk_citation(result.chunk) for result in results]
