from sqlmodel import Session

from src.domain.models import Orgao
from src.infra.repository.base_repository import BaseRepository


class OrgaoRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, Orgao)
