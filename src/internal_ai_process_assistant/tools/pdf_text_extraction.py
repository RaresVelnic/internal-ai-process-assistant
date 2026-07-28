"""Safe PDF text extraction utilities for controlled project input files."""

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from internal_ai_process_assistant.tools.input_file_validation import validate_input_file


DEFAULT_MAX_PAGES = 5
DEFAULT_MAX_CHARS_PER_PAGE = 2_000


@dataclass(frozen=True)
class PdfPageText:
    """Extracted text for one PDF page."""

    page_number: int
    text: str
    truncated: bool


@dataclass(frozen=True)
class PdfTextExtractionResult:
    """Structured result returned by the PDF text extraction tool."""

    filename: str
    page_count: int
    extracted_page_count: int
    pages: list[PdfPageText]


def extract_pdf_text(
    filename: str,
    project_root: Path | None = None,
    max_pages: int = DEFAULT_MAX_PAGES,
    max_chars_per_page: int = DEFAULT_MAX_CHARS_PER_PAGE,
) -> PdfTextExtractionResult:
    """Extract bounded text from a controlled PDF input file."""
    if max_pages < 1:
        raise ValueError("max_pages must be at least 1")

    if max_chars_per_page < 1:
        raise ValueError("max_chars_per_page must be at least 1")

    validated_file = validate_input_file(filename=filename, project_root=project_root)

    if validated_file.extension != ".pdf":
        raise ValueError("PDF text extraction requires a .pdf file")

    root = project_root or Path.cwd()
    pdf_path = root / validated_file.relative_path

    reader = PdfReader(pdf_path)

    if reader.is_encrypted:
        raise ValueError("PDF text extraction does not support encrypted files")

    selected_pages = reader.pages[:max_pages]
    pages: list[PdfPageText] = []

    for index, page in enumerate(selected_pages, start=1):
        text = page.extract_text() or ""
        truncated = len(text) > max_chars_per_page
        if truncated:
            text = text[:max_chars_per_page]

        pages.append(
            PdfPageText(
                page_number=index,
                text=text,
                truncated=truncated,
            )
        )

    return PdfTextExtractionResult(
        filename=validated_file.filename,
        page_count=len(reader.pages),
        extracted_page_count=len(pages),
        pages=pages,
    )
