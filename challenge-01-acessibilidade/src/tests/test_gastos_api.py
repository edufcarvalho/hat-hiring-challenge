from datetime import datetime, timedelta
from decimal import Decimal
from uuid import UUID

import time_machine
from fastapi.testclient import TestClient

from main import app
from src.infra.cache import clear_all_cached
from src.tests.utils.test_utils import BaseTest


class TestGastosAPI(BaseTest):
    def setUp(self):
        super().setUp()
        self.client = TestClient(app)

    def tearDown(self):
        clear_all_cached()
        super().tearDown()

    def test_listar_gastos_returns_all_expenses(self):
        """Test that /gastos returns all expenses when no filters applied."""
        response = self.client.get("/gastos")
        self.assertEqual(response.status_code, 200, "Expected status 200 for /gastos")

        data = response.json()
        self.assertIn("items", data, "'items' key missing in response")
        self.assertIn("total", data, "'total' key missing in response")
        self.assertIn("page", data, "'page' key missing in response")
        self.assertIn("size", data, "'size' key missing in response")

        self.assertEqual(len(data["items"]), 6, "Expected 6 items returned")
        self.assertEqual(data["total"], 6, "Expected total to be 6")
        self.assertEqual(data["page"], 0, "Expected page to be 0")
        self.assertEqual(data["size"], 100, "Expected default page size to be 100")

    def test_listar_gastos_with_orgao_filter(self):
        """Test that /gastos respects orgao filter."""
        response = self.client.get("/gastos?orgao=Ministerio A")
        self.assertEqual(
            response.status_code, 200, "Expected status 200 with orgao filter"
        )

        data = response.json()
        self.assertEqual(len(data["items"]), 3, "Expected 3 items for Ministerio A")
        self.assertEqual(data["total"], 3, "Expected total to be 3 for Ministerio A")

        orgao_ids = [item["orgao_id"] for item in data["items"]]
        self.assertEqual(
            len(set(orgao_ids)), 1, "Expected all orgao_ids to be identical"
        )

        descriptions = [item["descricao"] for item in data["items"]]
        expected_descriptions = {"Compra 1", "Compra 2", "Compra 5"}
        self.assertEqual(
            set(descriptions),
            expected_descriptions,
            "Descriptions do not match expected set",
        )

    def test_listar_gastos_with_ano_filter(self):
        """Test that /gastos respects ano filter."""
        response = self.client.get("/gastos?ano=2024")
        self.assertEqual(
            response.status_code, 200, "Expected status 200 with ano filter"
        )

        data = response.json()
        self.assertEqual(len(data["items"]), 6, "Expected 6 items for year 2024")
        self.assertEqual(data["total"], 6, "Expected total to be 6 for year 2024")

        for item in data["items"]:
            self.assertTrue(
                item["data_lancamento"].startswith("2024"),
                f"Item date {item['data_lancamento']} is not from 2024",
            )

    def test_listar_gastos_pagination(self):
        """Test that /gastos pagination works correctly."""
        response = self.client.get("/gastos?page=0&page_size=2")
        self.assertEqual(
            response.status_code, 200, "Expected status 200 for pagination request"
        )

        data = response.json()
        self.assertEqual(len(data["items"]), 2, "Expected 2 items on first page")
        self.assertEqual(data["total"], 6, "Expected total to be 6")
        self.assertEqual(data["page"], 0, "Expected page to be 0")
        self.assertEqual(data["size"], 2, "Expected size to be 2")

        response = self.client.get("/gastos?page=1&page_size=2")
        self.assertEqual(
            response.status_code, 200, "Expected status 200 for second page"
        )

        data = response.json()
        self.assertEqual(len(data["items"]), 2, "Expected 2 items on second page")
        self.assertEqual(data["total"], 6, "Expected total to be 6")
        self.assertEqual(data["page"], 1, "Expected page to be 1")
        self.assertEqual(data["size"], 2, "Expected size to be 2")

        response = self.client.get("/gastos?page=3&page_size=2")
        self.assertEqual(
            response.status_code, 200, "Expected status 200 for out-of-range page"
        )

        data = response.json()
        self.assertEqual(len(data["items"]), 0, "Expected no items on page 3")
        self.assertEqual(data["total"], 6, "Expected total to be 6")
        self.assertEqual(data["page"], 3, "Expected page to be 3")
        self.assertEqual(data["size"], 2, "Expected size to be 2")

    def test_detalhar_gasto_existing_id(self):
        """Test that /gastos/{id} returns correct expense for existing ID."""
        response = self.client.get("/gastos")
        self.assertEqual(
            response.status_code, 200, "Expected status 200 when listing gastos"
        )

        data = response.json()
        gasto_id = data["items"][0]["id"]

        response = self.client.get(f"/gastos/{gasto_id}")
        self.assertEqual(
            response.status_code, 200, "Expected status 200 for existing gasto"
        )

        data = response.json()
        self.assertEqual(
            data["id"], gasto_id, "Returned ID does not match requested ID"
        )
        self.assertEqual(
            data["descricao"], "Compra 1", "Unexpected descricao for first gasto"
        )

    def test_detalhar_gasto_nonexistent_id(self):
        """Test that /gastos/{id} returns null for non-existent ID."""
        nonexistent_id = UUID("00000000-0000-0000-0000-000000000000")

        response = self.client.get(f"/gastos/{nonexistent_id}")
        self.assertEqual(
            response.status_code, 200, "Expected status 200 for non-existent ID"
        )

        data = response.json()
        self.assertIsNone(data, "Expected None for non-existent gasto")

    def test_resumo_returns_valid_structure(self):
        """Test that /gastos/resumo returns a valid response structure."""
        response = self.client.get("/gastos/resumo")
        self.assertEqual(response.status_code, 200, "Expected status 200 for resumo")

        data = response.json()
        self.assertIn("gastos_por_categoria", data, "'gastos_por_categoria' missing")
        self.assertIn("top_gastos", data, "'top_gastos' missing")

        self.assertIsInstance(
            data["gastos_por_categoria"], list, "Expected list for gastos_por_categoria"
        )
        self.assertGreater(
            len(data["gastos_por_categoria"]),
            0,
            "Expected non-empty gastos_por_categoria",
        )

        self.assertIsInstance(data["top_gastos"], list, "Expected list for top_gastos")
        self.assertLessEqual(
            len(data["top_gastos"]), 5, "Expected at most 5 top gastos"
        )

    def test_resumo_returns_cached_result_on_second_call(self):
        """Test that the second call to /gastos/resumo returns cached result."""
        uncached = self.client.get("/gastos/resumo")
        self.assertEqual(uncached.status_code, 200, "Expected first call to succeed")

        cached = self.client.get("/gastos/resumo")
        self.assertEqual(cached.status_code, 200, "Expected second call to succeed")

        self.assertEqual(
            uncached.json(), cached.json(), "Cached response differs from original"
        )

    def test_resumo_cache_header_miss_on_first_call(self):
        """Test that first call to /gastos/resumo shows MISS in X-Cache header."""
        response = self.client.get("/gastos/resumo")
        self.assertEqual(response.status_code, 200, "Expected status 200 for resumo")

        self.assertEqual(
            response.headers.get("X-Cache"),
            "MISS",
            "Expected X-Cache MISS on first call",
        )

    def test_valor_min_greather_than_valor_max(self):
        """Test that call to /gastos with valor_min > value_max returns 400 Bad Request."""
        response = self.client.get("/gastos?valor_min=100&valor_max=50")
        self.assertEqual(response.status_code, 400, "Expected status Bad Request")

    def test_resumo_cache_header_hit_on_second_call_and_miss_after_sixty_seconds(self):
        """Test cache HIT then expiration behavior."""
        with time_machine.travel(datetime.now(), tick=True) as traveler:
            self.client.get("/gastos/resumo")

            response = self.client.get("/gastos/resumo")
            self.assertEqual(
                response.status_code, 200, "Expected status 200 for cached call"
            )
            self.assertEqual(
                response.headers.get("X-Cache"),
                "HIT",
                "Expected X-Cache=HIT on second call",
            )

            traveler.shift(timedelta(seconds=60))

            response = self.client.get("/gastos/resumo")
            self.assertEqual(
                response.status_code, 200, "Expected status 200 after TTL expiry"
            )
            self.assertEqual(
                response.headers.get("X-Cache"),
                "MISS",
                "Expected X-Cache=MISS after TTL expiry",
            )

    def test_resumo_cache_multiple_calls(self):
        """Test that multiple consecutive calls hit cache."""
        self.client.get("/gastos/resumo")

        for _ in range(5):
            response = self.client.get("/gastos/resumo")
            self.assertEqual(
                response.headers.get("X-Cache"),
                "HIT",
                "Expected cache HIT on repeated calls",
            )

    def test_resumo_with_filters(self):
        """Test that /gastos/resumo respects filters."""
        response = self.client.get("/gastos/resumo?orgao=Ministerio A")
        self.assertEqual(
            response.status_code, 200, "Expected status 200 with orgao filter"
        )

        data = response.json()
        total = sum(
            (Decimal(item["gasto_total"])) for item in data["gastos_por_categoria"]
        )
        self.assertEqual(total, 110, "Unexpected total for Ministerio A")

        response = self.client.get("/gastos/resumo?ano=2024")
        self.assertEqual(
            response.status_code, 200, "Expected status 200 with ano filter"
        )

        data = response.json()
        total = sum(
            (
                item["gasto_total"]
                if isinstance(item["gasto_total"], (int, float))
                else float(item["gasto_total"])
            )
            for item in data["gastos_por_categoria"]
        )
        self.assertEqual(total, 170, "Unexpected total for year 2024")

    def test_resumo_cache_expires_after_ttl(self):
        """Test that cache expires and returns MISS after TTL."""
        with time_machine.travel(datetime.now(), tick=False) as traveler:
            response = self.client.get("/gastos/resumo")
            self.assertEqual(
                response.headers.get("X-Cache"), "MISS", "First call should miss"
            )

            response = self.client.get("/gastos/resumo")
            self.assertEqual(
                response.headers.get("X-Cache"), "HIT", "Second call should hit"
            )

            traveler.shift(timedelta(seconds=120))

            response = self.client.get("/gastos/resumo")
            self.assertEqual(
                response.headers.get("X-Cache"), "MISS", "Call after TTL should miss"
            )
