from typing import Protocol
from uuid import UUID

from src.domain.models import Gasto, Orgao
from src.domain.schemas import (
    GastoParams,
    OrgaoParams,
    PaginatedResponse,
    RespostaResumo,
)


class GastoRepositoryInterface(Protocol):
    def list_all(self, params: GastoParams) -> PaginatedResponse: ...

    def list_by_id(self, id: UUID) -> Gasto | None: ...

    def get_summary(self, params: GastoParams) -> RespostaResumo: ...


class OrgaoRepositoryInterface(Protocol):
    def list_all(self, params: OrgaoParams) -> PaginatedResponse: ...

    def list_by_id(self, id: UUID) -> Orgao | None: ...
