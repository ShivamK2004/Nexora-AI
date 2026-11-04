# Local deployment notes

For development on Windows, run `start_windows.bat` or `start_windows.ps1`. The app listens on `127.0.0.1:8000` by default. Do not expose the development server directly to the public internet.

## Configuration

Provider selection is controlled by `LLM_PROVIDER=mock|gemini|ollama`. See `.env.example` for the complete variable list. Settings are loaded at process startup; restart the API after changing provider/model configuration.

## SQLite and local files

The default database URL is `sqlite:///data/agent_harness.db`. Attachment bytes are stored under `data/uploads/`; document chunks, conversations, messages, and memory records are stored in SQLite. The local data folder is git-ignored. Back up the database and upload folder together.

## Production checklist

Before multi-user/public deployment, add authentication, per-user ownership and tenant isolation, upload malware scanning, retention/deletion policy, request rate limits, managed secrets, backups, observability, TLS, and a privacy/security review. Add OCR and office/audio/video parsers only behind explicit file allowlists and size limits.
