"use client";

import { useState } from "react";
import { OBJETOS_COMUNES } from "@/lib/objetosComunes";
import { buscarObjetoPorId } from "@/lib/objetos";

// Normaliza texto eliminando tildes y pasando a minúsculas para comparar
function normalizar(s: string): string {
  return s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "");
}

// Distancia de Levenshtein (tolerancia a errores de tipeo como "lucuadora" → "licuadora")
function levenshtein(a: string, b: string): number {
  const m = a.length, n = b.length;
  const dp: number[][] = Array.from({ length: m + 1 }, (_, i) =>
    Array.from({ length: n + 1 }, (_, j) => (i === 0 ? j : j === 0 ? i : 0))
  );
  for (let i = 1; i <= m; i++)
    for (let j = 1; j <= n; j++)
      dp[i][j] = a[i - 1] === b[j - 1]
        ? dp[i - 1][j - 1]
        : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
  return dp[m][n];
}

function coincide(nombre: string, query: string): boolean {
  const n = normalizar(nombre);
  const q = normalizar(query);
  if (n.includes(q)) return true;
  // Fuzzy: verificar si alguna palabra del nombre tiene distancia corta al query
  const umbral = q.length <= 4 ? 1 : q.length <= 7 ? 2 : 3;
  return nombre.split(/[\s/]+/).some((palabra) => {
    const p = normalizar(palabra);
    return p.length >= q.length - 1 && levenshtein(p.slice(0, q.length + 2), q) <= umbral;
  });
}

export default function BuscadorObjeto({
  onEncontrado,
}: {
  onEncontrado: (objetoId: string) => void;
}) {
  const [abierto, setAbierto] = useState(false);
  const [texto, setTexto] = useState("");
  const [encontrado, setEncontrado] = useState<string | null>(null);

  const query = texto.trim();
  const resultados = query.length >= 2
    ? OBJETOS_COMUNES.filter((o) => coincide(o.nombre, query)).slice(0, 6)
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

      {query.length >= 2 && resultados.length === 0 && (
        <p className="mt-2 text-sm text-gray-500">
          No lo encontramos. Si es un aparato eléctrico o electrónico, probablemente
          entra en &quot;Equipos electrónicos&quot;.
        </p>
      )}
    </div>
  );
}
