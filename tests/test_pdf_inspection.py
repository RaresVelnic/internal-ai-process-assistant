from pathlib import Path

import pytest
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from internal_ai_process_assistant.tools.pdf_inspection import inspect_pdf


def create_pdf_file(path: Path) -> None:
    pdf = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(72, height - 72, "Internal AI Process Assistant")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(72, height - 105, "Demo PDF page one.")
    pdf.showPage()

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(72, height - 72, "Processing Notes")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(72, height - 105, "Demo PDF page two.")
    pdf.showPage()

    pdf.save()


def test_inspect_pdf_returns_page_metadata(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    create_pdf_file(input_dir / "sample.pdf")

    result = inspect_pdf("sample.pdf", project_root=tmp_path)

    assert result.filename == "sample.pdf"
    assert result.page_count == 2
    assert result.is_encrypted is False
    assert len(result.pages) == 2
    assert result.pages[0].page_number == 1
    assert result.pages[0].text_length > 0
    assert result.pages[1].page_number == 2
    assert result.pages[1].text_length > 0


def test_inspect_pdf_rejects_non_pdf_file(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text("name,amount\nAlice,100\n", encoding="utf-8")

    with pytest.raises(ValueError, match="requires a .pdf file"):
        inspect_pdf("sample.csv", project_root=tmp_path)


def test_inspect_pdf_rejects_nested_paths(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    nested_dir = input_dir / "nested"
    nested_dir.mkdir()
    create_pdf_file(nested_dir / "sample.pdf")

    with pytest.raises(ValueError, match="must not include directories"):
        inspect_pdf("nested/sample.pdf", project_root=tmp_path)
