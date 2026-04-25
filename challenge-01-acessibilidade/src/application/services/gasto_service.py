from uuid import UUID

from src.domain.models import Gasto
from src.domain.repositories import GastoRepositoryInterface
from src.domain.schemas import GastoParams, PaginatedResponse, RespostaResumo


class GastoService:
    def __init__(self, repository: GastoRepositoryInterface):
        self.repository = repository

    def list(self, params: GastoParams) -> PaginatedResponse:
        return self.repository.list_all(params)

    def detail(self, gasto_id: UUID) -> Gasto | None:
        return self.repository.list_by_id(gasto_id)

    def summary(self, params: GastoParams) -> RespostaResumo:
        return self.repository.get_summary(params)
