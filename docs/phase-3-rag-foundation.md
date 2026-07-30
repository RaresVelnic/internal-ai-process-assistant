# Phase 3: RAG Foundation

This document defines the incremental plan for Phase 3 of the Internal AI Process Assistant project.

Phase 3 introduces the foundation for Retrieval-Augmented Generation, but it does not start with an LLM, embeddings, or a vector database. The first goal is to prepare document text in a safe, structured, and traceable way.

## Starting point

At the end of Phase 2, the project supports:

- controlled input file validation;
- CSV inspection;
- basic CSV report generation;
- Excel workbook inspection;
- PDF metadata inspection;
- bounded PDF text extraction;
- synthetic demo files for CSV, Excel, and PDF;
- CLI access through the minimal rule-based agent;
- automated tests and documentation.

## Phase 3 Objective

Build a simple, testable RAG foundation.

The project should be able to:

- take extracted document text;
- split text into controlled chunks;
- attach source metadata to each chunk;
- preserve page/source traceability;
- prepare data structures suitable for embeddings and semantic search later.

## First Step: Document Text Chunking

The first implementation step is a standalone text chunking utility.

It should:

- accept text input;
- split text into chunks;
- support a configurable maximum chunk size;
- support a configurable overlap;
- return structured chunk objects;
- include chunk index metadata;
- avoid empty chunks;
- include automated tests.

It should not:

- call an LLM;
- create embeddings;
- use a vector database;
- perform semantic search;
- use LangChain;
- use LangGraph.

## Planned Data Model

A document chunk should contain:

- `text`: the chunk text;
- `chunk_index`: zero-based chunk number;
- `source_filename`: original filename;
- `source_type`: for example `pdf`, `csv`, `excel`, or `text`;
- `page_number`: optional page number when available.

## Security Decisions

- chunking operates only on text already extracted by controlled tools;
- no arbitrary filesystem reads are introduced;
- no external API calls are introduced;
- no runtime files are written by the first chunking utility;
- source metadata must be explicit and structured.

## Rejected for the first Phase 3 step

The following are intentionally deferred:

- OpenAI API integration;
- embeddings;
- vector database;
- RAG answer generation;
- LangChain;
- LangGraph;
- FastAPI;
- document upload endpoints;
- persistent indexing.

## Phase 3 Completion Criteria

Phase 3 MVP will be considered complete when:

- document text can be chunked with metadata;
- extracted PDF text can be transformed into chunks;
- chunks can be searched with a simple local keyword search;
- all new behavior is tested;
- documentation is updated;
- all changes are committed and pushed to GitHub.
