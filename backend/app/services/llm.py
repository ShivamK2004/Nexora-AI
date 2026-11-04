import httpx
from backend.app.config import get_settings


class LLMError(RuntimeError):
    pass


class LLMService:
    """Provider adapter. The app can later add a native NexoraLM implementation here."""

    def __init__(self):
        self.settings = get_settings()

    @property
    def provider(self) -> str:
        return self.settings.llm_provider.lower().strip()

    async def chat(self, messages: list[dict], system: str = "") -> str:
        provider = self.provider
        if provider == "mock":
            user_message = next((m for m in reversed(messages) if m.get("role") == "user"), {})
            user_text = user_message.get("content", "")
            # Do not echo extracted PDF/document contents as if that were an answer.
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
                "Choose Gemini or Ollama in the provider selector to generate an actual answer."
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
            payload = {
                "model": self.settings.ollama_model,
                "messages": payload_messages,
                "stream": False,
            }
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
            if not self.settings.gemini_api_key:
                raise LLMError("GEMINI_API_KEY is missing. Add it to your local .env file and restart Nexora.")
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
                        image_b64 = image
                        mime_type = "image/jpeg"
                    if image_b64:
                        parts.append({"inline_data": {"mime_type": mime_type, "data": image_b64}})
                if parts:
                    contents.append({"role": role, "parts": parts})
            payload = {"contents": contents, "generationConfig": {"temperature": 0.3}}
            if system:
                payload["system_instruction"] = {"parts": [{"text": system}]}
            url = (
                "https://generativelanguage.googleapis.com/v1beta/models/"
                + self.settings.gemini_model + ":generateContent"
            )
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

        raise LLMError(f"Unsupported LLM_PROVIDER: {provider}. Use mock, gemini, or ollama.")
