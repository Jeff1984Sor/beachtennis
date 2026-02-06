from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aula import Aula
from app.core.errors import api_error
from app.services.agenda_service import validar_agendamento


async def criar_aula(session: AsyncSession, data: dict) -> Aula:
    await validar_agendamento(session, str(data["agenda_id"]), str(data["unidade_id"]), data["inicio"], data["fim"])
    aula = Aula(**data)
    session.add(aula)
    await session.commit()
    await session.refresh(aula)
    return aula


async def listar_aulas(session: AsyncSession, agenda_id: str | None = None) -> list[Aula]:
    query = select(Aula)
    if agenda_id:
        query = query.where(Aula.agenda_id == agenda_id)
    result = await session.execute(query)
    return list(result.scalars())


async def obter_aula(session: AsyncSession, aula_id: str) -> Aula:
    result = await session.execute(select(Aula).where(Aula.id == aula_id))
    aula = result.scalar_one_or_none()
    if not aula:
        raise api_error("not_found", "Aula nao encontrada", 404)
    return aula