from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import OwnerType


class MediaFileOut(BaseModel):
    id: UUID
    unidade_id: UUID | None = None
    owner_type: OwnerType
    owner_id: UUID | None = None
    folder: str | None = None
    filename_storage: str
    filename_original: str | None = None
    content_type: str | None = None
    size_bytes: int | None = None
    checksum_sha256: str | None = None
    uploaded_by: UUID | None = None
    created_at: datetime | None = None