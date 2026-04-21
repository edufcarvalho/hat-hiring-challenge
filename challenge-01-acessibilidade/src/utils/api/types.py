from decimal import Decimal
from typing import Optional

from fastapi_pagination import Params as BaseParams


class Params(BaseParams):
    page: int = 0
    page_size: int = 100
    orgao: Optional[str] = None
    ano: Optional[int] = None
    mes: Optional[int] = None
    categoria: Optional[str] = None
    valor_min: Optional[Decimal] = None
    valor_max: Optional[Decimal] = None
