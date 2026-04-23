from decimal import Decimal
from unittest import TestCase

from fastapi import HTTPException

from src.domain.schemas import GastoParams as Params


class TestGastoParams(TestCase):
    def test_valor_min_greater_than_valor_max(self):
        # should raise HTTPException everytime receives valor_min > valor_max
        with self.assertRaises(HTTPException):
            Params(valor_min=Decimal(20.0), valor_max=Decimal(10.0))

    def test_valor_min_lesser_than_valor_min(self):
        valor_min = Decimal(10.0)
        valor_max = Decimal(20.0)
        params = Params(valor_min=valor_min, valor_max=valor_max)

        self.assertEqual(
            params.valor_min,
            valor_min,
            "Expected valor_min to be preserved when valor_max is greater than valor_min",
        )
        self.assertEqual(
            params.valor_max,
            valor_max,
            "Expected valor_max to be preserved when valor_max is greater than valor_min",
        )

    def test_valor_max_equals_valor_min(self):
        valor = Decimal(10.0)

        params = Params(valor_min=valor, valor_max=valor)

        self.assertEqual(params.valor_min, valor)
        self.assertEqual(params.valor_max, valor)
