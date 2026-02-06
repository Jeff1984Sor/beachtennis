import { StatusBar } from "expo-status-bar";
import { useEffect, useState } from "react";
import { StyleSheet, Text, View } from "react-native";

type Branding = {
  nome_empresa: string;
  tema?: Record<string, string> | null;
  fonte?: string | null;
  logo_url?: string | null;
};

export default function App() {
  const [branding, setBranding] = useState<Branding | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/public/branding")
      .then((res) => res.json())
      .then((data) => setBranding(data))
      .catch(() => setBranding(null));
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{branding?.nome_empresa || "Beach Tennis"}</Text>
      <Text style={styles.subtitle}>Login e operações do dia a dia</Text>
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Ficha do aluno</Text>
        <Text>Aulas · Financeiro · WhatsApp · Contrato · Anexos</Text>
      </View>
      <StatusBar style="dark" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f7f3ea",
    alignItems: "center",
    justifyContent: "center",
    padding: 24
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
    marginBottom: 8
  },
  subtitle: {
    fontSize: 16,
    marginBottom: 24
  },
  card: {
    backgroundColor: "#fff7ec",
    borderRadius: 16,
    padding: 20,
    width: "100%"
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 8
  }
});