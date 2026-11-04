# Nexora AI API Reference

Base URL: `http://127.0.0.1:8000`. OpenAPI docs: `/docs`.

If `API_KEY` is set, pass `X-Nexora-Key: <key>` on API requests.

## System

- `GET /api/health` — service status, active provider/model, and whether Gemini has a key configured (the key itself is never returned).
- `GET /api/models` — supported providers and configured model name.

## Chat and history

`POST /api/chat` accepts JSON for text-only chat:

```json
{"message":"Explain RAG","conversation_id":null}
```

It also accepts `multipart/form-data` with fields `message`, optional `conversation_id`, and repeated `files` fields for attachments. The response includes `conversation_id`, `answer`, `provider`, `model`, `citations`, and attachment metadata.

- `GET /api/conversations` — list recent conversations.
- `GET /api/conversations/{conversation_id}` — get messages and public attachment metadata.
- `DELETE /api/conversations/{conversation_id}` — delete a conversation and its stored chat attachments.
- `GET /api/attachments/{attachment_id}` — retrieve an attachment belonging to a saved chat.

Chat attachment formats: PDF, TXT, Markdown, CSV, JSON, Python, SQL, PNG, JPG/JPEG, WEBP, GIF. Up to five attachments per message; default per-file maximum is 10 MB, combined raw upload maximum is 14 MB, and combined image raw bytes are limited to 8 MB per message.

## Knowledge base

- `POST /api/documents` — multipart upload field `file`.
- `GET /api/documents` — list indexed document metadata.
- `DELETE /api/documents/{document_id}` — delete a document and its chunks.

Supported document extensions: `.txt`, `.md`, `.markdown`, `.csv`, `.json`, `.py`, `.sql`, `.pdf`.

## Memory

- `POST /api/memories` — JSON `{ "content": "...", "category": "preference" }`.
- `GET /api/memories` — list saved memories.
- `DELETE /api/memories/{memory_id}` — delete memory.

## Agents

- `GET /api/agents` — list worker IDs and descriptions.
- `POST /api/agents/run` — JSON `{ "task": "...", "agent": "planner" }`.

## Tools

- `POST /api/tools/calculate` — JSON `{ "expression": "(25 + 5) * 2" }`.
- `GET /api/tools/time` — UTC timestamp.

## Errors

- `400`: invalid upload or request data.
- `401`: configured API key missing/invalid.
- `404`: requested resource not found.
- `503`: model provider unavailable or misconfigured.
