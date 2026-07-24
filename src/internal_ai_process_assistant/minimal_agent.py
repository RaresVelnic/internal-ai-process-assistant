"""Minimal rule-based agent for Phase 1."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from internal_ai_process_assistant.tool_executor import ToolExecutionResult, execute_tool

AgentStatus = Literal["completed", "unsupported_request"]


@dataclass(frozen=True)
class AgentResponse:
    """Structured response returned by the minimal agent."""

    status: AgentStatus
    message: str
    tool_name: str | None = None
    result: ToolExecutionResult | None = None


SUPPORTED_FILE_LISTING_REQUESTS = {
    "list files in input": "input",
    "list files in workspace": "workspace",
    "list files in output": "output",
}

INSPECT_CSV_PREFIX = "inspect csv "


def run_minimal_agent(request: str, project_root: Path) -> AgentResponse:
    """Handle a small set of safe, rule-based requests."""
    normalized_request = request.strip().lower()

    file_listing_response = _try_handle_file_listing(normalized_request, project_root)
    if file_listing_response is not None:
        return file_listing_response

    csv_inspection_response = _try_handle_csv_inspection(normalized_request, project_root)
    if csv_inspection_response is not None:
        return csv_inspection_response

    return AgentResponse(
        status="unsupported_request",
        message="This request is not supported by the minimal Phase 1 agent.",
    )


def _try_handle_file_listing(request: str, project_root: Path) -> AgentResponse | None:
    """Handle explicit file listing requests."""
    area = SUPPORTED_FILE_LISTING_REQUESTS.get(request)

    if area is None:
        return None

    result = execute_tool(
        tool_name="list_available_files",
        arguments={"area": area},
        project_root=project_root,
    )

    return AgentResponse(
        status="completed",
        message=f"Listed files in {area}.",
        tool_name="list_available_files",
        result=result,
    )


def _try_handle_csv_inspection(request: str, project_root: Path) -> AgentResponse | None:
    """Handle explicit CSV inspection requests."""
    if not request.startswith(INSPECT_CSV_PREFIX):
        return None

    filename = request.removeprefix(INSPECT_CSV_PREFIX).strip()
    if not filename:
        return AgentResponse(
            status="unsupported_request",
            message="CSV inspection requires a filename.",
        )

    result = execute_tool(
        tool_name="inspect_csv",
        arguments={"filename": filename},
        project_root=project_root,
    )

    return AgentResponse(
        status="completed",
        message=f"Inspected CSV file {filename}.",
        tool_name="inspect_csv",
        result=result,
    )
