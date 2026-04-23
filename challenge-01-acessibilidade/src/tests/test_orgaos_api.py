from fastapi.testclient import TestClient

from main import app
from src.infra.cache import clear_all_cached
from src.tests.utils import BaseTest


class TestOrgaosAPI(BaseTest):
    def setUp(self):
        super().setUp()
        self.client = TestClient(app)

    def tearDown(self):
        clear_all_cached()
        super().tearDown()

    def test_listar_orgaos_returns_all_orgaos(self):
        """Test that /orgaos returns all orgaos"""
        response = self.client.get("/orgaos")
        self.assertEqual(response.status_code, 200, "Expected status 200 for /orgaos")

        data = response.json()

        first_orgao, second_orgao = sorted(data["items"], key=lambda e: e["nome"])

        self.assertEqual(
            first_orgao["nome"], "Ministerio A", "Expect first Orgao to be Ministerio A"
        )
        self.assertEqual(
            second_orgao["nome"],
            "Ministerio B",
            "Expect second Orgao to be Ministerio B",
        )
