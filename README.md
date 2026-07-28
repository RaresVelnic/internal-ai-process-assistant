# Internal AI Process Assistant

A portfolio project for building a practical internal AI assistant for document and data processing workflows.

The project demonstrates a secure, incremental backend-oriented approach to file processing, tool execution, and AI-ready workflow design.

## Current phase

Phase 2 MVP complete: controlled document processing foundation.

The project does not use an LLM yet. The current agent is intentionally rule-based so that the tool layer, validation model, runtime directories, tests, and documentation are stable before adding RAG or external AI APIs.

## Implemented capabilities

The project currently includes:

- a `src/` Python package layout;
- a local virtual environment workflow;
- pytest for automated tests;
- Ruff for linting;
- Docker installed and verified in the VM;
- GitHub repository synchronization;
- controlled runtime directories: `input/`, `workspace/`, and `output/`;
- shared input file validation;
- safe file listing;
- CSV inspection;
- basic CSV Markdown report generation;
- Excel workbook inspection;
- PDF metadata inspection;
- bounded PDF text extraction;
- a minimal tool registry;
- a controlled tool executor;
- a minimal rule-based agent;
- a small CLI entry point for local demos;
- synthetic demo files for CSV, Excel, and PDF.

## Environment

The local development environment used for the project:

- Windows 11 host;
- VirtualBox;
- Ubuntu Server 26.04 LTS VM;
- VS Code Remote SSH;
- Git and GitHub;
- Python 3.14;
- Docker Engine and Docker Compose.

## Repository structure

```text
src/internal_ai_process_assistant/
  cli.py
  minimal_agent.py
  tool_executor.py
  tool_registry.py
  tools/
    basic_report.py
    csv_inspection.py
    excel_inspection.py
    file_listing.py
    input_file_validation.py
    pdf_inspection.py
    pdf_text_extraction.py

tests/
docs/
examples/input/
input/
workspace/
output/
```

Runtime directories:

- `input/` is used for local files that the tools may read;
- `workspace/` is reserved for intermediate processing data;
- `output/` is used for generated results.

Runtime files are ignored by Git. Public demo files live in `examples/input/`.

## Run locally

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install the project in editable mode if needed:

```bash
python -m pip install -e .
```

Run tests:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

## Prepare demo input files

Copy the public synthetic demo files into the local runtime input directory:

```bash
cp examples/input/sample.csv input/sample.csv
cp examples/input/sample.xlsx input/sample.xlsx
cp examples/input/sample.pdf input/sample.pdf
```

## Minimal agent CLI demo

List files in the controlled input directory:

```bash
python -m internal_ai_process_assistant.cli "list files in input"
```

Validate an input file:

```bash
python -m internal_ai_process_assistant.cli "validate file sample.csv"
```

Inspect the demo CSV file:

```bash
python -m internal_ai_process_assistant.cli "inspect csv sample.csv"
```

Generate a basic Markdown report from the demo CSV file:

```bash
python -m internal_ai_process_assistant.cli "generate report for sample.csv"
```

Inspect the demo Excel workbook:

```bash
python -m internal_ai_process_assistant.cli "inspect excel sample.xlsx"
```

Inspect the demo PDF document:

```bash
python -m internal_ai_process_assistant.cli "inspect pdf sample.pdf"
```

Extract bounded text from the demo PDF document:

```bash
python -m internal_ai_process_assistant.cli "extract pdf text sample.pdf"
```

Generated reports are written to `output/`. Runtime output files are ignored by Git.

## Safety model

The project intentionally uses a limited tool model:

- tools can access only controlled project directories;
- input file tools read from `input/`;
- generated files are written to `output/`;
- arbitrary filesystem paths are rejected;
- nested input paths are rejected;
- unsupported file extensions are rejected;
- tools return structured results;
- no arbitrary shell execution is exposed;
- no unrestricted Python execution is exposed;
- runtime files are not committed to Git.

This safety layer is deliberately implemented before introducing LLM-driven tool selection.

## Not implemented yet

The following features are intentionally deferred to later phases:

- LLM integration;
- RAG;
- embeddings;
- vector database;
- LangChain;
- LangGraph;
- FastAPI;
- web UI;
- OCR;
- human-in-the-loop approvals;
- background jobs;
- deployment.

## Documentation

- [Phase 0 setup](docs/setup-phase-0.md)
- [Phase 1 minimal agent](docs/phase-1-minimal-agent.md)
- [Phase 2 processing plan](docs/phase-2-plan.md)

## Next phase

Phase 3 will introduce the RAG foundation.

The next planned technical step is document text preparation:

- take extracted document text;
- split it into controlled chunks;
- attach source metadata;
- prepare the structure needed for embeddings and semantic search.

No vector database or LLM is required for the first Phase 3 step.

## Goal

Build an internal assistant that can process PDF, CSV, and Excel files, call safe Python tools, generate reports, search over document content, and support controlled human-in-the-loop workflows.
