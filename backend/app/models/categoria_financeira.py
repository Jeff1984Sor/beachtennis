from sqlalchemy import String, Enum, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin
from app.models.enums import CategoriaTipo


class CategoriaFinanceira(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "categorias_financeiras"

    unidade_id: Mapped[str | None] = mapped_column(ForeignKey("unidades.id"), nullable=True)
    tipo: Mapped[CategoriaTipo] = mapped_column(Enum(CategoriaTipo))
    nome: Mapped[str] = mapped_column(String(255))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
