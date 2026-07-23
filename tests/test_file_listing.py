from pathlib import Path
from typing import cast

import pytest

from internal_ai_process_assistant.tools.file_listing import (
    ControlledArea,
    list_available_files,
)


def test_list_available_files_returns_structured_file_metadata(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / ".gitkeep").touch()
    (input_dir / "sample.csv").write_text("name,value\nAlice,10\n", encoding="utf-8")

    result = list_available_files("input", tmp_path)

    assert result.area == "input"
    assert len(result.files) == 1
    assert result.files[0].name == "sample.csv"
    assert result.files[0].relative_path == "input/sample.csv"
    assert result.files[0].size_bytes > 0
    assert result.files[0].is_file is True


def test_list_available_files_returns_empty_result_for_missing_area(
    tmp_path: Path,
) -> None:
    result = list_available_files("workspace", tmp_path)

    assert result.area == "workspace"
    assert result.files == []


def test_list_available_files_rejects_unsupported_area(tmp_path: Path) -> None:
    unsupported_area = cast(ControlledArea, "../outside")

    with pytest.raises(ValueError, match="Unsupported controlled area"):
        list_available_files(unsupported_area, tmp_path)
