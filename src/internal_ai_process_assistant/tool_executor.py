"""Controlled execution layer for registered tools."""

from pathlib import Path
from typing import Any

from internal_ai_process_assistant.tools.file_listing import (
    FileListResult,
    list_available_files,
)


def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
    project_root: Path,
) -> FileListResult:
    """Execute a registered tool with validated arguments."""
    if tool_name != "list_available_files":
        msg = f"Unsupported tool: {tool_name}"
        raise ValueError(msg)

    area = arguments.get("area")
    if area is None:
        msg = "Missing required argument: area"
        raise ValueError(msg)

    return list_available_files(area=area, project_root=project_root)  # type: ignore[arg-type]
