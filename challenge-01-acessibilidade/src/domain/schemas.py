from decimal import Decimal
from typing import Optional, TypeVar

from pydantic import BaseModel, Field, model_validator
from sqlmodel import SQLModel

from src.domain.models import Gasto
from src.domain.services import validate_gasto_interval

Model = TypeVar("Model", bound="SQLModel")


class GastoResumo(BaseModel):
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
        validate_gasto_interval(self.valor_min, self.valor_max)
        return self
