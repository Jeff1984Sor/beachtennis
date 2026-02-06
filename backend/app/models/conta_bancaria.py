from sqlalchemy import String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class ContaBancaria(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "contas_bancarias"

    unidade_id: Mapped[str] = mapped_column(ForeignKey("unidades.id"))
    nome: Mapped[str] = mapped_column(String(255))
    banco_agencia_conta: Mapped[str | None] = mapped_column(String(255))
    saldo_inicial: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)