from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.errors import api_error
from app.core.security import decode_token
from app.models.user import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> Usuario:
    try:
        payload = decode_token(token)
    except Exception as exc:
        raise api_error("auth_invalid", "Token invalido", status.HTTP_401_UNAUTHORIZED) from exc

    if payload.get("type") != "access":
        raise api_error("auth_invalid", "Token invalido", status.HTTP_401_UNAUTHORIZED)

    user_id = payload.get("sub")
    result = await session.execute(select(Usuario).where(Usuario.id == user_id))
    user = result.scalar_one_or_none()
    if not user or not user.ativo:
        raise api_error("auth_invalid", "Usuario inativo", status.HTTP_401_UNAUTHORIZED)
    return user


def require_permission(permission: str):
    async def _checker(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        perms = current_user.perfil_acesso.permissoes if current_user.perfil_acesso else {}
        if isinstance(perms, dict):
            allowed = perms.get(permission, False) or perms.get("*", False)
        else:
            allowed = False
        if not allowed:
            raise api_error("forbidden", "Sem permissao", status.HTTP_403_FORBIDDEN)
        return current_user

    return _checker
