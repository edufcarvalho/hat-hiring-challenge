"""Rotas para órgãos — implemente aqui."""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.domain.repository.orgao_repository import OrgaoRepository
from src.infra.database import get_session

router = APIRouter()


@router.get("")
def listar_orgaos(session: Session = Depends(get_session)):
    repository = OrgaoRepository(session)

    return repository.list_all()
