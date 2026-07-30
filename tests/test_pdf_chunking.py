from pathlib import Path

import pytest
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from internal_ai_process_assistant.rag.pdf_chunking import chunk_pdf_text


def create_pdf_file(path: Path, page_texts: list[str]) -> None:
    pdf = canvas.Canvas(str(path), pagesize=A4)
    _, height = A4

    for text in page_texts:
        pdf.setFont("Helvetica", 12)
        pdf.drawString(72, height - 72, text)
        pdf.showPage()

    pdf.save()


def test_chunk_pdf_text_returns_source_aware_chunks(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    create_pdf_file(
        input_dir / "sample.pdf",
        [
            "Internal AI Process Assistant page one",
            "Processing Notes page two",
        ],
    )

    chunks = chunk_pdf_text(
        filename="sample.pdf",
        project_root=tmp_path,
        chunk_size=100,
        chunk_overlap=10,
    )

    assert len(chunks) == 2
    assert chunks[0].chunk_index == 0
    assert chunks[0].source_filename == "sample.pdf"
    assert chunks[0].source_type == "pdf"
    assert chunks[0].page_number == 1
    assert "Internal AI Process Assistant" in chunks[0].text

    assert chunks[1].chunk_index == 1
    assert chunks[1].source_filename == "sample.pdf"
    assert chunks[1].source_type == "pdf"
    assert chunks[1].page_number == 2
    assert "Processing Notes" in chunks[1].text


def test_chunk_pdf_text_splits_long_pdf_page_text(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    create_pdf_file(input_dir / "sample.pdf", ["abcdefghij"])

    chunks = chunk_pdf_text(
        filename="sample.pdf",
        project_root=tmp_path,
        chunk_size=4,
        chunk_overlap=1,
    )

    assert [chunk.text for chunk in chunks] == ["abcd", "defg", "ghij"]
    assert [chunk.chunk_index for chunk in chunks] == [0, 1, 2]
    assert all(chunk.page_number == 1 for chunk in chunks)


def test_chunk_pdf_text_rejects_invalid_pdf_filename(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text("name,amount\nAlice,100\n", encoding="utf-8")

    with pytest.raises(ValueError, match="requires a .pdf file"):
        chunk_pdf_text(filename="sample.csv", project_root=tmp_path)


def test_chunk_pdf_text_rejects_invalid_chunk_limits(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    create_pdf_file(input_dir / "sample.pdf", ["Some PDF text"])

    with pytest.raises(ValueError, match="chunk_size must be at least 1"):
        chunk_pdf_text(filename="sample.pdf", project_root=tmp_path, chunk_size=0)

    with pytest.raises(ValueError, match="chunk_overlap must be smaller than chunk_size"):
        chunk_pdf_text(
            filename="sample.pdf",
            project_root=tmp_path,
            chunk_size=5,
            chunk_overlap=5,
        )
