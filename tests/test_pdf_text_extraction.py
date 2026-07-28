from pathlib import Path

import pytest
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from internal_ai_process_assistant.tools.pdf_text_extraction import extract_pdf_text


def create_pdf_file(path: Path, page_texts: list[str]) -> None:
    pdf = canvas.Canvas(str(path), pagesize=A4)
    _, height = A4

    for text in page_texts:
        pdf.setFont("Helvetica", 12)
        pdf.drawString(72, height - 72, text)
        pdf.showPage()

    pdf.save()


def test_extract_pdf_text_returns_bounded_page_text(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    create_pdf_file(
        input_dir / "sample.pdf",
        [
            "Internal AI Process Assistant",
            "Processing Notes",
        ],
    )

    result = extract_pdf_text("sample.pdf", project_root=tmp_path)

    assert result.filename == "sample.pdf"
    assert result.page_count == 2
    assert result.extracted_page_count == 2
    assert result.pages[0].page_number == 1
    assert "Internal AI Process Assistant" in result.pages[0].text
    assert result.pages[0].truncated is False
    assert result.pages[1].page_number == 2
    assert "Processing Notes" in result.pages[1].text


def test_extract_pdf_text_limits_number_of_pages(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    create_pdf_file(
        input_dir / "sample.pdf",
        [
            "Page one",
            "Page two",
            "Page three",
        ],
    )

    result = extract_pdf_text("sample.pdf", project_root=tmp_path, max_pages=2)

    assert result.page_count == 3
    assert result.extracted_page_count == 2
    assert [page.page_number for page in result.pages] == [1, 2]


def test_extract_pdf_text_truncates_long_page_text(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    create_pdf_file(input_dir / "sample.pdf", ["ABCDEFGHIJ"])

    result = extract_pdf_text(
        "sample.pdf",
        project_root=tmp_path,
        max_chars_per_page=5,
    )

    assert result.pages[0].text == "ABCDE"
    assert result.pages[0].truncated is True


def test_extract_pdf_text_rejects_non_pdf_file(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text("name,amount\nAlice,100\n", encoding="utf-8")

    with pytest.raises(ValueError, match="requires a .pdf file"):
        extract_pdf_text("sample.csv", project_root=tmp_path)


def test_extract_pdf_text_rejects_nested_paths(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    nested_dir = input_dir / "nested"
    nested_dir.mkdir()
    create_pdf_file(nested_dir / "sample.pdf", ["Nested file"])

    with pytest.raises(ValueError, match="must not include directories"):
        extract_pdf_text("nested/sample.pdf", project_root=tmp_path)


def test_extract_pdf_text_rejects_invalid_limits(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="max_pages must be at least 1"):
        extract_pdf_text("sample.pdf", project_root=tmp_path, max_pages=0)

    with pytest.raises(ValueError, match="max_chars_per_page must be at least 1"):
        extract_pdf_text("sample.pdf", project_root=tmp_path, max_chars_per_page=0)
