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

VALIDATE_FILE_PREFIX = "validate file "
INSPECT_CSV_PREFIX = "inspect csv "
INSPECT_EXCEL_PREFIX = "inspect excel "
INSPECT_PDF_PREFIX = "inspect pdf "
EXTRACT_PDF_TEXT_PREFIX = "extract pdf text "
GENERATE_REPORT_PREFIX = "generate report for "


def run_minimal_agent(request: str, project_root: Path) -> AgentResponse:
    """Handle a small set of safe, rule-based requests."""
    normalized_request = request.strip().lower()

    file_listing_response = _try_handle_file_listing(normalized_request, project_root)
    if file_listing_response is not None:
        return file_listing_response

    file_validation_response = _try_handle_file_validation(normalized_request, project_root)
    if file_validation_response is not None:
        return file_validation_response

    csv_inspection_response = _try_handle_csv_inspection(normalized_request, project_root)
    if csv_inspection_response is not None:
        return csv_inspection_response

    excel_inspection_response = _try_handle_excel_inspection(normalized_request, project_root)
    if excel_inspection_response is not None:
        return excel_inspection_response

    pdf_inspection_response = _try_handle_pdf_inspection(normalized_request, project_root)
    if pdf_inspection_response is not None:
        return pdf_inspection_response

    pdf_text_extraction_response = _try_handle_pdf_text_extraction(
        normalized_request,
        project_root,
    )
    if pdf_text_extraction_response is not None:
        return pdf_text_extraction_response

    report_generation_response = _try_handle_report_generation(normalized_request, project_root)
    if report_generation_response is not None:
        return report_generation_response

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


def _try_handle_file_validation(request: str, project_root: Path) -> AgentResponse | None:
    """Handle explicit input file validation requests."""
    if not request.startswith(VALIDATE_FILE_PREFIX):
        return None

    filename = request.removeprefix(VALIDATE_FILE_PREFIX).strip()
    if not filename:
        return AgentResponse(
            status="unsupported_request",
            message="File validation requires a filename.",
        )

    result = execute_tool(
        tool_name="validate_input_file",
        arguments={"filename": filename},
        project_root=project_root,
    )

    return AgentResponse(
        status="completed",
        message=f"Validated input file {filename}.",
        tool_name="validate_input_file",
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


def _try_handle_excel_inspection(request: str, project_root: Path) -> AgentResponse | None:
    """Handle explicit Excel inspection requests."""
    if not request.startswith(INSPECT_EXCEL_PREFIX):
        return None

    filename = request.removeprefix(INSPECT_EXCEL_PREFIX).strip()
    if not filename:
        return AgentResponse(
            status="unsupported_request",
            message="Excel inspection requires a filename.",
        )

    result = execute_tool(
        tool_name="inspect_excel",
        arguments={"filename": filename},
        project_root=project_root,
    )

    return AgentResponse(
        status="completed",
        message=f"Inspected Excel file {filename}.",
        tool_name="inspect_excel",
        result=result,
    )


def _try_handle_pdf_inspection(request: str, project_root: Path) -> AgentResponse | None:
    """Handle explicit PDF inspection requests."""
    if not request.startswith(INSPECT_PDF_PREFIX):
        return None

    filename = request.removeprefix(INSPECT_PDF_PREFIX).strip()
    if not filename:
        return AgentResponse(
            status="unsupported_request",
            message="PDF inspection requires a filename.",
        )

    result = execute_tool(
        tool_name="inspect_pdf",
        arguments={"filename": filename},
        project_root=project_root,
    )

    return AgentResponse(
        status="completed",
        message=f"Inspected PDF file {filename}.",
        tool_name="inspect_pdf",
        result=result,
    )


def _try_handle_pdf_text_extraction(
    request: str,
    project_root: Path,
) -> AgentResponse | None:
    """Handle explicit PDF text extraction requests."""
    if not request.startswith(EXTRACT_PDF_TEXT_PREFIX):
        return None

    filename = request.removeprefix(EXTRACT_PDF_TEXT_PREFIX).strip()
    if not filename:
        return AgentResponse(
            status="unsupported_request",
            message="PDF text extraction requires a filename.",
        )

    result = execute_tool(
        tool_name="extract_pdf_text",
        arguments={"filename": filename},
        project_root=project_root,
    )

    return AgentResponse(
        status="completed",
        message=f"Extracted text from PDF file {filename}.",
        tool_name="extract_pdf_text",
        result=result,
    )


def _try_handle_report_generation(request: str, project_root: Path) -> AgentResponse | None:
    """Handle explicit report generation requests."""
    if not request.startswith(GENERATE_REPORT_PREFIX):
        return None

    filename = request.removeprefix(GENERATE_REPORT_PREFIX).strip()
    if not filename:
        return AgentResponse(
            status="unsupported_request",
            message="Report generation requires a filename.",
        )

    result = execute_tool(
        tool_name="generate_basic_report",
        arguments={"filename": filename},
        project_root=project_root,
    )

    return AgentResponse(
        status="completed",
        message=f"Generated basic report for {filename}.",
        tool_name="generate_basic_report",
        result=result,
    )
