from typing import Tuple

from core.config import get_settings
from providers.claude_provider import ClaudeProvider
from providers.openai_provider import OpenAIProvider
from router_engine.passes.token_budget import ensure_within_budget


def choose_provider_and_respond(
    prompt: str, *, context_depth: int, output_format: str
) -> Tuple[str, str]:
    # Read settings to ensure configuration is initialized; value not used directly here.
    _settings = get_settings()

    primary = OpenAIProvider()
    fallback = ClaudeProvider()

    prompt_to_send = ensure_within_budget(prompt, context_depth=context_depth)

    try:
        return primary.generate(prompt_to_send, output_format=output_format)
    except Exception:
        return fallback.generate(prompt_to_send, output_format=output_format)
