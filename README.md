# Internal AI Process Assistant

A portfolio project for building a practical internal AI assistant for document and data processing workflows.

## Current phase

Phase 1: Minimal agent foundation.

## Environment

- Windows 11 host
- VirtualBox
- Ubuntu Server 26.04 LTS VM
- VS Code Remote SSH
- Git and GitHub
- Python 3.14
- Docker Engine and Docker Compose

## Project foundation

The project currently includes:

- a `src/` Python package layout;
- a local virtual environment workflow;
- pytest for automated tests;
- Ruff for linting;
- Docker installed and verified in the VM;
- GitHub repository synchronization;
- controlled runtime directories: `input/`, `workspace/`, and `output/`;
- a safe file listing tool;
- a safe CSV inspection tool;
- a minimal tool registry;
- a controlled tool executor;
- a minimal rule-based agent;
- a small CLI entry point for local demos.

## Run locally

Activate the virtual environment:

    source .venv/bin/activate

Install the project in editable mode if needed:

    python -m pip install -e .

Run tests:

    pytest

Run linting:

    ruff check .

## Minimal agent CLI demo

The runtime `input/` directory is ignored by Git, except for `.gitkeep`.

Copy the public demo file into the local runtime input directory:

    cp examples/input/sample.csv input/sample.csv

Run the minimal agent to list available files:

    python -m internal_ai_process_assistant.cli "list files in input"

Expected result:

    {
      "status": "completed",
      "message": "Listed files in input.",
      "tool_name": "list_available_files",
      "result": {
        "area": "input",
        "files": [
          {
            "name": "sample.csv",
            "relative_path": "input/sample.csv",
            "size_bytes": 74,
            "is_file": true
          }
        ]
      }
    }

Inspect the demo CSV file:

    python -m internal_ai_process_assistant.cli "inspect csv sample.csv"

Expected result:

    {
      "status": "completed",
      "message": "Inspected CSV file sample.csv.",
      "tool_name": "inspect_csv",
      "result": {
        "filename": "sample.csv",
        "row_count": 3,
        "column_count": 3,
        "columns": [
          "name",
          "department",
          "amount"
        ],
        "missing_values_by_column": {
          "name": 0,
          "department": 0,
          "amount": 0
        }
      }
    }

## Documentation

- [Phase 0 setup](docs/setup-phase-0.md)

## Goal

Build an internal assistant that can process PDF, CSV, and Excel files, call safe Python tools, generate reports, and support controlled human-in-the-loop workflows.
