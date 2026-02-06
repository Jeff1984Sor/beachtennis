import Link from "next/link";

export default function HomePage() {
  return (
    <div className="grid">
      <header className="header">
        <div className="logo">Beach Tennis Admin</div>
        <nav className="nav">
          <Link href="/branding">Branding</Link>
          <Link href="/comissoes">Comissões</Link>
          <Link href="/contratos">Contratos</Link>
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