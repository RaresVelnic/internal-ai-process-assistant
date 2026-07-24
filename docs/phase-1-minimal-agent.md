# Phase 1: Minimal Agent Foundation

This document describes the first functional version of the Internal AI Process Assistant.

The goal of Phase 1 is to build a minimal, safe agent foundation before introducing LLMs, LangChain, LangGraph, RAG, FastAPI, or a web interface.

## Current Scope

The current agent is rule-based and deterministic.

It can handle a small set of supported text requests and execute only registered, safe Python tools.

Supported requests:

    list files in input
    list files in workspace
    list files in output
    inspect csv <filename.csv>

Unsupported requests are rejected with a structured response instead of being guessed or executed.

## Architecture

Current request flow:

    CLI request
        -> minimal agent
        -> controlled tool executor
        -> safe tool
        -> structured result

Current modules:

    src/internal_ai_process_assistant/cli.py
    src/internal_ai_process_assistant/minimal_agent.py
    src/internal_ai_process_assistant/tool_executor.py
    src/internal_ai_process_assistant/tool_registry.py
    src/internal_ai_process_assistant/tools/file_listing.py

## Controlled Runtime Directories

The project uses three controlled runtime directories:

    input/
    workspace/
    output/

These directories are part of the project structure, but their runtime contents are ignored by Git.

Only `.gitkeep` files are versioned inside these directories.

Public demo files are stored separately under:

    examples/input/

This keeps real runtime data out of version control while still allowing reproducible demos.

## Implemented Tool: list_available_files

The first safe tool is:

    list_available_files(area, project_root)

It lists direct entries from one controlled project directory.

Allowed areas:

    input
    workspace
    output

The tool does not accept arbitrary filesystem paths.

The tool returns structured data:

    FileListResult
    FileInfo

The result includes:

    area
    file name
    relative path
    size in bytes
    whether the entry is a file

## Implemented Tool: inspect_csv

The second safe tool is:

    inspect_csv(filename, project_root)

It inspects a CSV file located in the controlled `input/` directory.

The tool accepts a simple filename, not an arbitrary path.

It rejects:

    directory paths
    parent directory references
    non-CSV files
    missing files

The tool returns structured data:

    CsvInspectionResult

The result includes:

    filename
    row count
    column count
    column names
    missing values by column

## Tool Registry

The tool registry exposes metadata about available tools.

Current registry function:

    list_tools()

Current registered tools:

    list_available_files
    inspect_csv

The registry returns structured metadata such as tool name, description, and allowed parameter values.

## Tool Executor

The controlled executor is responsible for running tools by name.

Current executor function:

    execute_tool(tool_name, arguments, project_root)

It rejects unsupported tools and missing required arguments.

It does not provide shell access, unrestricted Python execution, or arbitrary filesystem access.

## Minimal Agent

The minimal agent is implemented as:

    run_minimal_agent(request, project_root)

It normalizes request text and supports only explicit safe requests.

If the request is supported, it calls the controlled executor.

If the request is unsupported, it returns:

    unsupported_request

This behavior is intentional. The agent should be predictable and safe before any LLM is introduced.

## CLI Demo

The project includes a small CLI entry point:

    python -m internal_ai_process_assistant.cli "list files in input"

Demo setup:

    cp examples/input/sample.csv input/sample.csv

Run:

    python -m internal_ai_process_assistant.cli "list files in input"

Expected behavior:

    The command returns JSON with status completed and lists sample.csv from the input directory.

Inspect the demo CSV file:

    python -m internal_ai_process_assistant.cli "inspect csv sample.csv"

Expected behavior:

    The command returns JSON with status completed and a structured CSV summary.

## Validation

Run tests:

    pytest

Run linting:

    ruff check .

Current test coverage includes:

    app metadata
    safe file listing
    safe CSV inspection
    tool registry
    controlled tool executor
    minimal rule-based agent
    CLI behavior

## Security Constraints

The current implementation intentionally avoids:

    arbitrary shell execution
    arbitrary Python execution
    unrestricted filesystem access
    recursive filesystem traversal
    LLM-generated tool calls
    automatic file modification
    deletion or overwrite operations

Tools must be explicit, registered, validated, and tested.

## Phase 1 Decisions

### Start with a rule-based agent instead of an LLM agent

Reason: the project should establish safe execution boundaries before adding LLM-based decision making.

Rejected alternative: connecting an LLM immediately.

Impact: the first version is simple but predictable, testable, and safe.

### Use controlled runtime directories

Reason: the assistant should only operate in known project areas.

Rejected alternative: allowing user-provided filesystem paths.

Impact: safer file handling and easier testing.

### Return structured data from tools

Reason: later layers such as APIs, UIs, reports, and LLM summaries can consume structured results reliably.

Rejected alternative: returning only free-form strings.

Impact: slightly more upfront modeling, but better long-term maintainability.

### Separate registry, executor, agent, and tool logic

Reason: each layer has a clear responsibility.

Rejected alternative: putting all logic in one script.

Impact: more files, but cleaner testing and safer future extension.

### Keep runtime data out of Git

Reason: real input/output data may contain sensitive information.

Rejected alternative: committing files directly from input, workspace, or output.

Impact: demo data lives under examples, while runtime data remains local.

## What Is Not Included Yet

Phase 1 does not include:

    LLM integration
    LangChain
    LangGraph
    RAG
    FastAPI
    web UI
    Dockerfile
    PDF or Excel processing
    human-in-the-loop approval flows

These will be introduced incrementally after the minimal tool execution foundation is stable.
