"""Rotas para gastos públicos — implemente aqui."""

import logging

from fastapi import APIRouter, Depends, Response

from src.domain.repository.gasto_reposity import GastoRepository
from src.infra.database import get_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("")
def listar_gastos(
    response: Response,
    offset: int = 0,
    limit: int = 100,
    session=Depends(get_session),
):
    repository = GastoRepository(session)
    result = repository.list_all(offset, limit)
    # logger.info(f"Cache info: {repository.list_all.cache_info()}")
    cache_status = "HIT" if repository.list_all.cache_info().hits > 0 else "MISS"
    response.headers["X-Cache-Status"] = cache_status
    return result


@router.get("/resumo")
def resumo_gastos():
    logger.info(f"Cache info: {resumo_gastos.cache_info()}")
    # TODO: Implemente com cache em memória (header X-Cache: HIT/MISS)
    raise NotImplementedError


@router.get("/{gasto_id}")
def detalhar_gasto(gasto_id: str):
    # TODO: Implemente
    raise NotImplementedError
