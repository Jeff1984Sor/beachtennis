from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aula import Aula
from app.core.errors import api_error
from app.services.agenda_service import validar_agendamento
from app.models.enums import AulaStatus


async def criar_aula(session: AsyncSession, data: dict) -> Aula:
    await validar_agendamento(session, str(data["agenda_id"]), str(data["unidade_id"]), data["inicio"], data["fim"])
    aula = Aula(**data)
    session.add(aula)
    await session.commit()
    await session.refresh(aula)
    return aula


async def listar_aulas(session: AsyncSession, agenda_id: str | None = None, inicio: datetime | None = None, fim: datetime | None = None) -> list[Aula]:
    query = select(Aula)
    if agenda_id:
        query = query.where(Aula.agenda_id == agenda_id)
    if inicio:
        query = query.where(Aula.inicio >= inicio)
    if fim:
        query = query.where(Aula.fim <= fim)
    result = await session.execute(query)
    return list(result.scalars())


async def obter_aula(session: AsyncSession, aula_id: str) -> Aula:
    result = await session.execute(select(Aula).where(Aula.id == aula_id))
    aula = result.scalar_one_or_none()
    if not aula:
        raise api_error("not_found", "Aula nao encontrada", 404)
    return aula


async def atualizar_aula(session: AsyncSession, aula_id: str, data: dict) -> Aula:
    aula = await obter_aula(session, aula_id)

    novo_inicio = data.get("inicio", aula.inicio)
    novo_fim = data.get("fim", aula.fim)
    nova_agenda = str(data.get("agenda_id", aula.agenda_id))
    nova_unidade = str(data.get("unidade_id", aula.unidade_id))

    if "status" in data and data["status"] == AulaStatus.cancelada:
        aula.status = AulaStatus.cancelada
        await session.commit()
        await session.refresh(aula)
        return aula

    await validar_agendamento(session, nova_agenda, nova_unidade, novo_inicio, novo_fim)

    for key, value in data.items():
        if value is not None:
            setattr(aula, key, value)

    await session.commit()
    await session.refresh(aula)
    return aula


async def cancelar_aula(session: AsyncSession, aula_id: str) -> Aula:
    aula = await obter_aula(session, aula_id)
    aula.status = AulaStatus.cancelada
    await session.commit()
    await session.refresh(aula)
    return aula