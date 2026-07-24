"""Minimal rule-based agent for Phase 1."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from internal_ai_process_assistant.tool_executor import execute_tool
from internal_ai_process_assistant.tools.file_listing import FileListResult

AgentStatus = Literal["completed", "unsupported_request"]


@dataclass(frozen=True)
class AgentResponse:
    """Structured response returned by the minimal agent."""

    status: AgentStatus
    message: str
    tool_name: str | None = None
    result: FileListResult | None = None


SUPPORTED_REQUESTS = {
    "list files in input": "input",
    "list files in workspace": "workspace",
    "list files in output": "output",
}


def run_minimal_agent(request: str, project_root: Path) -> AgentResponse:
    """Handle a small set of safe, rule-based requests."""
    normalized_request = request.strip().lower()
    area = SUPPORTED_REQUESTS.get(normalized_request)

    if area is None:
        return AgentResponse(
            status="unsupported_request",
            message="This request is not supported by the minimal Phase 1 agent.",
        )

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
