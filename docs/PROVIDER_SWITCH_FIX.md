# Provider selector and document chat fix (v1.0.0)

The previous UI exposed the active provider as a status badge but did not offer a way to change it. The sample `.env` defaulted to `LLM_PROVIDER=mock`, so uploads were extracted but no language model was called. Mock mode echoed part of the user message (including the start of extracted file content), which could look like a failed PDF summary.

## What changed

- Added an **AI PROVIDER** selector for Mock, Google Gemini, and Ollama local.
- Added `POST /api/provider`; selection is applied immediately and persisted to the project `.env`.
- Added clear configuration status when Gemini is selected without `GEMINI_API_KEY`.
- Mock mode now states that no model was called and never echoes extracted document text.
- The `Access key` button is explicitly documented as the optional local Nexora API access key, not the Gemini key.

## PDF behavior

The app extracts selectable PDF text locally and passes it in the user message to the selected provider. Once Gemini or Ollama is active, the selected model can summarize the supplied text. Image-only/scanned PDF pages are not OCR'd in this release; use a text-searchable PDF or add OCR separately.

## Gemini model

The default `gemini-3.8-flash` model ID is listed as a stable Gemini API model by Google.
