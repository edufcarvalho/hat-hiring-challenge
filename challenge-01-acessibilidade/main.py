"""
HAT Thinking — Challenge 01: Painel de Transparência Pública
Ponto de entrada da aplicação FastAPI.
"""
from fastapi import FastAPI
from src.api.routes import gastos, orgaos
from src.infra.database import create_db_and_tables

app = FastAPI(
    title="HAT Challenge 01 — Transparência Pública",
    description="API para consulta de gastos públicos federais com foco em acessibilidade.",
    version="0.1.0",
)


@app.on_event("startup")
async def startup_event():
    create_db_and_tables()


app.include_router(gastos.router, prefix="/gastos", tags=["Gastos"])
app.include_router(orgaos.router, prefix="/orgaos", tags=["Órgãos"])


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "challenge": "01-acessibilidade"}
