import os
import unittest
from unittest.mock import patch

from backend.app.config import get_settings
from backend.app.services.llm import LLMService


class FakeResponse:
    is_error = False

    def raise_for_status(self):
        return None

    def json(self):
        return {
            "message": {"content": "Ollama test response"},
            "candidates": [{"content": {"parts": [{"text": "Gemini test response"}]}}],
        }


class FakeAsyncClient:
    last_request = None

    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, url, **kwargs):
        FakeAsyncClient.last_request = {"url": url, **kwargs}
        return FakeResponse()


class ProviderTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.environment = patch.dict(os.environ, {
            "NEXORA_LLM_PROVIDER": "gemini",
            "GEMINI_API_KEY": "unit-test-key",
            "GEMINI_MODEL": "gemini-3.8-flash",
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "OLLAMA_MODEL": "llama3:latest",
        })
        self.environment.start()
        get_settings.cache_clear()

    async def asyncTearDown(self):
        self.environment.stop()
        get_settings.cache_clear()

    async def test_gemini_receives_image_and_returns_text(self):
        with patch("backend.app.services.llm.httpx.AsyncClient", FakeAsyncClient):
            answer = await LLMService().chat([
                {"role": "user", "content": "What is this?", "images": [
                    {"data": "YWJj", "mime_type": "image/png"}
                ]}
            ])
        self.assertEqual(answer, "Gemini test response")
        request = FakeAsyncClient.last_request
        self.assertIn("gemini-3.8-flash:generateContent", request["url"])
        self.assertEqual(request["headers"]["x-goog-api-key"], "unit-test-key")
        image = request["json"]["contents"][0]["parts"][1]["inline_data"]
        self.assertEqual(image["mime_type"], "image/png")
        self.assertEqual(image["data"], "YWJj")

    async def test_ollama_receives_base64_images(self):
        os.environ["NEXORA_LLM_PROVIDER"] = "ollama"
        get_settings.cache_clear()
        with patch("backend.app.services.llm.httpx.AsyncClient", FakeAsyncClient):
            answer = await LLMService().chat([
                {"role": "user", "content": "What is this?", "images": [
                    {"data": "YWJj", "mime_type": "image/png"}
                ]}
            ])
        self.assertEqual(answer, "Ollama test response")
        self.assertEqual(FakeAsyncClient.last_request["json"]["messages"][0]["images"], ["YWJj"])


if __name__ == "__main__":
    unittest.main()
