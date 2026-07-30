from pathlib import Path

import pytest
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from internal_ai_process_assistant.rag.pdf_retrieval import search_pdf_text


def create_pdf_file(path: Path, page_texts: list[str]) -> None:
    pdf = canvas.Canvas(str(path), pagesize=A4)
    _, height = A4

    for text in page_texts:
        pdf.setFont("Helvetica", 12)
        pdf.drawString(72, height - 72, text)
        pdf.showPage()

    pdf.save()


def test_search_pdf_text_returns_source_aware_matches(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    create_pdf_file(
        input_dir / "sample.pdf",
        [
            "Internal assistant overview",
            "Privacy policy and data protection notes",
        ],
    )

    result = search_pdf_text(
        filename="sample.pdf",
        query="privacy",
        project_root=tmp_path,
    )

    assert result.filename == "sample.pdf"
    assert result.query == "privacy"
    assert result.match_count == 1
    assert result.matches[0].match_count == 1
    assert result.matches[0].chunk.source_filename == "sample.pdf"
    assert result.matches[0].chunk.source_type == "pdf"
    assert result.matches[0].chunk.page_number == 2
    assert "Privacy policy" in result.matches[0].chunk.text


def test_search_pdf_text_returns_empty_matches_for_blank_query(tmp_path: Path) -> None:
    result = search_pdf_text(
        filename="sample.pdf",
        query="   ",
        project_root=tmp_path,
    )

    assert result.filename == "sample.pdf"
    assert result.query == "   "
    assert result.match_count == 0
    assert result.matches == []


def test_search_pdf_text_returns_empty_matches_when_query_not_found(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    create_pdf_file(input_dir / "sample.pdf", ["Internal assistant overview"])

    result = search_pdf_text(
        filename="sample.pdf",
        query="invoice",
        project_root=tmp_path,
    )

    assert result.filename == "sample.pdf"
    assert result.query == "invoice"
    assert result.match_count == 0
    assert result.matches == []


def test_search_pdf_text_uses_chunk_limits(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    create_pdf_file(input_dir / "sample.pdf", ["assistant assistant assistant"])

    result = search_pdf_text(
        filename="sample.pdf",
        query="assistant",
        project_root=tmp_path,
        chunk_size=10,
        chunk_overlap=0,
    )

    assert result.match_count >= 1
    assert all(match.chunk.source_filename == "sample.pdf" for match in result.matches)


def test_search_pdf_text_rejects_non_pdf_file(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text("name,amount\nAlice,100\n", encoding="utf-8")

    with pytest.raises(ValueError, match="requires a .pdf file"):
        search_pdf_text(
            filename="sample.csv",
            query="alice",
            project_root=tmp_path,
        )
