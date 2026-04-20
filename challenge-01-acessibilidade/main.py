"""
HAT Thinking — Challenge 01: Painel de Transparência Pública
Ponto de entrada da aplicação FastAPI.
"""

from fastapi import FastAPI
from sqlmodel import select

from src.api.routes import gastos, orgaos
from src.domain.models import Orgao
from src.infra.database import create_db_and_tables, get_session
from src.infra.seed import seed_database


def lifespan(app: FastAPI):
    create_db_and_tables()
    with next(get_session()) as session:
        query = select(Orgao).limit(1)
        result = session.exec(query).first()
        if not result:
            seed_database()
    yield


app = FastAPI(
    title="HAT Challenge 01 — Transparência Pública",
    description="API para consulta de gastos públicos federais com foco em acessibilidade.",
    version="0.1.0",
    lifespan=lifespan,
)


app.include_router(gastos.router, prefix="/gastos", tags=["Gastos"])
app.include_router(orgaos.router, prefix="/orgaos", tags=["Órgãos"])


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "challenge": "01-acessibilidade"}
