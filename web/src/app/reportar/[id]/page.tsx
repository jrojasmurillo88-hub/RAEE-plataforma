"use client";

import { useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { postReporte, type TipoReporte } from "@/lib/api";

const OPCIONES_TIPO: { value: TipoReporte; label: string }[] = [
  { value: "cerrado", label: "El punto está cerrado" },
  { value: "horario_incorrecto", label: "El horario es incorrecto" },
  { value: "direccion_incorrecta", label: "La dirección es incorrecta" },
  { value: "otro", label: "Otro" },
];

export default function ReportarPage() {
  const params = useParams<{ id: string }>();
  const [tipo, setTipo] = useState<TipoReporte>("cerrado");
  const [detalle, setDetalle] = useState("");
  const [enviado, setEnviado] = useState(false);
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function enviar(e: React.FormEvent) {
    e.preventDefault();
    setEnviando(true);
    setError(null);
    try {
      await postReporte({
        punto_id: Number(params.id),
        tipo,
        detalle: detalle.trim() || undefined,
      });
      setEnviado(true);
    } catch {
      setError("No pudimos enviar el reporte. Intenta de nuevo.");
    } finally {
      setEnviando(false);
    }
  }

  if (enviado) {
    return (
      <main className="flex flex-1 flex-col items-center justify-center gap-4 p-6 text-center">
        <p className="text-base font-medium text-gray-900">
          Gracias por avisarnos. Vamos a verificar la información de ese punto.
        </p>
        <Link
          href="/mapa"
          className="text-sm text-emerald-700 underline"
        >
          ¿Quieres buscar otro punto cercano?
        </Link>
      </main>
    );
  }

  return (
    <main className="flex flex-1 flex-col bg-gray-50 px-4 py-6">
      <form onSubmit={enviar} className="mx-auto w-full max-w-md">
        <Link
          href={`/punto/${params.id}`}
          className="text-sm text-gray-500 hover:text-gray-800"
        >
          ← Volver al punto
        </Link>

        <h1 className="mt-3 text-lg font-bold text-gray-900">
          Reportar un problema
        </h1>

        <div className="mt-4 flex flex-col gap-2">
          {OPCIONES_TIPO.map((opcion) => (
            <label
              key={opcion.value}
              className={`flex items-center gap-2 rounded-lg border p-3 text-sm ${
                tipo === opcion.value
                  ? "border-emerald-500 bg-emerald-50"
                  : "border-gray-200 bg-white"
              }`}
            >
              <input
                type="radio"
                name="tipo"
                value={opcion.value}
                checked={tipo === opcion.value}
                onChange={() => setTipo(opcion.value)}
              />
              {opcion.label}
            </label>
          ))}
        </div>

        <textarea
          value={detalle}
          onChange={(e) => setDetalle(e.target.value)}
          placeholder="Detalle adicional (opcional)"
          className="mt-4 w-full rounded-lg border border-gray-200 p-3 text-sm"
          rows={3}
        />

        {error && <p className="mt-2 text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={enviando}
          className="mt-4 w-full rounded-xl bg-emerald-600 px-4 py-3 text-center text-base font-semibold text-white shadow hover:bg-emerald-700 disabled:opacity-60"
        >
          {enviando ? "Enviando…" : "Enviar reporte"}
        </button>
      </form>
    </main>
  );
}
