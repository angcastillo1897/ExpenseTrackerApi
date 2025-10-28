from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: int
    name: str
    transaction_type: str
    user_id: int
    icon_name: str | None
    icon_bg_color: str | None

    class Config:
        from_attributes = True
