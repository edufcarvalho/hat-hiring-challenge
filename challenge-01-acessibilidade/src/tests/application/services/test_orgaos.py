from src.application import OrgaoService
from src.domain.schemas import OrgaoParams as Params
from src.infra.repository import OrgaoRepository
from src.tests.utils import BaseTest


class TestOrgaoService(BaseTest):
    def setUp(self):
        super().setUp()
        self.service = OrgaoService(OrgaoRepository(self.session))

    def test_list_returns_filtered_orgaos(self):
        result = self.service.list(Params(orgao="Ministerio B"))

        self.assertEqual(result.total, 1)
        self.assertEqual(result.items[0].nome, "Ministerio B")
