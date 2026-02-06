"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "../lib/api";
import { getToken } from "../lib/auth";
import { FieldDef, RESOURCE_DEFS, ResourceDef } from "../lib/resources";

type ItemRecord = Record<string, any>;

const EMPTY_VALUE = "";

const titleize = (value: string) =>
  value
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());

const parseValue = (field: FieldDef, raw: string | boolean) => {
  if (field.type === "boolean") {
    return Boolean(raw);
  }
  if (raw === "") {
    return null;
  }
  if (field.type === "number") {
    const num = Number(raw);
    if (Number.isNaN(num)) {
      throw new Error(`Valor inválido para ${field.key}`);
    }
    return num;
  }
  if (field.type === "json") {
    if (typeof raw !== "string") return raw;
    return raw.trim() === "" ? null : JSON.parse(raw);
  }
  return raw;
};

export default function CadastrosPage() {
  const router = useRouter();
  const [resourceKey, setResourceKey] = useState(RESOURCE_DEFS[0].key);
  const [items, setItems] = useState<ItemRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<ItemRecord | null>(null);
  const [form, setForm] = useState<Record<string, any>>({});
  const [saving, setSaving] = useState(false);

  const resource = useMemo<ResourceDef>(() => {
    return RESOURCE_DEFS.find((item) => item.key === resourceKey) || RESOURCE_DEFS[0];
  }, [resourceKey]);

  useEffect(() => {
    if (!getToken()) {
      router.push("/login");
      return;
    }
    void loadItems();
  }, [resourceKey, router]);

  const loadItems = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch(`/admin/${resourceKey}?limit=50&offset=0`);
      if (res.status === 401) {
        router.push("/login");
        return;
      }
      const data = await res.json();
      setItems(Array.isArray(data) ? data : []);
    } catch (err) {
      setError("Falha ao carregar os registros.");
    } finally {
      setLoading(false);
    }
  };

  const openNew = () => {
    const initial: Record<string, any> = {};
    resource.fields.forEach((field) => {
      initial[field.key] = field.type === "boolean" ? false : EMPTY_VALUE;
    });
    setForm(initial);
    setEditing(null);
    setModalOpen(true);
  };

  const openEdit = (item: ItemRecord) => {
    const initial: Record<string, any> = {};
    resource.fields.forEach((field) => {
      if (field.type === "json") {
        initial[field.key] = item[field.key]
          ? JSON.stringify(item[field.key], null, 2)
          : "";
      } else if (field.type === "boolean") {
        initial[field.key] = Boolean(item[field.key]);
      } else {
        initial[field.key] = item[field.key] ?? "";
      }
    });
    setForm(initial);
    setEditing(item);
    setModalOpen(true);
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    try {
      const payload: Record<string, any> = {};
      resource.fields.forEach((field) => {
        payload[field.key] = parseValue(field, form[field.key]);
      });

      const res = await apiFetch(
        editing ? `/admin/${resourceKey}/${editing.id}` : `/admin/${resourceKey}`,
        {
          method: editing ? "PUT" : "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        }
      );

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data?.message || "Erro ao salvar.");
        return;
      }

      setModalOpen(false);
      await loadItems();
    } catch (err: any) {
      setError(err?.message || "Erro ao salvar.");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (item: ItemRecord) => {
    if (!confirm("Remover este item?")) return;
    setSaving(true);
    setError(null);
    try {
      const res = await apiFetch(`/admin/${resourceKey}/${item.id}`, {
        method: "DELETE"
      });
      if (!res.ok) {
        setError("Erro ao remover.");
        return;
      }
      await loadItems();
    } finally {
      setSaving(false);
    }
  };

  const listColumns = resource.listColumns || resource.fields.slice(0, 4).map((f) => f.key);

  return (
    <div className="grid">
      <section className="card">
        <div className="label">Cadastros completos</div>
        <h2>Gerencie todas as tabelas</h2>
        <p>Selecione o módulo no menu abaixo e use o botão Novo para cadastrar.</p>
      </section>

      <div className="module-tabs">
        {RESOURCE_DEFS.map((item) => (
          <button
            key={item.key}
            className={`chip ${resourceKey === item.key ? "active" : ""}`}
            onClick={() => setResourceKey(item.key)}
          >
            {item.label}
          </button>
        ))}
      </div>

      <section className="card">
        <div className="section-header">
          <div>
            <div className="label">Tabela</div>
            <h3>{resource.label}</h3>
          </div>
          <button className="button" onClick={openNew}>
            Novo
          </button>
        </div>

        {loading ? <p>Carregando...</p> : null}
        {error ? <p className="error">{error}</p> : null}

        <div className="list">
          {items.length === 0 && !loading ? (
            <p className="muted">Nenhum item cadastrado.</p>
          ) : null}
          {items.map((item) => (
            <div key={item.id} className="list-item">
              <div className="list-meta">
                <div className="list-title">{item.id}</div>
                <div className="list-fields">
                  {listColumns.map((col) => (
                    <span key={col} className="pill">
                      {titleize(col)}: {String(item[col] ?? "-")}
                    </span>
                  ))}
                </div>
              </div>
              <div className="list-actions">
                <button className="button ghost" onClick={() => openEdit(item)}>
                  Editar
                </button>
                <button className="button danger" onClick={() => handleDelete(item)}>
                  Excluir
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      {modalOpen ? (
        <div className="modal-backdrop" onClick={() => setModalOpen(false)}>
          <div className="modal-card" onClick={(event) => event.stopPropagation()}>
            <div className="section-header">
              <div>
                <div className="label">Cadastro</div>
                <h3>{editing ? "Editar item" : "Novo item"}</h3>
              </div>
              <button className="button ghost" onClick={() => setModalOpen(false)}>
                Fechar
              </button>
            </div>

            <div className="form-grid">
              {resource.fields.map((field) => {
                const value = form[field.key];
                const label = field.label || titleize(field.key);
                if (field.type === "textarea" || field.type === "json") {
                  return (
                    <label key={field.key} className="form-field">
                      <span className="label">{label}</span>
                      <textarea
                        className="input textarea"
                        value={value || ""}
                        onChange={(event) =>
                          setForm((prev) => ({ ...prev, [field.key]: event.target.value }))
                        }
                        placeholder={field.type === "json" ? "{ }" : ""}
                      />
                    </label>
                  );
                }
                if (field.type === "boolean") {
                  return (
                    <label key={field.key} className="form-field checkbox">
                      <input
                        type="checkbox"
                        checked={Boolean(value)}
                        onChange={(event) =>
                          setForm((prev) => ({ ...prev, [field.key]: event.target.checked }))
                        }
                      />
                      <span>{label}</span>
                    </label>
                  );
                }
                const inputType =
                  field.type === "number"
                    ? "number"
                    : field.type === "date"
                      ? "date"
                      : field.type === "time"
                        ? "time"
                        : field.type === "datetime"
                          ? "datetime-local"
                          : "text";
                return (
                  <label key={field.key} className="form-field">
                    <span className="label">{label}</span>
                    <input
                      className="input"
                      type={inputType}
                      value={value ?? ""}
                      onChange={(event) =>
                        setForm((prev) => ({ ...prev, [field.key]: event.target.value }))
                      }
                    />
                  </label>
                );
              })}
            </div>

            {error ? <p className="error">{error}</p> : null}
            <button className="button" onClick={handleSave} disabled={saving}>
              {saving ? "Salvando..." : "Salvar"}
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
