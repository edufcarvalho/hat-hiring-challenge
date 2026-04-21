"""Rotas para gastos públicos — implemente aqui."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Response

from src.domain.repository import GastoRepository
from src.infra.database import get_session
from src.utils.api.cache import cache
from src.utils.api.types import Params

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
    total = repository.count()

    return {
        "items": items,
        "total": total,
        "page": params.page,
        "size": params.page_size,
    }


@router.get("/resumo")
@cache(expire=60)
def resumo_gastos(
    response: Response, params: Params = Depends(Params), session=Depends(get_session)
):
    repository = GastoRepository(session)
    result = repository.get_summary(params)

    return result


@router.get("/{gasto_id}")
def detalhar_gasto(gasto_id: UUID, session=Depends(get_session)):
    repository = GastoRepository(session)
    result = repository.get_expense(gasto_id)

    return result
