from typing import Optional


class PromptOven:
    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def get(self, name: str) -> Optional[str]:
        return self._store.get(name)

    def set(self, name: str, prompt: str) -> None:
        self._store[name] = prompt
