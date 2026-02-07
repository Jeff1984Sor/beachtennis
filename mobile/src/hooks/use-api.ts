import { useQuery } from "@tanstack/react-query";
import { apiRequest } from "@/api/client";

export function useAgenda(dia: string) {
  return useQuery({ queryKey: ["agenda-dia", dia], queryFn: () => apiRequest<{ aulas: any[] }>(`/mobile/agenda-dia?dia=${dia}`) });
}

export function useAlunos() {
  return useQuery({ queryKey: ["alunos-mobile"], queryFn: () => apiRequest<{ items: any[] }>("/mobile/alunos") });
}

export function useFinanceiro(tipo: "receber" | "pagar") {
  return useQuery({ queryKey: ["financeiro", tipo], queryFn: () => apiRequest<any>(`/mobile/financeiro?tipo=${tipo}`) });
}
