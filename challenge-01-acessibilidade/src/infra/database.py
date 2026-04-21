"""Database configuration and setup."""

import os
from typing import Optional

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL")
ECHO_ENABLED = os.getenv("ECHO_ENABLED", "true") == "true"

_engine: Optional[Engine] = None


def _get_engine() -> Engine:
    global _engine

    if _engine is None:
        _engine = create_engine(
            DATABASE_URL,
            echo=ECHO_ENABLED,
            connect_args={"check_same_thread": False},
        )

    return _engine


def set_engine(engine: Engine):
    global _engine
    _engine = engine


def create_db_and_tables():
    """Create database and tables."""
    SQLModel.metadata.create_all(_get_engine())


def get_session():
    """Get database session."""
    with Session(_get_engine()) as session:
        yield session


def engine() -> Engine:
    return _get_engine()
