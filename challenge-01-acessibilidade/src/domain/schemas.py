from decimal import Decimal

from pydantic import BaseModel

from src.domain.models import Gasto


class GastoResumo(BaseModel, from_attributes=True):
    nome_categoria: str
    gasto_total: Decimal


class RespostaResumo(BaseModel):
    gastos_por_categoria: list[GastoResumo]
    top_gastos: list[Gasto]
