from __future__ import annotations

import json

import redis  # type: ignore[import-untyped]
from core.config import get_settings
from oven.schemas import PromptRecord

PREFIX = "lor3:prompts"


def _client() -> redis.Redis:
    settings = get_settings()
    if not settings.redis_url:
        raise RuntimeError("REDIS_URL not configured")
    return redis.from_url(settings.redis_url, decode_responses=True)


def _key(name: str) -> str:
    return f"{PREFIX}:{name}"


def list_names() -> list[str]:
    r = _client()
    names = r.smembers(f"{PREFIX}:names")
    return sorted(list(names)) if names else []


def get_prompt(name: str) -> PromptRecord | None:
    r = _client()
    raw = r.get(_key(name))
    if not raw:
        return None
    data = json.loads(raw)
    return PromptRecord(**data)


def set_prompt(name: str, record: PromptRecord) -> None:
    r = _client()
    with r.pipeline(transaction=False) as p:
        p.set(_key(name), json.dumps(record.model_dump()))
        p.sadd(f"{PREFIX}:names", name)
        p.execute()


def load_many(prompts: dict[str, PromptRecord]) -> int:
    if not prompts:
        return 0
    r = _client()
    with r.pipeline(transaction=False) as p:
        for name, rec in prompts.items():
            p.set(_key(name), json.dumps(rec.model_dump()))
            p.sadd(f"{PREFIX}:names", name)
        p.execute()
    return len(prompts)


def clear() -> None:
    r = _client()
    names = list_names()
    if not names:
        return
    with r.pipeline(transaction=False) as p:
        for name in names:
            p.delete(_key(name))
        p.delete(f"{PREFIX}:names")
        p.execute()


# Placeholder for Redis-backed prompt cache implementation
