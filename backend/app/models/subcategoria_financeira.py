from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class SubcategoriaFinanceira(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "subcategorias_financeiras"

    categoria_id: Mapped[str] = mapped_column(ForeignKey("categorias_financeiras.id"))
    nome: Mapped[str] = mapped_column(String(255))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)