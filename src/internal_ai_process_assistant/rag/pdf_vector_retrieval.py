"""Local PDF vector retrieval workflow using deterministic embeddings."""

from dataclasses import dataclass
from pathlib import Path

from internal_ai_process_assistant.rag.citations import format_chunk_citation
from internal_ai_process_assistant.rag.embeddings import create_deterministic_embedding, embed_chunks
from internal_ai_process_assistant.rag.pdf_chunking import chunk_pdf_text
from internal_ai_process_assistant.rag.vector_store import InMemoryVectorStore


DEFAULT_VECTOR_RETRIEVAL_TOP_K = 3


@dataclass(frozen=True)
class PdfVectorRetrievalMatch:
    """One PDF vector retrieval match."""

    text: str
    score: float
    citation: str
    chunk_index: int
    source_filename: str
    page_number: int | None


@dataclass(frozen=True)
class PdfVectorRetrievalResult:
    """Structured PDF vector retrieval result."""

    filename: str
    query: str
    match_count: int
    matches: list[PdfVectorRetrievalMatch]


def retrieve_pdf_chunks_by_vector(
    filename: str,
    query: str,
    project_root: Path,
    top_k: int = DEFAULT_VECTOR_RETRIEVAL_TOP_K,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> PdfVectorRetrievalResult:
    """Retrieve PDF chunks with deterministic vector similarity."""
    normalized_query = query.strip()

    if not normalized_query:
        return PdfVectorRetrievalResult(
            filename=filename,
            query=query,
            match_count=0,
            matches=[],
        )

    chunks = chunk_pdf_text(
        filename=filename,
        project_root=project_root,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    embedded_chunks = embed_chunks(chunks)

    store = InMemoryVectorStore()
    store.add_many(embedded_chunks)

    query_embedding = create_deterministic_embedding(normalized_query)
    search_results = store.search(query_embedding, top_k=top_k)

    matches = [
        PdfVectorRetrievalMatch(
            text=result.embedded_chunk.chunk.text,
            score=result.score,
            citation=format_chunk_citation(result.embedded_chunk.chunk),
            chunk_index=result.embedded_chunk.chunk.chunk_index,
            source_filename=result.embedded_chunk.chunk.source_filename,
            page_number=result.embedded_chunk.chunk.page_number,
        )
        for result in search_results
    ]

    return PdfVectorRetrievalResult(
        filename=filename,
        query=normalized_query,
        match_count=len(matches),
        matches=matches,
    )
