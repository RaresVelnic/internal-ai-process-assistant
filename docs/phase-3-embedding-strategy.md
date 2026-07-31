# Phase 3: Embedding Strategy

This document records the initial embedding strategy for the Internal AI Process Assistant project.

The project already has a local retrieval foundation:

- controlled PDF text extraction;
- source-aware text chunking;
- local keyword search;
- local PDF retrieval;
- formatted citations.

The next step is to prepare semantic retrieval with embeddings, without introducing unnecessary complexity too early.

## Goal

Add semantic retrieval in a controlled and testable way.

The embedding layer should allow the project to:

- convert document chunks into vectors;
- preserve source metadata for every vector;
- compare semantic retrieval with keyword retrieval;
- keep retrieval results explainable through citations;
- prepare for future LLM-generated answers.

## Non-goals for the first embedding step

The first embedding step should not introduce:

- LangChain;
- LangGraph;
- FastAPI;
- a web UI;
- complex vector database infrastructure;
- background jobs;
- multi-user indexing;
- production deployment;
- automatic LLM answer generation.

## Candidate approaches

### Option 1: API-based embeddings

Use an external embeddings API.

Advantages:

- simple to integrate;
- no local model runtime;
- good quality embeddings;
- closer to real AI integration work.

Tradeoffs:

- requires an API key;
- introduces network dependency;
- may have usage cost;
- tests must avoid real API calls by default.

### Option 2: Local embeddings model

Use a local embedding model.

Advantages:

- no external API key;
- can run offline;
- useful for privacy-oriented architecture discussions.

Tradeoffs:

- extra dependencies;
- larger installation footprint;
- possible CPU performance issues inside the VM;
- more moving parts before the project actually needs them.

### Option 3: Deterministic fake embeddings for infrastructure tests

Use a small deterministic embedding function only for tests and local infrastructure development.

Advantages:

- no API key;
- no network access;
- stable tests;
- lets us design the embedding and vector store interfaces safely.

Tradeoffs:

- not semantic;
- not useful for real retrieval quality;
- must later be replaced or complemented by real embeddings.

## Initial decision

Start with an embedding interface and deterministic fake embeddings for tests.

Reason:

- the project needs stable infrastructure before external AI calls;
- tests should remain fast and deterministic;
- source metadata and vector storage can be designed without depending on a provider;
- real embeddings can be added behind the same interface later.

## Planned first implementation

The first implementation should add:

- an `EmbeddingVector` data structure;
- an `EmbeddedChunk` data structure;
- a deterministic embedding function for tests;
- a function that embeds `DocumentChunk` objects;
- automated tests.

The implementation should not call external APIs.

## Future provider implementation

After the interface is stable, the project can add a real embeddings provider.

The provider decision should consider:

- API cost;
- quality;
- privacy implications;
- ease of setup;
- compatibility with the future vector store;
- portfolio value.

## Security decisions

- no API keys are added in this step;
- no secrets are committed to Git;
- no external API calls happen in tests;
- embeddings preserve source metadata;
- retrieval must continue to return citations.

## Success criteria

This strategy step is complete when:

- the embedding strategy is documented;
- no runtime behavior changes are introduced;
- tests still pass;
- Ruff still passes;
- documentation is committed and pushed.
