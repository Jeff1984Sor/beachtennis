"use client";

import { useEffect, useState } from "react";
import { StyleSheet, Text, View, TextInput, TouchableOpacity, ScrollView } from "react-native";
import { StatusBar } from "expo-status-bar";
import AsyncStorage from "@react-native-async-storage/async-storage";

type Branding = {
  nome_empresa: string;
};

type TokenPair = {
  access_token: string;
  refresh_token: string;
};

type Aula = {
  id: string;
  inicio: string;
  fim: string;
  status: string;
};

const diasSemana = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"];
const horas = Array.from({ length: 16 }, (_, i) => 6 + i);
const TOKEN_KEY = "bt_mobile_token";

const startOfWeek = (date: Date) => {
  const d = new Date(date);
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1);
  return new Date(d.setDate(diff));
};

const formatDate = (date: Date) =>
  `${date.getDate().toString().padStart(2, "0")}/${(date.getMonth() + 1)
    .toString()
    .padStart(2, "0")}`;

const loadToken = async () => {
  const raw = await AsyncStorage.getItem(TOKEN_KEY);
  return raw ? (JSON.parse(raw) as TokenPair) : null;
};

const saveToken = async (token: TokenPair) => {
  await AsyncStorage.setItem(TOKEN_KEY, JSON.stringify(token));
};

const clearToken = async () => {
  await AsyncStorage.removeItem(TOKEN_KEY);
};

export default function App() {
  const [branding, setBranding] = useState<Branding | null>(null);
  const [email, setEmail] = useState("admin@local");
  const [password, setPassword] = useState("admin123");
  const [token, setToken] = useState<TokenPair | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [aulas, setAulas] = useState<Aula[]>([]);
  const [weekStart, setWeekStart] = useState<Date>(startOfWeek(new Date()));

  useEffect(() => {
    fetch("http://localhost:8000/public/branding")
      .then((res) => res.json())
      .then((data) => setBranding(data))
      .catch(() => setBranding(null));
  }, []);

  useEffect(() => {
    loadToken().then((stored) => {
      if (stored) setToken(stored);
    });
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
      await saveToken(data);
    } catch (err) {
      setError("Falha ao conectar na API");
    }
  };

  const refreshToken = async (): Promise<TokenPair | null> => {
    if (!token) return null;
    const res = await fetch("http://localhost:8000/auth/refresh", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: token.refresh_token })
    });
    if (!res.ok) {
      return null;
    }
    const data = (await res.json()) as TokenPair;
    setToken(data);
    await saveToken(data);
    return data;
  };

  const carregarSemana = async (baseDate: Date) => {
    if (!token) return;
    const inicio = new Date(baseDate);
    const fim = new Date(baseDate);
    fim.setDate(fim.getDate() + 6);
    fim.setHours(23, 59, 59, 999);

    const callApi = async (accessToken: string) =>
      fetch(
        `http://localhost:8000/agenda/aulas?inicio=${inicio.toISOString()}&fim=${fim.toISOString()}`,
        {
          headers: { Authorization: `Bearer ${accessToken}` }
        }
      );

    let res = await callApi(token.access_token);
    if (res.status === 401) {
      const refreshed = await refreshToken();
      if (refreshed) {
        res = await callApi(refreshed.access_token);
      }
    }

    if (!res.ok) {
      setError("Erro ao carregar agenda");
      return;
    }
    const data = (await res.json()) as Aula[];
    setAulas(data);
  };

  const changeWeek = (delta: number) => {
    const next = new Date(weekStart);
    next.setDate(next.getDate() + delta * 7);
    setWeekStart(next);
    carregarSemana(next);
  };

  const aulasPorDia = (dayIndex: number) =>
    aulas.filter((aula) => new Date(aula.inicio).getDay() === dayIndex);

  const aulasPorDiaHora = (dayIndex: number, hour: number) =>
    aulasPorDia(dayIndex).filter((aula) => new Date(aula.inicio).getHours() === hour);

  const logout = async () => {
    setToken(null);
    await clearToken();
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
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
        {token ? (
          <TouchableOpacity style={styles.buttonSecondary} onPress={logout}>
            <Text style={styles.buttonText}>Sair</Text>
          </TouchableOpacity>
        ) : null}
        {error ? <Text style={styles.error}>{error}</Text> : null}
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Agenda semanal</Text>
        <View style={styles.weekHeader}>
          <TouchableOpacity style={styles.buttonSmall} onPress={() => changeWeek(-1)}>
            <Text style={styles.buttonText}>?</Text>
          </TouchableOpacity>
          <Text>
            {formatDate(weekStart)} - {formatDate(new Date(weekStart.getTime() + 6 * 86400000))}
          </Text>
          <TouchableOpacity style={styles.buttonSmall} onPress={() => changeWeek(1)}>
            <Text style={styles.buttonText}>?</Text>
          </TouchableOpacity>
        </View>
        <TouchableOpacity style={styles.button} onPress={() => carregarSemana(weekStart)}>
          <Text style={styles.buttonText}>Atualizar</Text>
        </TouchableOpacity>

        <View style={styles.gridHeader}>
          <View style={styles.timeCell} />
          {diasSemana.map((dia) => (
            <View key={dia} style={styles.dayHeaderCell}>
              <Text style={styles.dayTitle}>{dia}</Text>
            </View>
          ))}
        </View>
        {horas.map((hour) => (
          <View key={hour} style={styles.gridRow}>
            <View style={styles.timeCell}>
              <Text style={styles.muted}>{`${hour}:00`}</Text>
            </View>
            {diasSemana.map((_, dayIdx) => {
              const itens = aulasPorDiaHora(dayIdx, hour);
              return (
                <View key={`${dayIdx}-${hour}`} style={styles.gridCell}>
                  {itens.length === 0 ? (
                    <Text style={styles.muted}>-</Text>
                  ) : (
                    itens.map((aula) => (
                      <Text key={aula.id} style={styles.gridItem}>
                        {aula.status}
                      </Text>
                    ))
                  )}
                </View>
              );
            })}
          </View>
        ))}
      </View>

      <StatusBar style="dark" />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: "#f7f3ea",
    alignItems: "center",
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
  buttonSecondary: {
    backgroundColor: "#0b5563",
    borderRadius: 10,
    padding: 12,
    alignItems: "center",
    marginBottom: 8
  },
  buttonSmall: {
    backgroundColor: "#ff7a00",
    borderRadius: 8,
    padding: 6,
    alignItems: "center"
  },
  buttonText: {
    color: "white",
    fontWeight: "600"
  },
  error: {
    color: "#c44536"
  },
  weekHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8
  },
  gridHeader: {
    flexDirection: "row",
    borderBottomWidth: 1,
    borderColor: "#e0d4c0",
    paddingBottom: 4
  },
  gridRow: {
    flexDirection: "row",
    borderBottomWidth: 1,
    borderColor: "#f0e5d3",
    paddingVertical: 2
  },
  timeCell: {
    width: 54,
    alignItems: "center",
    justifyContent: "center"
  },
  dayHeaderCell: {
    flex: 1,
    alignItems: "center"
  },
  gridCell: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 6
  },
  dayTitle: {
    fontWeight: "600",
    marginBottom: 4
  },
  gridItem: {
    fontSize: 12,
    backgroundColor: "#ffe3c2",
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 6
  },
  muted: {
    color: "#6b6a65"
  }
});