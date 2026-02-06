from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.core.deps import get_current_user
from app.core.errors import api_error
from app.schemas.media import MediaFileOut
from app.services.media_service import save_upload, file_path
from app.models.media_file import MediaFile
from app.models.enums import OwnerType

router = APIRouter(prefix="/media")


@router.post("/upload", response_model=MediaFileOut)
async def upload_media(
    file: UploadFile = File(...),
    owner_type: OwnerType = OwnerType.outro,
    owner_id: str | None = None,
    unidade_id: str | None = None,
    folder: str | None = None,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> MediaFileOut:
    media = await save_upload(session, file, owner_type, owner_id, unidade_id, folder, str(user.id))
    return MediaFileOut.model_validate(media)


@router.get("/{media_id}")
async def get_media(
    media_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    result = await session.execute(select(MediaFile).where(MediaFile.id == media_id))
    media = result.scalar_one_or_none()
    if not media:
        raise api_error("not_found", "Arquivo nao encontrado", 404)
    path = file_path(media)
    if not path.exists():
        raise api_error("not_found", "Arquivo nao encontrado", 404)
    return FileResponse(path)


@router.delete("/{media_id}")
async def delete_media(
    media_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    result = await session.execute(select(MediaFile).where(MediaFile.id == media_id))
    media = result.scalar_one_or_none()
    if not media:
        raise api_error("not_found", "Arquivo nao encontrado", 404)
    path = file_path(media)
    if path.exists():
        path.unlink()
    await session.delete(media)
    await session.commit()
    return {"status": "deleted"}