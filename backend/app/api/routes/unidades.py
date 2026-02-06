from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.deps import get_current_user
from app.core.errors import api_error
from app.schemas.unidade import UnidadeOut, UnidadeCreate, UnidadeUpdate
from app.models.unidade import Unidade

router = APIRouter(prefix="/unidades")


@router.get("", response_model=list[UnidadeOut])
async def listar(
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> list[UnidadeOut]:
    result = await session.execute(select(Unidade))
    return [UnidadeOut.model_validate(u) for u in result.scalars()]


@router.post("", response_model=UnidadeOut)
async def criar(
    payload: UnidadeCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> UnidadeOut:
    unidade = Unidade(**payload.model_dump())
    session.add(unidade)
    await session.commit()
    await session.refresh(unidade)
    return UnidadeOut.model_validate(unidade)


@router.put("/{unidade_id}", response_model=UnidadeOut)
async def atualizar(
    unidade_id: str,
    payload: UnidadeUpdate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> UnidadeOut:
    result = await session.execute(select(Unidade).where(Unidade.id == unidade_id))
    unidade = result.scalar_one_or_none()
    if not unidade:
        raise api_error("not_found", "Unidade nao encontrada", 404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(unidade, key, value)
    await session.commit()
    await session.refresh(unidade)
    return UnidadeOut.model_validate(unidade)


@router.delete("/{unidade_id}")
async def remover(
    unidade_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    result = await session.execute(select(Unidade).where(Unidade.id == unidade_id))
    unidade = result.scalar_one_or_none()
    if not unidade:
        raise api_error("not_found", "Unidade nao encontrada", 404)
    await session.delete(unidade)
    await session.commit()
    return {"status": "deleted"}