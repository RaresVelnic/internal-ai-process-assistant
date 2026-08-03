"""Local PDF vector retrieval workflow using deterministic embeddings."""

from dataclasses import dataclass
from pathlib import Path

from internal_ai_process_assistant.rag.citations import format_chunk_citation
from internal_ai_process_assistant.rag.embedding_costs import (
    DEFAULT_MAX_EMBEDDING_CHUNKS_PER_RUN,
    DEFAULT_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN,
    validate_embedding_usage_limits,
)
from internal_ai_process_assistant.rag.embeddings import (
    DeterministicEmbeddingProvider,
    EmbeddingProvider,
    embed_chunks,
)
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
    embedding_model_name: str
    estimated_tokens: int
    estimated_cost_usd: str


@dataclass(frozen=True)
class PdfVectorRetrievalEstimate:
    """Dry-run estimate for PDF vector retrieval."""

    filename: str
    chunk_count: int
    embedding_model_name: str
    estimated_tokens: int
    estimated_cost_usd: str


def estimate_pdf_vector_retrieval_usage(
    filename: str,
    project_root: Path,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    max_chunks: int = DEFAULT_MAX_EMBEDDING_CHUNKS_PER_RUN,
    max_estimated_tokens: int = DEFAULT_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN,
) -> PdfVectorRetrievalEstimate:
    """Estimate PDF vector retrieval usage without creating embeddings."""
    chunks = chunk_pdf_text(
        filename=filename,
        project_root=project_root,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    usage_estimate = validate_embedding_usage_limits(
        chunks=chunks,
        max_chunks=max_chunks,
        max_estimated_tokens=max_estimated_tokens,
    )

    return PdfVectorRetrievalEstimate(
        filename=filename,
        chunk_count=usage_estimate.chunk_count,
        embedding_model_name=usage_estimate.model_name,
        estimated_tokens=usage_estimate.estimated_tokens,
        estimated_cost_usd=str(usage_estimate.estimated_cost_usd),
    )


def retrieve_pdf_chunks_by_vector(
    filename: str,
    query: str,
    project_root: Path,
    top_k: int = DEFAULT_VECTOR_RETRIEVAL_TOP_K,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    max_chunks: int = DEFAULT_MAX_EMBEDDING_CHUNKS_PER_RUN,
    max_estimated_tokens: int = DEFAULT_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN,
    provider: EmbeddingProvider | None = None,
) -> PdfVectorRetrievalResult:
    """Retrieve PDF chunks with deterministic vector similarity."""
    normalized_query = query.strip()

    if not normalized_query:
        return PdfVectorRetrievalResult(
            filename=filename,
            query=query,
            match_count=0,
            matches=[],
            embedding_model_name="text-embedding-3-small",
            estimated_tokens=0,
            estimated_cost_usd="0.0000000",
        )

    chunks = chunk_pdf_text(
        filename=filename,
        project_root=project_root,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    usage_estimate = validate_embedding_usage_limits(
        chunks=chunks,
        max_chunks=max_chunks,
        max_estimated_tokens=max_estimated_tokens,
    )
    embedding_provider = provider or DeterministicEmbeddingProvider()
    embedded_chunks = embed_chunks(chunks, provider=embedding_provider)

    store = InMemoryVectorStore()
    store.add_many(embedded_chunks)

    query_embedding = embedding_provider.embed_text(normalized_query)
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
        embedding_model_name=usage_estimate.model_name,
        estimated_tokens=usage_estimate.estimated_tokens,
        estimated_cost_usd=str(usage_estimate.estimated_cost_usd),
    )
