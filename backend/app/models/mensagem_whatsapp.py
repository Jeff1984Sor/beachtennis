from datetime import datetime

from sqlalchemy import String, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin
from app.models.enums import MensagemTipo, MensagemStatus, MensagemProvider


class MensagemWhatsApp(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "mensagens_whatsapp"

    unidade_id: Mapped[str] = mapped_column(ForeignKey("unidades.id"))
    aluno_id: Mapped[str] = mapped_column(ForeignKey("alunos.id"))
    tipo: Mapped[MensagemTipo] = mapped_column(Enum(MensagemTipo))
    template_key: Mapped[str | None] = mapped_column(String(120))
    conteudo: Mapped[str] = mapped_column(Text)
    status: Mapped[MensagemStatus] = mapped_column(Enum(MensagemStatus))
    provider: Mapped[MensagemProvider] = mapped_column(Enum(MensagemProvider))
    provider_message_id: Mapped[str | None] = mapped_column(String(120))
    erro: Mapped[str | None] = mapped_column(String(255))
    agendada_para: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))
    enviada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))
    created_by: Mapped[str | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)