"""
HAT Thinking — Challenge 02: Motor de Rotas Sustentáveis
Ponto de entrada da aplicação FastAPI.
"""

from fastapi import FastAPI

from src.api.routes import rotas

app = FastAPI(
    title="HAT Challenge 02 — Rotas Sustentáveis",
    description="API para cálculo de rotas de menor emissão de carbono para frotas urbanas.",
    version="0.1.0",
)

app.include_router(rotas.router, prefix="/rotas", tags=["Rotas"])


@app.get("/veiculos/perfis", tags=["Veículos"])
def listar_perfis():
    """Retorna os perfis de veículo disponíveis com seus fatores de emissão."""
    # TODO: Implemente este endpoint
    raise NotImplementedError


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "challenge": "02-sustentabilidade"}
