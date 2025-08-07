from typing import Tuple

import httpx
from core.config import get_settings
from providers.base import Provider


class OpenAIProvider(Provider):
    name = "openai:gpt-4"

    def generate(
        self, prompt: str, *, _output_format: str = "markdown", system: str | None = None
    ) -> Tuple[str, str]:
        settings = get_settings()
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY not configured")

        # Minimal call using OpenAI's REST compatible endpoint via httpx to avoid SDK lock-in
        # For real usage, replace with the official openai SDK if preferred.
        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        payload = {
            "model": "gpt-4o-mini",  # a small default; can be switched via config later
            "messages": messages,
        }
        with httpx.Client(timeout=30) as client:
            resp = client.post(
                "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
            )
            resp.raise_for_status()
            data = resp.json()
        try:
            content = data["choices"][0]["message"]["content"]
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"OpenAI response parsing failed: {data}") from exc

        return (content, self.name)
