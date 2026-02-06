from datetime import date

from sqlalchemy import String, Date, Boolean, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class Aluno(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "alunos"

    unidade_id: Mapped[str] = mapped_column(ForeignKey("unidades.id"))
    nome: Mapped[str] = mapped_column(String(255))
    cpf: Mapped[str | None] = mapped_column(String(20))
    data_nascimento: Mapped[date | None] = mapped_column(Date)
    telefone: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(255))
    endereco_id: Mapped[str | None] = mapped_column(ForeignKey("enderecos.id"))
    observacoes: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str | None] = mapped_column(String(50))
    whatsapp_numero: Mapped[str | None] = mapped_column(String(50))
    whatsapp_opt_in: Mapped[bool] = mapped_column(Boolean, default=False)
    whatsapp_ultimo_contato_em: Mapped[date | None] = mapped_column(Date)
    whatsapp_tags: Mapped[list | None] = mapped_column(JSON)