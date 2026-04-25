import json
from decimal import Decimal
from unittest import TestCase

from pydantic import BaseModel, ValidationError
from starlette.requests import Request

from src.api.tools.exception_handlers import (
    register_exception_handlers,
    validation_error_handler,
    value_error_handler,
)
from src.domain.exceptions import DomainValidationError, ValidationIssue
from src.domain.schemas import GastoParams


class DummyModel(BaseModel):
    quantidade: int


def _build_request(path="/test"):
    return Request(
        {
            "type": "http",
            "method": "GET",
            "path": path,
            "headers": [],
            "query_string": b"",
            "client": ("testclient", 50000),
            "server": ("testserver", 80),
            "scheme": "http",
            "http_version": "1.1",
        }
    )


class TestExceptionHandlers(TestCase):
    def test_validation_error_handler_formats_domain_validation_error(self):
        request = _build_request("/gastos")

        with self.assertRaises(ValidationError) as context:
            GastoParams(valor_min=Decimal("100"), valor_max=Decimal("50"))

        response = validation_error_handler(request, context.exception)
        data = json.loads(response.body)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["path"], "/gastos")
        self.assertEqual(len(data["errors"]), 2)
        self.assertEqual(data["errors"][0]["location"], ["query", "valor_min"])
        self.assertEqual(data["errors"][1]["location"], ["query", "valor_max"])

    def test_validation_error_handler_formats_generic_validation_error(self):
        request = _build_request("/dummy")

        with self.assertRaises(ValidationError) as context:
            DummyModel(quantidade="abc")

        response = validation_error_handler(request, context.exception)
        data = json.loads(response.body)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["path"], "/dummy")
        self.assertEqual(len(data["errors"]), 1)
        self.assertEqual(data["errors"][0]["location"], ["request"])

    def test_value_error_handler_formats_generic_value_error(self):
        request = _build_request("/health")

        response = value_error_handler(request, ValueError("erro generico"))
        data = json.loads(response.body)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["path"], "/health")
        self.assertEqual(len(data["errors"]), 1)
        self.assertEqual(data["errors"][0]["location"], ["request"])

    def test_value_error_handler_formats_domain_validation_error(self):
        request = _build_request("/gastos")
        error = DomainValidationError(
            "Erro de dominio.",
            errors=[
                ValidationIssue(
                    location=("query", "campo"),
                    message="Campo invalido.",
                )
            ],
        )

        response = value_error_handler(request, error)
        data = json.loads(response.body)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["path"], "/gastos")
        self.assertEqual(len(data["errors"]), 1)
        self.assertEqual(data["errors"][0]["location"], ["query", "campo"])

    def test_register_exception_handlers_registers_both_types(self):
        from fastapi import FastAPI

        app = FastAPI()

        register_exception_handlers(app)

        self.assertIn(ValidationError, app.exception_handlers)
        self.assertIn(ValueError, app.exception_handlers)
