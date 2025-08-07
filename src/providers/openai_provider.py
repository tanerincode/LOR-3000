from typing import Tuple

from providers.base import Provider


class OpenAIProvider(Provider):
    name = "openai:gpt-4"

    def generate(self, prompt: str, *, output_format: str = "markdown") -> Tuple[str, str]:
        # Placeholder implementation
        return (f"[OpenAI response in {output_format}] {prompt}", self.name)
