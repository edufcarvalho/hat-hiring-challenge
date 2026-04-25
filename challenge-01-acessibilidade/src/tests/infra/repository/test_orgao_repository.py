from src.domain.models import Orgao
from src.domain.schemas import OrgaoParams as Params
from src.domain.schemas import PaginatedResponse
from src.infra.repository import OrgaoRepository
from src.tests.utils import BaseTest


class TestOrgaoRepository(BaseTest):
    def setUp(self):
        super().setUp(Orgao)
        self.repository = OrgaoRepository(self.session)

    def test_list_all(self):
        """Test .list_all without passing any filtering params"""
        params = Params()
        result = self.repository.list_all(params)

        self.assertTrue(
            all(isinstance(item, Orgao) for item in result.items),
            "All returns should be Orgaos",
        )
        self.assertIsInstance(result, PaginatedResponse, "Response should be paginated")

    def test_list_all_filtering(self):
        """Test .list_all filtering looking for a specific Orgao"""
        params = Params(orgao="Ministerio B")
        result = self.repository.list_all(params)

        self.assertEqual(
            result.items[0].nome, "Ministerio B", "Should return the filtered Orgao"
        )
        self.assertIsInstance(result.items[0], Orgao, "Should return an Orgao")
        self.assertIsInstance(result, PaginatedResponse, "Response should be paginated")

    def test_list_all_filtering_for_an_inexistant_orgao(self):
        """Test .list_all filtering looking for a inexistant Orgao"""
        params = Params(orgao="Ministerio da Magia")
        result = self.repository.list_all(params)

        self.assertIsInstance(result, PaginatedResponse, "Response should be paginated")
        self.assertEqual(len(result.items), 0, "Should return an empty list")
