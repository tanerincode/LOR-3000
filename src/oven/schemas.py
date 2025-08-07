from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class PromptRecord(BaseModel):
    name: str
    system: str
    version: Optional[str] = None
    description: Optional[str] = None
    template: Optional[str] = None


