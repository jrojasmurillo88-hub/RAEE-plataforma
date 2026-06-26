"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  obtenerProximoCheckinListo,
  marcarResuelto,
  type CheckinPendiente,
} from "@/lib/checkins";
import { postEntrega, postReporte } from "@/lib/api";
import { pesoEstimadoGramos } from "@/lib/pesos";

const UMBRAL_NORMA_SOCIAL = 5;

type Paso = "pregunta" | "impacto" | "cerrado" | "enviando";

export default function CheckinPrompt() {
  const [checkin, setCheckin] = useState<CheckinPendiente | null>(null);
  const [paso, setPaso] = useState<Paso>("pregunta");
  const [conteoZona, setConteoZona] = useState(0);

  useEffect(() => {
    setCheckin(obtenerProximoCheckinListo());
  }, []);

  function siguienteCheckin() {
    setPaso("pregunta");
    setCheckin(obtenerProximoCheckinListo());
  }

  if (!checkin) return null;

  async function responderEntregado() {
    setPaso("enviando");
    try {
      const resp = await postEntrega({ punto_id: checkin!.puntoId });
      setConteoZona(resp.conteo_zona);
    } catch {
      setConteoZona(0);
    }
    marcarResuelto(checkin!.puntoId);
    setPaso("impacto");
  }

  function responderNoPude() {
    marcarResuelto(checkin!.puntoId);
    siguienteCheckin();
  }

  async function responderCerrado() {
    setPaso("enviando");
    try {
      await postReporte({ punto_id: checkin!.puntoId, tipo: "cerrado" });
    } catch {
      // si falla el reporte no bloqueamos el cierre del check-in
    }
    marcarResuelto(checkin!.puntoId);
    setPaso("cerrado");
  }

  const peso = pesoEstimadoGramos(checkin.sistema);

  return (
    <div className="fixed inset-0 z-[2000] flex items-center justify-center bg-black/40 px-4">
      <div className="w-full max-w-sm rounded-xl bg-white p-5 shadow-xl">
        {paso === "pregunta" && (
          <>
            <p className="text-base font-semibold text-gray-900">
              ¿Pudiste entregar en {checkin.nombrePunto}?
            </p>
            <div className="mt-4 flex flex-col gap-2">
              <button
                onClick={responderEntregado}
                className="rounded-lg bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-emerald-700"
              >
                Sí, lo entregué
              </button>
              <button
                onClick={responderNoPude}
                className="rounded-lg border border-gray-200 px-4 py-2.5 text-sm font-medium text-gray-700 hover:border-gray-300"
              >
                No pude ir
              </button>
              <button
                onClick={responderCerrado}
                className="rounded-lg border border-gray-200 px-4 py-2.5 text-sm font-medium text-gray-700 hover:border-gray-300"
              >
                El punto estaba cerrado
              </button>
            </div>
          </>
        )}

        {paso === "enviando" && (
          <p className="text-sm text-gray-500">Un momento…</p>
        )}

        {paso === "impacto" && (
          <>
            <p className="text-base font-semibold text-gray-900">
              🌱 Entregaste aproximadamente {peso >= 1000 ? `${(peso / 1000).toFixed(1)} kg` : `${peso} g`} de
              residuos electrónicos.
            </p>
            <p className="mt-2 text-sm text-gray-600">
              Eso es parte de las miles de toneladas que Colombia recupera cada año.
            </p>
            {conteoZona >= UMBRAL_NORMA_SOCIAL && (
              <p className="mt-2 text-sm text-gray-600">
                En tu zona, {conteoZona} personas entregaron RAEE en el último mes.
              </p>
            )}
            <button
              onClick={siguienteCheckin}
              className="mt-4 w-full rounded-lg bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-emerald-700"
            >
              Cerrar
            </button>
          </>
        )}

        {paso === "cerrado" && (
          <>
            <p className="text-base font-semibold text-gray-900">
              Gracias por avisarnos. Vamos a verificar la información de ese punto.
            </p>
            <Link
              href="/"
              onClick={siguienteCheckin}
              className="mt-4 block text-center text-sm text-emerald-700 underline"
            >
              ¿Quieres buscar otro punto cercano?
            </Link>
            <button
              onClick={siguienteCheckin}
              className="mt-3 w-full rounded-lg border border-gray-200 px-4 py-2.5 text-sm font-medium text-gray-700 hover:border-gray-300"
            >
              Cerrar
            </button>
          </>
        )}
      </div>
    </div>
  );
}
