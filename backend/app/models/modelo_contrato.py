from sqlalchemy import String, Text, Enum, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin
from app.models.enums import MotorTemplate


class ModeloContrato(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "modelos_contrato"

    unidade_id: Mapped[str] = mapped_column(ForeignKey("unidades.id"))
    nome: Mapped[str] = mapped_column(String(255))
    descricao: Mapped[str | None] = mapped_column(String(255))
    conteudo_html: Mapped[str] = mapped_column(Text)
    motor_template: Mapped[MotorTemplate] = mapped_column(Enum(MotorTemplate))
    versao: Mapped[int] = mapped_column(Integer, default=1)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_by: Mapped[str | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)