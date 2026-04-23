from decimal import Decimal
from typing import TypeVar, Optional

from pydantic import model_validator, Field, BaseModel
from sqlmodel import SQLModel

from src.domain.models import Gasto

Model = TypeVar("Model", bound="SQLModel")


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
    page: int = Field(default=0, ge=0)
    page_size: int = Field(default=100, ge=0)


class OrgaoParams(PaginatedParams):
    orgao: Optional[str] = None


class GastoParams(OrgaoParams):
    ano: Optional[int] = None
    mes: Optional[int] = None
    categoria: Optional[str] = None
    valor_min: Optional[Decimal] = Field(default=None, ge=0)
    valor_max: Optional[Decimal] = Field(default=None, ge=0)

    @model_validator(mode="after")
    def min_should_be_le_than_max(self):
        if self.valor_min is not None and self.valor_max is not None:
            if self.valor_min > self.valor_max:
                raise ValueError("Valor_min nunca deve ser maior que valor_max")

        return self
