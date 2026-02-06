from sqlalchemy import Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class AgendaUnidade(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "agenda_unidades"
    __table_args__ = (UniqueConstraint("agenda_id", "unidade_id", name="uq_agenda_unidade"),)

    agenda_id: Mapped[str] = mapped_column(ForeignKey("agendas.id"))
    unidade_id: Mapped[str] = mapped_column(ForeignKey("unidades.id"))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)