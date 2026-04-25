from fastapi import Depends
from sqlmodel import Session

from src.application import GastoService, OrgaoService
from src.infra.database import get_session
from src.infra.repository import GastoRepository, OrgaoRepository


def get_gasto_service(
    session: Session = Depends(get_session),
) -> GastoService:
    return GastoService(GastoRepository(session))


def get_orgao_service(
    session: Session = Depends(get_session),
) -> OrgaoService:
    return OrgaoService(OrgaoRepository(session))
