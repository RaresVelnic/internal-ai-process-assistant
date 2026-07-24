from pathlib import Path

import pytest

from internal_ai_process_assistant.tools.input_file_validation import (
    validate_input_file,
)


def test_validate_input_file_returns_metadata_for_csv(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text("name,amount\nAlice,10\n", encoding="utf-8")

    result = validate_input_file("sample.csv", tmp_path)

    assert result.filename == "sample.csv"
    assert result.extension == ".csv"
    assert result.size_bytes > 0
    assert result.relative_path == "input/sample.csv"


def test_validate_input_file_accepts_xlsx_extension(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "workbook.xlsx").write_bytes(b"fake-xlsx-for-validation-only")

    result = validate_input_file("workbook.xlsx", tmp_path)

    assert result.extension == ".xlsx"
    assert result.relative_path == "input/workbook.xlsx"


def test_validate_input_file_accepts_pdf_extension(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "document.pdf").write_bytes(b"%PDF-1.4")

    result = validate_input_file("document.pdf", tmp_path)

    assert result.extension == ".pdf"
    assert result.relative_path == "input/document.pdf"


def test_validate_input_file_rejects_directory_paths(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="must not include directories"):
        validate_input_file("../sample.csv", tmp_path)


def test_validate_input_file_rejects_empty_filename(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        validate_input_file("   ", tmp_path)


def test_validate_input_file_rejects_unsupported_extension(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "notes.txt").write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported input file extension"):
        validate_input_file("notes.txt", tmp_path)


def test_validate_input_file_rejects_missing_file(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    with pytest.raises(FileNotFoundError, match="Input file not found"):
        validate_input_file("missing.csv", tmp_path)


def test_validate_input_file_rejects_directories(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "folder.csv").mkdir()

    with pytest.raises(ValueError, match="Input path is not a file"):
        validate_input_file("folder.csv", tmp_path)
