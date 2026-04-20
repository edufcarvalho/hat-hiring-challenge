from cachetools import TTLCache, cached
from cachetools.keys import hashkey
from sqlmodel import Session, select

from src.domain.models import Gasto


class GastoRepository:
    _cache = TTLCache(maxsize=100, ttl=60)

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def _make_key(_, offset: int, limit: int):
        return hashkey(offset, limit)

    @cached(cache=_cache, key=_make_key, info=True)
    def list_all(self, offset: int = 0, limit: int = 100):
        query = select(Gasto).offset(offset).limit(limit)
        result = self.session.exec(query).all()
        return result

    def get_summary(self):
        raise NotImplementedError

    def get_expense(self, gasto_id: int):
        raise NotImplementedError
