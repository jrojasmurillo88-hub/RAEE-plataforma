import { Suspense } from "react";
import MapaContenido from "./MapaContenido";

export default function MapaPage() {
  return (
    <Suspense fallback={<div className="flex-1 p-6 text-gray-500">Cargando…</div>}>
      <MapaContenido />
    </Suspense>
  );
}
