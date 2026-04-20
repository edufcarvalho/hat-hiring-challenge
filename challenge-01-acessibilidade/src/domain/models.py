from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel
from uuid6 import uuid8

from src.domain.enums import TipoPessoa


class Gasto(SQLModel, table=True):
    __tablename__ = "gastos"

    id: UUID = Field(default_factory=uuid8, primary_key=True)
    orgao_id: UUID = Field(
        default=None,
        foreign_key="orgaos.id",
        description="ID do órgão responsável pelo gasto",
    )
    categoria_id: UUID = Field(
        default=None, foreign_key="categorias.id", description="Categoria do gasto"
    )
    descricao: str = Field(description="Descrição do gasto")
    valor: Decimal = Field(description="Valor do gasto em BRL", decimal_places=2)
    data_lancamento: date = Field(index=True, description="Data de lançamento do gasto")
    favorecido_id: UUID = Field(
        default=None,
        foreign_key="favorecidos.id",
        description="ID do favorecido do gasto",
    )

    orgao: Optional["Orgao"] = Relationship(back_populates="gastos")
    categoria: Optional["Categoria"] = Relationship(back_populates="gastos")
    favorecido: Optional["Favorecido"] = Relationship(back_populates="gastos")


class GastoResumo(BaseModel, from_attributes=True):
    nome_categoria: str
    gasto_total: Decimal


class RespostaResumo(BaseModel):
    gastos_por_categoria: list[GastoResumo]
    top_gastos: list[Gasto]


class Orgao(SQLModel, table=True):
    __tablename__ = "orgaos"

    id: UUID = Field(default_factory=uuid8, primary_key=True)
    nome: str = Field(
        unique=True, index=True, description="Nome do ministério ou órgão"
    )
    sigla: Optional[str] = Field(
        default=None, description="Acrônimo do ministério ou órgão"
    )

    gastos: list[Gasto] = Relationship(back_populates="orgao")


class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: UUID = Field(default_factory=uuid8, primary_key=True)
    nome: str = Field(unique=True, index=True, description="Nome da categoria de gasto")

    gastos: list[Gasto] = Relationship(back_populates="categoria")


class Favorecido(SQLModel, table=True):
    __tablename__ = "favorecidos"

    id: UUID = Field(default_factory=uuid8, primary_key=True)
    nome: str = Field(index=True, description="Nome do favorecido do gasto")
    tipo: TipoPessoa = Field(
        default=None,
        description="Tipo do favorecido (ex: pessoa física, empresa, etc.)",
    )

    gastos: list[Gasto] = Relationship(back_populates="favorecido")
