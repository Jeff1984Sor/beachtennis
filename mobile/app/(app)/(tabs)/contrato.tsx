import { ScrollView, Text } from "react-native";
import { Card } from "@/components/Card";
import { useAuth } from "@/store/auth-store";

export default function ContratoScreen() {
  const { me } = useAuth();
  return <ScrollView contentContainerStyle={{ padding: 16, gap: 12 }}><Card><Text style={{ fontSize: 22, fontWeight: "800" }}>Contrato</Text><Text>Visualização de contrato para aluno logado.</Text><Text>ID aluno: {me?.aluno_id || "-"}</Text></Card></ScrollView>;
}
