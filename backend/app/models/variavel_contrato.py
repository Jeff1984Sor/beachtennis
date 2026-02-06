from sqlalchemy import String, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class VariavelContrato(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "variaveis_contrato"

    chave: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    descricao: Mapped[str] = mapped_column(String(255))
    exemplo: Mapped[str | None] = mapped_column(String(255))
    categoria: Mapped[str] = mapped_column(String(50))
    tipo: Mapped[str] = mapped_column(String(50))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)