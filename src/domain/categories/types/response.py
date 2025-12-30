from src.core.base_schema import CamelModel


class CategoryResponse(CamelModel):
    id: int
    name: str
    transaction_type: str
    user_id: int
    icon_name: str | None
    icon_bg_color: str | None
