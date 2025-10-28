from typing import Literal, Optional

from pydantic import BaseModel


class CategoryCreateRequest(BaseModel):
    name: str
    transaction_type: Literal["income", "expense"]
    icon_name: str
    icon_bg_color: str


class CategoryUpdateRequest(BaseModel):
    name: Optional[str] = None
    icon_name: Optional[str] = None
    icon_bg_color: Optional[str] = None
