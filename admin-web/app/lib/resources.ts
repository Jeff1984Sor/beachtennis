export type FieldType =
  | "text"
  | "number"
  | "date"
  | "datetime"
  | "time"
  | "boolean"
  | "json"
  | "textarea";

export type FieldDef = {
  key: string;
  label?: string;
  type?: FieldType;
};

export type ResourceDef = {
  key: string;
  label: string;
  fields: FieldDef[];
  listColumns?: string[];
};

export const RESOURCE_DEFS: ResourceDef[] = [
  {
    key: "alunos",
    label: "Alunos",
    listColumns: ["nome", "telefone", "email", "status"],
    fields: [
      { key: "unidade_id" },
      { key: "nome" },
      { key: "cpf" },
      { key: "data_nascimento", type: "date" },
      { key: "telefone" },
      { key: "email" },
      { key: "endereco_id" },
      { key: "observacoes", type: "textarea" },
      { key: "status" },
      { key: "whatsapp_numero" },
      { key: "whatsapp_opt_in", type: "boolean" },
      { key: "whatsapp_ultimo_contato_em", type: "date" },
      { key: "whatsapp_tags", type: "json" }
    ]
  },
  {
    key: "profissionais",
    label: "Profissionais",
    listColumns: ["nome", "tipo", "telefone", "email"],
    fields: [
      { key: "unidade_id" },
      { key: "nome" },
      { key: "tipo" },
      { key: "registro" },
      { key: "telefone" },
      { key: "email" },
      { key: "endereco_id" },
      { key: "usuario_id" },
      { key: "status" },
      { key: "comissao_tipo" },
      { key: "comissao_valor", type: "number" }
    ]
  },
  {
    key: "usuarios",
    label: "Usuários",
    listColumns: ["nome", "email", "ativo"],
    fields: [
      { key: "nome" },
      { key: "email" },
      { key: "senha_hash" },
      { key: "telefone" },
      { key: "perfil_acesso_id" },
      { key: "unidade_id" },
      { key: "ativo", type: "boolean" },
      { key: "last_login_at", type: "datetime" }
    ]
  },
  {
    key: "perfis_acesso",
    label: "Perfis de Acesso",
    listColumns: ["nome", "ativo"],
    fields: [
      { key: "nome" },
      { key: "permissoes", type: "json" },
      { key: "ativo", type: "boolean" }
    ]
  },
  {
    key: "unidades",
    label: "Unidades",
    listColumns: ["nome", "slug", "telefone", "ativo"],
    fields: [
      { key: "nome" },
      { key: "slug" },
      { key: "telefone" },
      { key: "email" },
      { key: "cnpj" },
      { key: "endereco_id" },
      { key: "capacidade_simultanea", type: "number" },
      { key: "custo_aula", type: "number" },
      { key: "valor_cobrado_aula", type: "number" },
      { key: "ativo", type: "boolean" }
    ]
  },
  {
    key: "planos",
    label: "Planos",
    listColumns: ["nome", "tipo", "preco", "ativo"],
    fields: [
      { key: "unidade_id" },
      { key: "nome" },
      { key: "tipo" },
      { key: "aulas_por_semana", type: "number" },
      { key: "qtd_aulas_pacote", type: "number" },
      { key: "duracao_meses", type: "number" },
      { key: "preco", type: "number" },
      { key: "ativo", type: "boolean" }
    ]
  },
  {
    key: "contratos",
    label: "Contratos",
    listColumns: ["aluno_id", "plano_id", "status", "dia_vencimento"],
    fields: [
      { key: "unidade_id" },
      { key: "aluno_id" },
      { key: "plano_id" },
      { key: "data_inicio", type: "date" },
      { key: "data_fim", type: "date" },
      { key: "status" },
      { key: "dia_vencimento", type: "number" },
      { key: "desconto_valor", type: "number" },
      { key: "desconto_percentual", type: "number" },
      { key: "observacoes", type: "textarea" },
      { key: "modelo_contrato_id" },
      { key: "contrato_renderizado_html", type: "textarea" },
      { key: "contrato_renderizado_pdf_media_id" },
      { key: "data_geracao_contrato", type: "datetime" },
      { key: "status_documento" }
    ]
  },
  {
    key: "agendas",
    label: "Agendas",
    listColumns: ["nome", "ativa"],
    fields: [
      { key: "nome" },
      { key: "descricao" },
      { key: "ativa", type: "boolean" }
    ]
  },
  {
    key: "agenda_unidades",
    label: "Agenda x Unidade",
    listColumns: ["agenda_id", "unidade_id", "ativo"],
    fields: [
      { key: "agenda_id" },
      { key: "unidade_id" },
      { key: "ativo", type: "boolean" }
    ]
  },
  {
    key: "disponibilidades_agenda",
    label: "Disponibilidades (Agenda)",
    listColumns: ["agenda_id", "dia_semana", "hora_inicio", "hora_fim"],
    fields: [
      { key: "agenda_id" },
      { key: "dia_semana", type: "number" },
      { key: "hora_inicio", type: "time" },
      { key: "hora_fim", type: "time" },
      { key: "capacidade_base", type: "number" },
      { key: "ativo", type: "boolean" }
    ]
  },
  {
    key: "disponibilidades_unidade_override",
    label: "Overrides (Unidade)",
    listColumns: ["agenda_id", "unidade_id", "dia_semana", "hora_inicio"],
    fields: [
      { key: "agenda_id" },
      { key: "unidade_id" },
      { key: "dia_semana", type: "number" },
      { key: "hora_inicio", type: "time" },
      { key: "hora_fim", type: "time" },
      { key: "capacidade_override", type: "number" },
      { key: "ativo", type: "boolean" }
    ]
  },
  {
    key: "bloqueios_agenda",
    label: "Bloqueios",
    listColumns: ["agenda_id", "tipo", "impacto", "ativo"],
    fields: [
      { key: "agenda_id" },
      { key: "unidade_id" },
      { key: "tipo" },
      { key: "titulo" },
      { key: "motivo", type: "textarea" },
      { key: "impacto" },
      { key: "capacidade_nova", type: "number" },
      { key: "dia_semana", type: "number" },
      { key: "hora_inicio", type: "time" },
      { key: "hora_fim", type: "time" },
      { key: "data_inicio", type: "date" },
      { key: "data_fim", type: "date" },
      { key: "ativo", type: "boolean" }
    ]
  },
  {
    key: "aulas",
    label: "Aulas",
    listColumns: ["aluno_id", "inicio", "fim", "status"],
    fields: [
      { key: "agenda_id" },
      { key: "unidade_id" },
      { key: "aluno_id" },
      { key: "profissional_id" },
      { key: "inicio", type: "datetime" },
      { key: "fim", type: "datetime" },
      { key: "status" },
      { key: "origem" },
      { key: "observacoes", type: "textarea" }
    ]
  },
  {
    key: "mensagens_whatsapp",
    label: "WhatsApp",
    listColumns: ["aluno_id", "tipo", "status", "provider"],
    fields: [
      { key: "unidade_id" },
      { key: "aluno_id" },
      { key: "tipo" },
      { key: "template_key" },
      { key: "conteudo", type: "textarea" },
      { key: "status" },
      { key: "provider" },
      { key: "provider_message_id" },
      { key: "erro", type: "textarea" },
      { key: "agendada_para", type: "datetime" },
      { key: "enviada_em", type: "datetime" },
      { key: "created_by" }
    ]
  },
  {
    key: "modelos_contrato",
    label: "Modelos de Contrato",
    listColumns: ["nome", "motor_template", "ativo", "versao"],
    fields: [
      { key: "unidade_id" },
      { key: "nome" },
      { key: "descricao" },
      { key: "conteudo_html", type: "textarea" },
      { key: "motor_template" },
      { key: "versao", type: "number" },
      { key: "ativo", type: "boolean" },
      { key: "created_by" }
    ]
  },
  {
    key: "variaveis_contrato",
    label: "Variáveis de Contrato",
    listColumns: ["chave", "categoria", "tipo", "ativo"],
    fields: [
      { key: "chave" },
      { key: "descricao" },
      { key: "exemplo" },
      { key: "categoria" },
      { key: "tipo" },
      { key: "ativo", type: "boolean" }
    ]
  },
  {
    key: "categorias_financeiras",
    label: "Categorias Financeiras",
    listColumns: ["nome", "tipo", "ativo"],
    fields: [
      { key: "unidade_id" },
      { key: "tipo" },
      { key: "nome" },
      { key: "ativo", type: "boolean" }
    ]
  },
  {
    key: "subcategorias_financeiras",
    label: "Subcategorias",
    listColumns: ["categoria_id", "nome", "ativo"],
    fields: [
      { key: "categoria_id" },
      { key: "nome" },
      { key: "ativo", type: "boolean" }
    ]
  },
  {
    key: "contas_bancarias",
    label: "Contas Bancárias",
    listColumns: ["nome", "banco_agencia_conta", "ativo"],
    fields: [
      { key: "unidade_id" },
      { key: "nome" },
      { key: "banco_agencia_conta" },
      { key: "saldo_inicial", type: "number" },
      { key: "ativo", type: "boolean" }
    ]
  },
  {
    key: "contas_receber",
    label: "Contas a Receber",
    listColumns: ["aluno_id", "valor", "data_vencimento", "status"],
    fields: [
      { key: "unidade_id" },
      { key: "aluno_id" },
      { key: "contrato_id" },
      { key: "descricao" },
      { key: "valor", type: "number" },
      { key: "data_vencimento", type: "date" },
      { key: "status" },
      { key: "categoria_id" },
      { key: "subcategoria_id" },
      { key: "forma_pagamento" },
      { key: "conta_bancaria_id" },
      { key: "data_pagamento", type: "date" },
      { key: "juros_multa_desconto", type: "number" },
      { key: "observacoes", type: "textarea" }
    ]
  },
  {
    key: "contas_pagar",
    label: "Contas a Pagar",
    listColumns: ["fornecedor_nome", "valor", "data_vencimento", "status"],
    fields: [
      { key: "unidade_id" },
      { key: "fornecedor_nome" },
      { key: "profissional_id" },
      { key: "descricao" },
      { key: "valor", type: "number" },
      { key: "data_vencimento", type: "date" },
      { key: "status" },
      { key: "categoria_id" },
      { key: "subcategoria_id" },
      { key: "conta_bancaria_id" },
      { key: "data_pagamento", type: "date" },
      { key: "observacoes", type: "textarea" }
    ]
  },
  {
    key: "movimentos_bancarios",
    label: "Movimentos Bancários",
    listColumns: ["tipo", "origem", "valor", "data_movimento"],
    fields: [
      { key: "unidade_id" },
      { key: "conta_bancaria_id" },
      { key: "tipo" },
      { key: "origem" },
      { key: "receber_id" },
      { key: "pagar_id" },
      { key: "transferencia_group_id" },
      { key: "valor", type: "number" },
      { key: "data_movimento", type: "date" },
      { key: "categoria_id" },
      { key: "subcategoria_id" },
      { key: "descricao" },
      { key: "created_by" }
    ]
  },
  {
    key: "regras_comissao",
    label: "Regras de Comissão",
    listColumns: ["unidade_id", "dia_pagamento", "ativa"],
    fields: [
      { key: "unidade_id" },
      { key: "ativa", type: "boolean" },
      { key: "dia_pagamento", type: "number" },
      { key: "competencia_tipo" },
      { key: "base_calculo" },
      { key: "categoria_financeira_id" },
      { key: "subcategoria_id" }
    ]
  },
  {
    key: "execucoes_rotina",
    label: "Execuções de Rotina",
    listColumns: ["chave", "status", "executada_em"],
    fields: [
      { key: "chave" },
      { key: "executada_em", type: "datetime" },
      { key: "status" },
      { key: "detalhes_erro", type: "textarea" }
    ]
  },
  {
    key: "enderecos",
    label: "Endereços",
    listColumns: ["logradouro", "numero", "cidade", "estado"],
    fields: [
      { key: "logradouro" },
      { key: "numero" },
      { key: "complemento" },
      { key: "bairro" },
      { key: "cidade" },
      { key: "estado" },
      { key: "cep" },
      { key: "pais" },
      { key: "latitude", type: "number" },
      { key: "longitude", type: "number" }
    ]
  },
  {
    key: "empresa_config",
    label: "Empresa (Config)",
    listColumns: ["nome_empresa", "fonte"],
    fields: [
      { key: "nome_empresa" },
      { key: "logo_media_id" },
      { key: "tema", type: "json" },
      { key: "fonte" }
    ]
  },
  {
    key: "media_files",
    label: "Media Files",
    listColumns: ["owner_type", "filename_storage", "size_bytes"],
    fields: [
      { key: "unidade_id" },
      { key: "owner_type" },
      { key: "owner_id" },
      { key: "folder" },
      { key: "filename_storage" },
      { key: "filename_original" },
      { key: "content_type" },
      { key: "size_bytes", type: "number" },
      { key: "checksum_sha256" },
      { key: "uploaded_by" }
    ]
  }
];
