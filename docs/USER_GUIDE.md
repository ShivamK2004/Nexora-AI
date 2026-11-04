# Nexora AI — User Guide

## Start on Windows

1. Extract the ZIP and open the `Nexora-AI-Complete` directory in PowerShell.
2. Run `start_windows.bat` (or `./start_windows.ps1` from PowerShell).
3. The script creates `.venv`, installs requirements, creates `.env` from `.env.example` when needed, and starts the server.
4. Open `http://127.0.0.1:8000`.

Edit `.env` before launching to select a provider. Only one provider is active per server process.

## Select Gemini

Set `LLM_PROVIDER=gemini`, put a valid Google AI Studio key in `GEMINI_API_KEY`, and set `GEMINI_MODEL=gemini-3.8-flash` (or another model available to your key). Restart the server after editing `.env`.

Gemini requests go directly from the Nexora backend to Google's Generative Language API. The key stays in the backend environment and is never sent to browser JavaScript.

## Select Ollama

Install and start Ollama, pull a local model, and set `LLM_PROVIDER=ollama`. Example for text chat:

```powershell
ollama pull llama3:latest
```

Then set:

```dotenv
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:latest
```

For image understanding, use an Ollama vision model instead of a text-only model. For example:

```powershell
ollama pull llama3.2-vision
```

Then set `OLLAMA_MODEL=llama3.2-vision`. Image support depends on the model; the ordinary `llama3:latest` model is not a vision model.

## Chat and history

Use **New chat** to start a separate conversation. Past chats are shown in the left sidebar; select one to reopen it. Use the search box to filter chats. The delete icon removes a conversation and the uploaded attachment files belonging to it.

## Attach files and photos

Use the plus button beside the message box, drag files onto the chat area, or paste an image from the clipboard. Up to five attachments can be sent with a message. Supported formats are PDF, TXT, Markdown, CSV, JSON, Python, SQL, PNG, JPG/JPEG, WEBP and GIF. The default per-file limit is 10 MB and total chat attachments are limited to 14 MB. Text is extracted from supported documents and supplied as context; images are sent to a multimodal provider when supported.

PDF support extracts selectable text. Scanned PDFs that contain only page images need OCR and are not parsed as text in this version. Office formats, audio, and video are not included yet.

## Knowledge base

Open Knowledge base and index a document to make its chunks searchable in later chats. This is separate from attaching a document to one message. Nexora retrieves relevant passages and provides source labels where available.

## Memory and agents

Memory lets you save notes explicitly. Agents provide bounded researcher, writer, coder, analyst, and planner workflows; they do not execute arbitrary shell commands or take external actions.

## Privacy and API keys

Chat history, document indexes, and uploaded chat attachments are stored locally in the configured SQLite/data directory. When Gemini is selected, user prompts, retrieved context, and uploaded files/images used in the request are sent to Google's API. With Ollama, the request is sent to the configured local Ollama server. Do not upload sensitive content unless you understand the provider and local machine access.

Never paste a real API key into source code or commit it to Git. Keep it in `.env`; `.gitignore` excludes that file.


### Change the active AI provider

Use the **AI PROVIDER** dropdown in the header. The selection is written to `.env` and applies immediately: `Mock` does not call a model, `Google Gemini` uses `GEMINI_API_KEY`, and `Ollama local` calls the local Ollama server. If Gemini is selected without a key, add `GEMINI_API_KEY` to `.env`. PDF text is extracted locally and sent to the selected provider; image-only scanned PDFs are not OCR'd by this starter.
