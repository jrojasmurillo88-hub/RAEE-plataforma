"use client";

import { useState } from "react";
import { OBJETOS_COMUNES } from "@/lib/objetosComunes";
import { buscarObjetoPorId } from "@/lib/objetos";

export default function BuscadorObjeto({
  onEncontrado,
}: {
  onEncontrado: (objetoId: string) => void;
}) {
  const [abierto, setAbierto] = useState(false);
  const [texto, setTexto] = useState("");
  const [encontrado, setEncontrado] = useState<string | null>(null);

  const resultados = texto.trim()
    ? OBJETOS_COMUNES.filter((o) =>
        o.nombre.toLowerCase().includes(texto.trim().toLowerCase())
      ).slice(0, 6)
    : [];

  function elegir(objetoId: string) {
    onEncontrado(objetoId);
    setEncontrado(objetoId);
  }

  if (!abierto) {
    return (
      <button
        onClick={() => setAbierto(true)}
        className="mt-4 text-sm text-emerald-700 underline"
      >
        ¿No sabes en qué categoría está tu objeto?
      </button>
    );
  }

  return (
    <div className="mt-4 w-full rounded-lg border border-gray-200 bg-white p-3 text-left">
      <p className="text-sm font-medium text-gray-700">
        Escribe qué tienes y te decimos la categoría:
      </p>
      <input
        type="text"
        value={texto}
        onChange={(e) => {
          setTexto(e.target.value);
          setEncontrado(null);
        }}
        placeholder="Ej: licuadora, pila, bombillo…"
        className="mt-2 w-full rounded-lg border border-gray-300 p-2 text-sm"
        autoFocus
      />

      {resultados.length > 0 && (
        <ul className="mt-2 flex flex-col gap-1">
          {resultados.map((r) => (
            <li key={r.nombre}>
              <button
                onClick={() => elegir(r.objetoId)}
                className="w-full rounded-md px-2 py-1.5 text-left text-sm text-gray-700 hover:bg-emerald-50"
              >
                {r.nombre}
              </button>
            </li>
          ))}
        </ul>
      )}

      {encontrado && (
        <p className="mt-2 text-sm text-emerald-700">
          Tu objeto entra en la categoría:{" "}
          <strong>{buscarObjetoPorId(encontrado)?.etiqueta}</strong> — ya la
          seleccionamos arriba.
        </p>
      )}

      {texto.trim() && resultados.length === 0 && (
        <p className="mt-2 text-sm text-gray-500">
          No lo encontramos. Si es un aparato eléctrico o electrónico, probablemente
          entra en &quot;Equipos electrónicos&quot;.
        </p>
      )}
    </div>
  );
}
