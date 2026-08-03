from pathlib import Path
from shutil import copyfile

import pytest

from internal_ai_process_assistant.rag.pdf_vector_retrieval import (
    PdfVectorRetrievalEstimate,
    PdfVectorRetrievalMatch,
    PdfVectorRetrievalResult,
    estimate_pdf_vector_retrieval_usage,
    retrieve_pdf_chunks_by_vector,
)


@pytest.fixture
def sample_pdf_in_input() -> str:
    source_path = Path("examples/input/sample.pdf")
    input_path = Path("input/sample.pdf")

    copyfile(source_path, input_path)

    return input_path.name


def test_retrieve_pdf_chunks_by_vector_returns_matches(sample_pdf_in_input: str) -> None:
    result = retrieve_pdf_chunks_by_vector(
        filename=sample_pdf_in_input,
        query="assistant",
        project_root=Path.cwd(),
        top_k=2,
    )

    assert isinstance(result, PdfVectorRetrievalResult)
    assert result.filename == sample_pdf_in_input
    assert result.query == "assistant"
    assert result.match_count == 2
    assert len(result.matches) == 2
    assert all(isinstance(match, PdfVectorRetrievalMatch) for match in result.matches)


def test_retrieve_pdf_chunks_by_vector_returns_usage_estimate(
    sample_pdf_in_input: str,
) -> None:
    result = retrieve_pdf_chunks_by_vector(
        filename=sample_pdf_in_input,
        query="assistant",
        project_root=Path.cwd(),
        top_k=1,
    )

    assert result.embedding_model_name == "text-embedding-3-small"
    assert result.estimated_tokens > 0
    assert float(result.estimated_cost_usd) > 0


def test_retrieve_pdf_chunks_by_vector_returns_citations(sample_pdf_in_input: str) -> None:
    result = retrieve_pdf_chunks_by_vector(
        filename=sample_pdf_in_input,
        query="processing",
        project_root=Path.cwd(),
        top_k=1,
    )

    assert result.matches[0].source_filename == sample_pdf_in_input
    assert result.matches[0].citation.startswith(sample_pdf_in_input)
    assert result.matches[0].page_number is not None


def test_retrieve_pdf_chunks_by_vector_returns_scores_in_descending_order(
    sample_pdf_in_input: str,
) -> None:
    result = retrieve_pdf_chunks_by_vector(
        filename=sample_pdf_in_input,
        query="assistant",
        project_root=Path.cwd(),
        top_k=3,
    )

    scores = [match.score for match in result.matches]

    assert scores == sorted(scores, reverse=True)


def test_retrieve_pdf_chunks_by_vector_strips_query(sample_pdf_in_input: str) -> None:
    result = retrieve_pdf_chunks_by_vector(
        filename=sample_pdf_in_input,
        query="  assistant  ",
        project_root=Path.cwd(),
        top_k=1,
    )

    assert result.query == "assistant"


def test_retrieve_pdf_chunks_by_vector_returns_empty_result_for_empty_query(
    sample_pdf_in_input: str,
) -> None:
    result = retrieve_pdf_chunks_by_vector(
        filename=sample_pdf_in_input,
        query="   ",
        project_root=Path.cwd(),
    )

    assert result.query == "   "
    assert result.match_count == 0
    assert result.matches == []
    assert result.estimated_tokens == 0
    assert result.estimated_cost_usd == "0.0000000"


def test_retrieve_pdf_chunks_by_vector_rejects_invalid_top_k(sample_pdf_in_input: str) -> None:
    with pytest.raises(ValueError, match="top_k must be at least 1"):
        retrieve_pdf_chunks_by_vector(
            filename=sample_pdf_in_input,
            query="assistant",
            project_root=Path.cwd(),
            top_k=0,
        )


def test_retrieve_pdf_chunks_by_vector_rejects_too_many_chunks(
    sample_pdf_in_input: str,
) -> None:
    with pytest.raises(ValueError, match="exceeds the limit of 1"):
        retrieve_pdf_chunks_by_vector(
            filename=sample_pdf_in_input,
            query="assistant",
            project_root=Path.cwd(),
            max_chunks=1,
        )


def test_retrieve_pdf_chunks_by_vector_rejects_too_many_estimated_tokens(
    sample_pdf_in_input: str,
) -> None:
    with pytest.raises(ValueError, match="exceeds the limit of 1"):
        retrieve_pdf_chunks_by_vector(
            filename=sample_pdf_in_input,
            query="assistant",
            project_root=Path.cwd(),
            max_estimated_tokens=1,
        )

def test_estimate_pdf_vector_retrieval_usage_returns_dry_run_estimate(
    sample_pdf_in_input: str,
) -> None:
    result = estimate_pdf_vector_retrieval_usage(
        filename=sample_pdf_in_input,
        project_root=Path.cwd(),
    )

    assert isinstance(result, PdfVectorRetrievalEstimate)
    assert result.filename == sample_pdf_in_input
    assert result.chunk_count > 0
    assert result.embedding_model_name == "text-embedding-3-small"
    assert result.estimated_tokens > 0
    assert float(result.estimated_cost_usd) > 0


def test_estimate_pdf_vector_retrieval_usage_applies_chunk_guardrail(
    sample_pdf_in_input: str,
) -> None:
    with pytest.raises(ValueError, match="exceeds the limit of 1"):
        estimate_pdf_vector_retrieval_usage(
            filename=sample_pdf_in_input,
            project_root=Path.cwd(),
            max_chunks=1,
        )


def test_estimate_pdf_vector_retrieval_usage_applies_token_guardrail(
    sample_pdf_in_input: str,
) -> None:
    with pytest.raises(ValueError, match="exceeds the limit of 1"):
        estimate_pdf_vector_retrieval_usage(
            filename=sample_pdf_in_input,
            project_root=Path.cwd(),
            max_estimated_tokens=1,
        )

