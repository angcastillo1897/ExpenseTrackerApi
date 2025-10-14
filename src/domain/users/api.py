# Presentation layer (HTTP routes, request/response handling).
#! TODO
# GET /user/profile or GET /user/me - Get current user info
# PUT /user/profile - Update user profile
# PATCH /user/profile - Partial profile updates
# POST /user/change-password - Change password (requires current password)
# GET /user/sessions - List active sessions/devices
# DELETE /user/sessions/{session_id} - Revoke specific session


from fastapi import APIRouter

from src.core.dependencies.async_bd import AsyncSessionDepends
from src.core.dependencies.auth_user import AuthUserDepends

from . import service, types

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/profile", response_model=types.UserSerializer)
async def get_user_profile(user: AuthUserDepends, db: AsyncSessionDepends):
    return await service.get_user_profile(db, user.id)
