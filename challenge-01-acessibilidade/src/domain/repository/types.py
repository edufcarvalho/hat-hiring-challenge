from sqlmodel import Session, SQLModel, func, select


class BaseRepository:
    def __init__(self, session: Session, model: SQLModel = SQLModel):
        self.session = session
        self.model = model

    def list_all(self, offset: int = 0, limit: int = 100):
        query = select(self.model).offset(offset).limit(limit)
        result = self.session.exec(query).all()
        return result

    def count(self) -> int:
        query = select(func.count(self.model.id))
        result = self.session.exec(query).one()
        return result

    def _apply_filters(self):
        pass
