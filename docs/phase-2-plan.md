# Phase 2: Document and File Processing Plan

Phase 2 builds on the rule-based MVP from Phase 1 and expands the assistant's ability to process files in a controlled, testable way.

The goal is to strengthen file validation and add practical document/data processing capabilities before introducing RAG, LLM orchestration, FastAPI, or a web interface.

## Starting Point

Phase 1 completed a minimal rule-based agent with:

    list_available_files()
    inspect_csv()
    generate_basic_report()

Current request flow:

    CLI request
        -> minimal rule-based agent
        -> controlled tool executor
        -> registered safe tools
        -> structured result or generated output

## Phase 2 Goals

Phase 2 focuses on controlled file processing.

Planned capabilities:

    validate files in controlled directories
    improve CSV inspection robustness
    add Excel file inspection
    add basic PDF text extraction
    generate controlled output files
    keep all runtime input/output data outside Git

## Controlled Runtime Directories

The assistant continues to operate only inside controlled project directories:

    input/
    workspace/
    output/

Rules:

    input/ is for files provided to the assistant
    workspace/ is for intermediate processing files
    output/ is for generated results

Runtime contents of these directories are ignored by Git.

Public demo files stay under:

    examples/

## Security Constraints

Phase 2 must not introduce:

    arbitrary filesystem access
    unrestricted shell execution
    unrestricted Python execution
    automatic deletion of user files
    overwriting user-provided input files
    processing files outside controlled directories

Tools must receive simple filenames or controlled identifiers, not arbitrary absolute paths.

Any operation that writes output must write only to the controlled output directory.

## Planned Tools

### validate_input_file

Purpose:

    Validate that a requested input file exists and has an allowed file type.

Initial supported file types:

    .csv
    .xlsx
    .pdf

The function should return structured metadata instead of free-form text.

### inspect_csv

Purpose:

    Improve the existing CSV inspection tool.

Possible improvements:

    detect empty files
    detect missing headers
    report delimiter assumptions
    handle inconsistent rows more clearly

### inspect_excel

Purpose:

    Inspect an Excel workbook from the input directory.

Initial behavior:

    list sheet names
    count rows and columns per sheet
    report empty sheets
    return structured metadata

### extract_pdf_text

Purpose:

    Extract basic text from a PDF file in the input directory.

Initial behavior:

    read a PDF
    extract text per page
    write extracted text to output or workspace
    return structured metadata

## Explicitly Out of Scope for Phase 2

Phase 2 does not include:

    LLM integration
    LangChain
    LangGraph
    RAG
    vector databases
    FastAPI
    web UI
    authentication
    deployment
    multi-agent workflows
    human-in-the-loop approval flows

These belong to later phases.

## Completion Criteria

Phase 2 is complete when:

    file validation is implemented and tested
    CSV inspection is more robust
    at least one Excel inspection workflow works
    at least one PDF text extraction workflow works
    generated outputs stay in output/
    runtime files remain ignored by Git
    pytest passes
    Ruff passes
    documentation is updated
    all changes are committed and pushed to GitHub

## Completed Step: Input File Validation Through Agent

The project now exposes input file validation end-to-end through the minimal agent workflow.

The validation flow is:

```text
User request
-> CLI
-> minimal rule-based agent
-> controlled tool executor
-> validate_input_file
-> structured validation result
```

Supported CLI example:

```bash
python -m internal_ai_process_assistant.cli "validate file sample.csv"
```

Expected structured result:

```json
{
  "status": "completed",
  "message": "Validated input file sample.csv.",
  "tool_name": "validate_input_file",
  "result": {
    "filename": "sample.csv",
    "extension": ".csv",
    "size_bytes": 74,
    "relative_path": "input/sample.csv"
  }
}
```

Security decisions:

- validation is limited to files inside the controlled `input/` directory;
- arbitrary filesystem paths are rejected;
- nested paths are rejected;
- unsupported extensions are rejected;
- allowed extensions are currently `.csv`, `.xlsx`, and `.pdf`;
- the tool returns structured metadata instead of free-form text.

This step prepares the project for safe document processing tools in Phase 2.

## Completed Step: Excel Inspection Workflow

The project now supports safe Excel workbook inspection through the minimal agent workflow.

The Excel inspection flow is:

```text
User request
-> CLI
-> minimal rule-based agent
-> controlled tool executor
-> inspect_excel
-> validate_input_file
-> openpyxl read-only workbook inspection
-> structured workbook metadata
```

Supported CLI example:

```bash
python -m internal_ai_process_assistant.cli "inspect excel sample.xlsx"
```

Expected structured result shape:

```json
{
  "status": "completed",
  "message": "Inspected Excel file sample.xlsx.",
  "tool_name": "inspect_excel",
  "result": {
    "filename": "sample.xlsx",
    "sheet_count": 2,
    "sheets": [
      {
        "name": "Expenses",
        "row_count": 4,
        "column_count": 3
      },
      {
        "name": "Summary",
        "row_count": 3,
        "column_count": 2
      }
    ]
  }
}
```

Implementation notes:

- `openpyxl` is used for `.xlsx` workbook inspection;
- `defusedxml` is installed as an XML parsing safety dependency;
- workbook loading uses `read_only=True` and `data_only=True`;
- the tool returns workbook metadata only;
- it does not modify, clean, transform, or export Excel data yet.

Security decisions:

- Excel inspection is limited to files inside the controlled `input/` directory;
- arbitrary filesystem paths are rejected by shared input validation;
- nested paths are rejected;
- only `.xlsx` files are accepted by the Excel inspection tool;
- runtime Excel files in `input/` remain ignored by Git;
- synthetic demo data is stored in `examples/input/sample.xlsx`.

Current validation commands:

```bash
python -m internal_ai_process_assistant.cli "inspect excel sample.xlsx"
pytest
ruff check .
```

This step prepares the project for later Excel cleanup and reporting workflows.
