import { useState } from "react";
import { ScrollView, Text } from "react-native";

import { Card } from "@/components/Card";
import { EmptyState } from "@/components/EmptyState";
import { ListItem } from "@/components/ListItem";
import { LoadingSkeleton } from "@/components/LoadingSkeleton";
import { Tabs } from "@/components/Tabs";
import { useFinanceiro } from "@/hooks/use-api";
import { useAuth } from "@/store/auth-store";

export default function FinanceiroScreen() {
  const { activeRole } = useAuth();
  const [tipo, setTipo] = useState<"receber" | "pagar">(activeRole === "professor" ? "pagar" : "receber");
  const query = useFinanceiro(tipo);
  const isGestor = activeRole === "gestor";

  return (
    <ScrollView contentContainerStyle={{ padding: 16, gap: 12 }}>
      <Card>
        <Text style={{ fontSize: 22, fontWeight: "800" }}>{activeRole === "professor" ? "Minhas Comissões" : "Financeiro"}</Text>
        {(isGestor || activeRole === "professor") ? <Tabs items={[{ key: "receber", label: "Receber" }, { key: "pagar", label: "Pagar" }]} value={tipo} onChange={(k) => setTipo(k as any)} /> : null}
      </Card>
      {query.isLoading ? <LoadingSkeleton /> : null}
      {!query.isLoading && (query.data?.itens?.length || 0) === 0 ? <EmptyState title="Sem lançamentos" subtitle="Não há itens para o período atual." /> : null}
      <Card><Text>Total previsto: R$ {query.data?.total_previsto?.toFixed?.(2) || "0,00"}</Text><Text>Total pago: R$ {query.data?.total_pago?.toFixed?.(2) || "0,00"}</Text></Card>
      {(query.data?.itens || []).map((i: any) => <Card key={i.id}><ListItem title={i.descricao} subtitle={i.data_vencimento} right={`R$ ${Number(i.valor).toFixed(2)}`} /></Card>)}
    </ScrollView>
  );
}
