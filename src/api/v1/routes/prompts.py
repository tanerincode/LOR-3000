from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from oven.manager import PromptOven


router = APIRouter()


@router.get("")
def list_prompts() -> dict:
    oven = PromptOven()
    return {"source": oven.source_path, "prompts": oven.names()}


@router.get("/{name}")
def get_prompt(name: str) -> dict:
    oven = PromptOven()
    rec = oven.get(name)
    if not rec:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return rec.model_dump()


@router.post("/reload")
def reload_prompts(path: Optional[str] = Query(default=None)) -> dict:
    oven = PromptOven()
    info = oven.reload(path)
    return {"reloaded": True, **info}


