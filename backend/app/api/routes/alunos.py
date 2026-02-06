from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.deps import get_current_user
from app.schemas.aluno import AlunoOut, AlunoCreate, AlunoUpdate, AlunoFichaOut
from app.schemas.media import MediaFileOut
from app.services.aluno_service import list_alunos, get_aluno, create_aluno, update_aluno, delete_aluno
from app.services.media_service import save_upload
from app.models.media_file import MediaFile
from app.models.enums import OwnerType

router = APIRouter(prefix="/alunos")


@router.get("", response_model=list[AlunoOut])
async def listar(
    limit: int = 20,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> list[AlunoOut]:
    alunos = await list_alunos(session, limit, offset)
    return [AlunoOut.model_validate(a) for a in alunos]


@router.post("", response_model=AlunoOut)
async def criar(
    payload: AlunoCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> AlunoOut:
    aluno = await create_aluno(session, payload.model_dump())
    return AlunoOut.model_validate(aluno)


@router.get("/{aluno_id}", response_model=AlunoOut)
async def obter(
    aluno_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> AlunoOut:
    aluno = await get_aluno(session, aluno_id)
    return AlunoOut.model_validate(aluno)


@router.put("/{aluno_id}", response_model=AlunoOut)
async def atualizar(
    aluno_id: str,
    payload: AlunoUpdate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> AlunoOut:
    aluno = await update_aluno(session, aluno_id, payload.model_dump(exclude_unset=True))
    return AlunoOut.model_validate(aluno)


@router.delete("/{aluno_id}")
async def remover(
    aluno_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    await delete_aluno(session, aluno_id)
    return {"status": "deleted"}


@router.get("/{aluno_id}/ficha", response_model=AlunoFichaOut)
async def ficha(
    aluno_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> AlunoFichaOut:
    aluno = await get_aluno(session, aluno_id)
    anexos_result = await session.execute(
        select(MediaFile).where(MediaFile.owner_type == OwnerType.aluno, MediaFile.owner_id == aluno_id)
    )
    anexos = [MediaFileOut.model_validate(m) for m in anexos_result.scalars()]
    return AlunoFichaOut(
        aluno=AlunoOut.model_validate(aluno),
        resumo_aulas={},
        resumo_financeiro={},
        resumo_whatsapp={},
        contrato_ativo=None,
        anexos=anexos,
    )


@router.get("/{aluno_id}/anexos", response_model=list[MediaFileOut])
async def listar_anexos(
    aluno_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> list[MediaFileOut]:
    result = await session.execute(
        select(MediaFile).where(MediaFile.owner_type == OwnerType.aluno, MediaFile.owner_id == aluno_id)
    )
    return [MediaFileOut.model_validate(m) for m in result.scalars()]


@router.post("/{aluno_id}/anexos/upload", response_model=MediaFileOut)
async def upload_anexo(
    aluno_id: str,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> MediaFileOut:
    media = await save_upload(
        session,
        file,
        owner_type=OwnerType.aluno,
        owner_id=aluno_id,
        unidade_id=None,
        folder="alunos",
        uploaded_by=str(user.id),
    )
    return MediaFileOut.model_validate(media)