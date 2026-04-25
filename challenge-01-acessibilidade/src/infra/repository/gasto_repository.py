from sqlmodel import Session, extract, func, select

from src.domain.models import Categoria, Gasto, Orgao
from src.domain.schemas import GastoParams as Params
from src.domain.schemas import GastoResumo, RespostaResumo
from src.infra.repository.base_repository import BaseRepository


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
        query = self._apply_filters(select(Gasto), params)
        query = query.order_by(Gasto.valor.desc()).limit(5)

        top_expenses = self.session.exec(query).all()
        result = RespostaResumo(
            gastos_por_categoria=expenses_per_category,
            top_gastos=top_expenses,
        )

        return result

    def _apply_filters(self, query, params: Params):
        if params.orgao:
            query = query.join(self.model.orgao).where(Orgao.nome == params.orgao)

        if params.ano is not None:
            query = query.where(
                extract("year", self.model.data_lancamento) == params.ano
            )

        if params.mes is not None:
            query = query.where(
                extract("month", self.model.data_lancamento) == params.mes
            )

        if params.categoria:
            query = query.join(self.model.categoria).where(
                Categoria.nome == params.categoria
            )

        if params.valor_min is not None:
            query = query.where(self.model.valor >= params.valor_min)

        if params.valor_max is not None:
            query = query.where(self.model.valor <= params.valor_max)

        return query
