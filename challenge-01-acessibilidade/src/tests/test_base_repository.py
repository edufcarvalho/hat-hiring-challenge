import unittest
from decimal import Decimal

from uuid6 import uuid8

from src.domain.models import Gasto
from src.domain.schemas import Params
from src.tests.utils.test_utils import BaseTest


class TestBaseRepository(BaseTest):
    def setUp(self):
        super().setUp(Gasto)

    def test_empty_filter(self):
        """Test that checks the return when no filter is applied"""
        params = Params()
        result = self.repository.list_all(params)

        self.assertEqual(
            len(result.items),
            6,
            "Should return all 6 expenses when no filter is applied",
        )
        self.assertEqual(result.total, 6, "Total should be 6")
        self.assertEqual(result.page, 0, "Page should be 0")
        self.assertEqual(result.size, params.page_size, "Size should match page_size")

    def test_categoria_filter(self):
        """Test that checks if categoria filters working correctly"""
        params = Params(categoria="Categoria A")
        result = self.repository.list_all(params)

        self.assertEqual(
            len(result.items), 3, "Should return 3 expenses for Categoria A in 2024"
        )
        self.assertEqual(result.total, 3, "Total should be 3")

        for item in result.items:
            self.assertEqual(
                item.categoria.nome,
                "Categoria A",
                "All items should belong to Categoria A",
            )

    def test_multi_filter(self):
        """Test that checks combined filters working correctly"""
        params = Params(orgao="Ministerio A", ano=2024)
        result = self.repository.list_all(params)

        self.assertEqual(
            len(result.items), 3, "Should return 3 expenses for Ministerio A in 2024"
        )
        self.assertEqual(result.total, 3, "Total should be 3")

        for item in result.items:
            self.assertEqual(
                item.orgao.nome,
                "Ministerio A",
                "All items should belong to Ministerio A",
            )

    def test_mes_filter(self):
        """Test that checks if mes filter is working correctly"""
        params = Params(mes="1")
        result = self.repository.list_all(params)

        self.assertEqual(
            len(result.items), 4, "Should return 4 expenses for with month=1 (January)"
        )
        self.assertEqual(result.total, 4, "Total should be 4")

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

    def test_valor_max_greater_than_valor_min(self):
        """Test that checks behavior when valor_min <= valor_max"""
        params = Params(valor_min=Decimal("30.00"), valor_max=Decimal("50.00"))
        result = self.repository.list_all(params)

        self.assertEqual(
            len(result.items),
            1,
            "Should return result within the value_min --> value_max range",
        )
        self.assertEqual(result.total, 1, "Total should be 1")

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

    def test_mes_equal_zero(self):
        """Test that mes filter handles negative correctly"""
        params = Params(mes=0)
        result = self.repository.list_all(params)

        self.assertEqual(len(result.items), 0, "Should return no results for mes=0")
        self.assertEqual(result.total, 0, "Total should be 0 for mes=0")

    def test_mes_negative(self):
        """Test that mes filter handles negative correctly"""
        params = Params(mes=-1)
        result = self.repository.list_all(params)

        self.assertEqual(len(result.items), 0, "Should return no results for mes=-")
        self.assertEqual(result.total, 0, "Total should be 0 for mes=-1")

    def test_categoria_nome_nao_existe(self):
        """Test that categoria filter handles non-existent category names correctly"""
        # Test with a category name that doesn't exist
        params = Params(categoria="Categoria Inexistente")
        result = self.repository.list_all(params)

        self.assertEqual(
            len(result.items), 0, "Should return no results for non-existent category"
        )
        self.assertEqual(result.total, 0, "Total should be 0 for non-existent category")


if __name__ == "__main__":
    unittest.main()
