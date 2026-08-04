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

## Completed Step: Text Chunking Utility

The project now includes a standalone text chunking utility for the RAG foundation.

The chunking flow is:

```text
text input
-> chunk_text
-> DocumentChunk[]
```

Each chunk includes:

- chunk text;
- zero-based chunk index;
- source filename;
- source type;
- optional page number.

Implementation notes:

- chunk size is configurable;
- chunk overlap is configurable;
- blank input returns an empty chunk list;
- invalid chunk limits are rejected;
- no filesystem access is performed;
- no external API calls are performed.

## Completed Step: PDF Text Chunking Utility

The project now connects controlled PDF text extraction to document chunking.

The PDF chunking flow is:

```text
PDF filename
-> extract_pdf_text
-> page text
-> chunk_text
-> source-aware PDF chunks
```

Implementation notes:

- PDF files are still read only from the controlled `input/` directory;
- PDF text extraction remains bounded;
- chunks preserve the source filename;
- chunks preserve `source_type="pdf"`;
- chunks preserve page numbers;
- chunk indexes are normalized across the full PDF.

## Completed Step: Local Keyword Search Over Chunks

The project now includes a simple local retrieval utility.

The keyword search flow is:

```text
DocumentChunk[]
-> search_chunks_by_keyword
-> ChunkSearchResult[]
```

Search behavior:

- case-insensitive matching;
- blank queries return no results;
- results include match counts;
- results preserve full source metadata;
- results are sorted by match count, then chunk index.

This is not semantic search yet. It is a deterministic retrieval baseline used before embeddings and vector search.

## Completed Step: Local PDF Retrieval Workflow

The project now supports local keyword retrieval over controlled PDF files.

The local PDF retrieval flow is:

```text
PDF filename + query
-> chunk_pdf_text
-> search_chunks_by_keyword
-> source-aware retrieval matches
```

The workflow is available internally as:

```python
search_pdf_text(filename, query, project_root)
```

It is also exposed through the minimal agent CLI:

```bash
python -m internal_ai_process_assistant.cli "search pdf sample.pdf for assistant"
```

Expected structured result shape:

```json
{
  "status": "completed",
  "message": "Searched PDF file sample.pdf for \"assistant\".",
  "tool_name": "search_pdf_text",
  "result": {
    "filename": "sample.pdf",
    "query": "assistant",
    "match_count": 1,
    "matches": [
      {
        "chunk": {
          "text": "Internal AI Process Assistant...",
          "chunk_index": 0,
          "source_filename": "sample.pdf",
          "source_type": "pdf",
          "page_number": 1
        },
        "match_count": 2
      }
    ]
  }
}
```

Security decisions:

- retrieval uses only text extracted by controlled PDF tools;
- no arbitrary filesystem reads are introduced;
- no external API calls are introduced;
- no embeddings are created yet;
- no vector database is used yet;
- source metadata is returned with each match.

### Current Phase 3 Status

Completed:

- document text chunking;
- PDF text chunking;
- local keyword search;
- local PDF keyword retrieval;
- retrieval citation formatting;
- deterministic embedding utilities;
- in-memory vector store;
- local PDF vector retrieval workflow;
- embedding provider abstraction;
- embedding provider factory;
- OpenAI embedding provider placeholder;
- embedding usage and cost guardrails;
- PDF vector retrieval dry-run estimate;
- PDF vector retrieval estimate tool;
- minimal agent and CLI integration;
- README and Phase 3 documentation updates.

Not implemented yet:

- real OpenAI embedding API calls;
- real semantic embeddings;
- persistent vector store;
- hybrid keyword/vector retrieval;
- LLM answer generation;
- LangChain;
- LangGraph.

## Completed Step: Retrieval Citation Formatting

The project now includes citation formatting for retrieval results.

Citation formatting converts technical chunk metadata into human-readable source references.

Example citation:

```text
sample.pdf, page 1, chunk 0
```

The citation flow is:

```text
DocumentChunk
-> format_chunk_citation
-> human-readable citation
```

For retrieval results:

```text
ChunkSearchResult[]
-> format_search_result_citations
-> citation list
```

Implementation notes:

- citations include the source filename;
- citations include the page number when available;
- citations include the chunk index;
- citations do not require filesystem access;
- citations do not require external API calls;
- citations are deterministic and testable.

The local PDF retrieval workflow now returns both technical matches and formatted citations.

Updated structured result shape:

```json
{
  "filename": "sample.pdf",
  "query": "assistant",
  "match_count": 1,
  "matches": [
    {
      "chunk": {
        "text": "Internal AI Process Assistant...",
        "chunk_index": 0,
        "source_filename": "sample.pdf",
        "source_type": "pdf",
        "page_number": 1
      },
      "match_count": 2
    }
  ],
  "citations": [
    "sample.pdf, page 1, chunk 0"
  ]
}
```

Why this matters:

- humans can see where a result came from;
- a future UI can display compact source references;
- a future LLM can use citations when generating answers;
- retrieval stays explainable before semantic search is introduced.

## Completed Step: Deterministic Vector Retrieval

The project now has a complete local vector retrieval workflow using deterministic embeddings.

The workflow is:

```text
User request
-> CLI
-> minimal rule-based agent
-> controlled tool executor
-> search_pdf_by_vector
-> PDF text extraction
-> source-aware chunking
-> deterministic embeddings
-> in-memory vector store
-> cosine similarity search
-> ranked matches with citations
```

Supported CLI example:

```bash
python -m internal_ai_process_assistant.cli "search pdf sample.pdf by vector for privacy"
```

Expected structured result shape:

```json
{
  "status": "completed",
  "message": "Searched PDF file sample.pdf by vector for \"privacy\".",
  "tool_name": "search_pdf_by_vector",
  "result": {
    "filename": "sample.pdf",
    "query": "privacy",
    "match_count": 2,
    "matches": [
      {
        "text": "...",
        "score": 0.0881160196684866,
        "citation": "sample.pdf, page 2, chunk 1",
        "chunk_index": 1,
        "source_filename": "sample.pdf",
        "page_number": 2
      }
    ]
  }
}
```

### Architecture Decision: Deterministic Embeddings First

Decision:

- use deterministic embeddings for the first vector retrieval pipeline;
- keep the embedding interface independent from any external provider;
- store embedded chunks in a simple in-memory vector store;
- use cosine similarity for local vector search.

Reason:

- tests remain fast, stable, and offline;
- no API key is required;
- no external API calls are introduced;
- no local model dependency is introduced yet;
- the project can validate the retrieval architecture before paying the complexity cost of real embeddings.

Rejected alternatives for this step:

- OpenAI or other API embeddings;
- local transformer embedding models;
- vector databases such as Chroma, Qdrant, or FAISS;
- LangChain abstractions;
- LLM-generated answers.

Impact:

- the retrieval pipeline is now structurally realistic;
- source citations remain attached to retrieval results;
- the vector search behavior is not semantically meaningful yet;
- deterministic vector rankings may look unintuitive for natural-language queries;
- real embeddings can later replace the deterministic provider behind the same interface.

### How the Current Embedding Model Works

The current embedding implementation is deterministic and intentionally simple.

It works by:

- normalizing text with case folding and whitespace cleanup;
- splitting the normalized text into tokens;
- hashing each token into one of a fixed number of vector dimensions;
- adding a deterministic token weight to that dimension;
- normalizing the final vector to unit length.

This creates stable vectors for the same input text. For example, these inputs produce the same vector:

```text
"Internal assistant"
"  internal   assistant  "
```

The current model is useful because it lets the project test:

- embedding data structures;
- chunk-to-vector conversion;
- vector storage;
- cosine similarity search;
- ranking behavior;
- source metadata preservation;
- citations attached to retrieved chunks;
- CLI and tool integration.

The current model is not a real semantic embedding model.

It does not understand:

- meaning;
- synonyms;
- paraphrases;
- context;
- domain concepts;
- semantic similarity.

For example, a real embedding model should understand that these are related:

```text
"privacy policy"
"data protection rules"
```

The deterministic model does not reliably understand that relationship. It only creates repeatable numeric vectors from token hashes.

### How the Current Vector Store Works

The current vector store is an in-memory store.

It works by:

- accepting `EmbeddedChunk` objects;
- keeping them in a Python list;
- embedding the query with the same deterministic embedding function;
- comparing the query vector with each stored chunk vector;
- ranking results by cosine similarity;
- returning the highest-scoring matches.

Cosine similarity measures whether two vectors point in a similar direction.

In this project, each vector search result keeps:

- the original chunk text;
- the similarity score;
- the source filename;
- the page number when available;
- the chunk index;
- the formatted citation.

This keeps retrieval explainable and traceable even before LLM-generated answers are introduced.

### Why This Is Still Useful Without Real Semantic Embeddings

This step validates the retrieval architecture without adding provider complexity too early.

The project can now prove that the following pipeline works end-to-end:

```text
controlled input file
-> extracted text
-> source-aware chunks
-> embeddings
-> vector storage
-> vector search
-> ranked matches
-> citations
-> CLI response
```

Later, a real embedding provider can replace only the embedding function.

The rest of the pipeline should remain mostly stable:

- chunk metadata;
- embedded chunk structure;
- vector store interface;
- retrieval result shape;
- citation formatting;
- tests around source traceability.

### Security Decisions

- PDF input still comes only from the controlled `input/` directory;
- file validation still rejects arbitrary paths and unsupported input types;
- no secrets are required;
- no network calls are made;
- runtime files remain ignored by Git;
- retrieval results preserve source filename, page number, chunk index, and citation text.

### Current Phase 3 Status

Completed:

- document text chunking;
- PDF text chunking;
- local keyword search;
- local PDF keyword retrieval;
- retrieval citation formatting;
- deterministic embedding utilities;
- in-memory vector store;
- local PDF vector retrieval workflow;
- tool registry and executor integration;
- minimal agent and CLI integration.

Not implemented yet:

- real semantic embeddings;
- persistent vector store;
- hybrid keyword/vector retrieval;
- LLM answer generation;
- LangChain;
- LangGraph.
