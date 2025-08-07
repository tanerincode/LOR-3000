from typing import Tuple

from core.config import get_settings
from providers.claude_provider import ClaudeProvider
from providers.openai_provider import OpenAIProvider
from router_engine.passes.token_budget import ensure_within_budget


def choose_provider_and_respond(
    prompt: str, *, context_depth: int, output_format: str, system: str | None = None
) -> Tuple[str, str]:
    settings = get_settings()

    providers_map = {
        "openai:gpt-4": OpenAIProvider(),
        "claude:opus": ClaudeProvider(),
    }

    route = [settings.primary, *settings.fallbacks]
    prompt_to_send = ensure_within_budget(prompt, context_depth=context_depth)
    last_err: Exception | None = None
    for key in route:
        provider = providers_map.get(key)
        if provider is None:
            continue
        try:
            return provider.generate(prompt_to_send, output_format=output_format, system=system)
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            continue
    raise RuntimeError(f"All providers failed: {last_err}")
