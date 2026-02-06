from datetime import time, datetime, date
from uuid import UUID

from pydantic import BaseModel

from app.schemas.base import UUIDModel, Timestamped
from app.models.enums import BloqueioTipo, BloqueioImpacto, AulaStatus, AulaOrigem


class AgendaBase(BaseModel):
    nome: str
    descricao: str | None = None
    ativa: bool = True


class AgendaCreate(AgendaBase):
    pass


class AgendaUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    ativa: bool | None = None


class AgendaOut(UUIDModel, Timestamped, AgendaBase):
    pass


class DisponibilidadeAgendaBase(BaseModel):
    agenda_id: UUID
    dia_semana: int
    hora_inicio: time
    hora_fim: time
    capacidade_base: int | None = None
    ativo: bool = True


class DisponibilidadeAgendaCreate(DisponibilidadeAgendaBase):
    pass


class DisponibilidadeAgendaOut(UUIDModel, Timestamped, DisponibilidadeAgendaBase):
    pass


class DisponibilidadeOverrideBase(BaseModel):
    agenda_id: UUID
    unidade_id: UUID
    dia_semana: int
    hora_inicio: time
    hora_fim: time
    capacidade_override: int | None = None
    ativo: bool = True


class DisponibilidadeOverrideCreate(DisponibilidadeOverrideBase):
    pass


class DisponibilidadeOverrideOut(UUIDModel, Timestamped, DisponibilidadeOverrideBase):
    pass


class BloqueioAgendaBase(BaseModel):
    agenda_id: UUID
    unidade_id: UUID | None = None
    tipo: BloqueioTipo
    titulo: str | None = None
    motivo: str | None = None
    impacto: BloqueioImpacto
    capacidade_nova: int | None = None
    dia_semana: int | None = None
    hora_inicio: time | None = None
    hora_fim: time | None = None
    data_inicio: date | None = None
    data_fim: date | None = None


class BloqueioAgendaCreate(BloqueioAgendaBase):
    pass


class BloqueioAgendaOut(UUIDModel, Timestamped, BloqueioAgendaBase):
    pass


class AulaBase(BaseModel):
    agenda_id: UUID
    unidade_id: UUID
    aluno_id: UUID
    profissional_id: UUID | None = None
    inicio: datetime
    fim: datetime
    status: AulaStatus = AulaStatus.agendada
    origem: AulaOrigem = AulaOrigem.manual
    observacoes: str | None = None


class AulaCreate(AulaBase):
    pass


class AulaOut(UUIDModel, Timestamped, AulaBase):
    pass