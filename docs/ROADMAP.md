# Nexora AI — Product and Engineering Roadmap

The roadmap is milestone-based, not a guarantee of calendar duration. Completion requires the stated exit criteria and tests.

## Stage 0 — Baseline and repository reconciliation

- [ ] Compare this package with the current `nexora-lm` repository before merging.
- [ ] Preserve existing valuable tokenizer/model/training work.
- [ ] Consolidate package naming, configuration, and documentation.
- [ ] Add CI and reproducible development setup.

**Exit:** one authoritative repository, clean setup from a fresh clone, tests passing.

## Stage 1 — NexoraGPT application hardening

- [x] FastAPI service and static web workspace.
- [x] Model-provider adapter for mock/Gemini/Ollama providers.
- [x] Conversation persistence.
- [ ] Streaming responses and cancellation.
- [ ] User identity, tenant isolation, and account lifecycle.
- [ ] Rate limits, request quotas, and abuse monitoring.

**Exit:** authenticated users can use the chat safely with provider failures handled and measured.

## Stage 2 — Nexora Knowledge

- [x] TXT/Markdown/PDF ingestion.
- [x] Chunking, retrieval, source metadata.
- [x] Optional embedding path.
- [ ] OCR for scanned PDFs and image files.
- [ ] Reranking, metadata filters, incremental re-indexing.
- [ ] Retrieval benchmark and citation faithfulness tests.
- [ ] Tenant-scoped access and deletion verification.

**Exit:** target retrieval metrics are met on a labelled evaluation set; citations are traceable to exact sources.

## Stage 3 — Nexora Memory

- [x] Explicit memory create/list/delete.
- [x] Relevance-based memory retrieval baseline.
- [ ] Memory edit, expiry, export, and audit history.
- [ ] Sensitivity detection and user consent controls.
- [ ] Conflict resolution and memory quality evaluation.

**Exit:** user can inspect, correct, export, and delete all stored memories.

## Stage 4 — Nexora Agents

- [x] Bounded planner/researcher/writer/coder/analyst workers.
- [x] Run persistence and retrieved evidence metadata.
- [ ] Typed tool registry and permission scopes.
- [ ] Human approval for external side effects.
- [ ] Workflow state, retries, timeout, cancellation, audit events.
- [ ] Sandboxed code execution service.

**Exit:** agent tool calls are permissioned, bounded, observable, and safely recoverable.

## Stage 5 — NexoraLM model research

- [x] Byte-level tokenizer prototype.
- [x] Causal Transformer prototype.
- [x] Minimal train and generation scripts.
- [ ] BPE/SentencePiece tokenizer and versioned vocab.
- [ ] Licensed, deduplicated, quality-filtered corpus and manifest.
- [ ] Resumeable checkpoints, AMP, gradient accumulation, eval splits.
- [ ] Experiment tracking, benchmark harness, contamination checks.
- [ ] SFT, LoRA/QLoRA, preference tuning, safety evaluation.
- [ ] Inference optimization, quantization, serving integration.

**Exit:** documented model card, reproducible training, benchmark results, data provenance, and known limitations.

## Stage 6 — Multimodal products

- [ ] Nexora Vision: image/document understanding and visual QA.
- [ ] Nexora Voice: streaming STT/TTS and interruption handling.
- [ ] Nexora Code: repository-aware coding workflows.
- [ ] Nexora Research: sourced multi-step research reports.
- [ ] Nexora Studio: documents, presentations, and data workspace.

**Exit:** each module has a defined evaluation set, product UX, and safety boundary.

## Stage 7 — Production and launch

- [ ] PostgreSQL, object storage, Redis, migrations, backup/restore.
- [ ] Authentication, authorization, tenant isolation.
- [ ] Secrets manager, TLS, security headers, WAF/rate limits.
- [ ] Monitoring, alerting, incident response, disaster recovery.
- [ ] Privacy notice, terms, data retention, deletion workflow.
- [ ] Load, pen, reliability, and cost testing.
- [ ] Beta release, user support, billing, developer API.

**Exit:** launch checklist approved by engineering, security, legal/privacy, and operations owners.
