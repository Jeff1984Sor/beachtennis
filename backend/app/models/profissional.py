from sqlalchemy import String, Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin
from app.models.enums import ProfissionalTipo, ComissaoTipo


class Profissional(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "profissionais"

    unidade_id: Mapped[str] = mapped_column(ForeignKey("unidades.id"))
    nome: Mapped[str] = mapped_column(String(255))
    tipo: Mapped[ProfissionalTipo] = mapped_column(Enum(ProfissionalTipo))
    registro: Mapped[str | None] = mapped_column(String(120))
    telefone: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(255))
    endereco_id: Mapped[str | None] = mapped_column(ForeignKey("enderecos.id"), nullable=True)
    usuario_id: Mapped[str | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50))
    comissao_tipo: Mapped[ComissaoTipo] = mapped_column(Enum(ComissaoTipo), default=ComissaoTipo.percentual)
    comissao_valor: Mapped[float] = mapped_column(Numeric(10, 2), default=0)