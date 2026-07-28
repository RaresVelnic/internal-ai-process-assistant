"""Controlled execution layer for registered tools."""

from pathlib import Path
from typing import Any

from internal_ai_process_assistant.tools.basic_report import (
    BasicReportResult,
    generate_basic_report,
)
from internal_ai_process_assistant.tools.csv_inspection import CsvInspectionResult, inspect_csv
from internal_ai_process_assistant.tools.excel_inspection import ExcelInspectionResult, inspect_excel
from internal_ai_process_assistant.tools.file_listing import FileListResult, list_available_files
from internal_ai_process_assistant.tools.input_file_validation import (
    InputFileValidationResult,
    validate_input_file,
)

ToolExecutionResult = (
    FileListResult | InputFileValidationResult | CsvInspectionResult | ExcelInspectionResult | BasicReportResult
)


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

    if tool_name == "validate_input_file":
        filename = _get_required_string_argument(arguments, "filename")
        return validate_input_file(filename=filename, project_root=project_root)

    if tool_name == "inspect_csv":
        filename = _get_required_string_argument(arguments, "filename")
        return inspect_csv(filename=filename, project_root=project_root)

    if tool_name == "inspect_excel":
        filename = _get_required_string_argument(arguments, "filename")
        return inspect_excel(filename=filename, project_root=project_root)

    if tool_name == "generate_basic_report":
        filename = _get_required_string_argument(arguments, "filename")
        return generate_basic_report(filename=filename, project_root=project_root)

    msg = f"Unsupported tool: {tool_name}"
    raise ValueError(msg)


def _get_required_string_argument(arguments: dict[str, Any], name: str) -> str:
    """Return a required string argument from a tool argument mapping."""
    value = arguments.get(name)
    if value is None:
        msg = f"Missing required argument: {name}"
        raise ValueError(msg)

    if not isinstance(value, str):
        msg = f"Argument {name} must be a string"
        raise ValueError(msg)

    return value
