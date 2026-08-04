from pathlib import Path

import pytest

from internal_ai_process_assistant.minimal_agent import run_minimal_agent
from internal_ai_process_assistant.tools.basic_report import BasicReportResult
from internal_ai_process_assistant.tools.csv_inspection import CsvInspectionResult
from internal_ai_process_assistant.tools.file_listing import FileListResult
from internal_ai_process_assistant.tools.input_file_validation import InputFileValidationResult


def test_run_minimal_agent_lists_files_in_input(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text("name,value\nAlice,10\n", encoding="utf-8")

    response = run_minimal_agent("list files in input", tmp_path)

    assert response.status == "completed"
    assert response.tool_name == "list_available_files"
    assert isinstance(response.result, FileListResult)
    assert response.result.area == "input"
    assert response.result.files[0].name == "sample.csv"


def test_run_minimal_agent_normalizes_request_text(tmp_path: Path) -> None:
    workspace_dir = tmp_path / "workspace"
    workspace_dir.mkdir()

    response = run_minimal_agent("  LIST FILES IN WORKSPACE  ", tmp_path)

    assert response.status == "completed"
    assert isinstance(response.result, FileListResult)
    assert response.result.area == "workspace"


def test_run_minimal_agent_validates_input_file(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text("name,amount\nAlice,10\n", encoding="utf-8")

    response = run_minimal_agent("validate file sample.csv", tmp_path)

    assert response.status == "completed"
    assert response.tool_name == "validate_input_file"
    assert isinstance(response.result, InputFileValidationResult)
    assert response.result.relative_path == "input/sample.csv"


def test_run_minimal_agent_rejects_empty_validation_filename(tmp_path: Path) -> None:
    response = run_minimal_agent("validate file   ", tmp_path)

    assert response.status == "unsupported_request"
    assert response.tool_name is None
    assert response.result is None


def test_run_minimal_agent_inspects_csv_file(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text(
        "name,amount\nAlice,10\nBob,\n",
        encoding="utf-8",
    )

    response = run_minimal_agent("inspect csv sample.csv", tmp_path)

    assert response.status == "completed"
    assert response.tool_name == "inspect_csv"
    assert isinstance(response.result, CsvInspectionResult)
    assert response.result.filename == "sample.csv"
    assert response.result.row_count == 2
    assert response.result.missing_values_by_column == {"name": 0, "amount": 1}


def test_run_minimal_agent_generates_basic_report(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text(
        "name,amount\nAlice,10\nBob,\n",
        encoding="utf-8",
    )

    response = run_minimal_agent("generate report for sample.csv", tmp_path)

    assert response.status == "completed"
    assert response.tool_name == "generate_basic_report"
    assert isinstance(response.result, BasicReportResult)
    assert response.result.report_relative_path == "output/sample_report.md"
    assert (tmp_path / "output" / "sample_report.md").exists()


def test_run_minimal_agent_rejects_empty_csv_filename(tmp_path: Path) -> None:
    response = run_minimal_agent("inspect csv   ", tmp_path)

    assert response.status == "unsupported_request"
    assert response.tool_name is None
    assert response.result is None


def test_run_minimal_agent_rejects_empty_report_filename(tmp_path: Path) -> None:
    response = run_minimal_agent("generate report for   ", tmp_path)

    assert response.status == "unsupported_request"
    assert response.tool_name is None
    assert response.result is None


def test_run_minimal_agent_rejects_unsupported_request(tmp_path: Path) -> None:
    response = run_minimal_agent("delete files in input", tmp_path)

    assert response.status == "unsupported_request"
    assert response.tool_name is None
    assert response.result is None


def test_run_minimal_agent_inspects_excel_file(tmp_path: Path) -> None:
    from openpyxl import Workbook

    from internal_ai_process_assistant.tools.excel_inspection import ExcelInspectionResult

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Expenses"
    sheet.append(["name", "amount"])
    sheet.append(["Alice Example", 100])
    workbook.save(input_dir / "sample.xlsx")

    response = run_minimal_agent("inspect excel sample.xlsx", tmp_path)

    assert response.status == "completed"
    assert response.tool_name == "inspect_excel"
    assert isinstance(response.result, ExcelInspectionResult)
    assert response.result.filename == "sample.xlsx"
    assert response.result.sheet_count == 1
    assert response.result.sheets[0].name == "Expenses"


def test_run_minimal_agent_rejects_empty_excel_filename(tmp_path: Path) -> None:
    response = run_minimal_agent("inspect excel   ", tmp_path)

    assert response.status == "unsupported_request"
    assert response.tool_name is None
    assert response.result is None


def test_run_minimal_agent_inspects_pdf_file(tmp_path: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    from internal_ai_process_assistant.tools.pdf_inspection import PdfInspectionResult

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    pdf_path = input_dir / "sample.pdf"
    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    _, height = A4
    pdf.drawString(72, height - 72, "Internal AI Process Assistant")
    pdf.showPage()
    pdf.save()

    response = run_minimal_agent("inspect pdf sample.pdf", tmp_path)

    assert response.status == "completed"
    assert response.tool_name == "inspect_pdf"
    assert isinstance(response.result, PdfInspectionResult)
    assert response.result.filename == "sample.pdf"
    assert response.result.page_count == 1
    assert response.result.pages[0].text_length > 0


def test_run_minimal_agent_rejects_empty_pdf_filename(tmp_path: Path) -> None:
    response = run_minimal_agent("inspect pdf   ", tmp_path)

    assert response.status == "unsupported_request"
    assert response.tool_name is None
    assert response.result is None


def test_run_minimal_agent_extracts_pdf_text(tmp_path: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    from internal_ai_process_assistant.tools.pdf_text_extraction import PdfTextExtractionResult

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    pdf_path = input_dir / "sample.pdf"
    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    _, height = A4
    pdf.drawString(72, height - 72, "Internal AI Process Assistant")
    pdf.showPage()
    pdf.save()

    response = run_minimal_agent("extract pdf text sample.pdf", tmp_path)

    assert response.status == "completed"
    assert response.tool_name == "extract_pdf_text"
    assert isinstance(response.result, PdfTextExtractionResult)
    assert response.result.filename == "sample.pdf"
    assert response.result.extracted_page_count == 1
    assert "Internal AI Process Assistant" in response.result.pages[0].text


def test_run_minimal_agent_rejects_empty_pdf_text_filename(tmp_path: Path) -> None:
    response = run_minimal_agent("extract pdf text   ", tmp_path)

    assert response.status == "unsupported_request"
    assert response.tool_name is None
    assert response.result is None


def test_run_minimal_agent_searches_pdf_text(tmp_path: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    from internal_ai_process_assistant.rag.pdf_retrieval import PdfRetrievalResult

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    pdf_path = input_dir / "sample.pdf"
    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    _, height = A4
    pdf.drawString(72, height - 72, "Privacy policy document")
    pdf.showPage()
    pdf.save()

    response = run_minimal_agent("search pdf sample.pdf for privacy", tmp_path)

    assert response.status == "completed"
    assert response.tool_name == "search_pdf_text"
    assert isinstance(response.result, PdfRetrievalResult)
    assert response.result.filename == "sample.pdf"
    assert response.result.query == "privacy"
    assert response.result.match_count == 1
    assert "Privacy policy" in response.result.matches[0].chunk.text
    assert response.result.citations == ["sample.pdf, page 1, chunk 0"]


def test_run_minimal_agent_rejects_pdf_search_without_query(tmp_path: Path) -> None:
    response = run_minimal_agent("search pdf sample.pdf", tmp_path)

    assert response.status == "unsupported_request"
    assert response.tool_name is None
    assert response.result is None


def test_run_minimal_agent_rejects_pdf_search_with_empty_query(tmp_path: Path) -> None:
    response = run_minimal_agent("search pdf sample.pdf for   ", tmp_path)

    assert response.status == "unsupported_request"
    assert response.tool_name is None
    assert response.result is None


def test_run_minimal_agent_searches_pdf_by_vector(tmp_path: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    from internal_ai_process_assistant.rag.pdf_vector_retrieval import PdfVectorRetrievalResult

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    pdf_path = input_dir / "sample.pdf"
    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    _, height = A4
    pdf.drawString(72, height - 72, "Privacy policy document")
    pdf.showPage()
    pdf.save()

    response = run_minimal_agent("search pdf sample.pdf by vector for privacy", tmp_path)

    assert response.status == "completed"
    assert response.tool_name == "search_pdf_by_vector"
    assert isinstance(response.result, PdfVectorRetrievalResult)
    assert response.result.filename == "sample.pdf"
    assert response.result.query == "privacy"
    assert response.result.match_count == 1
    assert "Privacy policy" in response.result.matches[0].text
    assert response.result.matches[0].citation == "sample.pdf, page 1, chunk 0"


def test_run_minimal_agent_rejects_pdf_vector_search_with_empty_query(tmp_path: Path) -> None:
    response = run_minimal_agent("search pdf sample.pdf by vector for   ", tmp_path)

    assert response.status == "unsupported_request"
    assert response.tool_name is None
    assert response.result is None

def test_run_minimal_agent_uses_configured_vector_search_chunk_limit(tmp_path: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    from internal_ai_process_assistant.config import AppConfig

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    pdf_path = input_dir / "sample.pdf"
    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    _, height = A4
    pdf.drawString(72, height - 72, "Privacy policy document")
    pdf.showPage()
    pdf.drawString(72, height - 72, "Second privacy page")
    pdf.showPage()
    pdf.save()

    config = AppConfig(
        embedding_provider="deterministic",
        openai_api_key=None,
        openai_embedding_model="text-embedding-3-small",
        max_embedding_chunks_per_run=1,
        max_estimated_embedding_tokens_per_run=20_000,
    )

    with pytest.raises(ValueError, match="exceeds the limit of 1"):
        run_minimal_agent(
            "search pdf sample.pdf by vector for privacy",
            tmp_path,
            config=config,
        )


def test_run_minimal_agent_estimates_pdf_vector_retrieval(tmp_path: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    from internal_ai_process_assistant.rag.pdf_vector_retrieval import (
        PdfVectorRetrievalEstimate,
    )

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    pdf_path = input_dir / "sample.pdf"
    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    _, height = A4
    pdf.drawString(72, height - 72, "Privacy policy document")
    pdf.showPage()
    pdf.save()

    response = run_minimal_agent("estimate vector search for sample.pdf", tmp_path)

    assert response.status == "completed"
    assert response.tool_name == "estimate_pdf_vector_retrieval"
    assert isinstance(response.result, PdfVectorRetrievalEstimate)
    assert response.result.filename == "sample.pdf"
    assert response.result.chunk_count > 0
    assert response.result.estimated_tokens > 0
    assert float(response.result.estimated_cost_usd) > 0


def test_run_minimal_agent_rejects_empty_pdf_vector_estimate_filename(
    tmp_path: Path,
) -> None:
    response = run_minimal_agent("estimate vector search for   ", tmp_path)

    assert response.status == "unsupported_request"
    assert response.tool_name is None
    assert response.result is None


def test_run_minimal_agent_uses_configured_vector_estimate_token_limit(
    tmp_path: Path,
) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    from internal_ai_process_assistant.config import AppConfig

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    pdf_path = input_dir / "sample.pdf"
    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    _, height = A4
    pdf.drawString(72, height - 72, "Privacy policy document")
    pdf.showPage()
    pdf.save()

    config = AppConfig(
        embedding_provider="deterministic",
        openai_api_key=None,
        openai_embedding_model="text-embedding-3-small",
        max_embedding_chunks_per_run=20,
        max_estimated_embedding_tokens_per_run=1,
    )

    with pytest.raises(ValueError, match="exceeds the limit of 1"):
        run_minimal_agent(
            "estimate vector search for sample.pdf",
            tmp_path,
            config=config,
        )
