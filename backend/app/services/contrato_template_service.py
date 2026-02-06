from datetime import date, datetime

from jinja2.sandbox import SandboxedEnvironment


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