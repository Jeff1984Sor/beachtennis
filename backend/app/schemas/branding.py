from pydantic import BaseModel

from app.schemas.base import UUIDModel, Timestamped


class EmpresaConfigBase(BaseModel):
    nome_empresa: str
    tema: dict | None = None
    fonte: str | None = None


class EmpresaConfigOut(UUIDModel, Timestamped, EmpresaConfigBase):
    logo_media_id: str | None = None
    logo_url: str | None = None


class EmpresaConfigUpdate(BaseModel):
    nome_empresa: str | None = None
    tema: dict | None = None
    fonte: str | None = None