from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import api_error
from app.models.aluno import Aluno


async def list_alunos(session: AsyncSession, limit: int, offset: int) -> list[Aluno]:
    result = await session.execute(select(Aluno).limit(limit).offset(offset))
    return list(result.scalars())


async def get_aluno(session: AsyncSession, aluno_id: str) -> Aluno:
    result = await session.execute(select(Aluno).where(Aluno.id == aluno_id))
    aluno = result.scalar_one_or_none()
    if not aluno:
        raise api_error("not_found", "Aluno nao encontrado", 404)
    return aluno


async def create_aluno(session: AsyncSession, data: dict) -> Aluno:
    aluno = Aluno(**data)
    session.add(aluno)
    await session.commit()
    await session.refresh(aluno)
    return aluno


async def update_aluno(session: AsyncSession, aluno_id: str, data: dict) -> Aluno:
    aluno = await get_aluno(session, aluno_id)
    for key, value in data.items():
        if value is not None:
            setattr(aluno, key, value)
    await session.commit()
    await session.refresh(aluno)
    return aluno


async def delete_aluno(session: AsyncSession, aluno_id: str) -> None:
    aluno = await get_aluno(session, aluno_id)
    await session.delete(aluno)
    await session.commit()