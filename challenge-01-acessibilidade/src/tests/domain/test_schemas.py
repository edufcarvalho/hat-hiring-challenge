from decimal import Decimal
from unittest import TestCase

from pydantic import ValidationError

from src.domain.exceptions import DomainValidationError
from src.domain.schemas import GastoParams, OrgaoParams, PaginatedParams


class TestPaginatedParams(TestCase):
    def test_defaults_are_applied(self):
        params = PaginatedParams()

        self.assertEqual(params.page, 0)
        self.assertEqual(params.page_size, 100)

    def test_negative_page_raises_validation_error(self):
        with self.assertRaises(ValidationError) as context:
            PaginatedParams(page=-1)

        error = context.exception.errors()[0]
        self.assertEqual(error["loc"], ("page",))
        self.assertEqual(error["type"], "greater_than_equal")

    def test_negative_page_size_raises_validation_error(self):
        with self.assertRaises(ValidationError) as context:
            PaginatedParams(page_size=-1)

        error = context.exception.errors()[0]
        self.assertEqual(error["loc"], ("page_size",))
        self.assertEqual(error["type"], "greater_than_equal")


class TestOrgaoParams(TestCase):
    def test_orgao_params_inherits_pagination_and_filter_values(self):
        params = OrgaoParams(orgao="Ministerio A", page=2, page_size=25)

        self.assertEqual(params.orgao, "Ministerio A")
        self.assertEqual(params.page, 2)
        self.assertEqual(params.page_size, 25)


class TestGastoParamsValidation(TestCase):
    def test_valor_min_greater_than_valor_max_raises_domain_validation_error(self):
        with self.assertRaises(ValidationError) as context:
            GastoParams(valor_min=Decimal("20"), valor_max=Decimal("10"))

        domain_error = context.exception.errors()[0]["ctx"]["error"]
        self.assertIsInstance(domain_error, DomainValidationError)
        self.assertEqual(domain_error.errors[0].location, ("query", "valor_min"))
        self.assertEqual(domain_error.errors[1].location, ("query", "valor_max"))

    def test_negative_valor_min_raises_validation_error(self):
        with self.assertRaises(ValidationError) as context:
            GastoParams(valor_min=Decimal("-1"))

        error = context.exception.errors()[0]
        self.assertEqual(error["loc"], ("valor_min",))
        self.assertEqual(error["type"], "greater_than_equal")

    def test_negative_valor_max_raises_validation_error(self):
        with self.assertRaises(ValidationError) as context:
            GastoParams(valor_max=Decimal("-1"))

        error = context.exception.errors()[0]
        self.assertEqual(error["loc"], ("valor_max",))
        self.assertEqual(error["type"], "greater_than_equal")

    def test_optional_filters_are_preserved(self):
        params = GastoParams(
            orgao="Ministerio A",
            ano=2024,
            mes=3,
            categoria="Categoria A",
            valor_min=Decimal("10.50"),
            valor_max=Decimal("99.90"),
            page=1,
            page_size=10,
        )

        self.assertEqual(params.orgao, "Ministerio A")
        self.assertEqual(params.ano, 2024)
        self.assertEqual(params.mes, 3)
        self.assertEqual(params.categoria, "Categoria A")
        self.assertEqual(params.valor_min, Decimal("10.50"))
        self.assertEqual(params.valor_max, Decimal("99.90"))
        self.assertEqual(params.page, 1)
        self.assertEqual(params.page_size, 10)
