from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    provider: str | None = None
    prompt_name: str | None = None
    prompt_version: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class ThreadOut(BaseModel):
    id: int
    title: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
