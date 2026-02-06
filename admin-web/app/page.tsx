"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { clearToken, getToken } from "./lib/auth";
import { useEffect } from "react";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    if (!getToken()) {
      router.push("/login");
    }
  }, [router]);

  const logout = () => {
    clearToken();
    router.push("/login");
  };

  return (
    <div className="grid">
      <header className="header">
        <div className="logo">Beach Tennis Admin</div>
        <nav className="nav">
          <Link href="/branding">Branding</Link>
          <Link href="/comissoes">Comissões</Link>
          <Link href="/contratos">Contratos</Link>
          <button className="button" onClick={logout}>
            Sair
          </button>
        </nav>
      </header>

      <section className="grid grid-2">
        <div className="card">
          <div className="label">Branding</div>
          <h2>Identidade visual centralizada</h2>
          <p>
            Atualize nome da empresa, paleta de cores, fonte e logotipo com
            preview imediato.
          </p>
          <Link href="/branding">Abrir editor</Link>
        </div>
        <div className="card">
          <div className="label">Comissões</div>
          <h2>Regras inteligentes por unidade</h2>
          <p>
            Configure o dia de pagamento e gere comissões do mês anterior com
            um clique.
          </p>
          <Link href="/comissoes">Configurar</Link>
        </div>
      </section>
    </div>
  );
}