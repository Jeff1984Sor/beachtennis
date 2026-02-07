import AsyncStorage from "@react-native-async-storage/async-storage";

const API_URL = process.env.EXPO_PUBLIC_API_URL || "http://localhost:8000";
const TOKEN_KEY = "bt.tokens";

export type TokenPair = { access_token: string; refresh_token: string; token_type?: string };

let refreshing: Promise<TokenPair | null> | null = null;

export async function loadTokens() {
  const raw = await AsyncStorage.getItem(TOKEN_KEY);
  return raw ? (JSON.parse(raw) as TokenPair) : null;
}

export async function saveTokens(tokens: TokenPair | null) {
  if (!tokens) {
    await AsyncStorage.removeItem(TOKEN_KEY);
    return;
  }
  await AsyncStorage.setItem(TOKEN_KEY, JSON.stringify(tokens));
}

async function refreshToken(refresh_token: string) {
  const res = await fetch(`${API_URL}/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token })
  });
  if (!res.ok) return null;
  return (await res.json()) as TokenPair;
}

export async function apiRequest<T>(path: string, init?: RequestInit, auth = true): Promise<T> {
  const tokens = await loadTokens();
  const headers: HeadersInit = { "Content-Type": "application/json", ...(init?.headers || {}) };
  if (auth && tokens?.access_token) {
    (headers as Record<string, string>).Authorization = `Bearer ${tokens.access_token}`;
  }

  let res = await fetch(`${API_URL}${path}`, { ...init, headers });

  if (res.status === 401 && auth && tokens?.refresh_token) {
    refreshing = refreshing || refreshToken(tokens.refresh_token);
    const next = await refreshing;
    refreshing = null;
    await saveTokens(next);
    if (next?.access_token) {
      (headers as Record<string, string>).Authorization = `Bearer ${next.access_token}`;
      res = await fetch(`${API_URL}${path}`, { ...init, headers });
    }
  }

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Erro ${res.status}`);
  }

  return (await res.json()) as T;
}

export async function uploadFile<T>(path: string, file: { uri: string; name: string; type: string }) {
  const tokens = await loadTokens();
  const form = new FormData();
  form.append("file", file as any);
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${tokens?.access_token}` },
    body: form
  });
  if (!res.ok) throw new Error("Falha no upload");
  return (await res.json()) as T;
}

export { API_URL };
