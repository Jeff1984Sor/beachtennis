"use client";

import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";

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
  const editor = useEditor({
    extensions: [StarterKit],
    content: "<h2>Modelo de Contrato</h2><p>Edite o texto e use as variáveis.</p>"
  });

  const insertVar = (value: string) => {
    editor?.chain().focus().insertContent(`{{ ${value} }}`).run();
  };

  return (
    <div className="grid grid-2">
      <div className="card">
        <div className="label">Editor</div>
        <EditorContent editor={editor} />
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
        <div className="preview">{editor?.getHTML() || ""}</div>
      </div>
    </div>
  );
}