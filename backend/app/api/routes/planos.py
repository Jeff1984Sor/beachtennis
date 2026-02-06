from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.deps import get_current_user
from app.core.errors import api_error
from app.schemas.plano import PlanoOut, PlanoCreate, PlanoUpdate
from app.models.plano import Plano

router = APIRouter(prefix="/planos")


@router.get("", response_model=list[PlanoOut])
async def listar(
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> list[PlanoOut]:
    result = await session.execute(select(Plano))
    return [PlanoOut.model_validate(p) for p in result.scalars()]


@router.post("", response_model=PlanoOut)
async def criar(
    payload: PlanoCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> PlanoOut:
    plano = Plano(**payload.model_dump())
    session.add(plano)
    await session.commit()
    await session.refresh(plano)
    return PlanoOut.model_validate(plano)


@router.put("/{plano_id}", response_model=PlanoOut)
async def atualizar(
    plano_id: str,
    payload: PlanoUpdate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> PlanoOut:
    result = await session.execute(select(Plano).where(Plano.id == plano_id))
    plano = result.scalar_one_or_none()
    if not plano:
        raise api_error("not_found", "Plano nao encontrado", 404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(plano, key, value)
    await session.commit()
    await session.refresh(plano)
    return PlanoOut.model_validate(plano)


@router.delete("/{plano_id}")
async def remover(
    plano_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    result = await session.execute(select(Plano).where(Plano.id == plano_id))
    plano = result.scalar_one_or_none()
    if not plano:
        raise api_error("not_found", "Plano nao encontrado", 404)
    await session.delete(plano)
    await session.commit()
    return {"status": "deleted"}