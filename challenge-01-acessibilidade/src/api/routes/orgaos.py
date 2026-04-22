"""Rotas para órgãos — implemente aqui."""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.domain.schemas import Params
from src.infra.database import get_session
from src.infra.repository import OrgaoRepository

router = APIRouter()


@router.get("")
def listar_orgaos(
    params: Params = Depends(Params),
    session: Session = Depends(get_session),
):
    repository = OrgaoRepository(session)

    return repository.list_all(params)
