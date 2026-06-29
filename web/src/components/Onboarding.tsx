"use client";

import { useEffect, useState } from "react";
import { CIUDADES_COLOMBIA } from "@/lib/ciudades";
import { guardarOnboarding, type IntencionDescarte } from "@/lib/onboarding";

const OPCIONES_INTENCION: { value: IntencionDescarte; label: string }[] = [
  { value: "pronto", label: "Sí, en los próximos días" },
  { value: "mes", label: "Sí, en el próximo mes" },
  { value: "explorando", label: "Solo estoy explorando" },
];

export default function Onboarding({ onCompletar }: { onCompletar: () => void }) {
  const [paso, setPaso] = useState<1 | 2>(1);
  const [mostrarPasoCiudad, setMostrarPasoCiudad] = useState(true);
  const [ciudad, setCiudad] = useState<string>("");
  const [intencion, setIntencion] = useState<IntencionDescarte | null>(null);

  useEffect(() => {
    if (!("permissions" in navigator)) return;
    navigator.permissions
      .query({ name: "geolocation" as PermissionName })
      .then((estado) => {
        if (estado.state === "granted") {
          setMostrarPasoCiudad(false);
          setPaso(2);
        }
      })
      .catch(() => {
        // navegador no soporta consulta de permisos; mostramos el selector de ciudad
      });
  }, []);

  function confirmarCiudad() {
    setPaso(2);
  }

  function elegirIntencion(valor: IntencionDescarte) {
    setIntencion(valor);
    guardarOnboarding({ ciudad: ciudad || null, intencion: valor });
  }

  if (paso === 1 && mostrarPasoCiudad) {
    return (
      <main className="flex flex-1 flex-col items-center justify-center bg-gray-50 px-6 py-10">
        <div className="w-full max-w-sm text-center">
          <h1 className="text-xl font-bold text-gray-900">¿En qué ciudad estás?</h1>
          <p className="mt-2 text-sm text-gray-500">
            Nos ayuda a mostrarte puntos relevantes para tu zona.
          </p>

          <select
            value={ciudad}
            onChange={(e) => setCiudad(e.target.value)}
            className="mt-6 w-full rounded-lg border border-gray-300 bg-white p-3 text-sm text-gray-700"
          >
            <option value="">Selecciona tu ciudad</option>
            {CIUDADES_COLOMBIA.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>

          <button
            onClick={confirmarCiudad}
            disabled={!ciudad}
            className="mt-4 w-full rounded-xl bg-emerald-600 px-4 py-3 text-base font-semibold text-white shadow hover:bg-emerald-700 disabled:opacity-40"
          >
            Continuar
          </button>

          <button
            onClick={() => setPaso(2)}
            className="mt-3 text-sm text-gray-400 underline hover:text-gray-600"
          >
            Omitir, ya tengo el GPS activo
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="flex flex-1 flex-col items-center justify-center bg-gray-50 px-6 py-10">
      <div className="w-full max-w-sm text-center">
        <h1 className="text-xl font-bold text-gray-900">
          ¿Tienes un dispositivo que entregar próximamente?
        </h1>
        <p className="mt-2 text-sm text-gray-500">
          Te enviamos un recordatorio en la fecha que pongas.
        </p>

        <div className="mt-6 flex flex-col gap-2">
          {OPCIONES_INTENCION.map((opcion) => (
            <button
              key={opcion.value}
              onClick={() => elegirIntencion(opcion.value)}
              className={`rounded-lg border p-3 text-sm font-medium transition ${
                intencion === opcion.value
                  ? "border-emerald-500 bg-emerald-50 text-emerald-800"
                  : "border-gray-200 bg-white text-gray-700 hover:border-gray-300"
              }`}
            >
              {opcion.label}
            </button>
          ))}
        </div>

        {intencion && (
          <div className="mt-6">
            {intencion !== "explorando" && (
              <p className="text-xs text-gray-500">
                Guardado. Pronto vamos a poder recordártelo automáticamente.
              </p>
            )}
            <button
              onClick={onCompletar}
              className="mt-3 w-full rounded-xl bg-emerald-600 px-4 py-3 text-base font-semibold text-white shadow hover:bg-emerald-700"
            >
              Continuar
            </button>
          </div>
        )}
      </div>
    </main>
  );
}
