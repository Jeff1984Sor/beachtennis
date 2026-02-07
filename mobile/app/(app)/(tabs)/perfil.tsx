import { ScrollView, Text } from "react-native";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { useAuth } from "@/store/auth-store";

export default function PerfilScreen() {
  const { me, activeRole, signOut } = useAuth();
  return (
    <ScrollView contentContainerStyle={{ padding: 16, gap: 12 }}>
      <Card>
        <Text style={{ fontSize: 22, fontWeight: "800" }}>{me?.nome}</Text>
        <Text>{me?.email}</Text>
        <Text>Visão ativa: {activeRole}</Text>
        <Text>Perfis: {me?.roles?.join(", ")}</Text>
      </Card>
      <Button title="Sair" onPress={signOut} />
    </ScrollView>
  );
}
