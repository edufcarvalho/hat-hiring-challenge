import logging
from uuid import UUID

from sqlmodel import Session, func, select

from src.domain.models import Categoria, Gasto, GastoResumo, RespostaResumo
from src.utils.api.types import Params
from src.utils.repository.types import BaseRepository

logger = logging.getLogger("uvicorn.error")


class GastoRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, Gasto)

    def get_summary(
        self,
        params: Params,
    ) -> RespostaResumo:
        query = (
            select(
                Categoria.nome.label("nome_categoria"),
                func.sum(Gasto.valor).label("gasto_total"),
            )
            .select_from(Gasto)
            .join(Categoria)
            .group_by(Categoria.id, Categoria.nome)
        )

        result = self.session.exec(self._apply_filters(query, params)).all()

        expenses_per_category = [
            GastoResumo(nome_categoria=row[0], gasto_total=row[1]) for row in result
        ]

        # Get top 5 expenses with filters applied
        query = select(Gasto)
        query = self._apply_filters(select(Gasto), params)
        query = query.order_by(Gasto.valor.desc()).limit(5)

        top_expenses = self.session.exec(query).all()
        result = RespostaResumo(
            gastos_por_categoria=expenses_per_category,
            top_gastos=top_expenses,
        )

        return result

    def get_expense(self, gasto_id: UUID):
        query = select(Gasto).where(Gasto.id == gasto_id).limit(1)
        expense = self.session.exec(query).first()

        return expense
