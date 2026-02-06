import asyncio
import os

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import SessionLocal
from app.services.comissao_service import gerar_comissoes


async def main() -> None:
    unidade_id = os.getenv("UNIDADE_ID")
    mes = os.getenv("MES")
    if not unidade_id or not mes:
        raise SystemExit("UNIDADE_ID e MES sao obrigatorios")

    async with SessionLocal() as session:
        await gerar_comissoes(session, unidade_id, mes)


if __name__ == "__main__":
    asyncio.run(main())