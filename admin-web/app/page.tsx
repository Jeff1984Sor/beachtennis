"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { getToken } from "./lib/auth";
import { useEffect } from "react";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    if (!getToken()) {
      router.push("/login");
    }
  }, [router]);

  return (
    <div className="grid">
      <section className="grid grid-2">
        <div className="card">
          <div className="label">Cadastros</div>
          <h2>Todas as tabelas</h2>
          <p>
            Crie, edite e organize todos os registros com formulário em modal.
          </p>
          <Link href="/cadastros">Abrir cadastros</Link>
        </div>
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
        <div className="card">
          <div className="label">Contratos</div>
          <h2>Templates com variáveis</h2>
          <p>Edite, teste e pré-visualize contratos reais.</p>
          <Link href="/contratos">Abrir contratos</Link>
        </div>
      </section>
    </div>
  );
}
