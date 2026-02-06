"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { clearToken, getToken } from "../lib/auth";

const NAV_ITEMS = [
  { href: "/", label: "Início" },
  { href: "/cadastros", label: "Cadastros" },
  { href: "/branding", label: "Branding" },
  { href: "/comissoes", label: "Comissões" },
  { href: "/contratos", label: "Contratos" }
];

export default function TopNav() {
  const pathname = usePathname();
  const router = useRouter();

  if (pathname === "/login") {
    return null;
  }

  const logout = () => {
    clearToken();
    router.push("/login");
  };

  const isAuthed = !!getToken();

  return (
    <header className="topbar">
      <div className="topbar-title">Beach Tennis Admin</div>
      <nav className="topbar-nav">
        {NAV_ITEMS.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={pathname === item.href ? "active" : ""}
          >
            {item.label}
          </Link>
        ))}
      </nav>
      {isAuthed ? (
        <button className="button ghost" onClick={logout}>
          Sair
        </button>
      ) : null}
    </header>
  );
}
