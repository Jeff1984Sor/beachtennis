from sqlalchemy import Boolean, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin
from app.models.enums import CompetenciaTipo, BaseCalculo


class RegraComissao(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "regras_comissao"

    unidade_id: Mapped[str] = mapped_column(ForeignKey("unidades.id"))
    ativa: Mapped[bool] = mapped_column(Boolean, default=True)
    dia_pagamento: Mapped[int] = mapped_column(Integer)
    competencia_tipo: Mapped[CompetenciaTipo] = mapped_column(Enum(CompetenciaTipo))
    base_calculo: Mapped[BaseCalculo] = mapped_column(Enum(BaseCalculo))
    categoria_financeira_id: Mapped[str] = mapped_column(ForeignKey("categorias_financeiras.id"))
    subcategoria_id: Mapped[str | None] = mapped_column(ForeignKey("subcategorias_financeiras.id"), nullable=True)