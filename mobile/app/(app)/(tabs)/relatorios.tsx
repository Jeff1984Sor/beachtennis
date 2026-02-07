import { useQuery } from "@tanstack/react-query";
import { ScrollView, Text } from "react-native";
import { Card } from "@/components/Card";
import { apiRequest } from "@/api/client";
import { useAuth } from "@/store/auth-store";

export default function RelatoriosScreen() {
  const { me } = useAuth();
  const q = useQuery({ queryKey: ["dre"], queryFn: () => apiRequest<any>(`/financeiro/dre?unidade_id=${me?.unidade_id}&inicio=${new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().slice(0,10)}&fim=${new Date().toISOString().slice(0,10)}&modo=caixa`) });
  return <ScrollView contentContainerStyle={{ padding: 16, gap: 12 }}><Card><Text style={{ fontSize: 22, fontWeight: "800" }}>DRE</Text><Text>Resultado: R$ {Number(q.data?.resultado || 0).toFixed(2)}</Text></Card></ScrollView>;
}
