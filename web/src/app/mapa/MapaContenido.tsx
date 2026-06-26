"use client";

import dynamic from "next/dynamic";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { fetchPuntosCercanos, type PuntoCercano } from "@/lib/api";
import { buscarObjetoPorTipo, type ObjetoRaee } from "@/lib/objetos";
import { construirUrlRutaGoogleMaps } from "@/lib/rutas";
import { agregarCheckinPendiente } from "@/lib/checkins";
import TarjetaPunto from "@/components/TarjetaPunto";
import TarjetaContacto from "@/components/TarjetaContacto";

const MapaPuntos = dynamic(() => import("@/components/MapaPuntos"), {
  ssr: false,
  loading: () => (
    <div className="flex h-full items-center justify-center text-gray-400">
      Cargando mapa…
    </div>
  ),
});

const RADIOS_BUSQUEDA = [5000, 20000, 50000];
const UBICACION_DEFAULT = { lat: 4.711, lng: -74.0721 }; // Bogotá, centro
const MAX_TARJETAS_POR_TIPO = 5;

type EstadoUbicacion = "buscando" | "ok" | "denegada" | "no-disponible";

interface ResultadoTipo {
  cargando: boolean;
  puntos: PuntoCercano[];
  radioUsado: number | null;
  error: string | null;
}

export default function MapaContenido() {
  const searchParams = useSearchParams();
  const parametroTipos = searchParams.get("tipos") ?? searchParams.get("tipo") ?? "";
  const tiposPedidos = parametroTipos.split(",").map((t) => t.trim()).filter(Boolean);
  const objetos: ObjetoRaee[] = tiposPedidos
    .map((t) => buscarObjetoPorTipo(t))
    .filter((o): o is ObjetoRaee => Boolean(o));

  const objetosContacto = objetos.filter((o) => o.contacto);
  const objetosMapa = objetos.filter((o) => !o.contacto);

  const [ubicacion, setUbicacion] = useState<{ lat: number; lng: number } | null>(null);
  const [estadoUbicacion, setEstadoUbicacion] = useState<EstadoUbicacion>("buscando");
  const [resultados, setResultados] = useState<Record<string, ResultadoTipo>>({});
  const [elegidos, setElegidos] = useState<Record<string, number>>({});

  function solicitarUbicacion() {
    setEstadoUbicacion("buscando");
    if (!("geolocation" in navigator)) {
      setEstadoUbicacion("no-disponible");
      setUbicacion(UBICACION_DEFAULT);
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setUbicacion({ lat: pos.coords.latitude, lng: pos.coords.longitude });
        setEstadoUbicacion("ok");
      },
      () => {
        setEstadoUbicacion("denegada");
        setUbicacion(UBICACION_DEFAULT);
      },
      { enableHighAccuracy: true, timeout: 8000 }
    );
  }

  useEffect(() => {
    solicitarUbicacion();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!ubicacion || objetosMapa.length === 0) return;

    let cancelado = false;

    objetosMapa.forEach((objeto) => {
      setResultados((actual) => ({
        ...actual,
        [objeto.tipoRaee]: { cargando: true, puntos: [], radioUsado: null, error: null },
      }));

      (async () => {
        for (const radio of RADIOS_BUSQUEDA) {
          try {
            const resultado = await fetchPuntosCercanos({
              lat: ubicacion.lat,
              lng: ubicacion.lng,
              radio,
              tipo: objeto.tipoRaee,
            });
            if (cancelado) return;
            if (resultado.length > 0 || radio === RADIOS_BUSQUEDA[RADIOS_BUSQUEDA.length - 1]) {
              setResultados((actual) => ({
                ...actual,
                [objeto.tipoRaee]: {
                  cargando: false,
                  puntos: resultado,
                  radioUsado: radio,
                  error: null,
                },
              }));
              if (resultado.length > 0) {
                setElegidos((actual) =>
                  actual[objeto.tipoRaee] ? actual : { ...actual, [objeto.tipoRaee]: resultado[0].id }
                );
              }
              return;
            }
          } catch {
            if (!cancelado) {
              setResultados((actual) => ({
                ...actual,
                [objeto.tipoRaee]: {
                  cargando: false,
                  puntos: [],
                  radioUsado: null,
                  error: "No pudimos cargar los puntos. ¿Está corriendo la API?",
                },
              }));
            }
            return;
          }
        }
      })();
    });

    return () => {
      cancelado = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ubicacion, parametroTipos]);

  const puntosPorId = new Map<number, PuntoCercano>();
  objetosMapa.forEach((o) => {
    resultados[o.tipoRaee]?.puntos.forEach((p) => puntosPorId.set(p.id, p));
  });
  const todosLosPuntos = Array.from(puntosPorId.values());
  const idsElegidos = Array.from(new Set(Object.values(elegidos)));

  const destinosRuta = objetosMapa
    .map((o) => {
      const idElegido = elegidos[o.tipoRaee];
      return resultados[o.tipoRaee]?.puntos.find((p) => p.id === idElegido);
    })
    .filter((p): p is PuntoCercano => Boolean(p))
    .filter((p, indice, arr) => arr.findIndex((otro) => otro.id === p.id) === indice)
    .sort((a, b) => a.distancia_metros - b.distancia_metros);

  const urlRuta = ubicacion && destinosRuta.length > 0
    ? construirUrlRutaGoogleMaps(ubicacion, destinosRuta)
    : null;

  const etiquetaTitulo = objetos.map((o) => o.etiqueta).join(" + ") || "objeto";

  return (
    <main className="flex flex-1 flex-col bg-gray-50">
      <header className="flex items-center gap-3 border-b bg-white px-4 py-3">
        <Link href="/" className="text-sm text-gray-500 hover:text-gray-800">
          ← Cambiar
        </Link>
        <h1 className="text-sm font-semibold text-gray-900">
          Puntos para entregar: {etiquetaTitulo}
        </h1>
      </header>

      {estadoUbicacion === "denegada" && (
        <div className="bg-amber-50 px-4 py-2 text-xs text-amber-800">
          No pudimos acceder a tu ubicación — mostrando resultados desde Bogotá.{" "}
          <button onClick={solicitarUbicacion} className="font-medium underline">
            Reintentar
          </button>
        </div>
      )}
      {estadoUbicacion === "no-disponible" && (
        <div className="bg-amber-50 px-4 py-2 text-xs text-amber-800">
          Tu navegador no soporta geolocalización — mostrando resultados desde Bogotá.
        </div>
      )}

      <div className="flex flex-1 flex-col md:flex-row">
        <section className="order-2 flex-1 overflow-y-auto p-4 md:order-1 md:max-w-sm">
          {estadoUbicacion === "buscando" && (
            <p className="text-sm text-gray-500">Buscando tu ubicación…</p>
          )}

          <div className="flex flex-col gap-3">
            {objetosContacto.map((objeto) => (
              <TarjetaContacto
                key={objeto.id}
                etiqueta={objeto.etiqueta}
                icono={objeto.icono}
                contacto={objeto.contacto!}
              />
            ))}

            {objetosMapa.map((objeto) => {
              const resultado = resultados[objeto.tipoRaee];
              return (
                <div key={objeto.id}>
                  <h2 className="mb-1 flex items-center gap-1 text-sm font-semibold text-gray-800">
                    <span>{objeto.icono}</span> {objeto.etiqueta}
                  </h2>

                  {!resultado || resultado.cargando ? (
                    <p className="text-sm text-gray-500">Buscando puntos cercanos…</p>
                  ) : resultado.error ? (
                    <p className="text-sm text-red-600">{resultado.error}</p>
                  ) : resultado.puntos.length === 0 ? (
                    <p className="text-sm text-gray-500">
                      No encontramos puntos cercanos para {objeto.etiqueta.toLowerCase()}.
                    </p>
                  ) : (
                    <>
                      {resultado.radioUsado && resultado.radioUsado > RADIOS_BUSQUEDA[0] && (
                        <p className="mb-1 text-xs text-gray-500">
                          Ampliamos la búsqueda a {resultado.radioUsado / 1000} km.
                        </p>
                      )}
                      <div className="flex flex-col gap-2">
                        {resultado.puntos.slice(0, MAX_TARJETAS_POR_TIPO).map((p) => (
                          <div key={p.id}>
                            <TarjetaPunto
                              punto={p}
                              seleccionado={elegidos[objeto.tipoRaee] === p.id}
                              onClick={() =>
                                setElegidos((actual) => ({ ...actual, [objeto.tipoRaee]: p.id }))
                              }
                            />
                            <Link
                              href={`/punto/${p.id}`}
                              className="mt-1 inline-block text-xs text-emerald-700 underline"
                            >
                              Ver detalle →
                            </Link>
                          </div>
                        ))}
                      </div>
                    </>
                  )}
                </div>
              );
            })}
          </div>

          {urlRuta && (
            <a
              href={urlRuta}
              target="_blank"
              rel="noopener noreferrer"
              onClick={() =>
                destinosRuta.forEach((p) =>
                  agregarCheckinPendiente({
                    puntoId: p.id,
                    nombrePunto: p.nombre,
                    sistema: p.sistema,
                  })
                )
              }
              className="mt-4 block w-full rounded-xl bg-emerald-600 px-4 py-3 text-center text-base font-semibold text-white shadow hover:bg-emerald-700"
            >
              {destinosRuta.length > 1
                ? `Planear ruta (${destinosRuta.length} paradas)`
                : "Cómo llegar"}
            </a>
          )}
        </section>

        <section className="order-1 h-[50vh] md:order-2 md:h-auto md:flex-1">
          {ubicacion && (
            <MapaPuntos
              puntos={todosLosPuntos}
              ubicacion={ubicacion}
              puntosElegidosIds={idsElegidos}
              onSeleccionarPunto={(id) => {
                const objeto = objetosMapa.find((o) =>
                  resultados[o.tipoRaee]?.puntos.some((p) => p.id === id)
                );
                if (objeto) {
                  setElegidos((actual) => ({ ...actual, [objeto.tipoRaee]: id }));
                }
              }}
            />
          )}
        </section>
      </div>
    </main>
  );
}
