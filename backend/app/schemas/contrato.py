from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import ContratoStatus, StatusDocumento
from app.schemas.base import UUIDModel, Timestamped


class ContratoBase(BaseModel):
    unidade_id: UUID
    aluno_id: UUID
    plano_id: UUID
    data_inicio: date | None = None
    data_fim: date | None = None
    status: ContratoStatus
    dia_vencimento: int
    desconto_valor: float | None = None
    desconto_percentual: float | None = None
    observacoes: str | None = None
    modelo_contrato_id: UUID | None = None
    contrato_renderizado_html: str | None = None
    contrato_renderizado_pdf_media_id: UUID | None = None
    data_geracao_contrato: datetime | None = None
    status_documento: StatusDocumento = StatusDocumento.nao_gerado


class ContratoCreate(ContratoBase):
    pass


class ContratoUpdate(BaseModel):
    data_inicio: date | None = None
    data_fim: date | None = None
    status: ContratoStatus | None = None
    dia_vencimento: int | None = None
    desconto_valor: float | None = None
    desconto_percentual: float | None = None
    observacoes: str | None = None
    modelo_contrato_id: UUID | None = None
    contrato_renderizado_html: str | None = None
    contrato_renderizado_pdf_media_id: UUID | None = None
    data_geracao_contrato: datetime | None = None
    status_documento: StatusDocumento | None = None


class ContratoOut(UUIDModel, Timestamped, ContratoBase):
    pass


class ContratoListOut(UUIDModel, ContratoBase):
    aluno_nome: str | None = None