"""Validation helpers for files in the controlled input directory."""

from dataclasses import dataclass
from pathlib import Path

ALLOWED_INPUT_EXTENSIONS = {".csv", ".xlsx", ".pdf"}


@dataclass(frozen=True)
class InputFileValidationResult:
    """Structured metadata for a validated input file."""

    filename: str
    extension: str
    size_bytes: int
    relative_path: str


def validate_input_file(filename: str, project_root: Path) -> InputFileValidationResult:
    """Validate a file located in the controlled input directory."""
    _validate_simple_filename(filename)

    input_path = project_root / "input" / filename
    extension = input_path.suffix.lower()

    if extension not in ALLOWED_INPUT_EXTENSIONS:
        msg = f"Unsupported input file extension: {extension}"
        raise ValueError(msg)

    if not input_path.exists():
        msg = f"Input file not found: {filename}"
        raise FileNotFoundError(msg)

    if not input_path.is_file():
        msg = f"Input path is not a file: {filename}"
        raise ValueError(msg)

    return InputFileValidationResult(
        filename=filename,
        extension=extension,
        size_bytes=input_path.stat().st_size,
        relative_path=input_path.relative_to(project_root).as_posix(),
    )


def _validate_simple_filename(filename: str) -> None:
    """Validate that only a simple filename is accepted."""
    if filename != Path(filename).name:
        msg = "Input filename must not include directories"
        raise ValueError(msg)

    if ".." in filename:
        msg = "Input filename must not include parent directory references"
        raise ValueError(msg)

    if not filename.strip():
        msg = "Input filename must not be empty"
        raise ValueError(msg)
