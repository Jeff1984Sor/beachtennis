from sqlalchemy import String, Boolean, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class Unidade(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "unidades"

    nome: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(120), unique=True)
    telefone: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(255))
    cnpj: Mapped[str | None] = mapped_column(String(30))
    endereco_id: Mapped[str | None] = mapped_column(ForeignKey("enderecos.id"))
    capacidade_simultanea: Mapped[int | None] = mapped_column(Integer)
    custo_aula: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    valor_cobrado_aula: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)