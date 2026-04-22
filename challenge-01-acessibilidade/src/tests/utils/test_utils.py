import unittest
from datetime import date
from decimal import Decimal

from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from src.domain.enums import TipoPessoa
from src.domain.models import Categoria, Favorecido, Gasto, Orgao
from src.infra.database import set_engine
from src.utils.repository.types import BaseRepository


class BaseTest(unittest.TestCase):
    def setUp(self, model=None):
        self.session, self.fixtures = self.create_test_session()
        self.engine = self.session.get_bind()
        set_engine(self.engine)

        if model:
            self.repository = BaseRepository(self.session, model)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def create_test_session(self) -> tuple[Session, dict[str, list[object]]]:
        engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        SQLModel.metadata.create_all(engine)

        session = Session(engine)

        orgaos = [
            Orgao(nome="Ministerio A", sigla="MA"),
            Orgao(nome="Ministerio B", sigla="MB"),
        ]
        categorias = [
            Categoria(nome="Categoria A"),
            Categoria(nome="Categoria B"),
        ]
        favorecidos = [
            Favorecido(nome="Favorecido 1", tipo=TipoPessoa.FISICA),
            Favorecido(nome="Favorecido 2", tipo=TipoPessoa.JURIDICA),
        ]
        gastos = [
            Gasto(
                orgao=orgaos[0],
                categoria=categorias[0],
                favorecido=favorecidos[0],
                descricao="Compra 1",
                valor=Decimal("10.00"),
                data_lancamento=date(2024, 1, 10),
            ),
            Gasto(
                orgao=orgaos[0],
                categoria=categorias[1],
                favorecido=favorecidos[0],
                descricao="Compra 2",
                valor=Decimal("40.00"),
                data_lancamento=date(2024, 1, 11),
            ),
            Gasto(
                orgao=orgaos[1],
                categoria=categorias[0],
                favorecido=favorecidos[1],
                descricao="Compra 3",
                valor=Decimal("20.00"),
                data_lancamento=date(2024, 1, 12),
            ),
            Gasto(
                orgao=orgaos[1],
                categoria=categorias[1],
                favorecido=favorecidos[1],
                descricao="Compra 4",
                valor=Decimal("15.00"),
                data_lancamento=date(2024, 1, 13),
            ),
            Gasto(
                orgao=orgaos[0],
                categoria=categorias[0],
                favorecido=favorecidos[0],
                descricao="Compra 5",
                valor=Decimal("60.00"),
                data_lancamento=date(2024, 3, 14),
            ),
            Gasto(
                orgao=orgaos[1],
                categoria=categorias[1],
                favorecido=favorecidos[1],
                descricao="Compra 6",
                valor=Decimal("25.00"),
                data_lancamento=date(2024, 2, 15),
            ),
        ]

        session.add_all(orgaos)
        session.add_all(categorias)
        session.add_all(favorecidos)
        session.add_all(gastos)
        session.commit()

        return session, {
            "orgaos": orgaos,
            "categorias": categorias,
            "favorecidos": favorecidos,
            "gastos": gastos,
        }
