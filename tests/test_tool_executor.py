from pathlib import Path

import pytest

from internal_ai_process_assistant.tool_executor import execute_tool


def test_execute_tool_runs_file_listing_tool(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.txt").write_text("hello", encoding="utf-8")

    result = execute_tool(
        tool_name="list_available_files",
        arguments={"area": "input"},
        project_root=tmp_path,
    )

    assert result.area == "input"
    assert len(result.files) == 1
    assert result.files[0].name == "sample.txt"


def test_execute_tool_runs_input_file_validation_tool(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text("name,amount\nAlice,10\n", encoding="utf-8")

    result = execute_tool(
        tool_name="validate_input_file",
        arguments={"filename": "sample.csv"},
        project_root=tmp_path,
    )

    assert result.filename == "sample.csv"
    assert result.extension == ".csv"
    assert result.relative_path == "input/sample.csv"


def test_execute_tool_runs_csv_inspection_tool(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text(
        "name,amount\nAlice,10\nBob,\n",
        encoding="utf-8",
    )

    result = execute_tool(
        tool_name="inspect_csv",
        arguments={"filename": "sample.csv"},
        project_root=tmp_path,
    )

    assert result.filename == "sample.csv"
    assert result.row_count == 2
    assert result.missing_values_by_column == {"name": 0, "amount": 1}


def test_execute_tool_runs_basic_report_tool(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text(
        "name,amount\nAlice,10\nBob,\n",
        encoding="utf-8",
    )

    result = execute_tool(
        tool_name="generate_basic_report",
        arguments={"filename": "sample.csv"},
        project_root=tmp_path,
    )

    assert result.source_filename == "sample.csv"
    assert result.report_filename == "sample_report.md"
    assert result.report_relative_path == "output/sample_report.md"
    assert (tmp_path / "output" / "sample_report.md").exists()


def test_execute_tool_rejects_unknown_tool(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Unsupported tool"):
        execute_tool(
            tool_name="delete_everything",
            arguments={"area": "input"},
            project_root=tmp_path,
        )


def test_execute_tool_requires_area_argument(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Missing required argument: area"):
        execute_tool(
            tool_name="list_available_files",
            arguments={},
            project_root=tmp_path,
        )


def test_execute_tool_requires_filename_argument_for_csv_inspection(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Missing required argument: filename"):
        execute_tool(
            tool_name="inspect_csv",
            arguments={},
            project_root=tmp_path,
        )


def test_execute_tool_requires_filename_argument_for_basic_report(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Missing required argument: filename"):
        execute_tool(
            tool_name="generate_basic_report",
            arguments={},
            project_root=tmp_path,
        )


def test_execute_tool_requires_filename_to_be_string(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="filename must be a string"):
        execute_tool(
            tool_name="inspect_csv",
            arguments={"filename": 123},
            project_root=tmp_path,
        )


def test_execute_tool_rejects_invalid_area(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Unsupported controlled area"):
        execute_tool(
            tool_name="list_available_files",
            arguments={"area": "../outside"},
            project_root=tmp_path,
        )


def test_execute_tool_runs_excel_inspection_tool(tmp_path: Path) -> None:
    from openpyxl import Workbook

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Expenses"
    sheet.append(["name", "amount"])
    sheet.append(["Alice Example", 100])
    workbook.save(input_dir / "sample.xlsx")

    result = execute_tool(
        tool_name="inspect_excel",
        arguments={"filename": "sample.xlsx"},
        project_root=tmp_path,
    )

    assert result.filename == "sample.xlsx"
    assert result.sheet_count == 1
    assert result.sheets[0].name == "Expenses"
    assert result.sheets[0].row_count == 2
    assert result.sheets[0].column_count == 2


def test_execute_tool_runs_pdf_inspection_tool(tmp_path: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    pdf_path = input_dir / "sample.pdf"
    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    _, height = A4
    pdf.drawString(72, height - 72, "Internal AI Process Assistant")
    pdf.showPage()
    pdf.save()

    result = execute_tool(
        tool_name="inspect_pdf",
        arguments={"filename": "sample.pdf"},
        project_root=tmp_path,
    )

    assert result.filename == "sample.pdf"
    assert result.page_count == 1
    assert result.is_encrypted is False
    assert result.pages[0].page_number == 1
    assert result.pages[0].text_length > 0


def test_execute_tool_runs_pdf_text_extraction_tool(tmp_path: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    pdf_path = input_dir / "sample.pdf"
    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    _, height = A4
    pdf.drawString(72, height - 72, "Internal AI Process Assistant")
    pdf.showPage()
    pdf.save()

    result = execute_tool(
        tool_name="extract_pdf_text",
        arguments={"filename": "sample.pdf"},
        project_root=tmp_path,
    )

    assert result.filename == "sample.pdf"
    assert result.page_count == 1
    assert result.extracted_page_count == 1
    assert "Internal AI Process Assistant" in result.pages[0].text
    assert result.pages[0].truncated is False


def test_execute_tool_runs_pdf_keyword_search_tool(tmp_path: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    pdf_path = input_dir / "sample.pdf"
    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    _, height = A4
    pdf.drawString(72, height - 72, "Privacy policy document")
    pdf.showPage()
    pdf.save()

    result = execute_tool(
        tool_name="search_pdf_text",
        arguments={"filename": "sample.pdf", "query": "privacy"},
        project_root=tmp_path,
    )

    assert result.filename == "sample.pdf"
    assert result.query == "privacy"
    assert result.match_count == 1
    assert "Privacy policy" in result.matches[0].chunk.text


def test_execute_tool_requires_query_argument_for_pdf_keyword_search(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Missing required argument: query"):
        execute_tool(
            tool_name="search_pdf_text",
            arguments={"filename": "sample.pdf"},
            project_root=tmp_path,
        )


def test_execute_tool_runs_pdf_vector_search_tool(tmp_path: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    pdf_path = input_dir / "sample.pdf"
    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    _, height = A4
    pdf.drawString(72, height - 72, "Privacy policy document")
    pdf.showPage()
    pdf.save()

    result = execute_tool(
        tool_name="search_pdf_by_vector",
        arguments={"filename": "sample.pdf", "query": "privacy"},
        project_root=tmp_path,
    )

    assert result.filename == "sample.pdf"
    assert result.query == "privacy"
    assert result.match_count == 1
    assert "Privacy policy" in result.matches[0].text
    assert result.matches[0].citation.startswith("sample.pdf")


def test_execute_tool_requires_query_argument_for_pdf_vector_search(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Missing required argument: query"):
        execute_tool(
            tool_name="search_pdf_by_vector",
            arguments={"filename": "sample.pdf"},
            project_root=tmp_path,
        )


def test_execute_tool_passes_pdf_vector_search_usage_limits(tmp_path: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

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

    with pytest.raises(ValueError, match="exceeds the limit of 1"):
        execute_tool(
            tool_name="search_pdf_by_vector",
            arguments={
                "filename": "sample.pdf",
                "query": "privacy",
                "max_chunks": 1,
            },
            project_root=tmp_path,
        )


def test_execute_tool_requires_pdf_vector_search_limit_to_be_integer(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="max_chunks must be an integer"):
        execute_tool(
            tool_name="search_pdf_by_vector",
            arguments={
                "filename": "sample.pdf",
                "query": "privacy",
                "max_chunks": "many",
            },
            project_root=tmp_path,
        )
