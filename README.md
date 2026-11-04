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

## Choose a provider and model

The chat header has two selectors: **AI Provider** and **Model**. Your selected provider/model is saved in this browser and sent with each chat request, so different browser users can choose different models without changing the server-wide environment.

Supported providers:

- **Mock** — interface testing only; it does not call an AI model.
- **Google Gemini** — requires `GEMINI_API_KEY`.
- **Anthropic Claude** — requires `ANTHROPIC_API_KEY`.
- **Ollama** — requires an Ollama server reachable from the Nexora backend; on Render, `localhost` means the Render container, not your PC.

Add provider secrets in your host dashboard (Render → Environment) or in local `.env`:

```dotenv
GEMINI_API_KEY=your_google_ai_studio_key
ANTHROPIC_API_KEY=your_anthropic_key
```

The Claude options use Anthropic's Messages API. Model availability depends on the account and provider. The model list is defined in `backend/app/services/models.py`; add or remove IDs there when provider model availability changes.

Gemini model choices include `gemini-3.8-flash` and `gemini-2.5-flash`. Google currently notes that access to Gemini 2.5 models is restricted for new projects, so use the latest generally available Gemini Flash choice if your account cannot access 2.5.

Claude choices include `claude-haiku-5-5`, `claude-sonnet-5-5`, and `claude-opus-5-5`. See the providers' official model catalogs before selecting a model for production.

The model selection is included in each chat request. Chat history, attachments, retrieval and the web UI remain independent of the chosen provider.

## License

MIT. Review third-party package, model, and dataset licenses independently before redistribution.


## Documents and images

PDF attachments with selectable text are extracted locally and included in the model prompt. Scanned/image-only PDF files need OCR before their contents can be summarized. Claude, Gemini and vision-capable Ollama models can receive supported image attachments.

### Multi-model selector (v1.0)

The chat header includes separate provider and model selectors. The chosen provider/model is saved in browser local storage and sent with each message. Server-side API keys remain in the backend environment and are never sent to the browser.
