import httpx
from backend.app.config import get_settings
from backend.app.services.models import supported_model


class LLMError(RuntimeError):
    pass


class LLMService:
    """Provider adapter for Gemini, Anthropic Claude, Ollama and mock mode."""

    def __init__(self):
        self.settings = get_settings()
        self.last_provider = self.settings.llm_provider.lower().strip()
        self.last_model = self.default_model(self.last_provider)

    @property
    def provider(self) -> str:
        return self.settings.llm_provider.lower().strip()

    def default_model(self, provider: str) -> str:
        return {
            "gemini": self.settings.gemini_model,
            "anthropic": self.settings.anthropic_model,
            "ollama": self.settings.ollama_model,
            "mock": "mock",
        }.get(provider, "")

    async def chat(
        self,
        messages: list[dict],
        system: str = "",
        provider_override: str | None = None,
        model_override: str | None = None,
    ) -> str:
        provider = (provider_override or self.provider).lower().strip()
        model = (model_override or self.default_model(provider)).strip()
        if provider not in {"mock", "gemini", "anthropic", "ollama"}:
            raise LLMError("Unsupported provider. Choose Mock, Gemini, Claude, or Ollama.")
        if not supported_model(provider, model, self.settings):
            raise LLMError(f"Unsupported model '{model}' for provider '{provider}'. Refresh Nexora's model list and choose a listed model.")
        self.last_provider = provider
        self.last_model = model

        if provider == "mock":
            user_message = next((m for m in reversed(messages) if m.get("role") == "user"), {})
            user_text = user_message.get("content", "")
            request_text = user_text.split("\n\n[Attached file:", 1)[0].strip()
            image_count = len(user_message.get("images", []))
            attached_files = user_text.count("\n\n[Attached file:")
            notes = []
            if attached_files:
                notes.append(f"{attached_files} document(s) were received and their text was extracted.")
            if image_count:
                notes.append(f"{image_count} image(s) were received.")
            suffix = " " + " ".join(notes) if notes else ""
            return (
                "[MOCK MODE — no language model was called] I received your request: "
                + (request_text[:300] or "Analyze the attached file(s).") + "." + suffix + "\n\n"
                "Choose Gemini, Claude, or Ollama to generate an actual answer."
            )

        if provider == "ollama":
            payload_messages = []
            for message in messages:
                item = {"role": message["role"], "content": message.get("content", "")}
                if message.get("images"):
                    item["images"] = [
                        image.get("data") if isinstance(image, dict) else image
                        for image in message["images"]
                    ]
                payload_messages.append(item)
            if system:
                payload_messages.insert(0, {"role": "system", "content": system})
            payload = {"model": model, "messages": payload_messages, "stream": False}
            url = self.settings.ollama_url.rstrip("/") + "/api/chat"
            try:
                async with httpx.AsyncClient(timeout=self.settings.llm_timeout_seconds) as client:
                    response = await client.post(url, json=payload)
                    response.raise_for_status()
                    data = response.json()
                answer = data.get("message", {}).get("content")
                if not isinstance(answer, str) or not answer.strip():
                    raise LLMError("Ollama returned an empty response. Check that the selected model is available.")
                return answer
            except LLMError:
                raise
            except (httpx.HTTPError, KeyError, ValueError) as exc:
                raise LLMError(f"Could not reach Ollama at {url}: {exc}") from exc

        if provider == "gemini":
            if not self.settings.gemini_api_key.strip():
                raise LLMError("GEMINI_API_KEY is missing. Add it to Render Environment (or your local .env) and restart Nexora.")
            contents = []
            for message in messages:
                role = "model" if message.get("role") == "assistant" else "user"
                parts = []
                content = message.get("content", "")
                if content:
                    parts.append({"text": content})
                for image in message.get("images", []):
                    if isinstance(image, dict):
                        image_b64 = image.get("data", "")
                        mime_type = image.get("mime_type", "image/jpeg")
                    else:
                        image_b64, mime_type = image, "image/jpeg"
                    if image_b64:
                        parts.append({"inline_data": {"mime_type": mime_type, "data": image_b64}})
                if parts:
                    contents.append({"role": role, "parts": parts})
            payload = {"contents": contents, "generationConfig": {"temperature": 0.3}}
            if system:
                payload["system_instruction"] = {"parts": [{"text": system}]}
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            headers = {"Content-Type": "application/json", "x-goog-api-key": self.settings.gemini_api_key}
            try:
                async with httpx.AsyncClient(timeout=self.settings.llm_timeout_seconds) as client:
                    response = await client.post(url, headers=headers, json=payload)
                    if response.is_error:
                        try:
                            detail = response.json().get("error", {}).get("message", response.text)
                        except ValueError:
                            detail = response.text
                        raise LLMError(f"Gemini API returned HTTP {response.status_code}: {detail[:700]}")
                    data = response.json()
                candidates = data.get("candidates", [])
                parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
                answer = "\n".join(part.get("text", "") for part in parts if part.get("text"))
                if not answer.strip():
                    block_reason = data.get("promptFeedback", {}).get("blockReason")
                    suffix = f" Prompt blocked: {block_reason}." if block_reason else ""
                    raise LLMError("Gemini returned no text content." + suffix)
                return answer
            except LLMError:
                raise
            except (httpx.HTTPError, KeyError, IndexError, ValueError) as exc:
                raise LLMError(f"Gemini request failed: {exc}") from exc

        if provider == "anthropic":
            if not self.settings.anthropic_api_key.strip():
                raise LLMError("ANTHROPIC_API_KEY is missing. Add it to Render Environment (or your local .env) to use Claude.")
            claude_messages = []
            for message in messages:
                role = message.get("role")
                if role not in {"user", "assistant"}:
                    continue
                blocks = []
                text = message.get("content", "")
                if text:
                    blocks.append({"type": "text", "text": text})
                for image in message.get("images", []):
                    image_data = image.get("data", "") if isinstance(image, dict) else image
                    media_type = image.get("mime_type", "image/jpeg") if isinstance(image, dict) else "image/jpeg"
                    if image_data:
                        if media_type not in {"image/jpeg", "image/png", "image/gif", "image/webp"}:
                            raise LLMError(f"Claude does not support this image type: {media_type}")
                        blocks.append({"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_data}})
                if blocks:
                    claude_messages.append({"role": role, "content": blocks})
            payload = {"model": model, "max_tokens": 2048, "messages": claude_messages}
            if system:
                payload["system"] = system
            headers = {
                "content-type": "application/json",
                "x-api-key": self.settings.anthropic_api_key,
                "anthropic-version": "2023-06-01",
            }
            url = "https://api.anthropic.com/v1/messages"
            try:
                async with httpx.AsyncClient(timeout=self.settings.llm_timeout_seconds) as client:
                    response = await client.post(url, headers=headers, json=payload)
                    if response.is_error:
                        try:
                            detail = response.json().get("error", {}).get("message", response.text)
                        except ValueError:
                            detail = response.text
                        raise LLMError(f"Claude API returned HTTP {response.status_code}: {detail[:700]}")
                    data = response.json()
                answer = "\n".join(
                    block.get("text", "") for block in data.get("content", [])
                    if block.get("type") == "text"
                )
                if not answer.strip():
                    raise LLMError("Claude returned an empty response.")
                return answer
            except LLMError:
                raise
            except (httpx.HTTPError, KeyError, ValueError) as exc:
                raise LLMError(f"Claude request failed: {exc}") from exc

        raise LLMError(f"Unsupported LLM_PROVIDER: {provider}.")
