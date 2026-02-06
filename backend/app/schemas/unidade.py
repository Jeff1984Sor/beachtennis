from uuid import UUID

from pydantic import BaseModel

from app.schemas.base import UUIDModel, Timestamped


class UnidadeBase(BaseModel):
    nome: str
    slug: str
    telefone: str | None = None
    email: str | None = None
    cnpj: str | None = None
    endereco_id: UUID | None = None
    capacidade_simultanea: int | None = None
    custo_aula: float = 0
    valor_cobrado_aula: float = 0
    ativo: bool = True


class UnidadeCreate(UnidadeBase):
    pass


class UnidadeUpdate(BaseModel):
    nome: str | None = None
    slug: str | None = None
    telefone: str | None = None
    email: str | None = None
    cnpj: str | None = None
    endereco_id: UUID | None = None
    capacidade_simultanea: int | None = None
    custo_aula: float | None = None
    valor_cobrado_aula: float | None = None
    ativo: bool | None = None


class UnidadeOut(UUIDModel, Timestamped, UnidadeBase):
    pass