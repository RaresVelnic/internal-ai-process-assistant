"""Safe CSV inspection tool for files in the controlled input directory."""

import csv
from dataclasses import dataclass
from pathlib import Path

from internal_ai_process_assistant.tools.input_file_validation import validate_input_file


@dataclass(frozen=True)
class CsvInspectionResult:
    """Structured result returned by the CSV inspection tool."""

    filename: str
    row_count: int
    column_count: int
    columns: tuple[str, ...]
    missing_values_by_column: dict[str, int]


def inspect_csv(filename: str, project_root: Path) -> CsvInspectionResult:
    """Inspect a CSV file from the controlled input directory."""
    validation = validate_input_file(filename=filename, project_root=project_root)

    if validation.extension != ".csv":
        msg = "CSV inspection requires a .csv file"
        raise ValueError(msg)

    csv_path = project_root / validation.relative_path

    with csv_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        columns = tuple(reader.fieldnames or ())
        missing_values_by_column = {column: 0 for column in columns}
        row_count = 0

        for row in reader:
            row_count += 1
            for column in columns:
                value = row.get(column)
                if value is None or value.strip() == "":
                    missing_values_by_column[column] += 1

    return CsvInspectionResult(
        filename=filename,
        row_count=row_count,
        column_count=len(columns),
        columns=columns,
        missing_values_by_column=missing_values_by_column,
    )
