from datetime import date
from uuid import UUID

from pydantic import BaseModel

from app.schemas.base import UUIDModel, Timestamped


class AlunoBase(BaseModel):
    unidade_id: UUID
    nome: str
    cpf: str | None = None
    data_nascimento: date | None = None
    telefone: str | None = None
    email: str | None = None
    endereco_id: UUID | None = None
    observacoes: str | None = None
    status: str | None = None
    whatsapp_numero: str | None = None
    whatsapp_opt_in: bool = False
    whatsapp_ultimo_contato_em: date | None = None
    whatsapp_tags: list | None = None


class AlunoCreate(AlunoBase):
    pass


class AlunoUpdate(BaseModel):
    nome: str | None = None
    cpf: str | None = None
    data_nascimento: date | None = None
    telefone: str | None = None
    email: str | None = None
    endereco_id: UUID | None = None
    observacoes: str | None = None
    status: str | None = None
    whatsapp_numero: str | None = None
    whatsapp_opt_in: bool | None = None
    whatsapp_ultimo_contato_em: date | None = None
    whatsapp_tags: list | None = None


class AlunoOut(UUIDModel, Timestamped, AlunoBase):
    pass


class AlunoFichaOut(BaseModel):
    aluno: AlunoOut
    resumo_aulas: dict
    resumo_financeiro: dict
    resumo_whatsapp: dict
    contrato_ativo: dict | None = None
    anexos: list