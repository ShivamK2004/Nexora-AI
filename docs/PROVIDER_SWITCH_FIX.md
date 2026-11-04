# Multi-provider and model selector (v1.0)

Version 1.0 adds a provider selector and a separate model selector. Model choices are browser-local and sent with each `/api/chat` request. Backend routes validate each provider/model pair against `backend/app/services/models.py`.

Supported providers are Mock, Google Gemini, Anthropic Claude, and Ollama. Claude uses the Anthropic Messages API and requires `ANTHROPIC_API_KEY`. Gemini requires `GEMINI_API_KEY`. Ollama must be reachable from the backend host.

To deploy, add `ANTHROPIC_API_KEY` and/or `GEMINI_API_KEY` in the hosting provider's environment settings, then push the updated project to GitHub and redeploy. Do not commit `.env` or place API keys in frontend code.
