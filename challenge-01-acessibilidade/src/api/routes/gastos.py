"""Rotas para gastos públicos — implemente aqui."""
from fastapi import APIRouter

router = APIRouter()


@router.get("")
def listar_gastos():
    # TODO: Implemente com filtros (orgao, ano, mes, categoria, valor_min, valor_max) e paginação
    raise NotImplementedError


@router.get("/resumo")
def resumo_gastos():
    # TODO: Implemente com cache em memória (header X-Cache: HIT/MISS)
    raise NotImplementedError


@router.get("/{gasto_id}")
def detalhar_gasto(gasto_id: str):
    # TODO: Implemente
    raise NotImplementedError
