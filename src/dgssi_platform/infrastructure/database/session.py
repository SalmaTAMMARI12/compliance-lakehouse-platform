from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from dgssi_platform.infrastructure.database.models.audit_model import Base
from dgssi_platform.shared.config import get_settings

_engine = create_engine(get_settings().postgres_dsn)
SessionLocal = sessionmaker(bind=_engine)


def get_session() -> Session:
    return SessionLocal()


def creer_tables() -> None:
    Base.metadata.create_all(_engine)