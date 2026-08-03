from decimal import Decimal

import pytest

from internal_ai_process_assistant.rag.embedding_costs import (
    DEFAULT_MAX_EMBEDDING_CHUNKS_PER_RUN,
    DEFAULT_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN,
    EmbeddingUsageEstimate,
    estimate_embedding_usage,
    estimate_text_tokens,
    validate_embedding_usage_limits,
)
from internal_ai_process_assistant.rag.text_chunking import DocumentChunk


def _chunk(text: str, chunk_index: int = 0) -> DocumentChunk:
    return DocumentChunk(
        text=text,
        chunk_index=chunk_index,
        source_filename="sample.pdf",
        source_type="pdf",
        page_number=1,
    )


def test_estimate_text_tokens_returns_zero_for_empty_text() -> None:
    assert estimate_text_tokens("   ") == 0


def test_estimate_text_tokens_estimates_one_token_for_short_text() -> None:
    assert estimate_text_tokens("abc") == 1


def test_estimate_text_tokens_uses_conservative_character_ratio() -> None:
    assert estimate_text_tokens("a" * 9) == 3


def test_estimate_embedding_usage_returns_chunk_count_tokens_and_cost() -> None:
    estimate = estimate_embedding_usage([_chunk("a" * 400), _chunk("b" * 400, chunk_index=1)])

    assert isinstance(estimate, EmbeddingUsageEstimate)
    assert estimate.chunk_count == 2
    assert estimate.estimated_tokens == 200
    assert estimate.estimated_cost_usd == Decimal("0.0000040")
    assert estimate.model_name == "text-embedding-3-small"


def test_validate_embedding_usage_limits_allows_small_request() -> None:
    estimate = validate_embedding_usage_limits([_chunk("small text")])

    assert estimate.chunk_count == 1
    assert estimate.estimated_tokens <= DEFAULT_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN
    assert DEFAULT_MAX_EMBEDDING_CHUNKS_PER_RUN == 20


def test_validate_embedding_usage_limits_rejects_too_many_chunks() -> None:
    chunks = [_chunk(f"chunk {index}", chunk_index=index) for index in range(3)]

    with pytest.raises(ValueError, match="exceeds the limit of 2"):
        validate_embedding_usage_limits(chunks, max_chunks=2)


def test_validate_embedding_usage_limits_rejects_too_many_tokens() -> None:
    chunks = [_chunk("a" * 100)]

    with pytest.raises(ValueError, match="exceeds the limit of 10"):
        validate_embedding_usage_limits(chunks, max_estimated_tokens=10)


def test_validate_embedding_usage_limits_rejects_invalid_max_chunks() -> None:
    with pytest.raises(ValueError, match="max_chunks must be at least 1"):
        validate_embedding_usage_limits([], max_chunks=0)


def test_validate_embedding_usage_limits_rejects_invalid_max_estimated_tokens() -> None:
    with pytest.raises(ValueError, match="max_estimated_tokens must be at least 1"):
        validate_embedding_usage_limits([], max_estimated_tokens=0)
