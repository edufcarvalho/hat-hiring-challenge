from src.domain.repositories import OrgaoRepositoryInterface
from src.domain.schemas import OrgaoParams, PaginatedResponse


class OrgaoService:
    def __init__(self, repository: OrgaoRepositoryInterface):
        self.repository = repository

    def list(self, params: OrgaoParams) -> PaginatedResponse:
        return self.repository.list_all(params)
