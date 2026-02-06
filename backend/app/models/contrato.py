from datetime import date, datetime

from sqlalchemy import String, Date, DateTime, Enum, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin
from app.models.enums import ContratoStatus, StatusDocumento


class Contrato(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "contratos"

    unidade_id: Mapped[str] = mapped_column(ForeignKey("unidades.id"))
    aluno_id: Mapped[str] = mapped_column(ForeignKey("alunos.id"))
    plano_id: Mapped[str] = mapped_column(ForeignKey("planos.id"))
    data_inicio: Mapped[date | None] = mapped_column(Date)
    data_fim: Mapped[date | None] = mapped_column(Date)
    status: Mapped[ContratoStatus] = mapped_column(Enum(ContratoStatus))
    dia_vencimento: Mapped[int] = mapped_column()
    desconto_valor: Mapped[float | None] = mapped_column(Numeric(10, 2))
    desconto_percentual: Mapped[float | None] = mapped_column(Numeric(10, 2))
    observacoes: Mapped[str | None] = mapped_column(Text)
    modelo_contrato_id: Mapped[str | None] = mapped_column(ForeignKey("modelos_contrato.id"))
    contrato_renderizado_html: Mapped[str | None] = mapped_column(Text)
    contrato_renderizado_pdf_media_id: Mapped[str | None] = mapped_column(ForeignKey("media_files.id"))
    data_geracao_contrato: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))
    status_documento: Mapped[StatusDocumento] = mapped_column(Enum(StatusDocumento), default=StatusDocumento.nao_gerado)