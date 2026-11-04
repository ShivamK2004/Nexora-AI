"""Supported model choices shown in the Nexora model selector."""
from backend.app.config import Settings

STATIC_MODEL_CATALOG = {
    "mock": [{"id": "mock", "label": "Mock (no AI)"}],
    "gemini": [
        {"id": "gemini-3.8-flash", "label": "Gemini 3.8 Flash · recommended"},
        {"id": "gemini-3.7-flash", "label": "Gemini 3.7 Flash"},
        {"id": "gemini-3.6-flash", "label": "Gemini 3.6 Flash"},
        {"id": "gemini-3.5-flash", "label": "Gemini 3.5 Flash"},
        {"id": "gemini-3.5-flash-lite", "label": "Gemini 3.5 Flash-Lite · fast"},
        {"id": "gemini-2.5-flash", "label": "Gemini 2.5 Flash"},
        {"id": "gemini-2.5-flash-lite", "label": "Gemini 2.5 Flash-Lite"},
        {"id": "gemini-2.5-pro", "label": "Gemini 2.5 Pro"},
    ],
    "anthropic": [
        {"id": "claude-haiku-5-5", "label": "Claude Haiku 5.5 · fastest"},
        {"id": "claude-sonnet-5-5", "label": "Claude Sonnet 5.5 · balanced"},
        {"id": "claude-opus-5-5", "label": "Claude Opus 5.5 · advanced"},
        {"id": "claude-fable-5-1", "label": "Claude Fable 5.1 · reasoning"},
    ],
}


def model_defaults(settings: Settings) -> dict[str, str]:
    return {
        "mock": "mock",
        "gemini": settings.gemini_model,
        "anthropic": settings.anthropic_model,
        "ollama": settings.ollama_model,
    }


def model_catalog(settings: Settings) -> dict[str, list[dict[str, str]]]:
    catalog = {key: list(value) for key, value in STATIC_MODEL_CATALOG.items()}
    # Ollama model tags are installed by the server owner and are not globally fixed.
    catalog["ollama"] = [{"id": settings.ollama_model, "label": settings.ollama_model}]
    return catalog


def supported_model(provider: str, model: str, settings: Settings) -> bool:
    provider = provider.strip().lower()
    model = model.strip()
    if provider == "ollama":
        return bool(model) and model == settings.ollama_model
    return any(item["id"] == model for item in model_catalog(settings).get(provider, []))
