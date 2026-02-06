from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, create_access_token, create_refresh_token
from app.core.errors import api_error
from app.models.user import Usuario


async def authenticate_user(session: AsyncSession, email: str, password: str) -> tuple[str, str]:
    result = await session.execute(select(Usuario).where(Usuario.email == email))
    user = result.scalar_one_or_none()
    if not user or not user.ativo:
        raise api_error("auth_invalid", "Credenciais invalidas", 401)
    if not verify_password(password, user.senha_hash):
        raise api_error("auth_invalid", "Credenciais invalidas", 401)

    user.last_login_at = datetime.utcnow()
    await session.commit()

    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))
    return access, refresh