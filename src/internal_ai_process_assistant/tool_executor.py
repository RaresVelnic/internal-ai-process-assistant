"""Controlled execution layer for registered tools."""

from pathlib import Path
from typing import Any

from internal_ai_process_assistant.config import AppConfig
from internal_ai_process_assistant.rag.embedding_provider_factory import get_embedding_provider

from internal_ai_process_assistant.rag.pdf_retrieval import PdfRetrievalResult, search_pdf_text
from internal_ai_process_assistant.rag.pdf_vector_retrieval import (
    PdfVectorRetrievalResult,
    retrieve_pdf_chunks_by_vector,
)

from internal_ai_process_assistant.tools.basic_report import (
    BasicReportResult,
    generate_basic_report,
)
from internal_ai_process_assistant.tools.csv_inspection import CsvInspectionResult, inspect_csv
from internal_ai_process_assistant.tools.excel_inspection import ExcelInspectionResult, inspect_excel
from internal_ai_process_assistant.tools.file_listing import FileListResult, list_available_files
from internal_ai_process_assistant.tools.pdf_inspection import PdfInspectionResult, inspect_pdf
from internal_ai_process_assistant.tools.pdf_text_extraction import (
    PdfTextExtractionResult,
    extract_pdf_text,
)
from internal_ai_process_assistant.tools.input_file_validation import (
    InputFileValidationResult,
    validate_input_file,
)

ToolExecutionResult = (
    FileListResult
    | InputFileValidationResult
    | CsvInspectionResult
    | ExcelInspectionResult
    | PdfInspectionResult
    | PdfTextExtractionResult
    | PdfRetrievalResult
    | PdfVectorRetrievalResult
    | BasicReportResult
)


def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
    project_root: Path,
    config: AppConfig | None = None,
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

    if tool_name == "inspect_pdf":
        filename = _get_required_string_argument(arguments, "filename")
        return inspect_pdf(filename=filename, project_root=project_root)

    if tool_name == "extract_pdf_text":
        filename = _get_required_string_argument(arguments, "filename")
        return extract_pdf_text(filename=filename, project_root=project_root)

    if tool_name == "search_pdf_text":
        filename = _get_required_string_argument(arguments, "filename")
        query = _get_required_string_argument(arguments, "query")
        return search_pdf_text(filename=filename, query=query, project_root=project_root)

    if tool_name == "search_pdf_by_vector":
        filename = _get_required_string_argument(arguments, "filename")
        query = _get_required_string_argument(arguments, "query")
        max_chunks = _get_optional_int_argument(arguments, "max_chunks")
        max_estimated_tokens = _get_optional_int_argument(arguments, "max_estimated_tokens")

        keyword_arguments = {}
        if max_chunks is not None:
            keyword_arguments["max_chunks"] = max_chunks
        if max_estimated_tokens is not None:
            keyword_arguments["max_estimated_tokens"] = max_estimated_tokens

        provider = get_embedding_provider(config) if config is not None else None

        return retrieve_pdf_chunks_by_vector(
            filename=filename,
            query=query,
            project_root=project_root,
            provider=provider,
            **keyword_arguments,
        )

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

def _get_optional_int_argument(arguments: dict[str, Any], name: str) -> int | None:
    """Return an optional integer argument from a tool argument mapping."""
    value = arguments.get(name)
    if value is None:
        return None

    if not isinstance(value, int):
        msg = f"Argument {name} must be an integer"
        raise ValueError(msg)

    return value

