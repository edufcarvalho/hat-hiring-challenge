import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Session, func, select

from src.domain.models import Categoria, Gasto, GastoResumo, RespostaResumo
from src.utils.repository.types import BaseRepository

logger = logging.getLogger("uvicorn.error")


class GastoRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, Gasto)

    def get_summary(
        self,
        start_date: Optional[datetime] = datetime.min,
        end_date: Optional[datetime] = datetime.max,
    ) -> list[GastoResumo]:
        query = (
            select(
                Categoria.nome.label("nome_categoria"),
                func.sum(Gasto.valor).label("gasto_total"),
            )
            .join(Gasto.categoria)
            .group_by(Categoria.id, Categoria.nome)
        )

        result = self.session.exec(query).all()

        expenses_per_category = [
            GastoResumo(nome_categoria=row[0], gasto_total=row[1]) for row in result
        ]

        query = (
            select(Gasto)
            .where(Gasto.data_lancamento.between(start_date, end_date))
            .order_by(Gasto.valor.desc())
            .limit(5)
        )

        result = RespostaResumo(
            gastos_por_categoria=expenses_per_category,
            top_gastos=self.session.exec(query).all(),
        )

        return result

    def get_expense(self, gasto_id: UUID):
        query = select(Gasto).where(Gasto.id == gasto_id).limit(1)
        expense = self.session.exec(query).first()

        return expense
