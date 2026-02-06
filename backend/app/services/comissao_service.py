from datetime import datetime, date
from calendar import monthrange

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import api_error
from app.models.aula import Aula
from app.models.conta_pagar import ContaPagar
from app.models.execucao_rotina import ExecucaoRotina
from app.models.profissional import Profissional
from app.models.unidade import Unidade
from app.models.regra_comissao import RegraComissao
from app.models.enums import AulaStatus, ContaStatus, ExecucaoStatus, ComissaoTipo, BaseCalculo


def _parse_mes(mes: str) -> tuple[date, date]:
    try:
        year, month = mes.split("-")
        year = int(year)
        month = int(month)
        last_day = monthrange(year, month)[1]
        return date(year, month, 1), date(year, month, last_day)
    except Exception as exc:
        raise api_error("invalid_mes", "Mes invalido. Use YYYY-MM", 400) from exc


async def gerar_comissoes(session: AsyncSession, unidade_id: str, mes: str) -> int:
    inicio, fim = _parse_mes(mes)
    chave = f"comissao:unidade:{unidade_id}:{mes}"

    existing = await session.execute(select(ExecucaoRotina).where(ExecucaoRotina.chave == chave))
    if existing.scalar_one_or_none():
        return 0

    regra_result = await session.execute(select(RegraComissao).where(RegraComissao.unidade_id == unidade_id, RegraComissao.ativa == True))
    regra = regra_result.scalar_one_or_none()
    if not regra:
        raise api_error("regra_inexistente", "Regra de comissao nao encontrada", 404)

    if regra.base_calculo != BaseCalculo.valor_cobrado_aula:
        raise api_error("base_calculo_invalida", "Base de calculo nao suportada", 400)

    unidade_result = await session.execute(select(Unidade).where(Unidade.id == unidade_id))
    unidade = unidade_result.scalar_one_or_none()
    if not unidade:
        raise api_error("unidade_inexistente", "Unidade nao encontrada", 404)

    prof_result = await session.execute(select(Profissional).where(Profissional.unidade_id == unidade_id))
    profissionais = list(prof_result.scalars())

    total_criados = 0
    for prof in profissionais:
        aulas_result = await session.execute(
            select(func.count(Aula.id))
            .where(
                Aula.unidade_id == unidade_id,
                Aula.profissional_id == prof.id,
                Aula.status == AulaStatus.realizada,
                Aula.inicio >= datetime.combine(inicio, datetime.min.time()),
                Aula.inicio <= datetime.combine(fim, datetime.max.time()),
            )
        )
        aulas_realizadas = aulas_result.scalar_one()
        if aulas_realizadas == 0:
            continue

        valor_base = float(unidade.valor_cobrado_aula or 0)

        comissao = 0
        if prof.comissao_tipo == ComissaoTipo.percentual:
            comissao = float(aulas_realizadas) * float(valor_base) * (float(prof.comissao_valor) / 100)
        else:
            comissao = float(aulas_realizadas) * float(prof.comissao_valor)

        if comissao <= 0:
            continue

        pagamento_ano = inicio.year if inicio.month < 12 else inicio.year + 1
        pagamento_mes = inicio.month + 1 if inicio.month < 12 else 1

        conta = ContaPagar(
            unidade_id=unidade_id,
            fornecedor_nome=prof.nome,
            profissional_id=prof.id,
            descricao=f"Comissao do professor - {mes}",
            valor=comissao,
            data_vencimento=date(pagamento_ano, pagamento_mes, regra.dia_pagamento),
            status=ContaStatus.aberto,
            categoria_id=regra.categoria_financeira_id,
            subcategoria_id=regra.subcategoria_id,
        )
        session.add(conta)
        total_criados += 1

    execucao = ExecucaoRotina(
        chave=chave,
        executada_em=datetime.utcnow(),
        status=ExecucaoStatus.sucesso,
    )
    session.add(execucao)
    await session.commit()
    return total_criados
