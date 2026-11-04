# Nexora AI — Detailed System Design

## Backend module boundaries

`main.py` owns app lifecycle, middleware, route registration, and static serving. Routers handle HTTP validation and status codes. Services implement reusable business logic. The database module provides short-lived SQLite connections and schema initialization/migration. This separation keeps provider changes independent from the chat API and frontend.

## Provider contract

`LLMService.chat(messages, system)` accepts normalized role/content messages plus optional image parts and returns assistant text. Supported providers:

- `mock`: deterministic UI/API smoke-test response only.
- `gemini`: Google Gemini `generateContent` REST API, including inline image parts.
- `ollama`: local Ollama `/api/chat` endpoint, including base64 images for vision-capable models.

The active provider is selected by `LLM_PROVIDER`. A future `nexora` provider should load NexoraLM's own tokenizer/checkpoint/inference implementation under the same contract.

## Chat and attachment lifecycle

`Browser -> JSON or multipart request -> Validate message/files -> Save local attachment bytes -> Extract supported document text -> Load recent history and recent image context -> Retrieve knowledge/memory -> Provider adapter -> Persist completed user/assistant exchange -> Return response`.

Supported chat attachments are PDF, TXT, Markdown, CSV, JSON, Python, SQL, PNG, JPG/JPEG, WEBP and GIF. The default per-file limit is 10 MB, combined raw file limit is 14 MB, and images together are limited to 8 MB per message. Document text is kept as private attachment metadata and inserted into provider context; image data is sent to a multimodal provider. User-visible history returns public attachment metadata only. Deleting a conversation removes its referenced attachment bytes.

## Knowledge lifecycle

`Upload -> File-size validation -> Extension allowlist -> Text extraction -> Normalization -> Chunking -> Optional embeddings -> Persistence -> Retrieval`.

The knowledge-base ingestion path indexes selectable PDF text and supported text/code files. The chat attachment path stores the original bytes locally and extracts text for the current conversation. OCR for scanned PDFs, office-file parsing, audio and video are future components.

## Agent execution model

The current orchestrator selects one specialist from a fixed allowlist. The specialist receives a task, a role-specific instruction, and up to three retrieved passages. It produces text and a persisted run record. It does not have shell access, browser automation, unrestricted function calling, or autonomous recursive delegation.

## NexoraLM research model

The model prototype is a decoder-only Transformer with byte IDs, learned token/position embeddings, causal multi-head attention, residual feed-forward blocks, LayerNorm, tied output/token embeddings, and next-token cross-entropy. The trainer samples random fixed-length windows and writes a checkpoint. The generator loads that checkpoint and autoregressively samples tokens. The prototype is not the current chat provider and is not a competitive pretrained assistant.

## API and schema evolution

Use additive API changes where possible. Version breaking external APIs under `/api/v1`. Keep model checkpoints paired with tokenizer/config versions and record training dataset manifests, source licenses, code commit, seed, hardware, and metrics.
