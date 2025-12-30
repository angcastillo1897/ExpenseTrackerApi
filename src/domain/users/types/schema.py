from datetime import datetime

from pydantic import EmailStr

from src.core.base_schema import CamelModel


class UserSerializer(CamelModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    full_name: str
    is_active: bool
    created_at: datetime
