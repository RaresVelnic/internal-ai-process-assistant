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


def test_execute_tool_rejects_invalid_area(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Unsupported controlled area"):
        execute_tool(
            tool_name="list_available_files",
            arguments={"area": "../outside"},
            project_root=tmp_path,
        )
