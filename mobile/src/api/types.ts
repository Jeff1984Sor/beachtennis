import { Role } from "@/theme";

export type MeResponse = {
  user_id: string;
  nome: string;
  email: string;
  roles: Role[];
  profissional_id?: string | null;
  aluno_id?: string | null;
  unidade_id?: string | null;
  agenda_id?: string | null;
};

export type AgendaItem = {
  id: string;
  inicio: string;
  fim: string;
  status: string;
  aluno_nome: string;
  professor_nome?: string | null;
  unidade_nome: string;
  aluno_id: string;
};
