from typing import Literal, Optional

from src.core.base_schema import CamelModel


class CategoryCreateRequest(CamelModel):
    name: str
    transaction_type: Literal["income", "expense"]
    icon_name: str
    icon_bg_color: str


class CategoryUpdateRequest(CamelModel):
    name: Optional[str] = None
    icon_name: Optional[str] = None
    icon_bg_color: Optional[str] = None
