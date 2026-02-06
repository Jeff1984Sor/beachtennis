"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "../lib/auth";

export default function ComissoesPage() {
  const router = useRouter();

  useEffect(() => {
    if (!getToken()) {
      router.push("/login");
    }
  }, [router]);

  return (
    <div className="card">
      <div className="label">Comissões</div>
      <h2>Configurar regras e gerar comissões</h2>
      <p>Conecte com a API para editar regras e disparar a geração mensal.</p>
    </div>
  );
}