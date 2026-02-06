"use client";

import { useEffect, useRef, useState } from "react";
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  ScrollView,
  PanResponder,
  Animated
} from "react-native";
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

type AulaLayout = Aula & { top: number; height: number };

const diasSemana = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"];
const TOKEN_KEY = "bt_mobile_token";
const CACHE_PREFIX = "bt_agenda_week_";
const START_HOUR = 6;
const END_HOUR = 22;
const ROW_HEIGHT = 48;
const MINUTES_PER_PIXEL = 60 / ROW_HEIGHT;

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

const weekKey = (weekStart: Date) => `${CACHE_PREFIX}${weekStart.toISOString().slice(0, 10)}`;

const loadWeekCache = async (weekStart: Date) => {
  const raw = await AsyncStorage.getItem(weekKey(weekStart));
  return raw ? (JSON.parse(raw) as Aula[]) : null;
};

const saveWeekCache = async (weekStart: Date, data: Aula[]) => {
  await AsyncStorage.setItem(weekKey(weekStart), JSON.stringify(data));
};

const cleanupOldCache = async (keepWeeks = 8) => {
  const keys = await AsyncStorage.getAllKeys();
  const agendaKeys = keys.filter((key) => key.startsWith(CACHE_PREFIX));
  const now = new Date();
  for (const key of agendaKeys) {
    const dateStr = key.replace(CACHE_PREFIX, "");
    const cachedDate = new Date(dateStr);
    const diffWeeks = (now.getTime() - cachedDate.getTime()) / (7 * 24 * 60 * 60 * 1000);
    if (diffWeeks > keepWeeks) {
      await AsyncStorage.removeItem(key);
    }
  }
};

export default function App() {
  const [branding, setBranding] = useState<Branding | null>(null);
  const [email, setEmail] = useState("admin@local");
  const [password, setPassword] = useState("admin123");
  const [token, setToken] = useState<TokenPair | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [aulas, setAulas] = useState<Aula[]>([]);
  const [weekStart, setWeekStart] = useState<Date>(startOfWeek(new Date()));
  const [draggingId, setDraggingId] = useState<string | null>(null);
  const dragY = useRef(new Animated.Value(0)).current;

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
    cleanupOldCache();
  }, []);

  useEffect(() => {
    loadWeekCache(weekStart).then((cached) => {
      if (cached) setAulas(cached);
    });
  }, [weekStart]);

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
    await saveWeekCache(baseDate, data);
  };

  const changeWeek = (delta: number) => {
    const next = new Date(weekStart);
    next.setDate(next.getDate() + delta * 7);
    setWeekStart(next);
    carregarSemana(next);
  };

  const aulasPorDia = (dayIndex: number) =>
    aulas.filter((aula) => new Date(aula.inicio).getDay() === dayIndex);

  const aulasDoDia = (dayIndex: number): AulaLayout[] => {
    const dia = aulasPorDia(dayIndex);
    return dia.map((aula) => {
      const inicio = new Date(aula.inicio);
      const fim = new Date(aula.fim);
      const startMin = (inicio.getHours() - START_HOUR) * 60 + inicio.getMinutes();
      const endMin = (fim.getHours() - START_HOUR) * 60 + fim.getMinutes();
      const top = Math.max(0, (startMin / 60) * ROW_HEIGHT);
      const height = Math.max(24, ((endMin - startMin) / 60) * ROW_HEIGHT);
      return { ...aula, top, height };
    });
  };

  const updateAula = async (aula: Aula, newStart: Date) => {
    if (!token) return;
    const durationMs = new Date(aula.fim).getTime() - new Date(aula.inicio).getTime();
    const newEnd = new Date(newStart.getTime() + durationMs);

    const res = await fetch(`http://localhost:8000/agenda/aulas/${aula.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token.access_token}`
      },
      body: JSON.stringify({ inicio: newStart.toISOString(), fim: newEnd.toISOString() })
    });

    if (!res.ok) {
      setError("Erro ao reagendar aula");
      return;
    }

    const updated = (await res.json()) as Aula;
    const next = aulas.map((item) => (item.id === updated.id ? updated : item));
    setAulas(next);
    await saveWeekCache(weekStart, next);
  };

  const createPanResponder = (aula: Aula) =>
    PanResponder.create({
      onStartShouldSetPanResponder: () => true,
      onPanResponderGrant: () => {
        setDraggingId(aula.id);
        dragY.setValue(0);
      },
      onPanResponderMove: (_, gesture) => {
        dragY.setValue(gesture.dy);
      },
      onPanResponderRelease: (_, gesture) => {
        const minutesDelta = Math.round(gesture.dy * MINUTES_PER_PIXEL / 15) * 15;
        const inicioAtual = new Date(aula.inicio);
        const novoInicio = new Date(inicioAtual.getTime() + minutesDelta * 60000);
        dragY.setValue(0);
        setDraggingId(null);
        updateAula(aula, novoInicio);
      }
    });

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

        <ScrollView horizontal>
          <View>
            <View style={styles.gridHeader}>
              <View style={styles.timeCell} />
              {diasSemana.map((dia) => (
                <View key={dia} style={styles.dayHeaderCell}>
                  <Text style={styles.dayTitle}>{dia}</Text>
                </View>
              ))}
            </View>
            <View style={styles.gridBody}>
              <View style={styles.timeColumn}>
                {Array.from({ length: END_HOUR - START_HOUR }).map((_, idx) => (
                  <View key={idx} style={styles.timeRow}>
                    <Text style={styles.muted}>{`${START_HOUR + idx}:00`}</Text>
                  </View>
                ))}
              </View>
              {diasSemana.map((_, dayIdx) => (
                <View key={dayIdx} style={styles.dayColumn}>
                  {Array.from({ length: END_HOUR - START_HOUR }).map((_, idx) => (
                    <View key={`${dayIdx}-${idx}`} style={styles.gridRowLine} />
                  ))}
                  {aulasDoDia(dayIdx).map((aula) => {
                    const responder = createPanResponder(aula);
                    const isDragging = draggingId === aula.id;
                    return (
                      <Animated.View
                        key={aula.id}
                        style={[
                          styles.aulaBlock,
                          { top: aula.top, height: aula.height },
                          isDragging && { transform: [{ translateY: dragY }] }
                        ]}
                        {...responder.panHandlers}
                      >
                        <Text style={styles.aulaText}>{aula.status}</Text>
                      </Animated.View>
                    );
                  })}
                </View>
              ))}
            </View>
          </View>
        </ScrollView>
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
    paddingBottom: 6,
    borderBottomWidth: 1,
    borderColor: "#e0d4c0"
  },
  gridBody: {
    flexDirection: "row"
  },
  timeColumn: {
    width: 56
  },
  timeRow: {
    height: ROW_HEIGHT,
    justifyContent: "center",
    alignItems: "center"
  },
  timeCell: {
    width: 56
  },
  dayHeaderCell: {
    width: 120,
    alignItems: "center"
  },
  dayColumn: {
    width: 120,
    height: (END_HOUR - START_HOUR) * ROW_HEIGHT,
    position: "relative",
    borderLeftWidth: 1,
    borderColor: "#f0e5d3"
  },
  gridRowLine: {
    height: ROW_HEIGHT,
    borderBottomWidth: 1,
    borderColor: "#f0e5d3"
  },
  dayTitle: {
    fontWeight: "600"
  },
  aulaBlock: {
    position: "absolute",
    left: 6,
    right: 6,
    backgroundColor: "#ffe3c2",
    borderRadius: 8,
    padding: 4
  },
  aulaText: {
    fontSize: 12,
    fontWeight: "600"
  },
  muted: {
    color: "#6b6a65"
  }
});