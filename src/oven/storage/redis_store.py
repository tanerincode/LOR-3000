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


def _key(name: str, version: str | None = None) -> str:
    if version:
        return f"{PREFIX}:{name}:{version}"
    return f"{PREFIX}:{name}"


def list_names() -> list[str]:
    r = _client()
    names = r.smembers(f"{PREFIX}:names")
    return sorted(list(names)) if names else []


def list_versions(name: str) -> list[str]:
    r = _client()
    versions = r.smembers(f"{PREFIX}:versions:{name}")
    return sorted(list(versions)) if versions else []


def get_prompt(name: str, version: str | None = None) -> PromptRecord | None:
    r = _client()
    raw = r.get(_key(name, version))
    if not raw:
        return None
    data = json.loads(raw)
    return PromptRecord(**data)


def latest_version(name: str) -> str | None:
    versions = list_versions(name)
    if not versions:
        return None
    numeric_pairs: list[tuple[int, str]] = []
    for v in versions:
        vv = v.lower().lstrip("v")
        if vv.isdigit():
            numeric_pairs.append((int(vv), v))
    if numeric_pairs:
        return max(numeric_pairs, key=lambda x: x[0])[1]
    return versions[-1]


def get_prompt_latest(name: str) -> PromptRecord | None:
    ver = latest_version(name)
    # Prefer explicit latest version if available; otherwise fall back to unversioned key
    rec = get_prompt(name, ver) if ver is not None else None
    if rec is not None:
        return rec
    return get_prompt(name, None)


def set_prompt(name: str, record: PromptRecord) -> None:
    r = _client()
    with r.pipeline(transaction=False) as p:
        payload = json.dumps(record.model_dump())
        # Set versioned key
        p.set(_key(name, record.version), payload)
        # Also set unversioned "latest" key for convenience
        p.set(_key(name, None), payload)
        p.sadd(f"{PREFIX}:names", name)
        if record.version:
            p.sadd(f"{PREFIX}:versions:{name}", record.version)
        p.execute()


def load_many(prompts: dict[str, PromptRecord]) -> int:
    if not prompts:
        return 0
    r = _client()
    with r.pipeline(transaction=False) as p:
        for name, rec in prompts.items():
            payload = json.dumps(rec.model_dump())
            # Set versioned key
            p.set(_key(name, rec.version), payload)
            # Set unversioned "latest" key
            p.set(_key(name, None), payload)
            p.sadd(f"{PREFIX}:names", name)
            if rec.version:
                p.sadd(f"{PREFIX}:versions:{name}", rec.version)
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
