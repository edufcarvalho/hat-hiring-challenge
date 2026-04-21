"""Rotas para gastos públicos — implemente aqui."""

import logging
import os
from uuid import UUID

from fastapi import APIRouter, Depends, Response

from src.domain.repository import GastoRepository
from src.infra.cache import cache
from src.infra.database import get_session
from src.utils.api.schemas import Params

CACHE_TTU = os.getenv("CACHE_TTU", 60)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("")
def listar_gastos(
    params: Params = Depends(Params),
    session=Depends(get_session),
):
    repository = GastoRepository(session)
    items = repository.list_all(params)

    return items


@router.get("/resumo")
@cache(expire=CACHE_TTU)
def resumo_gastos(
    response: Response, params: Params = Depends(Params), session=Depends(get_session)
):
    repository = GastoRepository(session)
    result = repository.get_summary(params)

    return result


@router.get("/{gasto_id}")
def detalhar_gasto(gasto_id: UUID, session=Depends(get_session)):
    repository = GastoRepository(session)
    result = repository.list_by_id(gasto_id)

    return result
