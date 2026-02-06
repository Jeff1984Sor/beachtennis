import { StatusBar } from "expo-status-bar";
import { useEffect, useState } from "react";
import { StyleSheet, Text, View, TextInput, TouchableOpacity } from "react-native";

type Branding = {
  nome_empresa: string;
  tema?: Record<string, string> | null;
  fonte?: string | null;
  logo_url?: string | null;
};

type TokenPair = {
  access_token: string;
  refresh_token: string;
};

export default function App() {
  const [branding, setBranding] = useState<Branding | null>(null);
  const [email, setEmail] = useState("admin@local");
  const [password, setPassword] = useState("admin123");
  const [token, setToken] = useState<TokenPair | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/public/branding")
      .then((res) => res.json())
      .then((data) => setBranding(data))
      .catch(() => setBranding(null));
  }, []);

  const handleLogin = async () => {
    setError(null);
    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      if (!res.ok) {
        setError("Credenciais inválidas");
        return;
      }
      const data = (await res.json()) as TokenPair;
      setToken(data);
    } catch (err) {
      setError("Falha ao conectar na API");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{branding?.nome_empresa || "Beach Tennis"}</Text>
      <Text style={styles.subtitle}>Login e operações do dia a dia</Text>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Entrar</Text>
        <TextInput
          style={styles.input}
          placeholder="Email"
          autoCapitalize="none"
          value={email}
          onChangeText={setEmail}
        />
        <TextInput
          style={styles.input}
          placeholder="Senha"
          secureTextEntry
          value={password}
          onChangeText={setPassword}
        />
        <TouchableOpacity style={styles.button} onPress={handleLogin}>
          <Text style={styles.buttonText}>Entrar</Text>
        </TouchableOpacity>
        {error ? <Text style={styles.error}>{error}</Text> : null}
        {token ? <Text>Token recebido ?</Text> : null}
      </View>

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
    width: "100%",
    marginBottom: 16
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 8
  },
  input: {
    backgroundColor: "#fffdf8",
    borderRadius: 10,
    padding: 10,
    marginBottom: 12
  },
  button: {
    backgroundColor: "#ff7a00",
    borderRadius: 10,
    padding: 12,
    alignItems: "center",
    marginBottom: 8
  },
  buttonText: {
    color: "white",
    fontWeight: "600"
  },
  error: {
    color: "#c44536"
  }
});