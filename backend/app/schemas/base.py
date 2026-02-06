from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class APIModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Timestamped(APIModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UUIDModel(APIModel):
    id: UUID