# DTOs / validation (Pydantic).

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class RegisterResponse(BaseModel):
    user: UserRead
    access_token: str
    refresh_token: str
