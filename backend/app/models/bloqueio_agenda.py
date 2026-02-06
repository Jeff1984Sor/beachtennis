from datetime import date, time

from sqlalchemy import String, Enum, ForeignKey, Integer, Date, Time, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin
from app.models.enums import BloqueioTipo, BloqueioImpacto


class BloqueioAgenda(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "bloqueios_agenda"

    agenda_id: Mapped[str] = mapped_column(ForeignKey("agendas.id"))
    unidade_id: Mapped[str | None] = mapped_column(ForeignKey("unidades.id"), nullable=True)
    tipo: Mapped[BloqueioTipo] = mapped_column(Enum(BloqueioTipo))
    titulo: Mapped[str | None] = mapped_column(String(255))
    motivo: Mapped[str | None] = mapped_column(String(255))
    impacto: Mapped[BloqueioImpacto] = mapped_column(Enum(BloqueioImpacto))
    capacidade_nova: Mapped[int | None] = mapped_column(Integer)
    dia_semana: Mapped[int | None] = mapped_column(Integer)
    hora_inicio: Mapped[time | None] = mapped_column(Time)
    hora_fim: Mapped[time | None] = mapped_column(Time)
    data_inicio: Mapped[date | None] = mapped_column(Date)
    data_fim: Mapped[date | None] = mapped_column(Date)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
