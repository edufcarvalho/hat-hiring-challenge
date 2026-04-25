"""Rotas para órgãos — implemente aqui."""

from fastapi import APIRouter, Depends

from src.api.tools import get_orgao_service
from src.application import OrgaoService
from src.domain.schemas import OrgaoParams as Params

router = APIRouter()


@router.get("")
def listar_orgaos(
    params: Params = Depends(Params),
    service: OrgaoService = Depends(get_orgao_service),
):
    return service.list(params)
