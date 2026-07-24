"""Controlled execution layer for registered tools."""

from pathlib import Path
from typing import Any

from internal_ai_process_assistant.tools.csv_inspection import CsvInspectionResult, inspect_csv
from internal_ai_process_assistant.tools.file_listing import FileListResult, list_available_files

ToolExecutionResult = FileListResult | CsvInspectionResult


def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
    project_root: Path,
) -> ToolExecutionResult:
    """Execute a registered tool with validated arguments."""
    if tool_name == "list_available_files":
        area = arguments.get("area")
        if area is None:
            msg = "Missing required argument: area"
            raise ValueError(msg)

        return list_available_files(area=area, project_root=project_root)  # type: ignore[arg-type]

    if tool_name == "inspect_csv":
        filename = arguments.get("filename")
        if filename is None:
            msg = "Missing required argument: filename"
            raise ValueError(msg)

        if not isinstance(filename, str):
            msg = "Argument filename must be a string"
            raise ValueError(msg)

        return inspect_csv(filename=filename, project_root=project_root)

    msg = f"Unsupported tool: {tool_name}"
    raise ValueError(msg)
