from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class EmpresaConfig(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "empresa_config"

    nome_empresa: Mapped[str] = mapped_column(String(255))
    logo_media_id: Mapped[str | None] = mapped_column(ForeignKey("media_files.id"), nullable=True)
    tema: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    fonte: Mapped[str | None] = mapped_column(String(120))

    logo: Mapped["MediaFile" | None] = relationship("MediaFile", foreign_keys=[logo_media_id])