from sqlalchemy import String, Enum, ForeignKey, Integer, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin
from app.models.enums import PlanoTipo


class Plano(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "planos"

    unidade_id: Mapped[str] = mapped_column(ForeignKey("unidades.id"))
    nome: Mapped[str] = mapped_column(String(255))
    tipo: Mapped[PlanoTipo] = mapped_column(Enum(PlanoTipo))
    aulas_por_semana: Mapped[int | None] = mapped_column(Integer)
    qtd_aulas_pacote: Mapped[int | None] = mapped_column(Integer)
    duracao_meses: Mapped[int | None] = mapped_column(Integer)
    preco: Mapped[float] = mapped_column(Numeric(10, 2))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)