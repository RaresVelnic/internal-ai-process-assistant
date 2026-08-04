import pytest

from internal_ai_process_assistant.config import (
    DEFAULT_ALLOW_PAID_EMBEDDING_CALLS,
    DEFAULT_EMBEDDING_PROVIDER,
    DEFAULT_MAX_EMBEDDING_CHUNKS_PER_RUN,
    DEFAULT_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN,
    DEFAULT_OPENAI_EMBEDDING_MODEL,
    load_config,
)


def test_load_config_uses_safe_defaults() -> None:
    config = load_config({})

    assert config.embedding_provider == DEFAULT_EMBEDDING_PROVIDER
    assert config.embedding_provider == "deterministic"
    assert config.openai_api_key is None
    assert config.openai_embedding_model == DEFAULT_OPENAI_EMBEDDING_MODEL
    assert config.max_embedding_chunks_per_run == DEFAULT_MAX_EMBEDDING_CHUNKS_PER_RUN
    assert (
        config.max_estimated_embedding_tokens_per_run
        == DEFAULT_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN
    )
    assert config.allow_paid_embedding_calls is DEFAULT_ALLOW_PAID_EMBEDDING_CALLS
    assert config.allow_paid_embedding_calls is False


def test_load_config_accepts_openai_provider_with_api_key() -> None:
    config = load_config(
        {
            "IAPA_EMBEDDING_PROVIDER": "openai",
            "OPENAI_API_KEY": "test-key",
            "IAPA_OPENAI_EMBEDDING_MODEL": "text-embedding-3-small",
        }
    )

    assert config.embedding_provider == "openai"
    assert config.openai_api_key == "test-key"
    assert config.openai_embedding_model == "text-embedding-3-small"


def test_load_config_normalizes_embedding_provider() -> None:
    config = load_config({"IAPA_EMBEDDING_PROVIDER": "  DETERMINISTIC  "})

    assert config.embedding_provider == "deterministic"


def test_load_config_rejects_unsupported_embedding_provider() -> None:
    with pytest.raises(ValueError, match="Unsupported embedding provider"):
        load_config({"IAPA_EMBEDDING_PROVIDER": "unknown"})


def test_load_config_requires_api_key_for_openai_provider() -> None:
    with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
        load_config({"IAPA_EMBEDDING_PROVIDER": "openai"})


def test_load_config_treats_empty_api_key_as_missing() -> None:
    with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
        load_config({"IAPA_EMBEDDING_PROVIDER": "openai", "OPENAI_API_KEY": "   "})


def test_load_config_reads_cost_guardrail_values() -> None:
    config = load_config(
        {
            "IAPA_MAX_EMBEDDING_CHUNKS_PER_RUN": "5",
            "IAPA_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN": "1000",
        }
    )

    assert config.max_embedding_chunks_per_run == 5
    assert config.max_estimated_embedding_tokens_per_run == 1000


def test_load_config_rejects_non_integer_guardrail_value() -> None:
    with pytest.raises(ValueError, match="IAPA_MAX_EMBEDDING_CHUNKS_PER_RUN must be an integer"):
        load_config({"IAPA_MAX_EMBEDDING_CHUNKS_PER_RUN": "many"})


def test_load_config_rejects_non_positive_guardrail_value() -> None:
    with pytest.raises(ValueError, match="IAPA_MAX_EMBEDDING_CHUNKS_PER_RUN must be at least 1"):
        load_config({"IAPA_MAX_EMBEDDING_CHUNKS_PER_RUN": "0"})

def test_load_config_reads_paid_embedding_calls_flag() -> None:
    config = load_config({"IAPA_ALLOW_PAID_EMBEDDING_CALLS": "true"})

    assert config.allow_paid_embedding_calls is True


@pytest.mark.parametrize("value", ["1", "true", "yes", "y", "on"])
def test_load_config_accepts_true_boolean_values(value: str) -> None:
    config = load_config({"IAPA_ALLOW_PAID_EMBEDDING_CALLS": value})

    assert config.allow_paid_embedding_calls is True


@pytest.mark.parametrize("value", ["0", "false", "no", "n", "off"])
def test_load_config_accepts_false_boolean_values(value: str) -> None:
    config = load_config({"IAPA_ALLOW_PAID_EMBEDDING_CALLS": value})

    assert config.allow_paid_embedding_calls is False


def test_load_config_rejects_invalid_paid_embedding_calls_flag() -> None:
    with pytest.raises(ValueError, match="IAPA_ALLOW_PAID_EMBEDDING_CALLS must be a boolean"):
        load_config({"IAPA_ALLOW_PAID_EMBEDDING_CALLS": "maybe"})

