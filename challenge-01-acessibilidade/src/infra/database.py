"""Database configuration and setup."""
import os

from sqlmodel import Session, SQLModel, create_engine

# Load environment variables from .env file
DATABASE_URL = os.getenv("DATABASE_URL")
ECHO_ENABLED = os.getenv("ECHO_ENABLED", "true") == "true"

# Create engine
engine = create_engine(
  DATABASE_URL,
  echo=ECHO_ENABLED,
  connect_args={"check_same_thread": False},
)


def create_db_and_tables():
  """Create database and tables."""
  SQLModel.metadata.create_all(engine)


def get_session():
  """Get database session."""
  with Session(engine) as session:
    yield session