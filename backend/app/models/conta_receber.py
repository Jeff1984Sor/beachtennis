from datetime import date

from sqlalchemy import String, Enum, ForeignKey, Date, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin
from app.models.enums import ContaStatus


class ContaReceber(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "contas_receber"

    unidade_id: Mapped[str] = mapped_column(ForeignKey("unidades.id"))
    aluno_id: Mapped[str] = mapped_column(ForeignKey("alunos.id"))
    contrato_id: Mapped[str | None] = mapped_column(ForeignKey("contratos.id"), nullable=True)
    descricao: Mapped[str] = mapped_column(String(255))
    valor: Mapped[float] = mapped_column(Numeric(10, 2))
    data_vencimento: Mapped[date] = mapped_column(Date)
    status: Mapped[ContaStatus] = mapped_column(Enum(ContaStatus))
    categoria_id: Mapped[str] = mapped_column(ForeignKey("categorias_financeiras.id"))
    subcategoria_id: Mapped[str | None] = mapped_column(ForeignKey("subcategorias_financeiras.id"), nullable=True)
    forma_pagamento: Mapped[str | None] = mapped_column(String(50))
    conta_bancaria_id: Mapped[str | None] = mapped_column(ForeignKey("contas_bancarias.id"), nullable=True)
    data_pagamento: Mapped[date | None] = mapped_column(Date)
    juros_multa_desconto: Mapped[float | None] = mapped_column(Numeric(10, 2))
    observacoes: Mapped[str | None] = mapped_column(Text)