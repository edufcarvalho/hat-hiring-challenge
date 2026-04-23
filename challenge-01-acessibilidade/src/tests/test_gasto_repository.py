import unittest
from decimal import Decimal

from src.domain.models import Gasto
from src.domain.schemas import GastoParams as Params
from src.domain.schemas import RespostaResumo
from src.infra.repository import GastoRepository
from src.tests.utils.test_utils import BaseTest


class TestGastoRepository(BaseTest):
    def setUp(self):
        super().setUp(Gasto)
        self.repository = GastoRepository(self.session)

    def test_get_summary_without_filters(self):
        params = Params()
        result = self.repository.get_summary(params)

        self.assertIsInstance(
            result,
            RespostaResumo,
            "Expected result to be an instance of RespostaResumo",
        )

        self.assertIsInstance(
            result.gastos_por_categoria,
            list,
            "Expected gastos_por_categoria to be a list",
        )

        self.assertGreater(
            len(result.gastos_por_categoria),
            0,
            "Expected gastos_por_categoria to have at least one item",
        )

        self.assertIsInstance(
            result.top_gastos, list, "Expected top_gastos to be a list"
        )

        self.assertEqual(
            len(result.top_gastos), 5, "Expected top_gastos to contain 5 items"
        )

        total_gastos = sum(item.gasto_total for item in result.gastos_por_categoria)
        expected_total = sum(gasto.valor for gasto in self.fixtures["gastos"])
        self.assertEqual(
            total_gastos,
            expected_total,
            "Total gastos_por_categoria does not match expected total",
        )

    def test_get_summary_with_orgao_filter(self):
        params = Params(orgao="Ministerio A")
        result = self.repository.get_summary(params)

        expected_gastos = [
            gasto
            for gasto in self.fixtures["gastos"]
            if gasto.orgao.nome == "Ministerio A"
        ]
        expected_total = sum(gasto.valor for gasto in expected_gastos)

        total_gastos = sum(item.gasto_total for item in result.gastos_por_categoria)
        self.assertEqual(
            total_gastos,
            expected_total,
            "Filtered total for 'Ministerio A' does not match expected total",
        )

    def test_get_summary_with_ano_filter(self):
        params = Params(ano=2024)
        result = self.repository.get_summary(params)

        expected_total = sum(gasto.valor for gasto in self.fixtures["gastos"])
        total_gastos = sum(item.gasto_total for item in result.gastos_por_categoria)
        self.assertEqual(
            total_gastos,
            expected_total,
            "Filtered total for year 2024 does not match expected total",
        )

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

        params = Params(categoria="Categoria Inexistente")
        result = self.repository.list_all(params)

        self.assertEqual(
            len(result.items), 0, "Should return no results for non-existent category"
        )
        self.assertEqual(result.total, 0, "Total should be 0 for non-existent category")

    def test_orgao_nome_nao_existe(self):
        """Test that categoria filter handles non-existent orgão names correctly"""

        params = Params(orgao="Orgão Inexistente")
        result = self.repository.list_all(params)

        self.assertEqual(
            len(result.items), 0, "Should return no results for non-existent orgão"
        )
        self.assertEqual(result.total, 0, "Total should be 0 for non-existent orgão")

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


if __name__ == "__main__":
    unittest.main()
