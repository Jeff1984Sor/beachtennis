from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.deps import get_current_user
from app.core.errors import api_error
from app.schemas.agenda import (
    AgendaOut,
    AgendaCreate,
    AgendaUpdate,
    DisponibilidadeAgendaOut,
    DisponibilidadeAgendaCreate,
    DisponibilidadeOverrideOut,
    DisponibilidadeOverrideCreate,
    BloqueioAgendaOut,
    BloqueioAgendaCreate,
    AulaOut,
    AulaCreate,
    AulaUpdate,
)
from app.models.agenda import Agenda
from app.models.disponibilidade_agenda import DisponibilidadeAgenda
from app.models.disponibilidade_unidade_override import DisponibilidadeUnidadeOverride
from app.models.bloqueio_agenda import BloqueioAgenda
from app.services.aula_service import criar_aula, listar_aulas, atualizar_aula, cancelar_aula

router = APIRouter(prefix="/agenda")


@router.get("", response_model=list[AgendaOut])
async def listar_agendas(
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    result = await session.execute(select(Agenda))
    return [AgendaOut.model_validate(a) for a in result.scalars()]


@router.post("", response_model=AgendaOut)
async def criar_agenda(
    payload: AgendaCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    agenda = Agenda(**payload.model_dump())
    session.add(agenda)
    await session.commit()
    await session.refresh(agenda)
    return AgendaOut.model_validate(agenda)


@router.put("/{agenda_id}", response_model=AgendaOut)
async def atualizar_agenda(
    agenda_id: str,
    payload: AgendaUpdate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    result = await session.execute(select(Agenda).where(Agenda.id == agenda_id))
    agenda = result.scalar_one_or_none()
    if not agenda:
        raise api_error("not_found", "Agenda nao encontrada", 404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(agenda, key, value)
    await session.commit()
    await session.refresh(agenda)
    return AgendaOut.model_validate(agenda)


@router.post("/disponibilidades", response_model=DisponibilidadeAgendaOut)
async def criar_disponibilidade(
    payload: DisponibilidadeAgendaCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    disp = DisponibilidadeAgenda(**payload.model_dump())
    session.add(disp)
    await session.commit()
    await session.refresh(disp)
    return DisponibilidadeAgendaOut.model_validate(disp)


@router.post("/overrides", response_model=DisponibilidadeOverrideOut)
async def criar_override(
    payload: DisponibilidadeOverrideCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    override = DisponibilidadeUnidadeOverride(**payload.model_dump())
    session.add(override)
    await session.commit()
    await session.refresh(override)
    return DisponibilidadeOverrideOut.model_validate(override)


@router.post("/bloqueios", response_model=BloqueioAgendaOut)
async def criar_bloqueio(
    payload: BloqueioAgendaCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    bloqueio = BloqueioAgenda(**payload.model_dump())
    session.add(bloqueio)
    await session.commit()
    await session.refresh(bloqueio)
    return BloqueioAgendaOut.model_validate(bloqueio)


@router.get("/aulas", response_model=list[AulaOut])
async def listar_aulas_endpoint(
    agenda_id: str | None = None,
    inicio: str | None = None,
    fim: str | None = None,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    inicio_dt = None
    fim_dt = None
    if inicio:
        inicio_dt = datetime.fromisoformat(inicio)
    if fim:
        fim_dt = datetime.fromisoformat(fim)
    aulas = await listar_aulas(session, agenda_id, inicio_dt, fim_dt)
    return [AulaOut.model_validate(a) for a in aulas]


@router.post("/aulas", response_model=AulaOut)
async def criar_aula_endpoint(
    payload: AulaCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    aula = await criar_aula(session, payload.model_dump())
    return AulaOut.model_validate(aula)


@router.put("/aulas/{aula_id}", response_model=AulaOut)
async def atualizar_aula_endpoint(
    aula_id: str,
    payload: AulaUpdate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    aula = await atualizar_aula(session, aula_id, payload.model_dump(exclude_unset=True))
    return AulaOut.model_validate(aula)


@router.post("/aulas/{aula_id}/cancelar", response_model=AulaOut)
async def cancelar_aula_endpoint(
    aula_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    aula = await cancelar_aula(session, aula_id)
    return AulaOut.model_validate(aula)
