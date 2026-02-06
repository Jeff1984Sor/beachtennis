from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.empresa_config import EmpresaConfig


async def get_empresa_config(session: AsyncSession) -> EmpresaConfig | None:
    result = await session.execute(select(EmpresaConfig))
    return result.scalar_one_or_none()


async def ensure_empresa_config(session: AsyncSession) -> EmpresaConfig:
    config = await get_empresa_config(session)
    if config:
        return config
    config = EmpresaConfig(nome_empresa="Beach Tennis School", tema=None, fonte=None)
    session.add(config)
    await session.commit()
    await session.refresh(config)
    return config


async def update_empresa_config(session: AsyncSession, data: dict) -> EmpresaConfig:
    config = await ensure_empresa_config(session)
    for key, value in data.items():
        if value is not None:
            setattr(config, key, value)
    await session.commit()
    await session.refresh(config)
    return config