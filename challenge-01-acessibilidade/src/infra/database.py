"""Database configuration and setup."""

import os
from collections.abc import Generator

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/challenge.db")
ECHO_ENABLED = os.getenv("ECHO_ENABLED", "true") == "true"

_engine: Engine | None = None


def _get_engine() -> Engine:
    global _engine

    if _engine is None:
        _engine = create_engine(
            DATABASE_URL,
            echo=ECHO_ENABLED,
            connect_args={"check_same_thread": False},
        )

    return _engine


def set_engine(engine: Engine | None) -> None:
    global _engine
    _engine = engine


def create_db_and_tables() -> None:
    """Create database and tables."""
    SQLModel.metadata.create_all(_get_engine())


def get_session() -> Generator[Session, None, None]:
    """Get database session."""
    with Session(_get_engine()) as session:
        yield session


def engine() -> Engine:
    return _get_engine()
