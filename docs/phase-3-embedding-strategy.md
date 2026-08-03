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

## Completed Implementation

The initial embedding strategy has now been implemented.

Implemented components:

- `EmbeddingVector`;
- `EmbeddedChunk`;
- deterministic embedding generation;
- chunk embedding conversion;
- in-memory vector storage;
- cosine similarity search;
- local PDF vector retrieval;
- tool registry and executor integration;
- minimal agent and CLI integration;
- automated tests for the embedding and vector retrieval path.

The implemented workflow is:

1. Extract bounded text from a controlled PDF input file.
2. Split extracted text into source-aware chunks.
3. Convert chunks into deterministic embedding vectors.
4. Store embedded chunks in an in-memory vector store.
5. Embed the user query with the same deterministic function.
6. Rank chunks by cosine similarity.
7. Return structured matches with source citations.

This confirms that the retrieval pipeline can operate end-to-end before introducing real semantic embeddings.

## Current Limitation

The current embedding implementation is deterministic, but not semantic.

It is useful for testing:

- data structures;
- metadata preservation;
- vector storage;
- similarity ranking;
- source citations;
- CLI and tool integration.

It is not useful for judging real semantic retrieval quality.

The deterministic embedding function does not understand synonyms, paraphrases, intent, or domain meaning. A future real embedding provider is required before the project can claim semantic search quality.

## Updated Decision

The project will keep deterministic embeddings as the default test provider.

Reason:

- tests remain offline;
- test results remain stable;
- no secrets are needed;
- no provider-specific code is forced into the core retrieval pipeline;
- the architecture can later support a real provider behind the same interface.

Future work should add a real embedding provider without removing deterministic embeddings, because deterministic embeddings remain valuable for fast infrastructure tests.

## Next Step

The next embedding-related step is to choose and implement a real embedding provider.

The first real provider should be selected based on:

- low setup friction;
- clear pricing or free tier;
- good documentation;
- reasonable privacy posture;
- compatibility with the existing `EmbeddingVector` and `EmbeddedChunk` structures;
- portfolio value for applied AI and backend roles.

The project should still avoid LLM-generated answers until semantic retrieval quality can be tested independently.

## Provider Decision: OpenAI Embeddings With Cost Guardrails

The first real embedding provider will be OpenAI `text-embedding-3-small`.

This provider is selected as the primary candidate for the first real semantic retrieval implementation.

Reasons:

- it has strong portfolio value for applied AI and backend roles;
- it is simple to integrate through a standard API workflow;
- it is suitable for semantic search and RAG foundations;
- it can replace the deterministic embedding provider behind the existing embedding interface;
- the current listed price is low enough for small synthetic demo workloads.

Important billing note:

- ChatGPT Plus does not include OpenAI API usage.
- OpenAI API usage is billed separately through the OpenAI Platform.
- The project must treat API usage as paid usage even if the developer has a ChatGPT Plus subscription.

Current pricing note:

- As of 2026-08-03, OpenAI lists `text-embedding-3-small` at `$0.02` per 1 million input tokens.
- Pricing can change, so implementation documentation should point to the official OpenAI pricing/model page rather than hard-coding assumptions in the code.

Approximate cost examples at `$0.02` per 1 million tokens:

- 100,000 tokens: about `$0.002`;
- 1,000,000 tokens: about `$0.02`;
- 10,000,000 tokens: about `$0.20`;
- 100,000,000 tokens: about `$2.00`.

The expected cost for the current demo project should be very small because the project uses tiny synthetic files. The main financial risk is not normal usage. The main risk is accidental repeated indexing, large files, or an uncontrolled loop.

## Cost Safety Policy

Real embedding API usage must be opt-in.

The project should enforce these rules before making real API calls:

- deterministic embeddings remain the default provider for tests;
- automated tests must not call the OpenAI API;
- OpenAI embeddings may run only when `OPENAI_API_KEY` is explicitly configured;
- real embeddings should require an explicit provider selection;
- no full-folder auto-indexing should happen by default;
- each run should limit the number of chunks sent to the provider;
- each run should estimate token usage before making API calls;
- each run should estimate cost before making API calls;
- large inputs should be rejected or require explicit confirmation in a later human-in-the-loop phase;
- retry behavior must be limited;
- API keys must never be committed to Git;
- API keys must never be printed in logs;
- API usage should be documented as paid usage.

Recommended initial limits:

- maximum chunks per embedding run: 20;
- maximum estimated input tokens per run: 20,000;
- default provider: deterministic;
- real provider: OpenAI only when explicitly selected.

At the current listed price, 20,000 tokens would cost roughly `$0.0004` with `text-embedding-3-small`.

## Rejected Provider Options For Now

Google Gemini free tier is rejected for this project stage.

Reason:

- the free tier may allow provider-side data use for product improvement;
- the project is security- and privacy-oriented;
- even though the current demo files are synthetic, the portfolio story should stay conservative.

Cohere, Voyage AI, Jina AI, and Hugging Face are deferred.

Reason:

- they may be useful later;
- some have generous free tiers or interesting search tooling;
- however, they introduce extra provider research and unfamiliar billing models;
- the current project benefits more from a conservative, widely recognized first provider.

## Updated Implementation Direction

The next implementation step is not to call the OpenAI API directly.

The next implementation step is to introduce an embedding provider abstraction.

The provider abstraction should support:

- deterministic embeddings for tests and offline development;
- OpenAI embeddings as a future opt-in provider;
- shared return types based on `EmbeddingVector`;
- consistent source metadata through `EmbeddedChunk`;
- cost estimation before paid provider calls.

This keeps the retrieval pipeline stable while allowing the real embedding provider to be added safely later.

## Completed Implementation: Embedding Usage Guardrails

The PDF vector retrieval workflow now applies embedding usage guardrails before generating embeddings.

Implemented behavior:

- extracted PDF chunks are counted before embedding;
- estimated token usage is calculated before embedding;
- estimated embedding cost is calculated before embedding;
- requests can be rejected if they exceed the configured chunk limit;
- requests can be rejected if they exceed the configured estimated token limit;
- the CLI response includes the embedding model name;
- the CLI response includes estimated token usage;
- the CLI response includes estimated cost in USD.

Current default limits:

- maximum chunks per embedding run: 20;
- maximum estimated input tokens per run: 20,000;
- default pricing reference: OpenAI `text-embedding-3-small`.

The cost estimate is informational for the deterministic provider, because deterministic embeddings do not call an external API.

The same guardrails are intentionally applied now so that a future OpenAI embedding provider can use the existing safety layer instead of adding cost control later.

Example CLI result fields:

- `embedding_model_name`;
- `estimated_tokens`;
- `estimated_cost_usd`.

This keeps the retrieval workflow transparent and prepares the project for paid embedding providers without making real API calls yet.

## Completed Implementation: Runtime Embedding Configuration

The embedding safety settings are now connected to the runtime workflow.

Implemented behavior:

- `.env.example` documents embedding-related configuration;
- `.env` remains ignored by Git;
- the default embedding provider is `deterministic`;
- the `openai` provider option requires `OPENAI_API_KEY`;
- the CLI loads runtime config before running the minimal agent;
- the minimal agent accepts optional runtime config;
- PDF vector retrieval receives configured embedding usage limits;
- the tool executor validates optional vector retrieval limit arguments;
- automated tests verify safe defaults and config error handling.

Current configuration variables:

- `IAPA_EMBEDDING_PROVIDER`;
- `OPENAI_API_KEY`;
- `IAPA_OPENAI_EMBEDDING_MODEL`;
- `IAPA_MAX_EMBEDDING_CHUNKS_PER_RUN`;
- `IAPA_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN`.

Security impact:

- real API usage remains opt-in;
- missing OpenAI API keys fail fast when the OpenAI provider is selected;
- deterministic embeddings remain safe for tests and local development;
- cost guardrails can be changed without editing code;
- no secrets are committed to Git;
- no OpenAI API calls are made yet.

This prepares the project for a future OpenAI embedding provider while keeping the current runtime offline and controlled.

## Completed Step: Embedding Provider Factory

The project now has a central embedding provider factory.

Decision:

- provider selection is handled by `get_embedding_provider`;
- `deterministic` returns the local deterministic embedding provider;
- `openai` is recognized as a valid configured provider;
- `openai` intentionally raises `NotImplementedError` until the real provider is implemented;
- PDF vector retrieval now receives its embedding provider through configuration.

Reason:

- provider selection should live in one place;
- tests and local development must remain deterministic by default;
- OpenAI integration should be opt-in and explicit;
- the project should not make paid API calls before the provider implementation and safety checks are ready;
- future providers can be added behind the same interface.

Rejected alternatives for this step:

- calling OpenAI directly from the PDF retrieval workflow;
- hardcoding provider selection inside vector retrieval;
- introducing LangChain provider abstractions too early;
- adding a real API dependency before the internal provider boundary is stable.

Impact:

- the vector retrieval workflow is now provider-aware;
- deterministic embeddings remain the default;
- OpenAI is prepared as a future provider but cannot run accidentally;
- the architecture is easier to test and extend;
- cost and privacy guardrails remain intact.

Current behavior:

- `IAPA_EMBEDDING_PROVIDER=deterministic` works for local vector retrieval;
- `IAPA_EMBEDDING_PROVIDER=openai` requires `OPENAI_API_KEY`;
- after config loads successfully, OpenAI provider selection still fails intentionally with `NotImplementedError`;
- no OpenAI API calls are made yet.
