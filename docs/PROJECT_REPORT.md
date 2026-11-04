# Nexora AI — Complete Project Report

**Project:** Nexora AI / NexoraLM / NexoraGPT  
**Version:** 1.0.0 chat workspace release  
**Report date:** 4 November 2026  
**Prepared for:** Nexora AI project development  
**Status:** Runnable prototype and engineering baseline; not a trained large-scale foundation model.

## Abstract

Nexora AI is designed as a modular AI ecosystem rather than a single chatbot. The project combines a conversational interface, configurable language-model provider, document-grounded question answering, explicit user-managed memory, bounded specialist agents, utility tools, and a separate research implementation of a small decoder-only Transformer. The architecture is intentionally modular so that the local prototype can evolve toward a self-hosted and independently trained model platform.

## 1. Problem statement

A developer building an AI assistant needs more than a model endpoint. The product also requires conversation state, document ingestion, retrieval, safe tool execution, memory controls, application interfaces, deployment, evaluation, and governance. These concerns are often implemented in disconnected prototypes. Nexora AI provides one repository and a common API boundary for the initial ecosystem.

## 2. Objectives

1. Provide a runnable web-based AI workspace.
2. Separate product orchestration from the underlying model provider.
3. Support cloud validation through Gemini and local inference through Ollama.
4. Enable document upload, parsing, chunking, retrieval, and source metadata.
5. Provide explicit create/list/delete controls for saved memory.
6. Add bounded specialist-agent workflows and safe built-in tools.
7. Establish a small, inspectable Transformer training baseline.
8. Include tests, architecture diagrams, documentation, and container deployment.

## 3. Scope and honest implementation status

| Capability | Included status | Notes |
|---|---|---|
| FastAPI application | Implemented | Local development API |
| Browser UI | Implemented | Vanilla HTML/CSS/JS workspace |
| Mock LLM provider | Implemented | Deterministic demonstration only |
| Gemini provider | Implemented | Requires valid Google AI Studio key; text and image request handling |
| Ollama provider | Implemented | Requires running Ollama service; image input needs a vision model |
| Conversation persistence | Implemented | SQLite; searchable list, reopen, and delete in UI |
| Chat attachments | Implemented | PDF/text/code and image uploads; originals stored locally |
| TXT/MD/PDF ingestion | Implemented | PDF text extraction; scanned PDF OCR not included |
| Chunking and lexical retrieval | Implemented | Baseline retrieval, not full production search |
| Optional embedding retrieval | Implemented as optional path | Requires `requirements-embeddings.txt` and configured model |
| User-managed memory | Implemented | Explicit CRUD; simple relevance matching |
| Specialist agents | Implemented | Bounded prompt-based workers; no autonomous external execution |
| Safe calculator/time tools | Implemented | AST allowlist calculator |
| NexoraLM prototype | Implemented | Byte tokenizer and small PyTorch decoder Transformer |
| Large-scale pretraining | Not supplied | Requires licensed corpus and significant compute |
| Voice/audio/video | Roadmap | Not included in this release |
| Multi-tenant account system | Not implemented | Must be added before public SaaS use |

## 4. System overview

The frontend calls a FastAPI gateway. Chat orchestration accepts multipart messages with attachments, loads recent conversation history and relevant prior images, retrieves matching document chunks and saved memories, constructs a bounded prompt, calls Gemini or Ollama through the provider adapter, and persists the completed exchange and local attachment metadata. Document upload extracts text, divides it into overlapping chunks, optionally embeds them, and stores chunk metadata. Specialist agents share the retrieval and provider services but are constrained to generating text; they do not run arbitrary shell commands or perform external actions.

The separate NexoraLM research path contains a byte tokenizer, causal decoder Transformer, next-token training loop, checkpoint writer, and text generation command. It provides a foundation for learning and iteration but is intentionally independent from the web chat provider adapter.

## 5. Technology stack

- Python 3.11+
- FastAPI, Uvicorn, Pydantic, HTTPX
- SQLite for local persistence
- Vanilla HTML, CSS, and JavaScript
- PyTorch for optional model research and training
- pypdf for text-based PDF parsing
- sentence-transformers for optional embedding-based retrieval
- Docker and Docker Compose for packaging

## 6. Key design choices

**Provider abstraction:** the app does not assume a particular model vendor. It uses a provider adapter to support mock mode, Ollama, or other model endpoints.

**Local-first storage:** SQLite makes the prototype easy to run on a laptop. A multi-user production deployment should migrate to PostgreSQL and tenant-scoped records.

**Retrieval grounding:** documents are converted to chunks and returned as source metadata. The current default is lexical retrieval; optional embeddings can improve semantic matching. Retrieval quality must be evaluated on a curated question set before deployment.

**Explicit memory:** users save and delete memories through the UI/API. The starter does not silently create long-term memories from every chat.

**Bounded tools:** calculator input is parsed with Python AST and accepts only arithmetic nodes. The app never evaluates arbitrary code from a user prompt.

## 7. Data flow

1. The user submits a text or multipart chat message with optional file/photo attachments.
2. The API validates files and saves original attachment bytes locally.
3. The API loads up to 16 recent messages and bounded recent image context.
4. Knowledge and memory services retrieve a small number of relevant records.
5. Retrieved content is explicitly framed as untrusted reference material.
6. Gemini or Ollama generates a response through the provider adapter.
7. The completed user/assistant exchange and attachment metadata are stored in SQLite.
8. The response returns with source metadata and attachment URLs.

## 8. Testing and verification

The test suite covers calculator correctness and rejection of arbitrary code, chunk creation, byte-tokenizer round trips, service health, mock chat, document upload, image/file chat attachment persistence, history retrieval/deletion, and mocked Gemini/Ollama provider request construction. Run it with `python -m unittest discover -s tests -v`. The test suite is a baseline; production quality requires broader integration tests, provider contract tests, load tests, retrieval benchmark datasets, security testing, and model evaluations.

## 9. Security, privacy, and limitations

The starter supports an optional shared API-key gate. It does not implement user accounts, tenant isolation, full authorization, distributed rate limiting, malware scanning, production-grade audit trails, or managed secret storage. Use only trusted documents in the prototype. Uploaded content is untrusted and must never be treated as tool instructions. Do not expose a development instance to the public internet with the default settings. A production release needs security review, privacy notices, retention/deletion policies, backup/restore procedures, monitoring, and a proper identity provider.

## 10. Deployment

For local development, install dependencies, copy `.env.example` to `.env`, and run Uvicorn. For containerized use, configure `.env` and run `docker compose up --build`. The Docker Compose file persists the SQLite database in a named volume. A scalable deployment should use a managed database, object storage, an inference service, HTTPS reverse proxy, secrets manager, metrics/logging, and horizontal scaling.

## 11. Future development plan

The next milestones are: (a) audit existing NexoraLM code and reconcile it with this structure; (b) add resumable mixed-precision training and richer tokenizer/data pipelines; (c) establish model and RAG benchmarks; (d) add authentication and tenant boundaries; (e) build coding/research integrations with human approval; (f) add multimodal vision and voice services; and (g) harden deployment and governance before public launch. See `ROADMAP.md` for phased deliverables and exit criteria.

## 12. Conclusion

This repository delivers a coherent starting platform: a functioning local UI/API, selectable model provider, document retrieval, managed memories, bounded agent tasks, safe utility tools, an educational NexoraLM training path, tests, and engineering documentation. It should be treated as the first integrated engineering release. It is not evidence that a large independent model has been trained or that the system is ready for unrestricted public production.
