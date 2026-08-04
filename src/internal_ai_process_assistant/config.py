"""Application configuration helpers."""

from dataclasses import dataclass
import os


SUPPORTED_EMBEDDING_PROVIDERS = ("deterministic", "openai")
DEFAULT_EMBEDDING_PROVIDER = "deterministic"
DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_MAX_EMBEDDING_CHUNKS_PER_RUN = 20
DEFAULT_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN = 20_000
DEFAULT_ALLOW_PAID_EMBEDDING_CALLS = False


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration for the application."""

    embedding_provider: str
    openai_api_key: str | None
    openai_embedding_model: str
    max_embedding_chunks_per_run: int
    max_estimated_embedding_tokens_per_run: int
    allow_paid_embedding_calls: bool


def load_config(environ: dict[str, str] | None = None) -> AppConfig:
    """Load application config from environment variables."""
    environment = environ if environ is not None else os.environ

    embedding_provider = environment.get(
        "IAPA_EMBEDDING_PROVIDER",
        DEFAULT_EMBEDDING_PROVIDER,
    ).strip().lower()

    if embedding_provider not in SUPPORTED_EMBEDDING_PROVIDERS:
        raise ValueError(f"Unsupported embedding provider: {embedding_provider}")

    openai_api_key = _empty_string_to_none(environment.get("OPENAI_API_KEY"))

    if embedding_provider == "openai" and openai_api_key is None:
        raise ValueError("OPENAI_API_KEY is required when IAPA_EMBEDDING_PROVIDER=openai")

    return AppConfig(
        embedding_provider=embedding_provider,
        openai_api_key=openai_api_key,
        openai_embedding_model=environment.get(
            "IAPA_OPENAI_EMBEDDING_MODEL",
            DEFAULT_OPENAI_EMBEDDING_MODEL,
        ).strip(),
        max_embedding_chunks_per_run=_get_positive_int(
            environment,
            "IAPA_MAX_EMBEDDING_CHUNKS_PER_RUN",
            DEFAULT_MAX_EMBEDDING_CHUNKS_PER_RUN,
        ),
        max_estimated_embedding_tokens_per_run=_get_positive_int(
            environment,
            "IAPA_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN",
            DEFAULT_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN,
        ),
        allow_paid_embedding_calls=_get_bool(
            environment,
            "IAPA_ALLOW_PAID_EMBEDDING_CALLS",
            DEFAULT_ALLOW_PAID_EMBEDDING_CALLS,
        ),
    )


def _empty_string_to_none(value: str | None) -> str | None:
    if value is None:
        return None

    stripped_value = value.strip()
    return stripped_value or None


def _get_positive_int(
    environment: dict[str, str],
    name: str,
    default: int,
) -> int:
    raw_value = environment.get(name)

    if raw_value is None:
        return default

    try:
        value = int(raw_value)
    except ValueError as error:
        raise ValueError(f"{name} must be an integer") from error

    if value < 1:
        raise ValueError(f"{name} must be at least 1")

    return value


def _get_bool(
    environment: dict[str, str],
    name: str,
    default: bool,
) -> bool:
    raw_value = environment.get(name)

    if raw_value is None:
        return default

    normalized_value = raw_value.strip().lower()

    if normalized_value in {"1", "true", "yes", "y", "on"}:
        return True

    if normalized_value in {"0", "false", "no", "n", "off"}:
        return False

    raise ValueError(f"{name} must be a boolean")

