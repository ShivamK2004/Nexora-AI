# Nexora AI — System Architecture

## Architecture goals

- Separate the chat experience, orchestration, model inference, and data services.
- Validate the complete app using Gemini and Ollama before developing a native NexoraLM provider.
- Keep user memory explicit and manageable.
- Ground answers in retrieved documents when available.
- Preserve a separate research path for NexoraLM model training.

## High-level components

| Component | Responsibility | Current implementation |
|---|---|---|
| Web UI | Chat, searchable history, file/photo attachments, memories, agent workspace | Static HTML/CSS/JS |
| API gateway | Validation and route dispatch | FastAPI |
| Chat orchestrator | History, attachment context, retrieval, provider call | `routers/chat.py` |
| Provider adapter | Normalized chat interface | mock, Gemini, Ollama |
| Attachment store | Local uploaded originals and file URLs | Files under `data/uploads/` + SQLite metadata |
| Knowledge service | Parse, chunk, index, retrieve | SQLite + lexical/optional embedding score |
| Memory service | Explicit memory CRUD and matching | SQLite |
| Agent service | Choose and run bounded specialist prompt | Five prompt-based workers |
| Tool service | Arithmetic and UTC time | AST allowlist + datetime |
| NexoraLM research | Tokenization, Transformer, train/generate | PyTorch optional |
| Persistence | Conversations, messages, attachments, documents, chunks, memories | SQLite |

## Chat request sequence

1. Accept JSON text chat or multipart text/file/photo chat.
2. Validate file count, extension and size; save originals in the local data folder.
3. Extract readable text from supported document attachments.
4. Load up to 16 recent messages and recent image context.
5. Retrieve up to 4 knowledge chunks and 3 saved memories.
6. Invoke the active provider (mock, Gemini, or Ollama).
7. Persist the completed exchange and return its conversation ID, answer, citations and attachment metadata.

## Retrieval subsystem

Document ingestion accepts text-like files and PDFs with selectable text. Text is normalized and split into overlapping chunks. The default retriever scores token overlap. When an embedding model is configured and `sentence-transformers` is installed, vectors are stored with chunks and combined with lexical relevance. This is an initial hybrid retrieval baseline, not a full BM25/ANN production index.

## Trust boundaries

- Browser input and uploaded files are untrusted.
- Retrieved document text is untrusted reference material and cannot grant permissions.
- External model providers receive the prompt context and image/document data needed for a request.
- Provider keys stay in the backend environment; they must not be committed or returned from API routes.
- The current app is designed for local development and does not yet implement user authentication or multi-tenant data isolation.

## Scaling path

Replace local SQLite with PostgreSQL; add scanned-document OCR and secure object storage; move embeddings to Qdrant/pgvector; add identity/tenant middleware; add rate limits, secrets management, backups, monitoring, and a production security review. Introduce a `nexora` provider that calls the native NexoraLM inference engine when its own trained checkpoint is ready.
