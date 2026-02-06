from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.deps import get_current_user
from app.core.errors import api_error
from app.schemas.contrato import ContratoOut, ContratoCreate, ContratoUpdate
from app.models.contrato import Contrato

router = APIRouter(prefix="/contratos")


@router.get("", response_model=list[ContratoOut])
async def listar(
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> list[ContratoOut]:
    result = await session.execute(select(Contrato))
    return [ContratoOut.model_validate(c) for c in result.scalars()]


@router.post("", response_model=ContratoOut)
async def criar(
    payload: ContratoCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> ContratoOut:
    contrato = Contrato(**payload.model_dump())
    session.add(contrato)
    await session.commit()
    await session.refresh(contrato)
    return ContratoOut.model_validate(contrato)


@router.put("/{contrato_id}", response_model=ContratoOut)
async def atualizar(
    contrato_id: str,
    payload: ContratoUpdate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> ContratoOut:
    result = await session.execute(select(Contrato).where(Contrato.id == contrato_id))
    contrato = result.scalar_one_or_none()
    if not contrato:
        raise api_error("not_found", "Contrato nao encontrado", 404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(contrato, key, value)
    await session.commit()
    await session.refresh(contrato)
    return ContratoOut.model_validate(contrato)


@router.delete("/{contrato_id}")
async def remover(
    contrato_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    result = await session.execute(select(Contrato).where(Contrato.id == contrato_id))
    contrato = result.scalar_one_or_none()
    if not contrato:
        raise api_error("not_found", "Contrato nao encontrado", 404)
    await session.delete(contrato)
    await session.commit()
    return {"status": "deleted"}