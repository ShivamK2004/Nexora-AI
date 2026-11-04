# Nexora AI — Chat Workspace + NexoraLM Research Starter

Nexora AI is a local-first assistant workspace that lets you test the complete chat application flow with **Gemini or Ollama first**, while keeping the backend provider interface replaceable by your own **NexoraLM** model later.

This version is a testable product shell and model-development starter. It does not claim to be a trained foundation model. Gemini and Ollama are temporary providers for validating the app experience; they are not part of NexoraLM's eventual weights or training pipeline.

## What is included

- ChatGPT-style responsive web interface with new chats, searchable chat history, reopen/delete conversations, and a message composer.
- Upload up to five files per message; supports PDF, TXT, Markdown, CSV, JSON, Python, SQL, PNG, JPG/JPEG, WEBP, and GIF.
- Image previews, drag-and-drop, and clipboard image paste.
- SQLite persistence for conversations, messages, file metadata, knowledge documents, memories, and agent runs.
- Gemini native REST provider and Ollama `/api/chat` provider, selected using the `LLM_PROVIDER` environment variable.
- Text extraction from supported documents and local knowledge-base retrieval.
- Explicit user-managed memory and bounded text agents.
- A small byte-level decoder-only Transformer research prototype and training scripts under `model/nexora_lm/`.
- Unit/API tests, Windows launch scripts, Docker setup, API reference, and design documentation.

## Quick start — Windows

1. Extract `Nexora-AI-Complete.zip` and open the extracted `Nexora-AI-Complete` folder.
2. Copy `.env.example` to `.env` and edit `.env` with your provider choice and key.
3. Double-click `start_windows.bat`, or run `./start_windows.ps1` in PowerShell.
4. Open <http://127.0.0.1:8000>.

On first run, you can also start the script without `.env`; it creates `.env` with safe mock-mode defaults. Stop the server with Ctrl+C, edit `.env`, and run the script again to switch providers.

The script creates a virtual environment, installs dependencies, and starts Uvicorn. It does not require you to activate the environment manually.

### Manual start

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload
```

## Select Gemini

In `.env`:

```dotenv
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_google_ai_studio_key
GEMINI_MODEL=gemini-3.8-flash
```

Restart Nexora after changing `.env`. The Gemini key is only read by the backend and is not sent to frontend JavaScript. The Gemini API supports image input; this implementation sends images as inline image data.

## Select Ollama

Install Ollama and make sure its local service is running. For text-only chat:

```powershell
ollama pull llama3:latest
```

Then use:

```dotenv
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:latest
OLLAMA_TIMEOUT_SECONDS=120
```

For image understanding, use a vision-capable Ollama model. For example:

```powershell
ollama pull llama3.2-vision
```

Then set `OLLAMA_MODEL=llama3.2-vision`. A text-only model such as `llama3:latest` cannot understand attached photos; the backend will still forward the image payload, but the selected model must support vision.

## Switch provider

Set exactly one active provider in `.env`:

- `LLM_PROVIDER=mock` — deterministic local demo; no generated AI output.
- `LLM_PROVIDER=gemini` — Gemini API, requires `GEMINI_API_KEY`.
- `LLM_PROVIDER=ollama` — local Ollama server and selected model.

The app reads the settings at server startup, so restart Uvicorn after changing provider/model settings.

## User data and attachments

The default sample database URL is `sqlite:///data/agent_harness.db`. Chat history and uploaded files are stored locally under `data/`. The `.gitignore` excludes `.env`, virtual environments, and local data. Deleting a conversation also deletes the attachment files referenced by that conversation.

When Gemini is active, prompts, relevant chat context, and attached images/documents are sent to Google's API. When Ollama is active, the payload is sent to the configured local Ollama server. Review provider data practices before using private information. Scanned PDF OCR, office documents, audio/video, authentication, and production multi-user isolation are not included in this starter.

## Run tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Project layout

```text
backend/app/       FastAPI routes, settings, SQLite, LLM provider adapters
frontend/          Nexora web UI
model/nexora_lm/   Byte tokenizer, Transformer, training and generation prototype
scripts/           Dataset preparation and smoke checks
datasets/          Sample corpus and knowledge document
docs/              User, API, training, architecture, and security guides
tests/             API, core, and provider tests
```

## Later: replace Gemini/Ollama with NexoraLM

The chat route calls one provider service through a stable `chat(messages, system)` contract. Once NexoraLM has a usable checkpoint and inference engine, implement a native `nexora` provider in `backend/app/services/llm.py`, load your own checkpoint/tokenizer, and add `nexora` as an allowed provider. This keeps chat history, file upload, retrieval, UI, and database independent from whichever model generates the answer.

The included small byte-level Transformer is an educational pipeline smoke test—not a competitive assistant. Train it on a larger, licensed corpus, evaluate it, and build instruction tuning before routing everyday chats to it.

## License

MIT. Review third-party package, model, and dataset licenses independently before redistribution.


## Switching AI providers

Use the **AI PROVIDER** selector in the top-right of the web app. Choose **Google Gemini** or **Ollama local**; Nexora saves the selection to the project `.env` file and applies it immediately. `Mock` is only a test mode and does not generate AI answers. For Gemini, set `GEMINI_API_KEY` in `.env`. For Ollama, start the Ollama app and ensure the value in `OLLAMA_MODEL` is installed (`ollama list`).

PDF attachments with selectable text are extracted locally and included in the model prompt. Scanned/image-only PDF files need OCR before their contents can be summarized.
