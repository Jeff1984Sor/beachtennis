import { router } from "expo-router";
import { ScrollView, Text } from "react-native";

import { Card } from "@/components/Card";
import { EmptyState } from "@/components/EmptyState";
import { ListItem } from "@/components/ListItem";
import { LoadingSkeleton } from "@/components/LoadingSkeleton";
import { useAlunos } from "@/hooks/use-api";

export default function AlunosScreen() {
  const query = useAlunos();
  return (
    <ScrollView contentContainerStyle={{ padding: 16, gap: 12 }}>
      <Card><Text style={{ fontSize: 22, fontWeight: "800" }}>Alunos</Text></Card>
      {query.isLoading ? <LoadingSkeleton /> : null}
      {!query.isLoading && (query.data?.items?.length || 0) === 0 ? <EmptyState title="Nenhum aluno" subtitle="Quando houver matrículas, aparecerão aqui." /> : null}
      {(query.data?.items || []).map((a) => (
        <Card key={a.id}><ListItem title={a.nome} subtitle={a.email || a.telefone || "Sem contato"} right={a.status || "ativo"} onPress={() => router.push(`/alunos/${a.id}`)} /></Card>
      ))}
    </ScrollView>
  );
}
