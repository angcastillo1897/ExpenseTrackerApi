from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserSerializer(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
