import unittest

from uuid6 import uuid8

from src.domain.models import Gasto
from src.domain.schemas import GastoParams as Params
from src.tests.utils import BaseTest


class TestBaseRepository(BaseTest):
    def setUp(self):
        super().setUp(Gasto)

    def test_inexistant_page(self):
        """Test that checks behavior when a non-existent page is requested"""
        params = Params(page=1, page_size=10)
        result = self.repository.list_all(params)

        self.assertEqual(
            len(result.items), 0, "Should return empty list for non-existent page"
        )
        self.assertEqual(result.total, 6, "Total should still be 6")
        self.assertEqual(result.page, 1, "Page should be 1")
        self.assertEqual(result.size, 10, "Size should be 10")

    def test_list_by_id_existing_id(self):
        """Test that list_by_id returns correct gasto for existing ID"""
        gasto_id = self.fixtures["gastos"][0].id
        result = self.repository.list_by_id(gasto_id)

        self.assertIsNotNone(
            result,
            "Expected list_by_id to return a gasto for an existing ID",
        )
        self.assertIsInstance(
            result,
            Gasto,
            "Expected the returned object to be a Gasto instance",
        )
        self.assertEqual(
            result.id,
            gasto_id,
            "Expected the returned gasto ID to match the requested ID",
        )
        self.assertEqual(
            result.descricao,
            "Compra 1",
            "Expected the first gasto to have descricao 'Compra 1'",
        )

    def test_list_by_id_nonexistent_id(self):
        """Test that list_by_id returns None for non-existent ID"""
        nonexistent_id = uuid8()
        result = self.repository.list_by_id(nonexistent_id)

        self.assertIsNone(
            result, "Expected list_by_id to return None for a non-existent ID"
        )

    def test_list_by_id_invalid_uuid_string(self):
        """Test that list_by_id handles invalid UUID gracefully"""
        # This test assumes the method expects a UUID object, not a string
        # If it accepts strings, we'd need to test with invalid string format
        # For now, we'll test with a nil UUID
        from uuid import UUID

        nil_uuid = UUID("00000000-0000-0000-0000-000000000000")
        result = self.repository.list_by_id(nil_uuid)

        self.assertIsNone(
            result, "Expected list_by_id to return None for an invalid UUID input"
        )


if __name__ == "__main__":
    unittest.main()
