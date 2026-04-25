from typing import Any, Optional
from uuid import UUID

from sqlmodel import Session, SQLModel, func, select

from src.domain.schemas import PaginatedParams as Params
from src.domain.schemas import PaginatedResponse as Response


class BaseRepository:
    def __init__(self, session: Session, model: type[SQLModel] = SQLModel):
        self.session = session
        self.model = model

    def list_all(self, params: Params) -> Response:
        query = select(self.model)
        return self._apply_filters_and_paginate(query, params)

    def list_by_id(self, id: UUID) -> SQLModel | None:
        query = select(self.model).where(self.model.id == id).limit(1)
        object = self.session.exec(query).first()

        return object

    def count(self, params: Optional[Params] = None) -> int:
        query = select(func.count(self.model.id))

        if params:
            query = self._apply_filters(query, params)

        result = self.session.exec(query).one()
        return result

    def _paginate(self, query: Any, params: Params) -> Response:
        offset = params.page * params.page_size

        query = query.offset(offset).limit(params.page_size).order_by(self.model.id)
        result = self.session.exec(query).all()

        return Response(
            items=result,
            total=self.count(params),
            page=params.page,
            size=params.page_size,
        )

    def _apply_filters(self, query, params: Params) -> Any:
        return query

    def _apply_filters_and_paginate(self, query, params: Params) -> Response:
        return self._paginate(self._apply_filters(query, params), params)
