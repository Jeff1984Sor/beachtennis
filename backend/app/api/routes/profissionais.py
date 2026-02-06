from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.deps import get_current_user
from app.core.errors import api_error
from app.schemas.profissional import ProfissionalOut, ProfissionalCreate, ProfissionalUpdate
from app.models.profissional import Profissional

router = APIRouter(prefix="/profissionais")


@router.get("", response_model=list[ProfissionalOut])
async def listar(
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> list[ProfissionalOut]:
    result = await session.execute(select(Profissional))
    return [ProfissionalOut.model_validate(p) for p in result.scalars()]


@router.post("", response_model=ProfissionalOut)
async def criar(
    payload: ProfissionalCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> ProfissionalOut:
    profissional = Profissional(**payload.model_dump())
    session.add(profissional)
    await session.commit()
    await session.refresh(profissional)
    return ProfissionalOut.model_validate(profissional)


@router.put("/{profissional_id}", response_model=ProfissionalOut)
async def atualizar(
    profissional_id: str,
    payload: ProfissionalUpdate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> ProfissionalOut:
    result = await session.execute(select(Profissional).where(Profissional.id == profissional_id))
    profissional = result.scalar_one_or_none()
    if not profissional:
        raise api_error("not_found", "Profissional nao encontrado", 404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(profissional, key, value)
    await session.commit()
    await session.refresh(profissional)
    return ProfissionalOut.model_validate(profissional)


@router.delete("/{profissional_id}")
async def remover(
    profissional_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    result = await session.execute(select(Profissional).where(Profissional.id == profissional_id))
    profissional = result.scalar_one_or_none()
    if not profissional:
        raise api_error("not_found", "Profissional nao encontrado", 404)
    await session.delete(profissional)
    await session.commit()
    return {"status": "deleted"}


@router.get("/{profissional_id}/comissao/resumo")
async def resumo_comissao(
    profissional_id: str,
    mes: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    # Placeholder: resumo detalhado pode ser implementado com regras/contas
    return {"profissional_id": profissional_id, "mes": mes, "total": 0}