from sqlmodel import Session

from src.domain.models import Orgao
from src.infra.repository.base_repository import BaseRepository
from src.domain.schemas import OrgaoParams as Params

class OrgaoRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, Orgao)

    def _apply_filters(self, query, params: Params):
        if params.orgao:
            return query.where(self.model.nome == params.orgao)

        return query