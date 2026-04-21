from typing import Any

from pydantic import BaseModel
from sqlmodel import Session, SQLModel, extract, func, select

from src.domain.models import Categoria, Gasto, Orgao
from src.utils.api.types import Params


class PaginatedResponse(BaseModel):
    items: Any
    total: int
    page: int
    size: int


# from pdb import breakpoint
class BaseRepository:
    def __init__(self, session: Session, model: SQLModel = SQLModel):
        self.session = session
        self.model = model

    def list_all(self, params: Params):
        query = select(self.model)
        # breakpoint()
        return self._apply_filters_and_paginate(query, params)

    def count(self) -> int:
        query = select(func.count(self.model.id))
        result = self.session.exec(query).one()
        return result

    def _paginate(self, query, params: Params):
        offset = params.page * params.page_size

        query = query.offset(offset).limit(10)
        result = self.session.exec(query).all()

        return PaginatedResponse(
            items=result,
            total=self.count(),
            page=params.page,
            size=params.page_size,
        )

    def _apply_filters(self, query, params: Params):
        if params.orgao:
            query = query.where(Orgao.nome == params.orgao)

        if params.ano:
            query = query.where(extract("year", Gasto.data_lancamento) == params.ano)

        if params.mes:
            query = query.where(extract("month", Gasto.data_lancamento) == params.mes)

        if params.categoria:
            query = query.where(Categoria.nome == params.categoria)

        if params.valor_min:
            query = query.where(Gasto.valor >= params.valor_min)

        if params.valor_max:
            query = query.where(Gasto.valor <= params.valor_max)

        return query

    def _apply_filters_and_paginate(self, query, params):
        return self._paginate(self._apply_filters(query, params), params)
