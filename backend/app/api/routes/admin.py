from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.deps import get_current_user
from app.core.errors import api_error
from app.models import (
    Endereco,
    EmpresaConfig,
    MediaFile,
    PerfilAcesso,
    Usuario,
    Profissional,
    Unidade,
    Agenda,
    AgendaUnidade,
    Plano,
    Aluno,
    Contrato,
    DisponibilidadeAgenda,
    DisponibilidadeUnidadeOverride,
    BloqueioAgenda,
    Aula,
    MensagemWhatsApp,
    ModeloContrato,
    VariavelContrato,
    CategoriaFinanceira,
    SubcategoriaFinanceira,
    ContaBancaria,
    ContaReceber,
    ContaPagar,
    MovimentoBancario,
    RegraComissao,
    ExecucaoRotina,
)

router = APIRouter(prefix="/admin")

RESOURCE_MAP = {
    "enderecos": Endereco,
    "empresa_config": EmpresaConfig,
    "media_files": MediaFile,
    "perfis_acesso": PerfilAcesso,
    "usuarios": Usuario,
    "profissionais": Profissional,
    "unidades": Unidade,
    "agendas": Agenda,
    "agenda_unidades": AgendaUnidade,
    "planos": Plano,
    "alunos": Aluno,
    "contratos": Contrato,
    "disponibilidades_agenda": DisponibilidadeAgenda,
    "disponibilidades_unidade_override": DisponibilidadeUnidadeOverride,
    "bloqueios_agenda": BloqueioAgenda,
    "aulas": Aula,
    "mensagens_whatsapp": MensagemWhatsApp,
    "modelos_contrato": ModeloContrato,
    "variaveis_contrato": VariavelContrato,
    "categorias_financeiras": CategoriaFinanceira,
    "subcategorias_financeiras": SubcategoriaFinanceira,
    "contas_bancarias": ContaBancaria,
    "contas_receber": ContaReceber,
    "contas_pagar": ContaPagar,
    "movimentos_bancarios": MovimentoBancario,
    "regras_comissao": RegraComissao,
    "execucoes_rotina": ExecucaoRotina,
}


def get_model(resource: str):
    model = RESOURCE_MAP.get(resource)
    if not model:
        raise api_error("not_found", "Recurso nao encontrado", 404)
    return model


@router.get("/{resource}")
async def list_resource(
    resource: str,
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    model = get_model(resource)
    result = await session.execute(select(model).limit(limit).offset(offset))
    return [row.__dict__ for row in result.scalars()]


@router.get("/{resource}/{item_id}")
async def get_resource(
    resource: str,
    item_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    model = get_model(resource)
    result = await session.execute(select(model).where(model.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise api_error("not_found", "Item nao encontrado", 404)
    return item.__dict__


@router.post("/{resource}")
async def create_resource(
    resource: str,
    payload: dict,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    model = get_model(resource)
    payload.pop("id", None)
    item = model(**payload)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item.__dict__


@router.put("/{resource}/{item_id}")
async def update_resource(
    resource: str,
    item_id: str,
    payload: dict,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    model = get_model(resource)
    result = await session.execute(select(model).where(model.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise api_error("not_found", "Item nao encontrado", 404)
    for key, value in payload.items():
        if key == "id":
            continue
        setattr(item, key, value)
    await session.commit()
    await session.refresh(item)
    return item.__dict__


@router.delete("/{resource}/{item_id}")
async def delete_resource(
    resource: str,
    item_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    model = get_model(resource)
    result = await session.execute(select(model).where(model.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise api_error("not_found", "Item nao encontrado", 404)
    await session.delete(item)
    await session.commit()
    return {"status": "deleted"}