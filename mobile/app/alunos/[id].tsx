import * as DocumentPicker from "expo-document-picker";
import { useLocalSearchParams } from "expo-router";
import { useMutation, useQuery } from "@tanstack/react-query";
import { Linking, ScrollView, Text, View } from "react-native";
import { useState } from "react";

import { apiRequest, API_URL, uploadFile } from "@/api/client";
import { Badge } from "@/components/Badge";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { EmptyState } from "@/components/EmptyState";
import { ListItem } from "@/components/ListItem";
import { Tabs } from "@/components/Tabs";
import { useToast } from "@/store/toast-store";

export default function AlunoFichaScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [tab, setTab] = useState("aulas");
  const { show } = useToast();

  const ficha = useQuery({ queryKey: ["ficha", id], queryFn: () => apiRequest<any>(`/mobile/alunos/${id}/ficha`) });
  const anexos = useQuery({ queryKey: ["anexos", id], queryFn: () => apiRequest<any[]>(`/alunos/${id}/anexos`) });
  const upload = useMutation({ mutationFn: async () => {
    const file = await DocumentPicker.getDocumentAsync({ copyToCacheDirectory: true });
    if (file.canceled || !file.assets[0]) return;
    const f = file.assets[0];
    await uploadFile(`/alunos/${id}/anexos/upload`, { uri: f.uri, name: f.name, type: f.mimeType || "application/octet-stream" });
  }, onSuccess: () => { show("Anexo enviado"); anexos.refetch(); } });

  const aluno = ficha.data?.aluno;

  return (
    <ScrollView contentContainerStyle={{ padding: 16, gap: 12 }}>
      <Card>
        <Text style={{ fontSize: 24, fontWeight: "800" }}>{aluno?.nome || "Aluno"}</Text>
        <Badge label={aluno?.status || "ativo"} />
        <View style={{ flexDirection: "row", gap: 8 }}>
          <Button title="WhatsApp" variant="ghost" onPress={() => Linking.openURL(`https://wa.me/${aluno?.whatsapp_numero || ""}`)} />
          <Button title="Nova Aula" variant="ghost" onPress={() => show("Fluxo rápido de aula")}/>
          <Button title="Cobrança" variant="ghost" onPress={() => show("Fluxo rápido de cobrança")}/>
        </View>
      </Card>

      <Tabs items={[{ key: "aulas", label: "Aulas" }, { key: "financeiro", label: "Financeiro" }, { key: "whatsapp", label: "WhatsApp" }, { key: "contrato", label: "Contrato" }, { key: "anexos", label: "Anexos" }]} value={tab} onChange={setTab} />

      {tab === "aulas" ? <Card><Text>Total de aulas: {ficha.data?.resumo_aulas?.total ?? 0}</Text></Card> : null}
      {tab === "financeiro" ? <Card><Text>Total a receber: R$ {Number(ficha.data?.resumo_financeiro?.total_receber || 0).toFixed(2)}</Text></Card> : null}
      {tab === "whatsapp" ? <Card><Text>Mensagens: {ficha.data?.resumo_whatsapp?.total_mensagens ?? 0}</Text></Card> : null}
      {tab === "contrato" ? <Card><Text>Status: {ficha.data?.contrato_ativo?.status || "Sem contrato"}</Text></Card> : null}
      {tab === "anexos" ? (
        <Card>
          <Button title="Upload PDF/Imagem" onPress={() => upload.mutate()} />
          {(anexos.data || []).length === 0 ? <EmptyState title="Sem anexos" subtitle="Envie contratos, exames e documentos do aluno." /> : null}
          {(anexos.data || []).map((m: any) => (
            <ListItem key={m.id} title={m.file_name} subtitle={m.content_type} right="Abrir" onPress={() => Linking.openURL(`${API_URL}/media/${m.id}`)} />
          ))}
        </Card>
      ) : null}
    </ScrollView>
  );
}
