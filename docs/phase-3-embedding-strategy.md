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

## Completed Step: OpenAI Embedding Provider Placeholder

The project now has a dedicated OpenAI embedding provider placeholder.

Decision:

- OpenAI provider code lives in `openai_embeddings.py`;
- provider selection still happens through `get_embedding_provider`;
- the OpenAI provider stores the configured API key and model name;
- the provider validates empty API keys, empty model names, and empty text input;
- real OpenAI API calls are intentionally not implemented yet.

Reason:

- the project needs a clean provider boundary before adding a real SDK dependency;
- paid API calls should not be introduced accidentally;
- provider configuration can now be tested without network access;
- future OpenAI integration can be implemented inside one dedicated module;
- deterministic embeddings remain the default for local development and tests.

Rejected alternatives for this step:

- installing the OpenAI SDK immediately;
- calling the OpenAI API directly from retrieval code;
- placing OpenAI-specific logic inside the vector retrieval workflow;
- allowing OpenAI provider selection to silently call an external API.

Impact:

- the OpenAI integration path is now explicit;
- tests remain offline and deterministic;
- provider configuration is validated;
- the codebase is ready for a future real OpenAI provider implementation;
- no secrets are committed;
- no OpenAI API calls are made yet.

Current behavior:

- `IAPA_EMBEDDING_PROVIDER=deterministic` keeps using local deterministic embeddings;
- `IAPA_EMBEDDING_PROVIDER=openai` can construct an OpenAI provider placeholder when `OPENAI_API_KEY` is set;
- calling `embed_text()` on the OpenAI provider raises `NotImplementedError`;
- this prevents accidental paid API usage before the implementation is intentionally enabled.

## Completed Step: PDF Vector Retrieval Estimate CLI

The project now exposes PDF vector retrieval usage estimation through the minimal agent and CLI.

Decision:

- add `estimate_pdf_vector_retrieval` as a registered safe tool;
- expose the tool through the controlled executor;
- support the CLI request `estimate vector search for sample.pdf`;
- reuse the same chunk and token guardrails used by vector retrieval;
- return a structured estimate before embeddings are generated.

Reason:

- real embedding providers may create paid API usage;
- users should be able to estimate chunk count, token count, and cost before any embedding run;
- the estimate path should be available through the same safe tool execution model as the rest of the project;
- dry-run behavior improves transparency and supports future human-in-the-loop approvals.

Rejected alternatives for this step:

- estimating cost only inside the vector retrieval implementation;
- requiring a real OpenAI provider before estimating usage;
- hiding cost estimates from the CLI;
- allowing vector retrieval to proceed without a visible pre-flight estimate.

Impact:

- the CLI can now show an embedding usage estimate without creating embeddings;
- guardrails are exercised before retrieval or future API calls;
- the project has a safer path toward paid embedding providers;
- the result is structured and easy to display in future API/UI layers;
- no OpenAI API calls are made.

Supported CLI example:

`python -m internal_ai_process_assistant.cli "estimate vector search for sample.pdf"`

Example result shape:

`status`: `completed`

`tool_name`: `estimate_pdf_vector_retrieval`

`result.filename`: `sample.pdf`

`result.chunk_count`: number of chunks that would be embedded

`result.embedding_model_name`: embedding model used for estimation

`result.estimated_tokens`: estimated input tokens

`result.estimated_cost_usd`: estimated cost as a string

Current demo result:

- filename: `sample.pdf`;
- chunk count: `2`;
- estimated tokens: `105`;
- estimated cost USD: `0.0000021`.

## Completed Step: Explicit Paid Embedding Call Opt-In

The project now requires an explicit runtime opt-in before future paid embedding API calls can run.

Decision:

- add `IAPA_ALLOW_PAID_EMBEDDING_CALLS`;
- default the flag to `false`;
- parse the flag through application config;
- pass the flag into the OpenAI embedding provider placeholder;
- block OpenAI `embed_text()` when paid embedding calls are not explicitly allowed.

Reason:

- selecting the OpenAI provider should not be enough to trigger paid usage;
- API keys can be present in local environments accidentally;
- paid provider calls should require a separate explicit runtime decision;
- the future real OpenAI implementation should inherit this safety model;
- automated tests must remain offline and cost-free.

Rejected alternatives for this step:

- relying only on `OPENAI_API_KEY` presence;
- relying only on `IAPA_EMBEDDING_PROVIDER=openai`;
- adding the safety check later after implementing real API calls;
- allowing provider code to silently proceed toward paid calls.

Impact:

- future OpenAI API calls require two independent opt-ins;
- default local development remains deterministic and offline;
- tests verify that paid calls are blocked by default;
- the OpenAI provider boundary is safer before SDK integration;
- the project has a clearer privacy and cost-control story for portfolio review.

Current behavior:

- `IAPA_ALLOW_PAID_EMBEDDING_CALLS=false` is the default;
- OpenAI provider config can still be constructed for tests;
- calling OpenAI `embed_text()` with paid calls disabled raises `PermissionError`;
- calling OpenAI `embed_text()` with paid calls enabled still raises `NotImplementedError` because real API calls are not implemented yet;
- no OpenAI API calls are made.

## Completed Step: OpenAI Embedding Provider Implementation

The project now has a real OpenAI embedding provider implementation behind the existing provider interface.

Decision:

- add the official OpenAI Python SDK as a pinned dependency;
- implement `OpenAIEmbeddingProvider` using `client.embeddings.create`;
- request embeddings with `encoding_format="float"`;
- convert the OpenAI embedding response into the project-local `EmbeddingVector`;
- keep the OpenAI client injectable for tests;
- keep paid calls blocked unless `IAPA_ALLOW_PAID_EMBEDDING_CALLS=true`.

Reason:

- the project needs real semantic embedding support behind the same interface as deterministic embeddings;
- the OpenAI provider should be isolated inside one module;
- tests must remain offline and cost-free;
- client injection allows reliable unit tests without network access;
- explicit paid-call opt-in protects against accidental API usage.

Rejected alternatives for this step:

- calling OpenAI directly from retrieval code;
- using the OpenAI client globally;
- allowing tests to call the real API;
- relying only on `OPENAI_API_KEY` as the safety mechanism;
- returning raw OpenAI SDK objects instead of project-local `EmbeddingVector` objects.

Impact:

- the codebase can now create real OpenAI embeddings when explicitly configured;
- deterministic embeddings remain the default;
- OpenAI calls still require both provider selection and paid-call opt-in;
- tests verify the provider using a fake injected client;
- the vector retrieval pipeline can later use real semantic embeddings without changing its public result shape.

Current behavior:

- `IAPA_EMBEDDING_PROVIDER=deterministic` remains the safe default;
- `IAPA_EMBEDDING_PROVIDER=openai` selects the OpenAI provider;
- `OPENAI_API_KEY` is required for OpenAI provider configuration;
- `IAPA_ALLOW_PAID_EMBEDDING_CALLS=false` blocks `embed_text()` with `PermissionError`;
- `IAPA_ALLOW_PAID_EMBEDDING_CALLS=true` allows the provider to call its configured client;
- tests use an injected fake client and make no network calls.

Smoke test results:

- with paid calls disabled, OpenAI `embed_text()` is blocked before any API call;
- with paid calls enabled and a fake injected client, the provider sends normalized text, model name, and `encoding_format="float"`;
- the fake embedding response is converted into an `EmbeddingVector`.

## Planned Step: Live OpenAI Embedding Smoke Test

The project is technically ready for a very small live OpenAI embedding smoke test, but the test must remain manual and opt-in.

Decision:

- do not run live OpenAI API calls in automated tests;
- do not require live OpenAI calls for normal development;
- run live embedding tests only manually;
- require `IAPA_EMBEDDING_PROVIDER=openai`;
- require `OPENAI_API_KEY`;
- require `IAPA_ALLOW_PAID_EMBEDDING_CALLS=true`;
- run a tiny single-text embedding request first, before using PDF chunks.

Reason:

- OpenAI API usage is billed separately from ChatGPT Plus;
- live calls introduce network dependency;
- live calls should never happen accidentally in `pytest`;
- a tiny manual smoke test validates credentials and SDK integration with minimal cost;
- the PDF vector retrieval flow already has a dry-run estimator before larger embedding workloads.

Estimated cost:

- the first smoke test should embed only a very short string such as `hello world`;
- estimated token usage should be tiny;
- expected cost should be far below one cent;
- pricing can change, so official OpenAI pricing should be checked before broader usage.

Manual live smoke test prerequisites:

- confirm `git status` is clean;
- confirm `pytest` and `ruff check .` pass;
- create or update local `.env` only, never `.env.example`, with a real API key;
- do not commit `.env`;
- estimate PDF vector retrieval cost before embedding larger files;
- keep `IAPA_MAX_EMBEDDING_CHUNKS_PER_RUN` and `IAPA_MAX_ESTIMATED_EMBEDDING_TOKENS_PER_RUN` conservative.

Manual live smoke test environment:

- `IAPA_EMBEDDING_PROVIDER=openai`;
- `OPENAI_API_KEY=<real local key>`;
- `IAPA_OPENAI_EMBEDDING_MODEL=text-embedding-3-small`;
- `IAPA_ALLOW_PAID_EMBEDDING_CALLS=true`.

Safety checklist:

- `.env` is ignored by Git;
- API key is never printed;
- API key is never committed;
- live smoke test uses one short input first;
- automated tests continue to use fake clients or deterministic embeddings;
- paid provider usage remains explicit and reversible.
