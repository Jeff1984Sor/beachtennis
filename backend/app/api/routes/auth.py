from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.auth import LoginRequest, RefreshRequest, TokenPair
from app.services.auth_service import authenticate_user
from app.core.security import decode_token, create_access_token, create_refresh_token
from app.core.errors import api_error

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_session)) -> TokenPair:
    access, refresh = await authenticate_user(session, payload.email, payload.password)
    return TokenPair(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenPair)
async def refresh(payload: RefreshRequest) -> TokenPair:
    try:
        data = decode_token(payload.refresh_token)
    except Exception as exc:
        raise api_error("auth_invalid", "Refresh token invalido", 401) from exc
    if data.get("type") != "refresh":
        raise api_error("auth_invalid", "Refresh token invalido", 401)
    subject = data.get("sub")
    return TokenPair(access_token=create_access_token(subject), refresh_token=create_refresh_token(subject))