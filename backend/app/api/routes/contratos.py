from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, cast, String

from app.core.database import get_session
from app.core.deps import get_current_user
from app.core.errors import api_error
from app.schemas.contrato import ContratoOut, ContratoCreate, ContratoUpdate, ContratoListOut
from app.models.contrato import Contrato
from app.models.aluno import Aluno
from app.services.contrato_template_service import render_template, build_context

router = APIRouter(prefix="/contratos")


class PreviewRequest(BaseModel):
    content_html: str
    data: dict | None = None
    contrato_id: str | None = None
    aluno_id: str | None = None
    unidade_id: str | None = None
    plano_id: str | None = None


class PreviewResponse(BaseModel):
    rendered_html: str


@router.get("", response_model=list[ContratoListOut])
async def listar(
    search: str | None = None,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> list[ContratoListOut]:
    query = select(Contrato, Aluno.nome).join(Aluno, Aluno.id == Contrato.aluno_id)
    if search:
        pattern = f"%{search}%"
        query = query.where(or_(Aluno.nome.ilike(pattern), cast(Contrato.id, String).ilike(pattern)))
    result = await session.execute(query)
    items = []
    for contrato, aluno_nome in result.all():
        base = ContratoListOut.model_validate(contrato).model_dump()
        base["aluno_nome"] = aluno_nome
        items.append(ContratoListOut(**base))
    return items


@router.get("/{contrato_id}", response_model=ContratoOut)
async def obter(
    contrato_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> ContratoOut:
    result = await session.execute(select(Contrato).where(Contrato.id == contrato_id))
    contrato = result.scalar_one_or_none()
    if not contrato:
        raise api_error("not_found", "Contrato nao encontrado", 404)
    return ContratoOut.model_validate(contrato)


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


@router.post("/preview", response_model=PreviewResponse)
async def preview(
    payload: PreviewRequest,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> PreviewResponse:
    context = await build_context(
        session=session,
        contrato_id=payload.contrato_id,
        aluno_id=payload.aluno_id,
        unidade_id=payload.unidade_id,
        plano_id=payload.plano_id,
    )
    if payload.data:
        context.update(payload.data)
    rendered = render_template(payload.content_html, context)
    return PreviewResponse(rendered_html=rendered)