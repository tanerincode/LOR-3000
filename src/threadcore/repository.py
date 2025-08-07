from __future__ import annotations

from uuid import UUID

from oven.schemas import PromptRecord
from sqlalchemy import select
from sqlalchemy.orm import Session
from threadcore.models import Message, PromptVersion, Thread
from threadcore.models import Session as DbSession


def create_session(session: Session, user_id: str | None = None) -> DbSession:
    obj = DbSession(user_id=user_id)
    session.add(obj)
    session.flush()
    return obj


def create_thread(session: Session, session_id: UUID, title: str | None = None) -> Thread:
    obj = Thread(session_id=session_id, title=title)
    session.add(obj)
    session.flush()
    return obj


def add_message(
    session: Session,
    thread_id: UUID,
    role: str,
    content: str,
    *,
    provider: str | None = None,
    prompt_name: str | None = None,
    prompt_version: str | None = None,
    token_count: int | None = None,
    cost_cents: int | None = None,
) -> Message:
    obj = Message(
        thread_id=thread_id,
        role=role,
        content=content,
        provider=provider,
        prompt_name=prompt_name,
        prompt_version=prompt_version,
        token_count=token_count,
        cost_cents=cost_cents,
    )
    session.add(obj)
    session.flush()
    return obj


def get_thread_messages(session: Session, thread_id: UUID) -> list[Message]:
    stmt = select(Message).where(Message.thread_id == thread_id).order_by(Message.id.asc())
    return list(session.scalars(stmt))


def upsert_prompt_version(
    session: Session,
    name: str,
    version: str | None,
    system: str,
    description: str | None = None,
    template: str | None = None,
) -> PromptVersion:
    stmt = select(PromptVersion).where(PromptVersion.name == name, PromptVersion.version == version)
    existing = session.scalars(stmt).first()
    if existing:
        existing.system = system
        existing.description = description
        existing.template = template
        session.add(existing)
        session.flush()
        return existing
    obj = PromptVersion(
        name=name, version=version, system=system, description=description, template=template
    )
    session.add(obj)
    session.flush()
    return obj


def list_prompt_names(session: Session) -> list[str]:
    stmt = select(PromptVersion.name).distinct().order_by(PromptVersion.name.asc())
    return [row[0] for row in session.execute(stmt).all()]


def get_prompt_record(
    session: Session, name: str, version: str | None = None
) -> PromptRecord | None:
    if version is not None:
        stmt = (
            select(PromptVersion)
            .where(PromptVersion.name == name, PromptVersion.version == version)
            .order_by(PromptVersion.id.desc())
        )
    else:
        stmt = (
            select(PromptVersion)
            .where(PromptVersion.name == name)
            .order_by(PromptVersion.id.desc())
        )
    row = session.scalars(stmt).first()
    if not row:
        return None
    return PromptRecord(name=row.name, system=row.system, version=row.version)


def save_many_prompts(session: Session, prompts: dict[str, PromptRecord]) -> int:
    count = 0
    for name, rec in prompts.items():
        upsert_prompt_version(
            session,
            name=name,
            version=rec.version,
            system=rec.system,
            description=rec.description,
            template=rec.template,
        )
        count += 1
    return count


def list_prompt_versions(session: Session, name: str) -> list[str]:
    stmt = (
        select(PromptVersion.version)
        .where(PromptVersion.name == name, PromptVersion.version.is_not(None))
        .order_by(PromptVersion.version.asc())
    )
    return [row[0] for row in session.execute(stmt).all() if row[0] is not None]


def get_latest_prompt_record(session: Session, name: str) -> PromptRecord | None:
    versions = list_prompt_versions(session, name)
    latest_version: str | None = None
    numeric_pairs: list[tuple[int, str]] = []
    for v in versions:
        vv = v.lower().lstrip("v")
        if vv.isdigit():
            numeric_pairs.append((int(vv), v))
    if numeric_pairs:
        latest_version = max(numeric_pairs, key=lambda x: x[0])[1]
    else:
        latest_version = versions[-1] if versions else None
    return get_prompt_record(session, name, latest_version)
