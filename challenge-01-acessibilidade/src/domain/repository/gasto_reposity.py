import logging
import time
from datetime import datetime
from typing import Optional
from uuid import UUID

from cachetools import TTLCache, cached
from cachetools.keys import hashkey
from sqlmodel import Session, func, select

from src.domain.models import Categoria, Gasto, GastoResumo, RespostaResumo

logger = logging.getLogger("uvicorn.error")


class GastoRepository:
    _cache = TTLCache(maxsize=100, ttl=60, timer=time.time)

    def __init__(self, session: Session):
        self.session = session

    @classmethod
    def clear_cache(cls):
        cls._cache.clear()

    @staticmethod
    def _make_key(_, *args):
        return hashkey(args)

    def list_all(self, offset: int = 0, limit: int = 100):
        query = select(Gasto).offset(offset).limit(limit)
        result = self.session.exec(query).all()
        return result

    @cached(cache=_cache, key=_make_key, info=True)
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
