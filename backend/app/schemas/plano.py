from uuid import UUID

from pydantic import BaseModel

from app.models.enums import PlanoTipo
from app.schemas.base import UUIDModel, Timestamped


class PlanoBase(BaseModel):
    unidade_id: UUID
    nome: str
    tipo: PlanoTipo
    aulas_por_semana: int | None = None
    qtd_aulas_pacote: int | None = None
    duracao_meses: int | None = None
    preco: float
    ativo: bool = True


class PlanoCreate(PlanoBase):
    pass


class PlanoUpdate(BaseModel):
    nome: str | None = None
    tipo: PlanoTipo | None = None
    aulas_por_semana: int | None = None
    qtd_aulas_pacote: int | None = None
    duracao_meses: int | None = None
    preco: float | None = None
    ativo: bool | None = None


class PlanoOut(UUIDModel, Timestamped, PlanoBase):
    pass