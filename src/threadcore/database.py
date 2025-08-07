from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from core.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

_ENGINE = None
_SESSION_FACTORY: sessionmaker[Session] | None = None


def get_engine():  # type: ignore[no-untyped-def]
    global _ENGINE
    if _ENGINE is None:
        settings = get_settings()
        if not settings.database_url:
            raise RuntimeError("DATABASE_URL not configured")
        _ENGINE = create_engine(settings.database_url, pool_pre_ping=True)
    return _ENGINE


def get_session_factory() -> sessionmaker[Session]:
    global _SESSION_FACTORY
    if _SESSION_FACTORY is None:
        _SESSION_FACTORY = sessionmaker(bind=get_engine(), expire_on_commit=False, class_=Session)
    return _SESSION_FACTORY


@contextmanager
def db_session() -> Iterator[Session]:
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
