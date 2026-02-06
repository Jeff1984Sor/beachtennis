from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.deps import get_current_user
from app.core.errors import api_error
from app.schemas.regra_comissao import RegraComissaoOut, RegraComissaoCreate, RegraComissaoUpdate
from app.models.regra_comissao import RegraComissao
from app.services.comissao_service import gerar_comissoes

router = APIRouter()


@router.get("/regras-comissao", response_model=list[RegraComissaoOut])
async def listar_regras(
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> list[RegraComissaoOut]:
    result = await session.execute(select(RegraComissao))
    return [RegraComissaoOut.model_validate(r) for r in result.scalars()]


@router.post("/regras-comissao", response_model=RegraComissaoOut)
async def criar_regra(
    payload: RegraComissaoCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> RegraComissaoOut:
    regra = RegraComissao(**payload.model_dump())
    session.add(regra)
    await session.commit()
    await session.refresh(regra)
    return RegraComissaoOut.model_validate(regra)


@router.put("/regras-comissao/{regra_id}", response_model=RegraComissaoOut)
async def atualizar_regra(
    regra_id: str,
    payload: RegraComissaoUpdate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> RegraComissaoOut:
    result = await session.execute(select(RegraComissao).where(RegraComissao.id == regra_id))
    regra = result.scalar_one_or_none()
    if not regra:
        raise api_error("not_found", "Regra nao encontrada", 404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(regra, key, value)
    await session.commit()
    await session.refresh(regra)
    return RegraComissaoOut.model_validate(regra)


@router.delete("/regras-comissao/{regra_id}")
async def remover_regra(
    regra_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    result = await session.execute(select(RegraComissao).where(RegraComissao.id == regra_id))
    regra = result.scalar_one_or_none()
    if not regra:
        raise api_error("not_found", "Regra nao encontrada", 404)
    await session.delete(regra)
    await session.commit()
    return {"status": "deleted"}


@router.post("/comissoes/gerar")
async def gerar(
    unidade_id: str,
    mes: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    total = await gerar_comissoes(session, unidade_id, mes)
    return {"status": "ok", "total": total}