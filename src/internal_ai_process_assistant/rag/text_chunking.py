"""Text chunking utilities for the RAG foundation."""

from dataclasses import dataclass


DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 50


@dataclass(frozen=True)
class DocumentChunk:
    """A chunk of text with source metadata."""

    text: str
    chunk_index: int
    source_filename: str
    source_type: str
    page_number: int | None = None


def chunk_text(
    text: str,
    source_filename: str,
    source_type: str,
    page_number: int | None = None,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[DocumentChunk]:
    """Split text into bounded chunks with source metadata."""
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must not be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    normalized_text = text.strip()
    if not normalized_text:
        return []

    chunks: list[DocumentChunk] = []
    start = 0

    while start < len(normalized_text):
        end = min(start + chunk_size, len(normalized_text))
        chunk = normalized_text[start:end].strip()

        if chunk:
            chunks.append(
                DocumentChunk(
                    text=chunk,
                    chunk_index=len(chunks),
                    source_filename=source_filename,
                    source_type=source_type,
                    page_number=page_number,
                )
            )

        if end == len(normalized_text):
            break

        start = end - chunk_overlap

    return chunks
