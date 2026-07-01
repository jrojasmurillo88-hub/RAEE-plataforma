"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { fetchPunto, type PuntoDetalle } from "@/lib/api";
import { nivelConfianza, textoConfianza, COLOR_CONFIANZA } from "@/lib/formato";
import { agregarCheckinPendiente } from "@/lib/checkins";

export default function PuntoDetallePage() {
  const params = useParams<{ id: string }>();
  const [punto, setPunto] = useState<PuntoDetalle | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPunto(params.id)
      .then(setPunto)
      .catch(() => setError("No pudimos cargar este punto."));
  }, [params.id]);

  if (error) {
    return (
      <main className="flex flex-1 flex-col items-center justify-center gap-3 p-6">
        <p className="text-sm text-red-600">{error}</p>
        <Link href="/" className="text-sm text-emerald-700 underline">
          Volver al inicio
        </Link>
      </main>
    );
  }

  if (!punto) {
    return (
      <main className="flex flex-1 items-center justify-center p-6">
        <p className="text-sm text-gray-500">Cargando…</p>
      </main>
    );
  }

  const confianza = nivelConfianza(punto.ultima_verificacion);
  const urlComoLlegar = `https://www.google.com/maps/dir/?api=1&destination=${punto.lat},${punto.lng}`;

  return (
    <main className="flex flex-1 flex-col bg-gray-50 px-4 py-6">
      <div className="mx-auto w-full max-w-md">
        <Link href="/mapa" className="text-sm text-gray-500 hover:text-gray-800">
          ← Volver a puntos cercanos
        </Link>

        <h1 className="mt-3 text-xl font-bold text-gray-900">{punto.nombre}</h1>
        <p className="mt-1 text-sm text-gray-600">
          {punto.direccion_texto ?? "Dirección no disponible"}
          {punto.ciudad ? `, ${punto.ciudad}` : ""}
        </p>
        <p className="mt-1 text-sm text-gray-500">Sistema: {punto.sistema}</p>

        <p className="mt-3 text-sm text-gray-700">
          {punto.horario ?? "Horario no disponible — se recomienda verificar antes de ir"}
        </p>

        <p className="mt-2 text-xs text-gray-600">
          {COLOR_CONFIANZA[confianza]} {textoConfianza(punto.ultima_verificacion)}
        </p>

        <a
          href={urlComoLlegar}
          target="_blank"
          rel="noopener noreferrer"
          onClick={() =>
            agregarCheckinPendiente({
              puntoId: punto.id,
              nombrePunto: punto.nombre,
              sistema: punto.sistema,
            })
          }
          className="mt-6 block w-full rounded-xl bg-emerald-600 px-4 py-3 text-center text-base font-semibold text-white shadow hover:bg-emerald-700"
        >
          Cómo llegar
        </a>

        <Link
          href={`/reportar/${punto.id}`}
          className="mt-3 block w-full rounded-xl border-2 border-red-500 px-4 py-2.5 text-center text-sm font-semibold text-red-600 hover:bg-red-50"
        >
          ⚠️ Reportar dato incorrecto
        </Link>
      </div>
    </main>
  );
}
