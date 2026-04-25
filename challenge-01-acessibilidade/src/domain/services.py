from decimal import Decimal

from src.domain.exceptions import DomainValidationError, ValidationIssue


def validate_gasto_interval(
    valor_min: Decimal | None,
    valor_max: Decimal | None,
) -> None:
    if valor_min is None or valor_max is None or valor_min <= valor_max:
        return

    raise DomainValidationError(
        "Nao foi possivel validar o intervalo de valores informado.",
        errors=[
            ValidationIssue(
                location=("query", "valor_min"),
                message="O valor_min deve ser menor ou igual ao valor_max informado.",
            ),
            ValidationIssue(
                location=("query", "valor_max"),
                message="O valor_max deve ser maior ou igual ao valor_min informado.",
            ),
        ],
    )
