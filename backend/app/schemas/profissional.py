from uuid import UUID

from pydantic import BaseModel

from app.models.enums import ProfissionalTipo, ComissaoTipo
from app.schemas.base import UUIDModel, Timestamped


class ProfissionalBase(BaseModel):
    unidade_id: UUID
    nome: str
    tipo: ProfissionalTipo
    registro: str | None = None
    telefone: str | None = None
    email: str | None = None
    endereco_id: UUID | None = None
    usuario_id: UUID | None = None
    status: str | None = None
    comissao_tipo: ComissaoTipo = ComissaoTipo.percentual
    comissao_valor: float = 0


class ProfissionalCreate(ProfissionalBase):
    pass


class ProfissionalUpdate(BaseModel):
    nome: str | None = None
    tipo: ProfissionalTipo | None = None
    registro: str | None = None
    telefone: str | None = None
    email: str | None = None
    endereco_id: UUID | None = None
    usuario_id: UUID | None = None
    status: str | None = None
    comissao_tipo: ComissaoTipo | None = None
    comissao_valor: float | None = None


class ProfissionalOut(UUIDModel, Timestamped, ProfissionalBase):
    pass