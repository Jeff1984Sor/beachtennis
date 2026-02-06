"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "../lib/auth";
import { apiFetch } from "../lib/api";

type Branding = {
  nome_empresa: string;
  fonte?: string | null;
  tema?: Record<string, string> | null;
  logo_url?: string | null;
};

export default function BrandingPage() {
  const router = useRouter();
  const [branding, setBranding] = useState<Branding | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!getToken()) {
      router.push("/login");
      return;
    }
    apiFetch("/public/branding", { auth: false })
      .then((res) => res.json())
      .then((data) => setBranding(data))
      .catch(() => setBranding(null));
  }, [router]);

  const updateField = (key: keyof Branding, value: string) => {
    if (!branding) return;
    setBranding({ ...branding, [key]: value });
  };

  const handleSave = async () => {
    if (!branding) return;
    setSaving(true);
    const token = getToken();
    await apiFetch("/config/branding", {
      method: "PUT",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({
        nome_empresa: branding.nome_empresa,
        fonte: branding.fonte,
        tema: branding.tema
      })
    });
    setSaving(false);
  };

  return (
    <div className="grid">
      <header className="header">
        <div className="logo">Branding Editor</div>
      </header>

      <div className="grid grid-2">
        <div className="card">
          <div className="label">Configuração</div>
          <label className="label">Nome da empresa</label>
          <input
            className="input"
            value={branding?.nome_empresa || ""}
            onChange={(event) => updateField("nome_empresa", event.target.value)}
          />
          <label className="label">Fonte</label>
          <input
            className="input"
            value={branding?.fonte || ""}
            onChange={(event) => updateField("fonte", event.target.value)}
          />
          <button className="button" onClick={handleSave} disabled={saving}>
            {saving ? "Salvando..." : "Salvar"}
          </button>
        </div>

        <div className="card preview">
          <div className="label">Preview</div>
          <h2 style={{ fontFamily: branding?.fonte || "inherit" }}>
            {branding?.nome_empresa || "Sua empresa"}
          </h2>
          <p>Veja como o app fica com as novas cores.</p>
          {branding?.logo_url ? <img src={branding.logo_url} alt="Logo" /> : null}
        </div>
      </div>
    </div>
  );
}
