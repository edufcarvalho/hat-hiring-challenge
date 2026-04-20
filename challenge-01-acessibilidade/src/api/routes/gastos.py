"""Rotas para gastos públicos — implemente aqui."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Response

from src.domain.repository.gasto_reposity import GastoRepository
from src.infra.database import get_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("")
def listar_gastos(
    response: Response,
    page: int = 0,
    page_size: int = 100,
    session=Depends(get_session),
):
    repository = GastoRepository(session)
    offset = page * page_size
    result = repository.list_all(offset, page_size)

    return result


@router.get("/resumo")
def resumo_gastos(response: Response, session=Depends(get_session)):
    repository = GastoRepository(session)
    result = repository.get_summary()

    is_hit = "HIT" if repository.get_summary.cache_info().hits > 0 else "MISS"
    response.headers["X-Cache"] = is_hit

    return result


@router.get("/{gasto_id}")
def detalhar_gasto(gasto_id: UUID, session=Depends(get_session)):
    repository = GastoRepository(session)
    result = repository.get_expense(gasto_id)

    return result
