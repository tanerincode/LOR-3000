from __future__ import annotations

from pydantic import BaseModel


class PromptRecord(BaseModel):
    name: str
    system: str
    version: str | None = None
    description: str | None = None
    template: str | None = None
