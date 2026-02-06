from uuid import UUID

from pydantic import BaseModel

from app.models.enums import CompetenciaTipo, BaseCalculo
from app.schemas.base import UUIDModel, Timestamped


class RegraComissaoBase(BaseModel):
    unidade_id: UUID
    ativa: bool = True
    dia_pagamento: int
    competencia_tipo: CompetenciaTipo = CompetenciaTipo.mes_anterior
    base_calculo: BaseCalculo = BaseCalculo.valor_cobrado_aula
    categoria_financeira_id: UUID
    subcategoria_id: UUID | None = None


class RegraComissaoCreate(RegraComissaoBase):
    pass


class RegraComissaoUpdate(BaseModel):
    ativa: bool | None = None
    dia_pagamento: int | None = None
    competencia_tipo: CompetenciaTipo | None = None
    base_calculo: BaseCalculo | None = None
    categoria_financeira_id: UUID | None = None
    subcategoria_id: UUID | None = None


class RegraComissaoOut(UUIDModel, Timestamped, RegraComissaoBase):
    pass