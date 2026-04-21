from datetime import date

from sqlmodel import Session, SQLModel, func, select

from src.domain.models import Categoria, Gasto, Orgao
from src.utils.api.types import Params


class BaseRepository:
    def __init__(self, session: Session, model: SQLModel = SQLModel):
        self.session = session
        self.model = model

    def list_all(self, params: Params):
        query = select(self.model)
        result = self.session.exec(self._apply_filters(query, params)).all()

        return result

    def count(self) -> int:
        query = select(func.count(self.model.id))
        result = self.session.exec(query).one()
        return result

    def _apply_filters(self, query, params: Params):
        if params.orgao:
            query.where(Orgao.nome == params.orgao)

        if params.ano:
            query.where(date(Gasto.data_lancamento).year == params.ano)

        if params.mes:
            query.where(date(Gasto.data_lancamento).month == params.mes)

        if params.categoria:
            query.where(Categoria.nome == params.categoria)

        if params.valor_min:
            query.where(Gasto.valor >= params.valor_min)

        if params.valor_max:
            query.where(Gasto.valor <= params.valor_max)

        return query
