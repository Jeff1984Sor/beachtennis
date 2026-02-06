from pydantic import BaseModel


class DREItem(BaseModel):
    categoria: str
    valor: float


class DREOut(BaseModel):
    modo: str
    periodo_inicio: str
    periodo_fim: str
    receitas: list[DREItem]
    despesas: list[DREItem]
    custo_operacional_aulas: float
    despesas_comissao: float
    resultado: float