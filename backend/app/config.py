from functools import lru_cache
from pathlib import Path
from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-backed configuration; accepts both Nexora and Agent Harness names."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    app_name: str = Field("Nexora AI", validation_alias=AliasChoices("NEXORA_APP_NAME", "APP_NAME"))
    env: str = Field("development", validation_alias=AliasChoices("NEXORA_ENV", "APP_ENV"))
    host: str = Field("127.0.0.1", validation_alias=AliasChoices("NEXORA_HOST", "HOST"))
    port: int = Field(8000, validation_alias=AliasChoices("NEXORA_PORT", "PORT"))
    data_dir: Path = Field(Path("./data"), validation_alias=AliasChoices("NEXORA_DATA_DIR", "DATA_DIR"))
    database_url: str = Field("", validation_alias=AliasChoices("NEXORA_DATABASE_URL", "DATABASE_URL"))
    max_upload_mb: int = Field(10, validation_alias=AliasChoices("NEXORA_MAX_UPLOAD_MB", "MAX_UPLOAD_MB"))
    allowed_origins: str = Field(
        "http://localhost:8000,http://127.0.0.1:8000",
        validation_alias=AliasChoices("NEXORA_ALLOWED_ORIGINS", "ALLOWED_ORIGINS"),
    )
    api_key: str = Field("", validation_alias=AliasChoices("NEXORA_API_KEY", "API_KEY"))

    llm_provider: str = Field("mock", validation_alias=AliasChoices("NEXORA_LLM_PROVIDER", "LLM_PROVIDER"))
    gemini_api_key: str = Field("", validation_alias=AliasChoices("GEMINI_API_KEY", "NEXORA_GEMINI_API_KEY"))
    gemini_model: str = Field("gemini-3.8-flash", validation_alias=AliasChoices("GEMINI_MODEL", "NEXORA_GEMINI_MODEL"))
    anthropic_api_key: str = Field("", validation_alias=AliasChoices("ANTHROPIC_API_KEY", "NEXORA_ANTHROPIC_API_KEY"))
    anthropic_model: str = Field("claude-sonnet-5-5", validation_alias=AliasChoices("ANTHROPIC_MODEL", "NEXORA_ANTHROPIC_MODEL"))
    ollama_url: str = Field(
        "http://localhost:11434",
        validation_alias=AliasChoices("OLLAMA_BASE_URL", "NEXORA_OLLAMA_URL", "OLLAMA_URL"),
    )
    ollama_model: str = Field("llama3:latest", validation_alias=AliasChoices("OLLAMA_MODEL", "NEXORA_OLLAMA_MODEL"))
    llm_timeout_seconds: int = Field(
        120,
        validation_alias=AliasChoices("OLLAMA_TIMEOUT_SECONDS", "REQUEST_TIMEOUT_SECONDS", "NEXORA_LLM_TIMEOUT_SECONDS"),
    )
    embedding_model: str = Field("", validation_alias=AliasChoices("NEXORA_EMBEDDING_MODEL", "EMBEDDING_MODEL"))

    workspace_dir: str = Field("workspace", validation_alias=AliasChoices("WORKSPACE_DIR", "NEXORA_WORKSPACE_DIR"))
    knowledge_base_dir: str = Field("knowledge_base", validation_alias=AliasChoices("KNOWLEDGE_BASE_DIR", "NEXORA_KNOWLEDGE_BASE_DIR"))
    log_dir: str = Field("logs", validation_alias=AliasChoices("LOG_DIR", "NEXORA_LOG_DIR"))
    benchmark_dataset: str = Field("benchmarks/tasks.json", validation_alias=AliasChoices("BENCHMARK_DATASET", "NEXORA_BENCHMARK_DATASET"))
    max_tool_output_chars: int = Field(8000, validation_alias=AliasChoices("MAX_TOOL_OUTPUT_CHARS", "NEXORA_MAX_TOOL_OUTPUT_CHARS"))
    max_workspace_file_bytes: int = Field(200000, validation_alias=AliasChoices("MAX_WORKSPACE_FILE_BYTES", "NEXORA_MAX_WORKSPACE_FILE_BYTES"))
    max_agent_steps: int = Field(5, validation_alias=AliasChoices("MAX_AGENT_STEPS", "NEXORA_MAX_AGENT_STEPS"))

    @property
    def cors_origins(self) -> list[str]:
        return [item.strip() for item in self.allowed_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
