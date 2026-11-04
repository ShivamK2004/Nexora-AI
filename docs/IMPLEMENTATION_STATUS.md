# Implementation Status Matrix

| Area | Present in ZIP | Working in starter | Additional work |
|---|---:|---:|---|
| FastAPI application | Yes | Yes | Production auth/tenant isolation |
| Web workspace | Yes | Yes: ChatGPT-style chat, searchable history, responsive layout | Accessibility, account UX |
| Mock chat provider | Yes | Yes | Not a real language model |
| Ollama provider | Yes | Text chat; image payloads sent to vision-capable models | Provider health checks and streaming |
| Gemini provider | Yes | Text and inline image requests; requires a valid API key | Streaming and file API reuse |
| Conversation history | Yes | Yes: list, search, reopen, delete, SQLite | Per-user access and migrations |
| Chat attachments | Yes | PDF/text/code files plus image uploads; attachment bytes persisted locally | Office/audio/video parsing, OCR, malware scanning |
| Document ingestion | Yes | TXT/MD/CSV/JSON/PY/SQL/PDF text | OCR and large file pipeline |
| Retrieval | Yes | Lexical baseline; optional embeddings | Reranker, ANN index, retrieval evaluation |
| Source metadata | Yes | Yes | Fine-grained page/offset citation fidelity |
| Memory | Yes | Explicit CRUD and matching | Edit/export/expiry/consent workflows |
| Agent framework | Yes | Bounded prompt workers | Tool permissions, approval, job queues |
| Calculator and time tools | Yes | Yes | More tools only with safety review |
| NexoraLM research | Yes | Training/generation code included | Data, compute, pretraining and evaluation |
| Vision input | Yes | Gemini inline images and Ollama base64 images for vision-capable models | Vision evaluation and OCR-specific UX |
| Voice | Roadmap only | No | STT/TTS and real-time audio |
| Coding agent | Prompt worker only | Text suggestions | Repository sandbox and test execution |
| Research agent | Prompt worker only | Text synthesis over local documents | Sourced web research and verification |
| Payments/billing | No | No | Product/business implementation |
| Multi-tenant SaaS | No | No | Identity, authorization, billing, operations |

The matrix is intentionally explicit. A module appearing in the roadmap or product naming does not mean that its full production implementation is included.
