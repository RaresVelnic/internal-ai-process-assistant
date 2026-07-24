from pathlib import Path

import pytest

from internal_ai_process_assistant.tools.csv_inspection import inspect_csv


def test_inspect_csv_returns_structured_summary(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text(
        "name,department,amount\n"
        "Alice,Finance,1200\n"
        "Bob,Operations,850\n"
        "Clara,HR,430\n",
        encoding="utf-8",
    )

    result = inspect_csv("sample.csv", tmp_path)

    assert result.filename == "sample.csv"
    assert result.row_count == 3
    assert result.column_count == 3
    assert result.columns == ("name", "department", "amount")
    assert result.missing_values_by_column == {
        "name": 0,
        "department": 0,
        "amount": 0,
    }


def test_inspect_csv_counts_missing_values(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "missing_values.csv").write_text(
        "name,department,amount\n"
        "Alice,Finance,1200\n"
        "Bob,,850\n"
        ",HR,\n",
        encoding="utf-8",
    )

    result = inspect_csv("missing_values.csv", tmp_path)

    assert result.row_count == 3
    assert result.missing_values_by_column == {
        "name": 1,
        "department": 1,
        "amount": 1,
    }


def test_inspect_csv_rejects_directory_paths(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="must not include directories"):
        inspect_csv("../sample.csv", tmp_path)


def test_inspect_csv_rejects_non_csv_files(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="must use the .csv extension"):
        inspect_csv("sample.txt", tmp_path)


def test_inspect_csv_rejects_missing_files(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    with pytest.raises(FileNotFoundError, match="CSV file not found"):
        inspect_csv("missing.csv", tmp_path)
