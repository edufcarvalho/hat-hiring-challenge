import unittest

from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from src.infra import database
from src.infra.database import (
    _get_engine,
    create_db_and_tables,
    engine,
    get_session,
    set_engine,
)


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.test_engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

    def tearDown(self):
        set_engine(None)
        database._engine = None
        self.test_engine.dispose()

    def test_set_engine(self):
        set_engine(self.test_engine)
        result = _get_engine()
        self.assertEqual(
            result,
            self.test_engine,
            "Expected _get_engine to return the engine set by set_engine",
        )

    def test_get_engine_returns_new__engine_when_no_engine_set_and_no_url(self):
        set_engine(None)

        self.assertIsNone(
            database._engine,
            "Expected the internal engine to be None after set_engine(None)",
        )

        self.assertIsInstance(
            _get_engine(),
            Engine,
            "Expected _get_engine to create a new SQLAlchemy engine when none is configured",
        )

    def test_engine_function(self):
        set_engine(self.test_engine)
        result = engine()
        self.assertEqual(
            result,
            self.test_engine,
            "Expected engine() helper to return the currently configured engine",
        )

    def test_create_db_and_tables(self):
        set_engine(self.test_engine)
        create_db_and_tables()
        self.assertIsNotNone(
            self.test_engine,
            "Expected the test engine to still be available after creating the database and tables",
        )

    def test_get_session(self):
        set_engine(self.test_engine)
        SQLModel.metadata.create_all(self.test_engine)

        sessions = list(get_session())
        self.assertEqual(
            len(sessions),
            1,
            "Expected get_session() to yield exactly one session",
        )
        self.assertIsInstance(
            sessions[0],
            Session,
            "Expected get_session() to yield a SQLModel Session object",
        )


if __name__ == "__main__":
    unittest.main()
