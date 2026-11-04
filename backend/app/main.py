from pathlib import Path
import os
import re
from fastapi import FastAPI, Header, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.app.config import get_settings
from backend.app.db import init_db
from backend.app.routers import chat, documents, memory, agents, tools

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0", description="Nexora AI assistant and research platform API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "X-Nexora-Key"],
)


@app.on_event("startup")
def startup():
    init_db()


def verify_api_key(x_nexora_key: str | None = Header(default=None)):
    if settings.api_key and x_nexora_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Missing or invalid X-Nexora-Key")


def _provider_details() -> dict:
    s = get_settings()
    provider = s.llm_provider.lower().strip()
    model = {"gemini": s.gemini_model, "ollama": s.ollama_model}.get(provider, "mock")
    configured = provider != "gemini" or bool(s.gemini_api_key.strip())
    message = ""
    if provider == "mock":
        message = "Mock mode is active. No language model is called."
    elif provider == "gemini" and not configured:
        message = "Gemini is selected, but GEMINI_API_KEY is missing from .env."
    elif provider == "ollama":
        message = "Ollama is selected. Make sure Ollama is running and this model is installed."
    return {
        "provider": provider,
        "model": model,
        "provider_configured": configured,
        "provider_message": message,
    }


def _env_file_path() -> Path:
    return Path.cwd() / ".env"


def _write_provider_to_env(provider: str) -> None:
    """Persist the UI selection in the project .env file without changing other values."""
    env_path = _env_file_path()
    existing = env_path.read_text(encoding="utf-8") if env_path.exists() else ""
    lines = existing.splitlines()
    replacement = f"LLM_PROVIDER={provider}"
    found = False
    for index, line in enumerate(lines):
        if re.match(r"^\s*LLM_PROVIDER\s*=", line):
            lines[index] = replacement
            found = True
            break
    if not found:
        if lines and lines[-1].strip():
            lines.append("")
        lines.append("# Active AI provider selected in the Nexora UI")
        lines.append(replacement)
    content = "\n".join(lines).rstrip() + "\n"
    temp_path = env_path.with_name(env_path.name + ".tmp")
    temp_path.write_text(content, encoding="utf-8", newline="\n")
    temp_path.replace(env_path)


@app.get("/api/health", tags=["system"])
def health():
    return {"status": "ok", "service": "nexora-ai", "version": "1.0.0", **_provider_details()}


@app.get("/api/models", tags=["system"])
def models():
    details = _provider_details()
    return {"active_provider": details["provider"], "configured_model": details["model"],
            "providers": ["mock", "gemini", "ollama"], "provider_configured": details["provider_configured"]}


@app.post("/api/provider", tags=["system"], dependencies=[Depends(verify_api_key)])
async def set_provider(request: Request):
    """Change the active provider from the frontend and persist it in .env."""
    try:
        payload = await request.json()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Send JSON containing a provider field.") from exc
    provider = str(payload.get("provider", "")).strip().lower()
    if provider not in {"mock", "gemini", "ollama"}:
        raise HTTPException(status_code=400, detail="Provider must be mock, gemini, or ollama.")
    try:
        _write_provider_to_env(provider)
    except OSError as exc:
        raise HTTPException(status_code=500, detail=f"Could not save provider selection to .env: {exc}") from exc
    # Environment values override .env values in Pydantic Settings; update both aliases
    # for this running process, then refresh the cached Settings object.
    os.environ["LLM_PROVIDER"] = provider
    os.environ["NEXORA_LLM_PROVIDER"] = provider
    get_settings.cache_clear()
    return {"saved": True, **_provider_details()}


for router in [chat.router, documents.router, memory.router, agents.router, tools.router]:
    app.include_router(router, dependencies=[Depends(verify_api_key)])

static_dir = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(static_dir / "index.html")
