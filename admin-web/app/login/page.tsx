"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { setToken } from "../lib/auth";
import { API_BASE } from "../lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("admin@local");
  const [password, setPassword] = useState("admin123");
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async () => {
    setError(null);
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    if (!res.ok) {
      setError("Credenciais inválidas");
      return;
    }
    const data = await res.json();
    setToken(data.access_token);
    router.push("/");
  };

  return (
    <div className="card" style={{ maxWidth: 420, margin: "0 auto" }}>
      <div className="label">Admin Login</div>
      <h2>Entrar</h2>
      <input
        className="input"
        placeholder="Email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
      />
      <input
        className="input"
        type="password"
        placeholder="Senha"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
      />
      <button className="button" onClick={handleLogin}>
        Entrar
      </button>
      {error ? <p>{error}</p> : null}
    </div>
  );
}
