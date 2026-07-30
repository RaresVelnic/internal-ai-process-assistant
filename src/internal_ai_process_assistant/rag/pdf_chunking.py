"""PDF chunking helpers for the RAG foundation."""

from pathlib import Path

from internal_ai_process_assistant.rag.text_chunking import (
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    DocumentChunk,
    chunk_text,
)
from internal_ai_process_assistant.tools.pdf_text_extraction import extract_pdf_text


def chunk_pdf_text(
    filename: str,
    project_root: Path,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[DocumentChunk]:
    """Extract controlled PDF text and split it into source-aware chunks."""
    extraction_result = extract_pdf_text(
        filename=filename,
        project_root=project_root,
    )

    chunks: list[DocumentChunk] = []

    for page in extraction_result.pages:
        page_chunks = chunk_text(
            text=page.text,
            source_filename=extraction_result.filename,
            source_type="pdf",
            page_number=page.page_number,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        for page_chunk in page_chunks:
            chunks.append(
                DocumentChunk(
                    text=page_chunk.text,
                    chunk_index=len(chunks),
                    source_filename=page_chunk.source_filename,
                    source_type=page_chunk.source_type,
                    page_number=page_chunk.page_number,
                )
            )

    return chunks
