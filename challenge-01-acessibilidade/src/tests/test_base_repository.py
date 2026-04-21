import unittest
from decimal import Decimal

from src.domain.models import Gasto
from src.tests.utils.repository import BaseRepositoryTest
from src.utils.api.types import Params


class TestBaseRepository(BaseRepositoryTest):
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
        params = Params(categoria="Categoria A", ano=2024)
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

    def test_inexistant_page(self):
        """Test that checks behavior when a non-existent page is requested"""
        params = Params(page=1, page_size=10)
        result = self.repository.list_all(params)

        self.assertEqual(
            len(result.items), 0, "Should return empty list for non-existent page"
        )
        self.assertEqual(
            result.total, 6, "Total should still be 6"
        )  # Total should still be 6
        self.assertEqual(result.page, 1, "Page should be 1")
        self.assertEqual(result.size, 10, "Size should be 10")

    def test_valor_min_greater_than_valor_max(self):
        """Test that checks behavior when valor_min > valor_max"""
        params = Params(valor_min=Decimal("50.00"), valor_max=Decimal("30.00"))
        result = self.repository.list_all(params)

        self.assertEqual(
            len(result.items), 0, "Should return no results when min > max"
        )
        self.assertEqual(result.total, 0, "Total should be 0")


if __name__ == "__main__":
    unittest.main()
