import asyncio

from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.perfil_acesso import PerfilAcesso
from app.models.user import Usuario
from app.models.empresa_config import EmpresaConfig
from app.models.agenda import Agenda
from app.models.categoria_financeira import CategoriaFinanceira
from app.models.enums import CategoriaTipo


async def run_seeds() -> None:
    async with SessionLocal() as session:
        perfil = (await session.execute(select(PerfilAcesso).where(PerfilAcesso.nome == "Admin"))).scalar_one_or_none()
        if not perfil:
            perfil = PerfilAcesso(nome="Admin", permissoes={"*": True}, ativo=True)
            session.add(perfil)

        admin = (await session.execute(select(Usuario).where(Usuario.email == "admin@local"))).scalar_one_or_none()
        if not admin:
            admin = Usuario(
                nome="Admin",
                email="admin@local",
                senha_hash=hash_password("admin123"),
                perfil_acesso=perfil,
                ativo=True,
            )
            session.add(admin)

        config = (await session.execute(select(EmpresaConfig))).scalar_one_or_none()
        if not config:
            config = EmpresaConfig(nome_empresa="Beach Tennis School", tema=None, fonte=None)
            session.add(config)

        agenda = (await session.execute(select(Agenda).where(Agenda.nome == "Agenda Principal"))).scalar_one_or_none()
        if not agenda:
            agenda = Agenda(nome="Agenda Principal", descricao="Agenda unificada", ativa=True)
            session.add(agenda)

        cat_receita = (await session.execute(select(CategoriaFinanceira).where(CategoriaFinanceira.nome == "Mensalidades"))).scalar_one_or_none()
        if not cat_receita:
            session.add(CategoriaFinanceira(unidade_id=None, tipo=CategoriaTipo.receita, nome="Mensalidades", ativo=True))

        cat_despesa = (await session.execute(select(CategoriaFinanceira).where(CategoriaFinanceira.nome == "Comissoes"))).scalar_one_or_none()
        if not cat_despesa:
            session.add(CategoriaFinanceira(unidade_id=None, tipo=CategoriaTipo.despesa, nome="Comissoes", ativo=True))

        await session.commit()


def main() -> None:
    asyncio.run(run_seeds())


if __name__ == "__main__":
    main()