"""
HAT Thinking — Challenge 03: Motor de Precificação de Propostas
Ponto de entrada da aplicação FastAPI.
"""
from fastapi import FastAPI
from src.api.routes import propostas
from src.infra.database import create_db_and_tables

app = FastAPI(
    title="HAT Challenge 03 — Motor de Precificação",
    description="API para criação, validação e aprovação de propostas comerciais de Professional Services.",
    version="0.1.0",
)


@app.on_event("startup")
async def startup_event():
    create_db_and_tables()


app.include_router(propostas.router, prefix="/propostas", tags=["Propostas"])


@app.get("/tabela-precos", tags=["Configuração"])
def tabela_precos():
    """Retorna a tabela de preços vigente por senioridade."""
    # TODO: Implemente este endpoint com os valores da tabela do CHALLENGE.md
    raise NotImplementedError


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "challenge": "03-precificacao"}
