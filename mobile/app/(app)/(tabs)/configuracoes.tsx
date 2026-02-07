import { useState } from "react";
import { ScrollView, Text, View } from "react-native";
import { useMutation, useQuery } from "@tanstack/react-query";

import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Input } from "@/components/Input";
import { apiRequest } from "@/api/client";
import { useAuth } from "@/store/auth-store";
import { useToast } from "@/store/toast-store";

export default function ConfigScreen() {
  const { me } = useAuth();
  const { show } = useToast();
  const [cep, setCep] = useState("");
  const [endereco, setEndereco] = useState<any>(null);
  const regras = useQuery({ queryKey: ["regras-comissao"], queryFn: () => apiRequest<any[]>("/regras-comissao") });
  const gerar = useMutation({ mutationFn: () => {
    const d = new Date(); d.setMonth(d.getMonth()-1);
    const mes = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}`;
    return apiRequest(`/comissoes/gerar?unidade_id=${me?.unidade_id}&mes=${mes}`, { method: "POST" });
  }, onSuccess: () => show("Comissões geradas") });

  return <ScrollView contentContainerStyle={{ padding: 16, gap: 12 }}>
    <Card><Text style={{ fontSize: 22, fontWeight: "800" }}>Configurações</Text><Text>Regra de comissão: {regras.data?.[0] ? "ativa" : "não configurada"}</Text><Button title="Gerar comissão do mês anterior" onPress={() => gerar.mutate()} /></Card>
    <Card><Text style={{ fontWeight: "800" }}>Buscar CEP</Text><Input label="CEP" value={cep} onChangeText={setCep} keyboardType="numeric" /><Button title="Buscar" onPress={async () => setEndereco(await apiRequest(`/utils/cep/${cep}` as any, undefined, false))} variant="ghost" />{endereco ? <View><Text>{endereco.logradouro}</Text><Text>{endereco.bairro} - {endereco.localidade}/{endereco.uf}</Text></View> : null}</Card>
  </ScrollView>;
}
