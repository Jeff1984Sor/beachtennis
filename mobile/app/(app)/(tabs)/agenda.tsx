import { useMemo, useState } from "react";
import { ScrollView, Text, View } from "react-native";

import { Badge } from "@/components/Badge";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { EmptyState } from "@/components/EmptyState";
import { LoadingSkeleton } from "@/components/LoadingSkeleton";
import { Tabs } from "@/components/Tabs";
import { useAgenda } from "@/hooks/use-api";
import { apiRequest } from "@/api/client";
import { useToast } from "@/store/toast-store";

function today() { return new Date().toISOString().slice(0, 10); }

export default function AgendaScreen() {
  const [dia, setDia] = useState(today());
  const [filtro, setFiltro] = useState("todos");
  const { show } = useToast();
  const query = useAgenda(dia);

  const items = useMemo(() => {
    const all = query.data?.aulas || [];
    return filtro === "todos" ? all : all.filter((a) => a.status === filtro);
  }, [query.data, filtro]);

  const updateStatus = async (id: string, status: string) => {
    await apiRequest(`/agenda/aulas/${id}`, { method: "PUT", body: JSON.stringify({ status }) });
    show("Status atualizado");
    query.refetch();
  };

  return (
    <ScrollView contentContainerStyle={{ padding: 16, gap: 12 }}>
      <Card>
        <Text style={{ fontSize: 22, fontWeight: "800" }}>Agenda do dia</Text>
        <Tabs items={[{ key: today(), label: "Hoje" }, { key: new Date(Date.now() + 86400000).toISOString().slice(0, 10), label: "Amanhã" }]} value={dia} onChange={setDia} />
        <Tabs items={[{ key: "todos", label: "Todos" }, { key: "confirmada", label: "Confirmadas" }, { key: "agendada", label: "Agendadas" }, { key: "realizada", label: "Realizadas" }]} value={filtro} onChange={setFiltro} />
      </Card>
      {query.isLoading ? <LoadingSkeleton height={120} /> : null}
      {!query.isLoading && items.length === 0 ? <EmptyState title="Sem aulas por aqui" subtitle="Ajuste a data ou filtros para ver aulas." /> : null}
      {items.map((a) => (
        <Card key={a.id}>
          <View style={{ flexDirection: "row", justifyContent: "space-between" }}>
            <Text style={{ fontWeight: "800", fontSize: 16 }}>{new Date(a.inicio).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</Text>
            <Badge label={a.status} tone={a.status === "realizada" ? "success" : a.status === "cancelada" ? "danger" : "neutral"} />
          </View>
          <Text>{a.aluno_nome} • {a.professor_nome || "Sem professor"}</Text>
          <Text>{a.unidade_nome}</Text>
          <View style={{ flexDirection: "row", gap: 8 }}>
            <Button title="Confirmar" onPress={() => updateStatus(a.id, "confirmada")} variant="ghost" />
            <Button title="Realizada" onPress={() => updateStatus(a.id, "realizada")} variant="ghost" />
            <Button title="Cancelar" onPress={() => updateStatus(a.id, "cancelada")} variant="ghost" />
          </View>
        </Card>
      ))}
    </ScrollView>
  );
}
