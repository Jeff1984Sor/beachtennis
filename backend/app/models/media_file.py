from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin
from app.models.enums import OwnerType


class MediaFile(UUIDMixin, Base):
    __tablename__ = "media_files"

    unidade_id: Mapped[str | None] = mapped_column(ForeignKey("unidades.id"), nullable=True)
    owner_type: Mapped[OwnerType] = mapped_column(Enum(OwnerType))
    owner_id: Mapped[str | None] = mapped_column(nullable=True)
    folder: Mapped[str | None] = mapped_column(String(120))
    filename_storage: Mapped[str] = mapped_column(String(255))
    filename_original: Mapped[str | None] = mapped_column(String(255))
    content_type: Mapped[str | None] = mapped_column(String(120))
    size_bytes: Mapped[int | None] = mapped_column(Integer)
    checksum_sha256: Mapped[str | None] = mapped_column(String(128))
    uploaded_by: Mapped[str | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())
