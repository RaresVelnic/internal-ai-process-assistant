from pathlib import Path

import pytest
from openpyxl import Workbook

from internal_ai_process_assistant.tools.excel_inspection import inspect_excel


def create_excel_file(path: Path) -> None:
    workbook = Workbook()

    expenses = workbook.active
    expenses.title = "Expenses"
    expenses.append(["name", "department", "amount"])
    expenses.append(["Alice Example", "Operations", 1200])
    expenses.append(["Bob Example", "Finance", 850])

    summary = workbook.create_sheet("Summary")
    summary.append(["metric", "value"])
    summary.append(["row_count", 2])

    workbook.save(path)


def test_inspect_excel_returns_workbook_metadata(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    create_excel_file(input_dir / "sample.xlsx")

    result = inspect_excel("sample.xlsx", project_root=tmp_path)

    assert result.filename == "sample.xlsx"
    assert result.sheet_count == 2
    assert result.sheets[0].name == "Expenses"
    assert result.sheets[0].row_count == 3
    assert result.sheets[0].column_count == 3
    assert result.sheets[1].name == "Summary"
    assert result.sheets[1].row_count == 2
    assert result.sheets[1].column_count == 2


def test_inspect_excel_rejects_non_excel_file(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text("name,amount\nAlice,100\n", encoding="utf-8")

    with pytest.raises(ValueError, match="requires a .xlsx file"):
        inspect_excel("sample.csv", project_root=tmp_path)


def test_inspect_excel_rejects_nested_paths(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    nested_dir = input_dir / "nested"
    nested_dir.mkdir()
    create_excel_file(nested_dir / "sample.xlsx")

    with pytest.raises(ValueError, match="must not include directories"):
        inspect_excel("nested/sample.xlsx", project_root=tmp_path)
