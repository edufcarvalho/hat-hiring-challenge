"""Rotas para gastos públicos — implemente aqui."""

import os
from uuid import UUID

from fastapi import APIRouter, Depends, Response

from src.api.tools import get_gasto_service
from src.application import GastoService
from src.domain.schemas import GastoParams as Params
from src.infra.cache import cache

CACHE_TTU = os.getenv("CACHE_TTU", 60)


router = APIRouter()


@router.get("")
def listar_gastos(
    params: Params = Depends(Params),
    service: GastoService = Depends(get_gasto_service),
):
    return service.list(params)


@router.get("/resumo")
@cache(expire=CACHE_TTU)
def resumo_gastos(
    response: Response,
    params: Params = Depends(Params),
    service: GastoService = Depends(get_gasto_service),
):
    return service.summary(params)


@router.get("/{gasto_id}")
def detalhar_gasto(
    gasto_id: UUID,
    service: GastoService = Depends(get_gasto_service),
):
    return service.detail(gasto_id)
