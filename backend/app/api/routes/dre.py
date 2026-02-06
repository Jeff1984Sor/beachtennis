from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.deps import get_current_user
from app.schemas.financeiro import DREOut
from app.services.dre_service import calcular_dre

router = APIRouter(prefix="/financeiro")


@router.get("/dre", response_model=DREOut)
async def dre(
    unidade_id: str,
    inicio: date,
    fim: date,
    modo: str = "caixa",
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> DREOut:
    dados = await calcular_dre(session, unidade_id, inicio, fim, modo)
    return DREOut(
        modo=modo,
        periodo_inicio=inicio.isoformat(),
        periodo_fim=fim.isoformat(),
        receitas=[{"categoria": item["categoria"], "valor": item["valor"]} for item in dados["receitas"]],
        despesas=[{"categoria": item["categoria"], "valor": item["valor"]} for item in dados["despesas"]],
        custo_operacional_aulas=dados["custo_operacional_aulas"],
        despesas_comissao=dados["despesas_comissao"],
        resultado=dados["resultado"],
    )