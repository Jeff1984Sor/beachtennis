from datetime import date, datetime, time, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.deps import get_current_user
from app.models.aluno import Aluno
from app.models.aula import Aula
from app.models.conta_pagar import ContaPagar
from app.models.conta_receber import ContaReceber
from app.models.contrato import Contrato
from app.models.mensagem_whatsapp import MensagemWhatsApp
from app.models.profissional import Profissional
from app.models.unidade import Unidade
from app.models.user import Usuario
from app.models.enums import ContaStatus

router = APIRouter(prefix="/mobile")


def _roles_for_user(user: Usuario, profissional: Profissional | None, aluno: Aluno | None) -> list[str]:
    roles: list[str] = []
    perfil_nome = (user.perfil_acesso.nome if user.perfil_acesso else "").lower()
    if any(tag in perfil_nome for tag in ["admin", "gestor", "recepcao", "financeiro"]):
        roles.append("gestor")
    if profissional and "professor" in str(profissional.tipo).lower():
        roles.append("professor")
    if aluno:
        roles.append("aluno")
    if not roles:
        roles.append("gestor")
    return list(dict.fromkeys(roles))


async def _identity(session: AsyncSession, user: Usuario) -> tuple[list[str], Profissional | None, Aluno | None]:
    profissional = (
        await session.execute(
            select(Profissional).where((Profissional.usuario_id == user.id) | (Profissional.email == user.email))
        )
    ).scalar_one_or_none()
    aluno = (await session.execute(select(Aluno).where(Aluno.email == user.email))).scalar_one_or_none()
    return _roles_for_user(user, profissional, aluno), profissional, aluno


@router.get("/agenda-dia")
async def agenda_dia(
    dia: date | None = None,
    session: AsyncSession = Depends(get_session),
    user: Usuario = Depends(get_current_user),
):
    roles, profissional, aluno = await _identity(session, user)
    day = dia or date.today()
    start_dt = datetime.combine(day, time.min)
    end_dt = datetime.combine(day, time.max)

    query = (
        select(Aula, Aluno.nome, Profissional.nome, Unidade.nome)
        .join(Aluno, Aluno.id == Aula.aluno_id)
        .join(Unidade, Unidade.id == Aula.unidade_id)
        .outerjoin(Profissional, Profissional.id == Aula.profissional_id)
        .where(and_(Aula.inicio >= start_dt, Aula.inicio <= end_dt))
        .order_by(Aula.inicio.asc())
    )
    if "gestor" not in roles:
        if "professor" in roles and profissional:
            query = query.where(Aula.profissional_id == profissional.id)
        elif "aluno" in roles and aluno:
            query = query.where(Aula.aluno_id == aluno.id)

    result = await session.execute(query)
    aulas = []
    for aula, aluno_nome, professor_nome, unidade_nome in result.all():
        aulas.append(
            {
                "id": str(aula.id),
                "inicio": aula.inicio,
                "fim": aula.fim,
                "status": str(aula.status.value if hasattr(aula.status, "value") else aula.status),
                "aluno_id": str(aula.aluno_id),
                "aluno_nome": aluno_nome,
                "profissional_id": str(aula.profissional_id) if aula.profissional_id else None,
                "professor_nome": professor_nome,
                "unidade_id": str(aula.unidade_id),
                "unidade_nome": unidade_nome,
            }
        )

    return {"dia": day.isoformat(), "aulas": aulas, "roles": roles}


@router.get("/financeiro")
async def financeiro(
    tipo: str = "receber",
    inicio: date | None = None,
    fim: date | None = None,
    session: AsyncSession = Depends(get_session),
    user: Usuario = Depends(get_current_user),
):
    roles, profissional, aluno = await _identity(session, user)
    start = inicio or (date.today().replace(day=1))
    finish = fim or (start + timedelta(days=40)).replace(day=1) - timedelta(days=1)

    if tipo == "pagar":
        query = select(ContaPagar).where(and_(ContaPagar.data_vencimento >= start, ContaPagar.data_vencimento <= finish))
        if "gestor" not in roles and profissional:
            query = query.where(ContaPagar.profissional_id == profissional.id)
        rows = (await session.execute(query.order_by(ContaPagar.data_vencimento.asc()))).scalars().all()
        items = [
            {
                "id": str(c.id),
                "descricao": c.descricao,
                "valor": float(c.valor),
                "status": str(c.status.value if hasattr(c.status, "value") else c.status),
                "data_vencimento": c.data_vencimento.isoformat(),
                "fornecedor_nome": c.fornecedor_nome,
                "profissional_id": str(c.profissional_id) if c.profissional_id else None,
            }
            for c in rows
        ]
    else:
        query = select(ContaReceber).where(and_(ContaReceber.data_vencimento >= start, ContaReceber.data_vencimento <= finish))
        if "aluno" in roles and aluno:
            query = query.where(ContaReceber.aluno_id == aluno.id)
        rows = (await session.execute(query.order_by(ContaReceber.data_vencimento.asc()))).scalars().all()
        items = [
            {
                "id": str(c.id),
                "descricao": c.descricao,
                "valor": float(c.valor),
                "status": str(c.status.value if hasattr(c.status, "value") else c.status),
                "data_vencimento": c.data_vencimento.isoformat(),
                "aluno_id": str(c.aluno_id),
            }
            for c in rows
        ]

    previsto = sum(i["valor"] for i in items)
    pago = sum(i["valor"] for i in items if i["status"] == ContaStatus.pago.value)
    return {
        "tipo": tipo,
        "inicio": start.isoformat(),
        "fim": finish.isoformat(),
        "total_previsto": previsto,
        "total_pago": pago,
        "itens": items,
        "roles": roles,
    }


@router.get("/alunos")
async def mobile_alunos(
    limit: int = 50,
    session: AsyncSession = Depends(get_session),
    user: Usuario = Depends(get_current_user),
):
    roles, profissional, aluno = await _identity(session, user)

    query = select(Aluno).order_by(Aluno.nome.asc()).limit(limit)
    if "gestor" not in roles:
        if "aluno" in roles and aluno:
            query = query.where(Aluno.id == aluno.id)
        elif "professor" in roles and profissional:
            query = query.join(Aula, Aula.aluno_id == Aluno.id).where(Aula.profissional_id == profissional.id).distinct()

    rows = (await session.execute(query)).scalars().all()
    return {
        "items": [
            {
                "id": str(a.id),
                "nome": a.nome,
                "status": a.status,
                "telefone": a.telefone,
                "email": a.email,
                "whatsapp_numero": a.whatsapp_numero,
            }
            for a in rows
        ],
        "roles": roles,
    }


@router.get("/alunos/{aluno_id}/ficha")
async def mobile_ficha(
    aluno_id: str,
    session: AsyncSession = Depends(get_session),
    user: Usuario = Depends(get_current_user),
):
    aluno = (await session.execute(select(Aluno).where(Aluno.id == aluno_id))).scalar_one_or_none()
    if not aluno:
        return {"detail": "Aluno nao encontrado"}

    aulas_q = await session.execute(select(func.count(Aula.id)).where(Aula.aluno_id == aluno_id))
    receber_q = await session.execute(select(func.coalesce(func.sum(ContaReceber.valor), 0)).where(ContaReceber.aluno_id == aluno_id))
    mensagens_q = await session.execute(select(func.count(MensagemWhatsApp.id)).where(MensagemWhatsApp.aluno_id == aluno_id))
    contrato_q = (
        await session.execute(
            select(Contrato).where(Contrato.aluno_id == aluno_id).order_by(Contrato.created_at.desc()).limit(1)
        )
    ).scalar_one_or_none()

    return {
        "aluno": {
            "id": str(aluno.id),
            "nome": aluno.nome,
            "status": aluno.status,
            "telefone": aluno.telefone,
            "email": aluno.email,
            "whatsapp_numero": aluno.whatsapp_numero,
        },
        "resumo_aulas": {"total": aulas_q.scalar_one()},
        "resumo_financeiro": {"total_receber": float(receber_q.scalar_one())},
        "resumo_whatsapp": {"total_mensagens": mensagens_q.scalar_one()},
        "contrato_ativo": (
            {
                "id": str(contrato_q.id),
                "status": str(contrato_q.status.value if hasattr(contrato_q.status, "value") else contrato_q.status),
                "data_inicio": contrato_q.data_inicio.isoformat() if contrato_q.data_inicio else None,
                "data_fim": contrato_q.data_fim.isoformat() if contrato_q.data_fim else None,
            }
            if contrato_q
            else None
        ),
    }
