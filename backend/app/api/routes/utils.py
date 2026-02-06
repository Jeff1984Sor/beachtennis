import re

import httpx
from fastapi import APIRouter

from app.core.errors import api_error

router = APIRouter(prefix="/utils")


@router.get("/cep/{cep}")
async def consulta_cep(cep: str):
    cep = re.sub(r"\D", "", cep)
    if len(cep) != 8:
        raise api_error("cep_invalido", "CEP invalido", 400)
    url = f"https://viacep.com.br/ws/{cep}/json/"
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
    if response.status_code != 200:
        raise api_error("cep_erro", "Erro ao consultar CEP", 502)
    data = response.json()
    if data.get("erro"):
        raise api_error("cep_nao_encontrado", "CEP nao encontrado", 404)
    return data