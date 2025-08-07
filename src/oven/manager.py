from __future__ import annotations

from core.config import get_settings
from oven.loader import load_prompts_from_file
from oven.schemas import PromptRecord


class PromptOven:
    def __init__(self) -> None:
        self._store: dict[str, PromptRecord] = {}
        settings = get_settings()
        if settings.prompts_file:
            try:
                self._store = load_prompts_from_file(settings.prompts_file)
            except Exception:
                self._store = {}

    def get(self, name: str) -> PromptRecord | None:
        return self._store.get(name)

    def set(self, name: str, prompt: PromptRecord) -> None:
        self._store[name] = prompt
