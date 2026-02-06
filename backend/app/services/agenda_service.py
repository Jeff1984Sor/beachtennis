from datetime import datetime

from sqlalchemy import and_, or_, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import api_error
from app.models.agenda_unidade import AgendaUnidade
from app.models.agenda import Agenda
from app.models.disponibilidade_agenda import DisponibilidadeAgenda
from app.models.disponibilidade_unidade_override import DisponibilidadeUnidadeOverride
from app.models.bloqueio_agenda import BloqueioAgenda
from app.models.unidade import Unidade
from app.models.aula import Aula
from app.models.enums import BloqueioTipo, BloqueioImpacto, AulaStatus


def _time_overlap(start_a, end_a, start_b, end_b) -> bool:
    return start_a < end_b and end_a > start_b


def _matches_time_window(hora_inicio, hora_fim, inicio, fim) -> bool:
    if hora_inicio is None or hora_fim is None:
        return True
    return hora_inicio <= inicio.time() and hora_fim >= fim.time()


def _matches_day(dia_semana: int | None, inicio: datetime) -> bool:
    if dia_semana is None:
        return True
    return dia_semana == inicio.weekday()


async def validar_agendamento(session: AsyncSession, agenda_id: str, unidade_id: str, inicio: datetime, fim: datetime) -> int:
    if fim <= inicio:
        raise api_error("horario_invalido", "Horario fim deve ser maior que inicio", 400)

    agenda_unidade = await session.execute(
        select(AgendaUnidade).where(
            AgendaUnidade.agenda_id == agenda_id,
            AgendaUnidade.unidade_id == unidade_id,
            AgendaUnidade.ativo == True,
        )
    )
    if not agenda_unidade.scalar_one_or_none():
        raise api_error("agenda_unidade_invalida", "Unidade nao vinculada a agenda", 400)

    disponibilidade = await session.execute(
        select(DisponibilidadeAgenda).where(
            DisponibilidadeAgenda.agenda_id == agenda_id,
            DisponibilidadeAgenda.dia_semana == inicio.weekday(),
            DisponibilidadeAgenda.ativo == True,
            DisponibilidadeAgenda.hora_inicio <= inicio.time(),
            DisponibilidadeAgenda.hora_fim >= fim.time(),
        )
    )
    base = disponibilidade.scalar_one_or_none()
    if not base:
        raise api_error("fora_disponibilidade", "Horario fora da disponibilidade base", 400)

    override = await session.execute(
        select(DisponibilidadeUnidadeOverride).where(
            DisponibilidadeUnidadeOverride.agenda_id == agenda_id,
            DisponibilidadeUnidadeOverride.unidade_id == unidade_id,
            DisponibilidadeUnidadeOverride.dia_semana == inicio.weekday(),
            DisponibilidadeUnidadeOverride.ativo == True,
            DisponibilidadeUnidadeOverride.hora_inicio <= inicio.time(),
            DisponibilidadeUnidadeOverride.hora_fim >= fim.time(),
        )
    )
    override_row = override.scalar_one_or_none()

    unidade_result = await session.execute(select(Unidade).where(Unidade.id == unidade_id))
    unidade = unidade_result.scalar_one_or_none()
    if not unidade:
        raise api_error("unidade_inexistente", "Unidade nao encontrada", 404)

    capacidade = unidade.capacidade_simultanea or 0
    if base.capacidade_base is not None:
        capacidade = min(capacidade, base.capacidade_base)
    if override_row and override_row.capacidade_override is not None:
        capacidade = min(capacidade, override_row.capacidade_override)

    bloqueios_result = await session.execute(
        select(BloqueioAgenda).where(
            BloqueioAgenda.agenda_id == agenda_id,
            BloqueioAgenda.ativo == True,
            or_(BloqueioAgenda.unidade_id == None, BloqueioAgenda.unidade_id == unidade_id),
        )
    )
    for bloqueio in bloqueios_result.scalars():
        if bloqueio.tipo == BloqueioTipo.fixo:
            if not _matches_day(bloqueio.dia_semana, inicio):
                continue
            if not _matches_time_window(bloqueio.hora_inicio, bloqueio.hora_fim, inicio, fim):
                continue
        else:
            if bloqueio.data_inicio and inicio.date() < bloqueio.data_inicio:
                continue
            if bloqueio.data_fim and inicio.date() > bloqueio.data_fim:
                continue
            if not _matches_time_window(bloqueio.hora_inicio, bloqueio.hora_fim, inicio, fim):
                continue

        if bloqueio.impacto == BloqueioImpacto.bloquear_total:
            raise api_error("bloqueado", "Horario bloqueado", 400)
        if bloqueio.impacto == BloqueioImpacto.reduzir_capacidade and bloqueio.capacidade_nova is not None:
            capacidade = min(capacidade, bloqueio.capacidade_nova)

    if capacidade <= 0:
        raise api_error("capacidade_zero", "Capacidade insuficiente", 400)

    count_result = await session.execute(
        select(func.count(Aula.id)).where(
            Aula.agenda_id == agenda_id,
            Aula.unidade_id == unidade_id,
            Aula.status != AulaStatus.cancelada,
            Aula.inicio < fim,
            Aula.fim > inicio,
        )
    )
    total = count_result.scalar_one()
    if total >= capacidade:
        raise api_error("capacidade_excedida", "Capacidade excedida", 400)

    return capacidade