from __future__ import annotations

from contextlib import suppress

from core.config import get_settings
from oven.loader import load_prompts_from_file
from oven.schemas import PromptRecord
from oven.storage import redis_store

# Shared in-process store
_STORE: dict[str, PromptRecord] = {}
_SOURCE_PATH: str | None = None


class PromptOven:
    def __init__(self) -> None:
        global _STORE, _SOURCE_PATH
        settings = get_settings()
        use_redis = bool(settings.redis_url)
        if use_redis:
            # Attempt to read names from Redis; if empty and file provided, seed Redis
            with suppress(Exception):
                names = redis_store.list_names()
                if not names and settings.prompts_file:
                    prompts = load_prompts_from_file(settings.prompts_file)
                    with suppress(Exception):
                        redis_store.load_many(prompts)
                    _SOURCE_PATH = settings.prompts_file
            if "names" not in locals():
                use_redis = False

        if not use_redis and not _STORE and settings.prompts_file:
            try:
                _STORE = load_prompts_from_file(settings.prompts_file)
                _SOURCE_PATH = settings.prompts_file
            except Exception:
                _STORE = {}

    @property
    def store(self) -> dict[str, PromptRecord]:
        return _STORE

    @property
    def source_path(self) -> str | None:
        return _SOURCE_PATH

    def names(self) -> list[str]:
        settings = get_settings()
        if settings.redis_url:
            try:
                return redis_store.list_names()
            except Exception:
                pass
        return sorted(list(_STORE.keys()))

    def get(self, name: str) -> PromptRecord | None:
        settings = get_settings()
        if settings.redis_url:
            try:
                rec = redis_store.get_prompt(name)
                if rec is not None:
                    return rec
            except Exception:
                pass
        return _STORE.get(name)

    def set(self, name: str, prompt: PromptRecord) -> None:
        settings = get_settings()
        if settings.redis_url:
            try:
                redis_store.set_prompt(name, prompt)
                return
            except Exception:
                pass
        _STORE[name] = prompt

    def reload(self, path: str | None = None) -> dict[str, int | str | None]:
        global _STORE, _SOURCE_PATH
        file_path = path or _SOURCE_PATH or get_settings().prompts_file
        if not file_path:
            _STORE = {}
            _SOURCE_PATH = None
            return {"count": 0, "source": None}
        settings = get_settings()
        prompts = load_prompts_from_file(file_path)
        if settings.redis_url:
            try:
                count = redis_store.load_many(prompts)
                _SOURCE_PATH = file_path
                return {"count": count, "source": _SOURCE_PATH}
            except Exception:
                pass
        _STORE = prompts
        _SOURCE_PATH = file_path
        return {"count": len(_STORE), "source": _SOURCE_PATH}
