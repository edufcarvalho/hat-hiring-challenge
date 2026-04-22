import unittest

from src.domain.models import Gasto
from src.domain.schemas import Params, RespostaResumo
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


if __name__ == "__main__":
    unittest.main()
