from sqlalchemy import String, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class PerfilAcesso(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "perfis_acesso"

    nome: Mapped[str] = mapped_column(String(120))
    permissoes: Mapped[dict | None] = mapped_column(JSON)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)