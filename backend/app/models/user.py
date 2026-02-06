from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class Usuario(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "usuarios"

    nome: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    telefone: Mapped[str | None] = mapped_column(String(50))
    perfil_acesso_id: Mapped[str | None] = mapped_column(ForeignKey("perfis_acesso.id"))
    unidade_id: Mapped[str | None] = mapped_column(ForeignKey("unidades.id"))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))

    perfil_acesso: Mapped["PerfilAcesso" | None] = relationship("PerfilAcesso")