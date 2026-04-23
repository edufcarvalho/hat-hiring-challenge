from decimal import Decimal
from typing import TypeVar, Optional

from pydantic import BaseModel, model_validator

from src.domain.models import Gasto

Model = TypeVar("Model", bound="BaseModel")


class GastoResumo(BaseModel, from_attributes=True):
    nome_categoria: str
    gasto_total: Decimal


class PaginatedResponse(BaseModel):
    items: list[Model]
    total: int
    page: int
    size: int


class RespostaResumo(BaseModel):
    gastos_por_categoria: list[GastoResumo]
    top_gastos: list[Gasto]


class PaginatedParams(BaseModel):
    page: int = 0
    page_size: int = 100


class OrgaoParams(PaginatedParams):
    orgao: Optional[str] = None


class GastoParams(OrgaoParams):
    ano: Optional[int] = None
    mes: Optional[int] = None
    categoria: Optional[str] = None
    valor_min: Optional[Decimal] = None
    valor_max: Optional[Decimal] = None

    @model_validator(mode="after")
    def min_should_be_le_than_max(self):
        if self.valor_min is not None and self.valor_max is not None:
            if self.valor_min > self.valor_max:
                raise ValueError("Valor_min nunca deve ser maior que valor_max")

        return self
