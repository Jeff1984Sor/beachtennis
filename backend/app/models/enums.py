from enum import Enum


class OwnerType(str, Enum):
    empresa = "empresa"
    aluno = "aluno"
    profissional = "profissional"
    unidade = "unidade"
    contrato = "contrato"
    aula = "aula"
    financeiro = "financeiro"
    outro = "outro"


class ProfissionalTipo(str, Enum):
    professor = "professor"
    recepcao = "recepcao"
    admin = "admin"
    financeiro = "financeiro"


class PlanoTipo(str, Enum):
    mensalidade = "mensalidade"
    pacote_aulas = "pacote_aulas"


class ContratoStatus(str, Enum):
    ativo = "ativo"
    pausado = "pausado"
    cancelado = "cancelado"
    encerrado = "encerrado"


class StatusDocumento(str, Enum):
    nao_gerado = "nao_gerado"
    gerado = "gerado"
    assinado = "assinado"


class BloqueioTipo(str, Enum):
    fixo = "fixo"
    eventual = "eventual"


class BloqueioImpacto(str, Enum):
    bloquear_total = "bloquear_total"
    reduzir_capacidade = "reduzir_capacidade"


class AulaStatus(str, Enum):
    agendada = "agendada"
    confirmada = "confirmada"
    realizada = "realizada"
    cancelada = "cancelada"
    falta = "falta"


class AulaOrigem(str, Enum):
    manual = "manual"
    contrato = "contrato"
    remarcacao = "remarcacao"


class MensagemTipo(str, Enum):
    manual = "manual"
    automatica = "automatica"


class MensagemStatus(str, Enum):
    fila = "fila"
    enviada = "enviada"
    entregue = "entregue"
    lida = "lida"
    falhou = "falhou"
    cancelada = "cancelada"


class MensagemProvider(str, Enum):
    evolution = "evolution"
    waha = "waha"
    meta = "meta"
    outro = "outro"


class MotorTemplate(str, Enum):
    jinja2 = "jinja2"


class CategoriaTipo(str, Enum):
    receita = "receita"
    despesa = "despesa"


class ContaStatus(str, Enum):
    aberto = "aberto"
    pago = "pago"
    atrasado = "atrasado"
    cancelado = "cancelado"


class MovimentoTipo(str, Enum):
    entrada = "entrada"
    saida = "saida"
    transferencia = "transferencia"


class MovimentoOrigem(str, Enum):
    receber = "receber"
    pagar = "pagar"
    ajuste_manual = "ajuste_manual"
    transferencia = "transferencia"


class ComissaoTipo(str, Enum):
    percentual = "percentual"
    valor_por_aula = "valor_por_aula"


class CompetenciaTipo(str, Enum):
    mes_anterior = "mes_anterior"


class BaseCalculo(str, Enum):
    valor_cobrado_aula = "valor_cobrado_aula"
    receita_real = "receita_real"


class ExecucaoStatus(str, Enum):
    sucesso = "sucesso"
    falha = "falha"