"""Tests specifically for /gastos/resumo endpoint and its caching behavior."""

import os
from datetime import datetime, timedelta

import pytest
import time_machine
from fastapi.testclient import TestClient

from src.domain.repository import GastoRepository

os.environ["DATABASE_URL"] = "sqlite:///./data/challenge_test.db"


def test_resumo_returns_cached_result_on_second_call(client: TestClient):
    """Test that the second call to /gastos/resumo returns cached result."""
    uncached = client.get("/gastos/resumo")
    assert uncached.status_code == 200

    cached = client.get("/gastos/resumo")
    assert cached.status_code == 200

    uncached_data = uncached.json()
    cached_data = cached.json()

    assert uncached_data == cached_data


def test_resumo_cache_header_miss_on_first_call(client: TestClient):
    """Test that first call to /gastos/resumo shows MISS in X-Cache header."""
    response = client.get("/gastos/resumo")
    assert response.status_code == 200

    cache_header = response.headers.get("X-Cache")
    assert cache_header == "MISS"


def test_resumo_cache_header_hit_on_second_call_and_miss_after_sixty_seconds(
    client: TestClient,
):
    """Test that second call to /gastos/resumo shows HIT in X-Cache header."""
    with time_machine.travel(datetime.now(), tick=False) as traveler:
        client.get("/gastos/resumo")

        response = client.get("/gastos/resumo")
        assert response.status_code == 200

        cache_header = response.headers.get("X-Cache")
        assert cache_header == "HIT"

        traveler.shift(timedelta(seconds=100))
        response = client.get("/gastos/resumo")
        assert response.status_code == 200
        cache_header = response.headers.get("X-Cache")
        assert cache_header == "MISS"


def test_resumo_cache_multiple_calls(client: TestClient):
    """Test that multiple consecutive calls all hit cache after first call."""
    client.get("/gastos/resumo")

    for _ in range(5):
        response = client.get("/gastos/resumo")
        assert response.headers.get("X-Cache") == "HIT"


def test_resumo_returns_valid_structure(client: TestClient):
    """Test that /gastos/resumo returns a valid response structure."""
    response = client.get("/gastos/resumo")
    assert response.status_code == 200

    data = response.json()
    assert "gastos_por_categoria" in data
    assert "top_gastos" in data


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    from fastapi.testclient import TestClient

    from main import app

    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def clear_cache_before_test():
    GastoRepository.clear_cache()
    yield
    from src.infra.database import engine

    engine.dispose()
