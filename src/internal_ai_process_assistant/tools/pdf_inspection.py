"""Safe PDF inspection utilities for controlled project input files."""

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from internal_ai_process_assistant.tools.input_file_validation import validate_input_file


@dataclass(frozen=True)
class PdfPageInfo:
    """Structured metadata for one PDF page."""

    page_number: int
    text_length: int


@dataclass(frozen=True)
class PdfInspectionResult:
    """Structured metadata returned by the PDF inspection tool."""

    filename: str
    page_count: int
    is_encrypted: bool
    pages: list[PdfPageInfo]


def inspect_pdf(filename: str, project_root: Path | None = None) -> PdfInspectionResult:
    """Inspect a controlled PDF input file and return basic page metadata."""
    validated_file = validate_input_file(filename=filename, project_root=project_root)

    if validated_file.extension != ".pdf":
        raise ValueError("PDF inspection requires a .pdf file")

    root = project_root or Path.cwd()
    pdf_path = root / validated_file.relative_path

    reader = PdfReader(pdf_path)

    if reader.is_encrypted:
        return PdfInspectionResult(
            filename=validated_file.filename,
            page_count=len(reader.pages),
            is_encrypted=True,
            pages=[],
        )

    pages = [
        PdfPageInfo(
            page_number=index,
            text_length=len(page.extract_text() or ""),
        )
        for index, page in enumerate(reader.pages, start=1)
    ]

    return PdfInspectionResult(
        filename=validated_file.filename,
        page_count=len(reader.pages),
        is_encrypted=False,
        pages=pages,
    )
