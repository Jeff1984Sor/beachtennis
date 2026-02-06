from datetime import date

from sqlalchemy import String, Enum, ForeignKey, Date, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin
from app.models.enums import ContaStatus


class ContaPagar(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "contas_pagar"

    unidade_id: Mapped[str] = mapped_column(ForeignKey("unidades.id"))
    fornecedor_nome: Mapped[str] = mapped_column(String(255))
    profissional_id: Mapped[str | None] = mapped_column(ForeignKey("profissionais.id"), nullable=True)
    descricao: Mapped[str] = mapped_column(String(255))
    valor: Mapped[float] = mapped_column(Numeric(10, 2))
    data_vencimento: Mapped[date] = mapped_column(Date)
    status: Mapped[ContaStatus] = mapped_column(Enum(ContaStatus))
    categoria_id: Mapped[str] = mapped_column(ForeignKey("categorias_financeiras.id"))
    subcategoria_id: Mapped[str | None] = mapped_column(ForeignKey("subcategorias_financeiras.id"), nullable=True)
    conta_bancaria_id: Mapped[str | None] = mapped_column(ForeignKey("contas_bancarias.id"), nullable=True)
    data_pagamento: Mapped[date | None] = mapped_column(Date)
    observacoes: Mapped[str | None] = mapped_column(Text)