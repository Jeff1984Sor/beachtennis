from datetime import time

from sqlalchemy import Integer, Boolean, ForeignKey, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class DisponibilidadeUnidadeOverride(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "disponibilidades_unidade_override"

    agenda_id: Mapped[str] = mapped_column(ForeignKey("agendas.id"))
    unidade_id: Mapped[str] = mapped_column(ForeignKey("unidades.id"))
    dia_semana: Mapped[int] = mapped_column(Integer)
    hora_inicio: Mapped[time] = mapped_column(Time)
    hora_fim: Mapped[time] = mapped_column(Time)
    capacidade_override: Mapped[int | None] = mapped_column(Integer)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)