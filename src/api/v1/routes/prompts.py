from __future__ import annotations

from core.config import get_settings
from fastapi import APIRouter, HTTPException, Query
from oven.loader import load_prompts_from_file
from oven.manager import PromptOven
from oven.storage import redis_store
from threadcore.database import db_session
from threadcore.repository import list_prompt_versions as db_list_prompt_versions

router = APIRouter()


@router.get("")
def list_prompts() -> dict:
    oven = PromptOven()
    return {"source": oven.source_path, "prompts": oven.names()}


@router.get("/{name}")
def get_prompt(name: str, version: str | None = Query(default=None)) -> dict:
    oven = PromptOven()
    # For now, Oven.get() returns latest. If a specific version is requested and Redis is enabled,
    # fetch directly to honor version. Otherwise, latest from DB/Oven.
    if version is not None:
        try:
            rec = (
                redis_store.get_prompt_latest(name)
                if version == "latest"
                else redis_store.get_prompt(name, version)
            )
        except Exception:
            rec = None
    else:
        rec = oven.get(name)
    if not rec:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return rec.model_dump()


@router.post("/reload")
def reload_prompts(path: str | None = Query(default=None)) -> dict:
    oven = PromptOven()
    info = oven.reload(path)
    return {"reloaded": True, **info}


@router.get("/{name}/versions")
def list_versions(name: str) -> dict:
    # Try Redis first
    versions: list[str] = []
    try:
        versions = redis_store.list_versions(name)
    except Exception:
        versions = []
    if versions:
        return {"name": name, "versions": versions}

    # Fallback to DB
    try:
        with db_session() as s:
            versions = db_list_prompt_versions(s, name)
    except Exception:
        versions = []
    if versions:
        return {"name": name, "versions": versions}

    # Last resort: check YAML (single record version if present)
    settings = get_settings()
    if settings.prompts_file:
        try:
            prompts = load_prompts_from_file(settings.prompts_file)
            rec = prompts.get(name)
            if rec and rec.version:
                return {"name": name, "versions": [rec.version]}
        except Exception:
            pass

    return {"name": name, "versions": []}
