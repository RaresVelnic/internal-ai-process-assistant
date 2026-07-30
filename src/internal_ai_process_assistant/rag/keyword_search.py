"""Simple local keyword search over document chunks."""

from dataclasses import dataclass

from internal_ai_process_assistant.rag.text_chunking import DocumentChunk


@dataclass(frozen=True)
class ChunkSearchResult:
    """A keyword search match found in a document chunk."""

    chunk: DocumentChunk
    match_count: int


def search_chunks_by_keyword(
    chunks: list[DocumentChunk],
    query: str,
) -> list[ChunkSearchResult]:
    """Search chunks with a simple case-insensitive keyword match."""
    normalized_query = query.strip().lower()
    if not normalized_query:
        return []

    results: list[ChunkSearchResult] = []

    for chunk in chunks:
        normalized_text = chunk.text.lower()
        match_count = normalized_text.count(normalized_query)

        if match_count > 0:
            results.append(
                ChunkSearchResult(
                    chunk=chunk,
                    match_count=match_count,
                )
            )

    return sorted(
        results,
        key=lambda result: (-result.match_count, result.chunk.chunk_index),
    )
