from uuid import UUID

from src.application import GastoService
from src.domain.schemas import GastoParams as Params
from src.infra.repository import GastoRepository
from src.tests.utils import BaseTest


class TestGastoService(BaseTest):
    def setUp(self):
        super().setUp()
        self.service = GastoService(GastoRepository(self.session))

    def test_list_delegates_to_repository(self):
        result = self.service.list(Params(orgao="Ministerio A"))

        self.assertEqual(result.total, 3)
        self.assertEqual(len(result.items), 3)

    def test_detail_returns_existing_gasto(self):
        gasto_id = self.fixtures["gastos"][0].id

        result = self.service.detail(gasto_id)

        self.assertEqual(result.id, gasto_id)

    def test_detail_returns_none_for_missing_gasto(self):
        result = self.service.detail(UUID("00000000-0000-0000-0000-000000000000"))

        self.assertIsNone(result)

    def test_summary_returns_filtered_result(self):
        result = self.service.summary(Params(orgao="Ministerio A"))

        total = sum(item.gasto_total for item in result.gastos_por_categoria)
        self.assertEqual(total, 110)
