import asyncio
from datetime import date, datetime, timedelta

from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.agenda import Agenda
from app.models.aluno import Aluno
from app.models.aula import Aula
from app.models.categoria_financeira import CategoriaFinanceira
from app.models.conta_pagar import ContaPagar
from app.models.conta_receber import ContaReceber
from app.models.contrato import Contrato
from app.models.empresa_config import EmpresaConfig
from app.models.enums import (
    AulaOrigem,
    AulaStatus,
    BaseCalculo,
    CategoriaTipo,
    CompetenciaTipo,
    ComissaoTipo,
    ContaStatus,
    ContratoStatus,
    PlanoTipo,
    ProfissionalTipo,
    StatusDocumento,
)
from app.models.perfil_acesso import PerfilAcesso
from app.models.plano import Plano
from app.models.profissional import Profissional
from app.models.regra_comissao import RegraComissao
from app.models.unidade import Unidade
from app.models.user import Usuario


async def run_seeds() -> None:
    async with SessionLocal() as session:
        perfil_gestor = (await session.execute(select(PerfilAcesso).where(PerfilAcesso.nome == "Gestor"))).scalar_one_or_none()
        if not perfil_gestor:
            perfil_gestor = PerfilAcesso(nome="Gestor", permissoes={"*": True}, ativo=True)
            session.add(perfil_gestor)

        perfil_professor = (await session.execute(select(PerfilAcesso).where(PerfilAcesso.nome == "Professor"))).scalar_one_or_none()
        if not perfil_professor:
            perfil_professor = PerfilAcesso(
                nome="Professor",
                permissoes={"agenda": True, "alunos": True, "financeiro": True},
                ativo=True,
            )
            session.add(perfil_professor)

        perfil_aluno = (await session.execute(select(PerfilAcesso).where(PerfilAcesso.nome == "Aluno"))).scalar_one_or_none()
        if not perfil_aluno:
            perfil_aluno = PerfilAcesso(nome="Aluno", permissoes={"agenda": True, "financeiro": True}, ativo=True)
            session.add(perfil_aluno)

        config = (await session.execute(select(EmpresaConfig))).scalar_one_or_none()
        if not config:
            config = EmpresaConfig(nome_empresa="Beach Tennis Pro", tema={"primary": "#F97316", "secondary": "#0F766E"}, fonte="System")
            session.add(config)

        unidade = (await session.execute(select(Unidade).where(Unidade.slug == "principal"))).scalar_one_or_none()
        if not unidade:
            unidade = Unidade(
                nome="Unidade Principal",
                slug="principal",
                telefone="11999999999",
                email="contato@beach.local",
                custo_aula=35,
                valor_cobrado_aula=80,
                ativo=True,
            )
            session.add(unidade)
            await session.flush()

        agenda = (await session.execute(select(Agenda).where(Agenda.nome == "Agenda Principal"))).scalar_one_or_none()
        if not agenda:
            agenda = Agenda(nome="Agenda Principal", descricao="Agenda unificada", ativa=True)
            session.add(agenda)
            await session.flush()

        cat_receita = (
            await session.execute(select(CategoriaFinanceira).where(CategoriaFinanceira.nome == "Mensalidades"))
        ).scalar_one_or_none()
        if not cat_receita:
            cat_receita = CategoriaFinanceira(unidade_id=str(unidade.id), tipo=CategoriaTipo.receita, nome="Mensalidades", ativo=True)
            session.add(cat_receita)
            await session.flush()

        cat_despesa = (
            await session.execute(select(CategoriaFinanceira).where(CategoriaFinanceira.nome == "Comissoes"))
        ).scalar_one_or_none()
        if not cat_despesa:
            cat_despesa = CategoriaFinanceira(unidade_id=str(unidade.id), tipo=CategoriaTipo.despesa, nome="Comissoes", ativo=True)
            session.add(cat_despesa)
            await session.flush()

        plano = (await session.execute(select(Plano).where(Plano.nome == "Plano Mensal 2x"))).scalar_one_or_none()
        if not plano:
            plano = Plano(
                unidade_id=str(unidade.id),
                nome="Plano Mensal 2x",
                tipo=PlanoTipo.mensalidade,
                aulas_por_semana=2,
                qtd_aulas_pacote=None,
                duracao_meses=12,
                preco=640,
                ativo=True,
            )
            session.add(plano)
            await session.flush()

        gestor = (await session.execute(select(Usuario).where(Usuario.email == "gestor@local"))).scalar_one_or_none()
        if not gestor:
            gestor = Usuario(
                nome="Gestor",
                email="gestor@local",
                senha_hash=hash_password("gestor123"),
                perfil_acesso=perfil_gestor,
                unidade_id=str(unidade.id),
                ativo=True,
            )
            session.add(gestor)

        professor_user = (await session.execute(select(Usuario).where(Usuario.email == "professor@local"))).scalar_one_or_none()
        if not professor_user:
            professor_user = Usuario(
                nome="Professor",
                email="professor@local",
                senha_hash=hash_password("professor123"),
                perfil_acesso=perfil_professor,
                unidade_id=str(unidade.id),
                ativo=True,
            )
            session.add(professor_user)
            await session.flush()

        aluno_user = (await session.execute(select(Usuario).where(Usuario.email == "aluno@local"))).scalar_one_or_none()
        if not aluno_user:
            aluno_user = Usuario(
                nome="Aluno",
                email="aluno@local",
                senha_hash=hash_password("aluno123"),
                perfil_acesso=perfil_aluno,
                unidade_id=str(unidade.id),
                ativo=True,
            )
            session.add(aluno_user)

        professor = (await session.execute(select(Profissional).where(Profissional.email == "professor@local"))).scalar_one_or_none()
        if not professor:
            professor = Profissional(
                unidade_id=str(unidade.id),
                nome="Prof. Rafael",
                tipo=ProfissionalTipo.professor,
                telefone="11988887777",
                email="professor@local",
                usuario_id=str(professor_user.id),
                status="ativo",
                comissao_tipo=ComissaoTipo.percentual,
                comissao_valor=35,
            )
            session.add(professor)
            await session.flush()

        aluno = (await session.execute(select(Aluno).where(Aluno.email == "aluno@local"))).scalar_one_or_none()
        if not aluno:
            aluno = Aluno(
                unidade_id=str(unidade.id),
                nome="Ana Aluna",
                email="aluno@local",
                telefone="11977776666",
                status="ativo",
                whatsapp_numero="5511977776666",
                whatsapp_opt_in=True,
            )
            session.add(aluno)
            await session.flush()

        contrato = (await session.execute(select(Contrato).where(Contrato.aluno_id == aluno.id))).scalar_one_or_none()
        if not contrato:
            contrato = Contrato(
                unidade_id=str(unidade.id),
                aluno_id=str(aluno.id),
                plano_id=str(plano.id),
                data_inicio=date.today().replace(day=1),
                data_fim=None,
                status=ContratoStatus.ativo,
                dia_vencimento=10,
                desconto_valor=None,
                desconto_percentual=None,
                observacoes="Contrato ativo",
                status_documento=StatusDocumento.gerado,
            )
            session.add(contrato)

        regra = (await session.execute(select(RegraComissao).where(RegraComissao.unidade_id == unidade.id))).scalar_one_or_none()
        if not regra:
            regra = RegraComissao(
                unidade_id=str(unidade.id),
                ativa=True,
                dia_pagamento=5,
                competencia_tipo=CompetenciaTipo.mes_anterior,
                base_calculo=BaseCalculo.valor_cobrado_aula,
                categoria_financeira_id=str(cat_despesa.id),
                subcategoria_id=None,
            )
            session.add(regra)

        aula_existente = (
            await session.execute(select(Aula).where(Aula.aluno_id == aluno.id).limit(1))
        ).scalar_one_or_none()
        if not aula_existente:
            inicio_hoje = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
            for delta in [0, 1, 2]:
                aula = Aula(
                    agenda_id=str(agenda.id),
                    unidade_id=str(unidade.id),
                    aluno_id=str(aluno.id),
                    profissional_id=str(professor.id),
                    inicio=inicio_hoje + timedelta(days=delta),
                    fim=inicio_hoje + timedelta(days=delta, hours=1),
                    status=AulaStatus.confirmada if delta == 0 else AulaStatus.agendada,
                    origem=AulaOrigem.manual,
                    observacoes="Treino tecnico",
                )
                session.add(aula)

            inicio_mes_passado = (datetime.now().replace(day=1, hour=7, minute=30, second=0, microsecond=0) - timedelta(days=3))
            aula_realizada = Aula(
                agenda_id=str(agenda.id),
                unidade_id=str(unidade.id),
                aluno_id=str(aluno.id),
                profissional_id=str(professor.id),
                inicio=inicio_mes_passado,
                fim=inicio_mes_passado + timedelta(hours=1),
                status=AulaStatus.realizada,
                origem=AulaOrigem.manual,
                observacoes="Aula realizada para comissao",
            )
            session.add(aula_realizada)

        conta_receber = (
            await session.execute(select(ContaReceber).where(ContaReceber.aluno_id == aluno.id).limit(1))
        ).scalar_one_or_none()
        if not conta_receber:
            session.add(
                ContaReceber(
                    unidade_id=str(unidade.id),
                    aluno_id=str(aluno.id),
                    contrato_id=str(contrato.id) if contrato else None,
                    descricao="Mensalidade",
                    valor=640,
                    data_vencimento=date.today().replace(day=10),
                    status=ContaStatus.aberto,
                    categoria_id=str(cat_receita.id),
                    subcategoria_id=None,
                )
            )
            session.add(
                ContaReceber(
                    unidade_id=str(unidade.id),
                    aluno_id=str(aluno.id),
                    contrato_id=str(contrato.id) if contrato else None,
                    descricao="Mensalidade anterior",
                    valor=640,
                    data_vencimento=(date.today().replace(day=10) - timedelta(days=31)),
                    status=ContaStatus.pago,
                    categoria_id=str(cat_receita.id),
                    subcategoria_id=None,
                    data_pagamento=(date.today().replace(day=10) - timedelta(days=28)),
                )
            )

        conta_pagar = (
            await session.execute(select(ContaPagar).where(ContaPagar.profissional_id == professor.id).limit(1))
        ).scalar_one_or_none()
        if not conta_pagar:
            session.add(
                ContaPagar(
                    unidade_id=str(unidade.id),
                    fornecedor_nome=professor.nome,
                    profissional_id=str(professor.id),
                    descricao="Comissao professor",
                    valor=280,
                    data_vencimento=date.today().replace(day=5),
                    status=ContaStatus.aberto,
                    categoria_id=str(cat_despesa.id),
                    subcategoria_id=None,
                )
            )

        await session.commit()


def main() -> None:
    asyncio.run(run_seeds())


if __name__ == "__main__":
    main()

