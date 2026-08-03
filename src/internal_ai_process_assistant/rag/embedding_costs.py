"""Cost estimation and usage guardrails for embedding providers."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from internal_ai_process_assistant.rag.text_chunking import DocumentChunk


OPENAI_TEXT_EMBEDDING_3_SMALL_PRICE_PER_1M_TOKENS = Decimal("0.02")
DEFAULT_MAX_EMBEDDING_CHUNKS_PER_RUN = 20
DEFAULT_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN = 20_000


@dataclass(frozen=True)
class EmbeddingUsageEstimate:
    """Estimated usage and cost for an embedding request."""

    chunk_count: int
    estimated_tokens: int
    estimated_cost_usd: Decimal
    model_name: str


def estimate_text_tokens(text: str) -> int:
    """Estimate token count conservatively from text length."""
    normalized_text = text.strip()

    if not normalized_text:
        return 0

    return max(1, (len(normalized_text) + 3) // 4)


def estimate_embedding_usage(
    chunks: list[DocumentChunk],
    model_name: str = "text-embedding-3-small",
    price_per_1m_tokens: Decimal = OPENAI_TEXT_EMBEDDING_3_SMALL_PRICE_PER_1M_TOKENS,
) -> EmbeddingUsageEstimate:
    """Estimate token usage and cost for embedding chunks."""
    estimated_tokens = sum(estimate_text_tokens(chunk.text) for chunk in chunks)
    estimated_cost = (Decimal(estimated_tokens) / Decimal(1_000_000)) * price_per_1m_tokens

    return EmbeddingUsageEstimate(
        chunk_count=len(chunks),
        estimated_tokens=estimated_tokens,
        estimated_cost_usd=estimated_cost.quantize(Decimal("0.0000001"), rounding=ROUND_HALF_UP),
        model_name=model_name,
    )


def validate_embedding_usage_limits(
    chunks: list[DocumentChunk],
    max_chunks: int = DEFAULT_MAX_EMBEDDING_CHUNKS_PER_RUN,
    max_estimated_tokens: int = DEFAULT_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN,
) -> EmbeddingUsageEstimate:
    """Validate embedding usage against conservative local limits."""
    if max_chunks < 1:
        raise ValueError("max_chunks must be at least 1")

    if max_estimated_tokens < 1:
        raise ValueError("max_estimated_tokens must be at least 1")

    estimate = estimate_embedding_usage(chunks)

    if estimate.chunk_count > max_chunks:
        raise ValueError(
            f"Embedding request has {estimate.chunk_count} chunks, "
            f"which exceeds the limit of {max_chunks}"
        )

    if estimate.estimated_tokens > max_estimated_tokens:
        raise ValueError(
            f"Embedding request has an estimated {estimate.estimated_tokens} tokens, "
            f"which exceeds the limit of {max_estimated_tokens}"
        )

    return estimate
