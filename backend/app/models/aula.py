from datetime import datetime

from sqlalchemy import String, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin
from app.models.enums import AulaStatus, AulaOrigem


class Aula(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "aulas"

    agenda_id: Mapped[str] = mapped_column(ForeignKey("agendas.id"))
    unidade_id: Mapped[str] = mapped_column(ForeignKey("unidades.id"))
    aluno_id: Mapped[str] = mapped_column(ForeignKey("alunos.id"))
    profissional_id: Mapped[str | None] = mapped_column(ForeignKey("profissionais.id"), nullable=True)
    inicio: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    fim: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    status: Mapped[AulaStatus] = mapped_column(Enum(AulaStatus))
    origem: Mapped[AulaOrigem] = mapped_column(Enum(AulaOrigem))
    observacoes: Mapped[str | None] = mapped_column(Text)