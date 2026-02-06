import hashlib
import os
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.media_file import MediaFile
from app.models.enums import OwnerType


def _media_folder(base: str) -> Path:
    now = datetime.utcnow()
    return Path(base) / f"{now.year}" / f"{now.month:02d}"


async def save_upload(
    session: AsyncSession,
    file: UploadFile,
    owner_type: OwnerType,
    owner_id: str | None,
    unidade_id: str | None,
    folder: str | None,
    uploaded_by: str | None,
) -> MediaFile:
    media_root = Path(settings.media_root)
    target_folder = _media_folder(media_root)
    if folder:
        target_folder = target_folder / folder
    target_folder.mkdir(parents=True, exist_ok=True)

    extension = ""
    if file.filename and "." in file.filename:
        extension = "." + file.filename.split(".")[-1]

    storage_name = f"{uuid.uuid4()}{extension}"
    storage_path = target_folder / storage_name

    hasher = hashlib.sha256()
    size = 0
    with storage_path.open("wb") as buffer:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            buffer.write(chunk)
            hasher.update(chunk)
            size += len(chunk)

    media = MediaFile(
        unidade_id=unidade_id,
        owner_type=owner_type,
        owner_id=owner_id,
        folder=folder,
        filename_storage=str(storage_path.relative_to(media_root)),
        filename_original=file.filename,
        content_type=file.content_type,
        size_bytes=size,
        checksum_sha256=hasher.hexdigest(),
        uploaded_by=uploaded_by,
    )
    session.add(media)
    await session.commit()
    await session.refresh(media)
    return media


def file_path(media: MediaFile) -> Path:
    return Path(settings.media_root) / media.filename_storage