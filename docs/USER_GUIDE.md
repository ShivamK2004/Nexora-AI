# Nexora AI — User Guide

## Start on Windows

1. Extract the ZIP and open the `Nexora-AI-Complete` directory in PowerShell.
2. Run `start_windows.bat` (or `./start_windows.ps1` from PowerShell).
3. The script creates `.venv`, installs requirements, creates `.env` from `.env.example` when needed, and starts the server.
4. Open `http://127.0.0.1:8000`.

Set `.env` to choose the default provider for browsers that have no saved selection. Each browser can then choose its own provider and model from the chat header.

## Choose an AI provider and model

The chat header has two selectors. First choose a provider, then choose one of its models. Nexora saves this preference in the browser and sends it with each new message.

- **Google Gemini:** add `GEMINI_API_KEY` to `.env` locally or Render → Environment.
- **Anthropic Claude:** add `ANTHROPIC_API_KEY` to `.env` locally or Render → Environment.
- **Ollama:** install and start Ollama. The Ollama base URL must be reachable from the machine/container running Nexora. `localhost` on Render is the Render container, not your Windows computer.
- **Mock:** UI testing only; no real model is called.

For local Ollama text chat:

```powershell
ollama pull llama3:latest
```

For local Ollama vision chat, use a vision-capable model:

```powershell
ollama pull llama3.2-vision
```

Gemini and Claude model IDs shown in the dropdown come from the model catalog in `backend/app/services/models.py`. Access to individual models depends on the provider account. Google currently restricts Gemini 2.5 access for new projects; select a current generally available Gemini 3 Flash model if `gemini-2.5-flash` is unavailable to your key.

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


### API key privacy

Provider API keys are read only by the backend. Never place them in browser JavaScript or commit them to Git. On Render, set them in the service's Environment page. If a key is exposed in a screenshot, chat, or public repository, revoke it and create a replacement.
