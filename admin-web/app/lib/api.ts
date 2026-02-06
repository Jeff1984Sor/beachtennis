import { getToken } from "./auth";

export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

type FetchOptions = RequestInit & { auth?: boolean };

export const apiFetch = async (path: string, options: FetchOptions = {}) => {
  const headers = new Headers(options.headers || {});
  if (options.auth !== false) {
    const token = getToken();
    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    }
  }
  return fetch(`${API_BASE}${path}`, { ...options, headers });
};
