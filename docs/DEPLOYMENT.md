# Deployment notes

For local development on Windows, run `start_windows.bat` or `start_windows.ps1`. For Render, deploy the Dockerfile at the repository root and use a persistent disk mounted at `/var/data` for the SQLite database and uploaded files. Set `NEXORA_DATA_DIR=/var/data`.

## Provider secrets

Add only the API keys for providers you intend to use in Render → Environment:

- `GEMINI_API_KEY` — Google Gemini
- `ANTHROPIC_API_KEY` — Anthropic Claude
- `LLM_PROVIDER` — default provider when a browser has no saved preference (`mock`, `gemini`, `anthropic`, or `ollama`)
- `GEMINI_MODEL` — default Gemini model, e.g. `gemini-3.8-flash`
- `ANTHROPIC_MODEL` — default Claude model, e.g. `claude-sonnet-5-5`
- `OLLAMA_BASE_URL` and `OLLAMA_MODEL` — for an Ollama server reachable from the Render container

Never commit `.env` or API keys. The UI's provider/model choice is browser-specific and is sent with each chat request. It does not write provider API secrets to the frontend.

## Persistent storage

The default local database is SQLite under `data/`. In Render, set `NEXORA_DATA_DIR=/var/data` and attach a persistent disk mounted at `/var/data`; this keeps conversation records and uploaded attachments across deploys. Free Render instances may not support persistent disks, so check the plan before relying on persistence.

## Security / production checklist

Before multi-user public deployment, implement user authentication and per-user conversation ownership, rate limits and quotas, upload scanning, retention/deletion controls, backups, monitoring, and a privacy/security review. Keep provider keys as Render secrets. Do not expose a local unauthenticated Ollama endpoint to the public internet.
