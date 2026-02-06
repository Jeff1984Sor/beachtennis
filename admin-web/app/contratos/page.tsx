"use client";

import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "../lib/auth";

type Contrato = {
  id: string;
  aluno_id: string;
  unidade_id: string;
  plano_id: string;
  aluno_nome?: string | null;
};

const variaveis = [
  "aluno.nome",
  "aluno.endereco.cidade",
  "unidade.nome",
  "plano.preco",
  "contrato.data_inicio",
  "financeiro.total_em_aberto",
  "sistema.data_hoje",
  "profissional.nome",
  "empresa.nome_empresa"
];

const highlight = (text: string, term: string) => {
  if (!term) return text;
  const regex = new RegExp(`(${term})`, "gi");
  return text.replace(regex, "<mark>$1</mark>");
};

export default function ContratosPage() {
  const router = useRouter();
  const editor = useEditor({
    extensions: [StarterKit],
    content: "<h2>Modelo de Contrato</h2><p>Edite o texto e use as variáveis.</p>"
  });
  const [previewHtml, setPreviewHtml] = useState<string>("");
  const [contratos, setContratos] = useState<Contrato[]>([]);
  const [selectedContrato, setSelectedContrato] = useState<Contrato | null>(null);
  const [search, setSearch] = useState("");
  const [debounced, setDebounced] = useState("");
  const [activeIndex, setActiveIndex] = useState(0);

  const fetchContratos = async (value: string) => {
    const token = getToken();
    if (!token) return;
    const url = value
      ? `http://localhost:8000/contratos?search=${encodeURIComponent(value)}`
      : "http://localhost:8000/contratos";
    const res = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) return;
    const data = (await res.json()) as Contrato[];
    setContratos(data);
    setActiveIndex(0);
  };

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }
    fetchContratos("");
  }, [router]);

  useEffect(() => {
    const handle = setTimeout(() => {
      setDebounced(search);
    }, 350);
    return () => clearTimeout(handle);
  }, [search]);

  useEffect(() => {
    fetchContratos(debounced);
  }, [debounced]);

  const insertVar = (value: string) => {
    editor?.chain().focus().insertContent(`{{ ${value} }}`).run();
  };

  const selectContrato = async (id: string) => {
    const token = getToken();
    if (!token) return;
    const res = await fetch(`http://localhost:8000/contratos/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) return;
    const data = (await res.json()) as Contrato;
    const match = contratos.find((item) => item.id === id);
    setSelectedContrato({ ...data, aluno_nome: match?.aluno_nome });
  };

  const renderPreview = async () => {
    const html = editor?.getHTML() || "";
    const token = getToken();
    const res = await fetch("http://localhost:8000/contratos/preview", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({
        content_html: html,
        contrato_id: selectedContrato?.id || null,
        aluno_id: selectedContrato?.aluno_id || null,
        unidade_id: selectedContrato?.unidade_id || null,
        plano_id: selectedContrato?.plano_id || null
      })
    });
    const data = await res.json();
    setPreviewHtml(data.rendered_html || "");
  };

  const results = useMemo(() => contratos.slice(0, 10), [contratos]);

  const onKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (!results.length) return;
    if (event.key === "ArrowDown") {
      event.preventDefault();
      setActiveIndex((prev) => Math.min(prev + 1, results.length - 1));
    }
    if (event.key === "ArrowUp") {
      event.preventDefault();
      setActiveIndex((prev) => Math.max(prev - 1, 0));
    }
    if (event.key === "Enter") {
      event.preventDefault();
      const target = results[activeIndex];
      if (target) selectContrato(target.id);
    }
  };

  return (
    <div className="grid grid-2">
      <div className="card">
        <div className="label">Editor</div>
        <EditorContent editor={editor} />
        <label className="label">Buscar contrato/aluno</label>
        <input
          className="input"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Nome do aluno ou ID"
        />
        {search && (
          <div className="card" style={{ marginTop: 12 }}>
            {results.length === 0 ? (
              <p>Nenhum resultado.</p>
            ) : (
              results.map((contrato, idx) => (
                <button
                  key={contrato.id}
                  className="button"
                  style={{
                    outline: idx === activeIndex ? "2px solid #0b5563" : "none"
                  }}
                  onClick={() => selectContrato(contrato.id)}
                  dangerouslySetInnerHTML={{
                    __html: highlight(
                      contrato.aluno_nome
                        ? `${contrato.aluno_nome} - ${contrato.id}`
                        : contrato.id,
                      debounced
                    )
                  }}
                />
              ))
            )}
          </div>
        )}
        <label className="label">Selecionar contrato</label>
        <select
          className="input"
          value={selectedContrato?.id || ""}
          onChange={(event) => selectContrato(event.target.value)}
        >
          <option value="">Selecione...</option>
          {contratos.map((contrato) => (
            <option key={contrato.id} value={contrato.id}>
              {contrato.aluno_nome ? `${contrato.aluno_nome} - ${contrato.id}` : contrato.id}
            </option>
          ))}
        </select>
        {selectedContrato?.aluno_nome ? <p>Aluno: {selectedContrato.aluno_nome}</p> : null}
        <button className="button" onClick={renderPreview} style={{ marginTop: 12 }}>
          Atualizar preview
        </button>
      </div>
      <div className="card">
        <div className="label">Variáveis</div>
        <p>Clique para inserir no template:</p>
        <div className="grid">
          {variaveis.map((item) => (
            <button key={item} className="button" onClick={() => insertVar(item)}>
              {item}
            </button>
          ))}
        </div>
        <div className="label" style={{ marginTop: 16 }}>
          Preview
        </div>
        <div className="preview" dangerouslySetInnerHTML={{ __html: previewHtml }} />
      </div>
    </div>
  );
}