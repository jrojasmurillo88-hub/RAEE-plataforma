"use client";

import type { PuntoCercano } from "@/lib/api";
import {
  formatDistancia,
  minutosCaminando,
  nivelConfianza,
  textoConfianza,
  COLOR_CONFIANZA,
} from "@/lib/formato";

export default function TarjetaPunto({
  punto,
  seleccionado,
  onClick,
}: {
  punto: PuntoCercano;
  seleccionado?: boolean;
  onClick?: () => void;
}) {
  const confianza = nivelConfianza(punto.ultima_verificacion);

  return (
    <div
      onClick={onClick}
      className={`w-full rounded-lg border p-3 text-left transition cursor-pointer ${
        seleccionado
          ? "border-emerald-500 bg-emerald-50"
          : "border-gray-200 bg-white hover:border-gray-300"
      }`}
    >
      <div className="flex items-start justify-between gap-2">
        <span className="font-semibold text-gray-900">{punto.nombre}</span>
        <span className="whitespace-nowrap text-xs font-medium text-emerald-700">
          {formatDistancia(punto.distancia_metros)}
        </span>
      </div>
      <p className="mt-0.5 text-sm text-gray-500">
        {punto.ciudad ?? "Ciudad no especificada"} · {punto.sistema}
      </p>
      <p className="mt-0.5 text-xs text-gray-500">
        🚶 {minutosCaminando(punto.distancia_metros)} min caminando
      </p>
      <p className="mt-1 text-xs text-gray-600">
        {COLOR_CONFIANZA[confianza]} {textoConfianza(punto.ultima_verificacion)}
      </p>
    </div>
  );
}
