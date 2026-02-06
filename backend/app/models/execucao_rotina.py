from datetime import datetime

from sqlalchemy import String, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin
from app.models.enums import ExecucaoStatus


class ExecucaoRotina(UUIDMixin, Base):
    __tablename__ = "execucoes_rotina"

    chave: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    executada_em: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    status: Mapped[ExecucaoStatus] = mapped_column(Enum(ExecucaoStatus))
    detalhes_erro: Mapped[str | None] = mapped_column(String(255))