"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { OBJETOS_RAEE, OBJETO_DEFAULT_ID } from "@/lib/objetos";
import { obtenerOnboarding } from "@/lib/onboarding";
import Onboarding from "@/components/Onboarding";

export default function InicioPage() {
  const router = useRouter();
  const [onboardingListo, setOnboardingListo] = useState<boolean | null>(null);
  const [seleccionados, setSeleccionados] = useState<Set<string>>(
    new Set([OBJETO_DEFAULT_ID])
  );

  useEffect(() => {
    setOnboardingListo(obtenerOnboarding() !== null);
  }, []);

  function alternar(id: string) {
    setSeleccionados((actual) => {
      const nuevo = new Set(actual);
      if (nuevo.has(id)) nuevo.delete(id);
      else nuevo.add(id);
      return nuevo;
    });
  }

  function continuar() {
    const objetos = OBJETOS_RAEE.filter((o) => seleccionados.has(o.id));
    if (objetos.length === 0) return;
    const tipos = objetos.map((o) => o.tipoRaee).join(",");
    router.push(`/mapa?tipos=${encodeURIComponent(tipos)}`);
  }

  if (onboardingListo === null) {
    return <main className="flex-1 bg-gray-50" />;
  }

  if (!onboardingListo) {
    return <Onboarding onCompletar={() => setOnboardingListo(true)} />;
  }

  return (
    <main className="flex flex-1 flex-col items-center justify-center px-6 py-10 bg-gray-50">
      <div className="w-full max-w-md">
        <h1 className="text-2xl font-bold text-gray-900 text-center">
          ¿Qué quieres desechar?
        </h1>
        <p className="mt-2 text-sm text-gray-500 text-center">
          Elige uno o varios objetos y te mostramos los puntos de entrega más cercanos.
        </p>

        <div className="mt-8 grid grid-cols-3 gap-3">
          {OBJETOS_RAEE.map((objeto) => {
            const activo = seleccionados.has(objeto.id);
            return (
              <button
                key={objeto.id}
                onClick={() => alternar(objeto.id)}
                aria-pressed={activo}
                className={`flex flex-col items-center justify-center gap-2 rounded-xl border p-4 text-center text-sm font-medium transition hover:border-emerald-500 hover:bg-emerald-50 ${
                  activo
                    ? "border-emerald-500 bg-emerald-50 text-emerald-800"
                    : "border-gray-200 bg-white text-gray-700"
                }`}
              >
                <span className="text-3xl">{objeto.icono}</span>
                {objeto.etiqueta}
              </button>
            );
          })}
        </div>

        <button
          onClick={continuar}
          disabled={seleccionados.size === 0}
          className="mt-6 w-full rounded-xl bg-emerald-600 px-4 py-3 text-base font-semibold text-white shadow hover:bg-emerald-700 disabled:opacity-40"
        >
          {seleccionados.size > 1
            ? `Buscar puntos para ${seleccionados.size} objetos`
            : "Buscar puntos cercanos"}
        </button>
      </div>
    </main>
  );
}
