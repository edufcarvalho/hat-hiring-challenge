from sqlmodel import Session, select

from src.domain.models import Orgao


class OrgaoRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self, page: int = 0, page_size: int = 100):
        offset = page * page_size

        query = select(Orgao).offset(offset).limit(page_size)
        result = self.session.exec(query).all()
        return result
