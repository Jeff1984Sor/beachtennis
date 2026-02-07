from pydantic import BaseModel


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class MeResponse(BaseModel):
    user_id: str
    nome: str
    email: str
    roles: list[str]
    profissional_id: str | None = None
    aluno_id: str | None = None
    unidade_id: str | None = None
    agenda_id: str | None = None
