from datetime import date, datetime

from jinja2.sandbox import SandboxedEnvironment
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aluno import Aluno
from app.models.unidade import Unidade
from app.models.plano import Plano
from app.models.contrato import Contrato
from app.models.empresa_config import EmpresaConfig


def _format_date(value: date | datetime | None) -> str:
    if not value:
        return ""
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y")
    return value.strftime("%d/%m/%Y")


def _format_money(value: float | int | None) -> str:
    if value is None:
        return "R$ 0,00"
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def render_template(html: str, context: dict) -> str:
    env = SandboxedEnvironment(autoescape=False)
    env.filters["format_date"] = _format_date
    env.filters["format_money"] = _format_money
    env.filters["upper"] = lambda v: str(v).upper() if v is not None else ""
    env.filters["lower"] = lambda v: str(v).lower() if v is not None else ""

    template = env.from_string(html)
    return template.render(**context)


def default_context() -> dict:
    return {
        "aluno": {"nome": "Aluno Exemplo", "endereco": {"cidade": "Cidade"}},
        "unidade": {"nome": "Unidade Principal"},
        "plano": {"preco": 199.0},
        "contrato": {"data_inicio": date.today()},
        "financeiro": {"total_em_aberto": 0},
        "sistema": {"data_hoje": date.today()},
        "profissional": {"nome": "Professor"},
        "empresa": {"nome_empresa": "Beach Tennis School"},
    }


async def build_context(
    session: AsyncSession,
    contrato_id: str | None = None,
    aluno_id: str | None = None,
    unidade_id: str | None = None,
    plano_id: str | None = None,
) -> dict:
    context = default_context()

    if contrato_id:
        contrato = (await session.execute(select(Contrato).where(Contrato.id == contrato_id))).scalar_one_or_none()
        if contrato:
            context["contrato"] = {
                "data_inicio": contrato.data_inicio,
                "data_fim": contrato.data_fim,
                "status": contrato.status,
            }
            aluno_id = aluno_id or str(contrato.aluno_id)
            unidade_id = unidade_id or str(contrato.unidade_id)
            plano_id = plano_id or str(contrato.plano_id)

    if aluno_id:
        aluno = (await session.execute(select(Aluno).where(Aluno.id == aluno_id))).scalar_one_or_none()
        if aluno:
            context["aluno"] = {
                "nome": aluno.nome,
                "cpf": aluno.cpf,
                "email": aluno.email,
                "endereco": {"cidade": None},
            }

    if unidade_id:
        unidade = (await session.execute(select(Unidade).where(Unidade.id == unidade_id))).scalar_one_or_none()
        if unidade:
            context["unidade"] = {
                "nome": unidade.nome,
                "telefone": unidade.telefone,
            }

    if plano_id:
        plano = (await session.execute(select(Plano).where(Plano.id == plano_id))).scalar_one_or_none()
        if plano:
            context["plano"] = {"preco": float(plano.preco), "nome": plano.nome}

    empresa = (await session.execute(select(EmpresaConfig))).scalar_one_or_none()
    if empresa:
        context["empresa"] = {"nome_empresa": empresa.nome_empresa}

    return context