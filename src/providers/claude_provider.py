from typing import Tuple

from providers.base import Provider


class ClaudeProvider(Provider):
    name = "claude:opus"

    def generate(
        self, prompt: str, *, output_format: str = "markdown", system: str | None = None
    ) -> Tuple[str, str]:
        # Placeholder implementation (system ignored for now)
        _ = system
        return (f"[Claude response in {output_format}] {prompt}", self.name)
