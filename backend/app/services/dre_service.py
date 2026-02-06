from datetime import date

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conta_receber import ContaReceber
from app.models.conta_pagar import ContaPagar
from app.models.categoria_financeira import CategoriaFinanceira
from app.models.aula import Aula
from app.models.enums import AulaStatus, CategoriaTipo
from app.models.unidade import Unidade


def _periodo_filter(field, inicio: date, fim: date):
    return field.between(inicio, fim)


async def calcular_dre(session: AsyncSession, unidade_id: str, inicio: date, fim: date, modo: str) -> dict:
    if modo not in ("caixa", "competencia"):
        raise ValueError("modo invalido")

    data_receita = ContaReceber.data_pagamento if modo == "caixa" else ContaReceber.data_vencimento
    data_despesa = ContaPagar.data_pagamento if modo == "caixa" else ContaPagar.data_vencimento

    receitas_query = (
        select(ContaReceber.categoria_id, func.sum(ContaReceber.valor))
        .where(ContaReceber.unidade_id == unidade_id, _periodo_filter(data_receita, inicio, fim))
        .group_by(ContaReceber.categoria_id)
    )
    despesas_query = (
        select(ContaPagar.categoria_id, func.sum(ContaPagar.valor))
        .where(ContaPagar.unidade_id == unidade_id, _periodo_filter(data_despesa, inicio, fim))
        .group_by(ContaPagar.categoria_id)
    )

    receitas = list((await session.execute(receitas_query)).all())
    despesas = list((await session.execute(despesas_query)).all())

    receitas_items = []
    despesas_items = []

    for categoria_id, total in receitas:
        if not total:
            continue
        receitas_items.append({"categoria": str(categoria_id), "valor": float(total)})

    for categoria_id, total in despesas:
        if not total:
            continue
        despesas_items.append({"categoria": str(categoria_id), "valor": float(total)})

    aulas_realizadas = await session.execute(
        select(func.count(Aula.id))
        .where(
            Aula.unidade_id == unidade_id,
            Aula.status == AulaStatus.realizada,
            func.date(Aula.inicio) >= inicio,
            func.date(Aula.inicio) <= fim,
        )
    )
    total_aulas = aulas_realizadas.scalar_one()

    unidade_result = await session.execute(select(Unidade).where(Unidade.id == unidade_id))
    unidade = unidade_result.scalar_one_or_none()
    custo_operacional = float(total_aulas) * float(unidade.custo_aula or 0) if unidade else 0

    total_receitas = sum(item["valor"] for item in receitas_items)
    total_despesas = sum(item["valor"] for item in despesas_items)

    comissao_total = 0
    if despesas_items:
        categoria_ids = [categoria_id for categoria_id, _ in despesas if categoria_id is not None]
        categorias = await session.execute(select(CategoriaFinanceira).where(CategoriaFinanceira.id.in_(categoria_ids)))
        categoria_map = {str(cat.id): cat.nome for cat in categorias.scalars()}
        for item in despesas_items:
            if categoria_map.get(item["categoria"], "").lower() == "comissões" or categoria_map.get(item["categoria"], "").lower() == "comissoes":
                comissao_total += item["valor"]

    resultado = total_receitas - (total_despesas + custo_operacional)

    return {
        "receitas": receitas_items,
        "despesas": despesas_items,
        "custo_operacional_aulas": custo_operacional,
        "despesas_comissao": comissao_total,
        "resultado": resultado,
    }
