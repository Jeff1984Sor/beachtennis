from datetime import date

from sqlalchemy import String, Enum, ForeignKey, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin
from app.models.enums import MovimentoTipo, MovimentoOrigem


class MovimentoBancario(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "movimentos_bancarios"

    unidade_id: Mapped[str] = mapped_column(ForeignKey("unidades.id"))
    conta_bancaria_id: Mapped[str] = mapped_column(ForeignKey("contas_bancarias.id"))
    tipo: Mapped[MovimentoTipo] = mapped_column(Enum(MovimentoTipo))
    origem: Mapped[MovimentoOrigem] = mapped_column(Enum(MovimentoOrigem))
    receber_id: Mapped[str | None] = mapped_column(ForeignKey("contas_receber.id"), nullable=True)
    pagar_id: Mapped[str | None] = mapped_column(ForeignKey("contas_pagar.id"), nullable=True)
    transferencia_group_id: Mapped[str | None] = mapped_column(String(120))
    valor: Mapped[float] = mapped_column(Numeric(10, 2))
    data_movimento: Mapped[date] = mapped_column(Date)
    categoria_id: Mapped[str | None] = mapped_column(ForeignKey("categorias_financeiras.id"), nullable=True)
    subcategoria_id: Mapped[str | None] = mapped_column(ForeignKey("subcategorias_financeiras.id"), nullable=True)
    descricao: Mapped[str | None] = mapped_column(String(255))
    created_by: Mapped[str | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)