from pathlib import Path

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
