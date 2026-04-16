"""Rotas para cálculo de rotas sustentáveis — implemente aqui."""
from fastapi import APIRouter

router = APIRouter()


@router.post("/calcular")
def calcular_rota():
    # TODO: Algoritmo de menor emissão. Exato para <=8 paradas, heurístico para 9-15.
    # Resposta deve incluir campo "algoritmo_usado": "exato" | "heuristico"
    raise NotImplementedError


@router.post("/comparar")
def comparar_rotas():
    # TODO: Retorne menor emissão vs. menor distância com diferença percentual de CO₂
    raise NotImplementedError
