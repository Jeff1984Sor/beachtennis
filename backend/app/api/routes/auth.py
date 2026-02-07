from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.auth import LoginRequest, RefreshRequest, TokenPair, MeResponse
from app.services.auth_service import authenticate_user
from app.core.security import decode_token, create_access_token, create_refresh_token
from app.core.errors import api_error
from app.core.deps import get_current_user
from app.models.profissional import Profissional
from app.models.aluno import Aluno
from app.models.agenda import Agenda

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


@router.get("/me", response_model=MeResponse)
async def me(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
) -> MeResponse:
    roles: list[str] = []
    perfil_nome = (current_user.perfil_acesso.nome if current_user.perfil_acesso else "").lower()
    if any(tag in perfil_nome for tag in ["admin", "gestor", "recepcao", "financeiro"]):
        roles.append("gestor")

    profissional = (
        await session.execute(
            select(Profissional).where(
                (Profissional.usuario_id == current_user.id) | (Profissional.email == current_user.email)
            )
        )
    ).scalar_one_or_none()
    if profissional:
        if "professor" in str(profissional.tipo).lower():
            roles.append("professor")
        elif "gestor" not in roles:
            roles.append("gestor")

    aluno = (await session.execute(select(Aluno).where(Aluno.email == current_user.email))).scalar_one_or_none()
    if aluno:
        roles.append("aluno")

    if not roles:
        roles = ["gestor"]
    roles = list(dict.fromkeys(roles))

    agenda = (await session.execute(select(Agenda).where(Agenda.ativa.is_(True)))).scalars().first()

    return MeResponse(
        user_id=str(current_user.id),
        nome=current_user.nome,
        email=current_user.email,
        roles=roles,
        profissional_id=str(profissional.id) if profissional else None,
        aluno_id=str(aluno.id) if aluno else None,
        unidade_id=str(current_user.unidade_id) if current_user.unidade_id else None,
        agenda_id=str(agenda.id) if agenda else None,
    )
