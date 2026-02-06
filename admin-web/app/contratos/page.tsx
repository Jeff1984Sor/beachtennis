"use client";

import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "../lib/auth";

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

export default function ContratosPage() {
  const router = useRouter();
  const editor = useEditor({
    extensions: [StarterKit],
    content: "<h2>Modelo de Contrato</h2><p>Edite o texto e use as variáveis.</p>"
  });
  const [previewHtml, setPreviewHtml] = useState<string>("");
  const [contratoId, setContratoId] = useState("");
  const [alunoId, setAlunoId] = useState("");
  const [unidadeId, setUnidadeId] = useState("");
  const [planoId, setPlanoId] = useState("");

  useEffect(() => {
    if (!getToken()) {
      router.push("/login");
    }
  }, [router]);

  const insertVar = (value: string) => {
    editor?.chain().focus().insertContent(`{{ ${value} }}`).run();
  };

  const renderPreview = async () => {
    const html = editor?.getHTML() || "";
    const token = getToken();
    const res = await fetch("http://localhost:8000/contratos/preview", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({
        content_html: html,
        contrato_id: contratoId || null,
        aluno_id: alunoId || null,
        unidade_id: unidadeId || null,
        plano_id: planoId || null
      })
    });
    const data = await res.json();
    setPreviewHtml(data.rendered_html || "");
  };

  return (
    <div className="grid grid-2">
      <div className="card">
        <div className="label">Editor</div>
        <EditorContent editor={editor} />
        <label className="label">Contrato ID</label>
        <input className="input" value={contratoId} onChange={(e) => setContratoId(e.target.value)} />
        <label className="label">Aluno ID</label>
        <input className="input" value={alunoId} onChange={(e) => setAlunoId(e.target.value)} />
        <label className="label">Unidade ID</label>
        <input className="input" value={unidadeId} onChange={(e) => setUnidadeId(e.target.value)} />
        <label className="label">Plano ID</label>
        <input className="input" value={planoId} onChange={(e) => setPlanoId(e.target.value)} />
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