"""Basic report generation tool for inspected CSV files."""

from dataclasses import dataclass
from pathlib import Path

from internal_ai_process_assistant.tools.csv_inspection import inspect_csv


@dataclass(frozen=True)
class BasicReportResult:
    """Structured result returned by the basic report generation tool."""

    source_filename: str
    report_filename: str
    report_relative_path: str


def generate_basic_report(filename: str, project_root: Path) -> BasicReportResult:
    """Generate a basic Markdown report for a CSV file in the input directory."""
    inspection = inspect_csv(filename=filename, project_root=project_root)

    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)

    report_filename = _build_report_filename(filename)
    report_path = output_dir / report_filename

    report_content = _build_report_content(inspection)
    report_path.write_text(report_content, encoding="utf-8")

    return BasicReportResult(
        source_filename=filename,
        report_filename=report_filename,
        report_relative_path=report_path.relative_to(project_root).as_posix(),
    )


def _build_report_filename(filename: str) -> str:
    """Build a deterministic report filename from the source CSV filename."""
    source_path = Path(filename)
    return f"{source_path.stem}_report.md"


def _build_report_content(inspection: object) -> str:
    """Build Markdown report content from a CSV inspection result."""
    missing_values = "\n".join(
        f"- {column}: {count}"
        for column, count in inspection.missing_values_by_column.items()
    )

    columns = ", ".join(inspection.columns)

    return (
        f"# Basic CSV Report: {inspection.filename}\n\n"
        "## Summary\n\n"
        f"- Rows: {inspection.row_count}\n"
        f"- Columns: {inspection.column_count}\n"
        f"- Column names: {columns}\n\n"
        "## Missing Values\n\n"
        f"{missing_values}\n"
    )
