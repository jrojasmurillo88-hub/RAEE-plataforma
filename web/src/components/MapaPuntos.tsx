"use client";

import { MapContainer, TileLayer, Marker, Popup, useMap, useMapEvents } from "react-leaflet";
import L from "leaflet";
import { useEffect, useMemo } from "react";
import Link from "next/link";
import type { PuntoCercano } from "@/lib/api";
import { COLORES_CATEGORIA, OBJETOS_RAEE } from "@/lib/objetos";

const COLOR_DEFAULT = "#6b7280";

const iconoUsuario = L.divIcon({
  className: "",
  html: `<div style="
    width:14px; height:14px; border-radius:50%;
    background:#3b82f6; border:2px solid white;
    box-shadow:0 0 0 4px rgba(59,130,246,.3);
  "></div>`,
  iconSize: [14, 14],
  iconAnchor: [7, 7],
});

function crearIcono(objetoId: string | undefined, elegido: boolean): L.DivIcon {
  const color = (objetoId && COLORES_CATEGORIA[objetoId]) ?? COLOR_DEFAULT;
  const size = elegido ? 18 : 14;
  const borde = elegido ? "3px" : "2px";
  return L.divIcon({
    className: "",
    html: `<div style="
      width:${size}px; height:${size}px; border-radius:50%;
      background:${color}; border:${borde} solid white;
      box-shadow:0 1px ${elegido ? 4 : 3}px rgba(0,0,0,${elegido ? ".5" : ".4"});
    "></div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
  });
}


function AjustarVista({
  ubicacion,
  puntos,
}: {
  ubicacion: { lat: number; lng: number };
  puntos: PuntoCercano[];
}) {
  const map = useMap();
  useEffect(() => {
    if (puntos.length === 0) {
      map.setView([ubicacion.lat, ubicacion.lng], 14);
      return;
    }
    const bounds = L.latLngBounds([
      [ubicacion.lat, ubicacion.lng],
      ...puntos.map((p) => [p.lat, p.lng] as [number, number]),
    ]);
    map.fitBounds(bounds, { padding: [40, 40], maxZoom: 16 });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ubicacion.lat, ubicacion.lng, puntos.map((p) => p.id).join(","), map]);
  return null;
}

function calcularPosicionesVisibles(
  puntos: PuntoCercano[]
): Map<number, { posicion: [number, number]; tamanoGrupo: number }> {
  const grupos = new Map<string, PuntoCercano[]>();
  puntos.forEach((p) => {
    const clave = `${p.lat.toFixed(5)},${p.lng.toFixed(5)}`;
    const grupo = grupos.get(clave);
    if (grupo) grupo.push(p);
    else grupos.set(clave, [p]);
  });

  const RADIO_GRADOS = 0.00012;
  const resultado = new Map<number, { posicion: [number, number]; tamanoGrupo: number }>();
  grupos.forEach((grupo) => {
    if (grupo.length === 1) {
      resultado.set(grupo[0].id, { posicion: [grupo[0].lat, grupo[0].lng], tamanoGrupo: 1 });
      return;
    }
    grupo.forEach((p, i) => {
      const angulo = (2 * Math.PI * i) / grupo.length;
      resultado.set(p.id, {
        posicion: [p.lat + RADIO_GRADOS * Math.cos(angulo), p.lng + RADIO_GRADOS * Math.sin(angulo)],
        tamanoGrupo: grupo.length,
      });
    });
  });
  return resultado;
}

function SelectorUbicacion({
  activo,
  onElegir,
}: {
  activo: boolean;
  onElegir?: (lat: number, lng: number) => void;
}) {
  useMapEvents({
    click(e) {
      if (activo) onElegir?.(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
}

export default function MapaPuntos({
  puntos,
  ubicacion,
  puntosElegidosIds = [],
  puntoAObjetoId = new Map(),
  modoSeleccionUbicacion = false,
  onElegirUbicacion,
  onSeleccionarPunto,
}: {
  puntos: PuntoCercano[];
  ubicacion: { lat: number; lng: number };
  puntosElegidosIds?: number[];
  puntoAObjetoId?: Map<number, string>;
  modoSeleccionUbicacion?: boolean;
  onElegirUbicacion?: (lat: number, lng: number) => void;
  onSeleccionarPunto?: (id: number) => void;
}) {
  const posiciones = calcularPosicionesVisibles(puntos);

  // Categorías visibles en el mapa en este momento (para la leyenda)
  const categoriasVisibles = useMemo(() => {
    const ids = [...new Set(puntoAObjetoId.values())];
    return ids
      .map((id) => OBJETOS_RAEE.find((o) => o.id === id))
      .filter(Boolean) as typeof OBJETOS_RAEE;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [[...puntoAObjetoId.values()].join(",")]);

  return (
    <div className="relative h-full w-full">
      {categoriasVisibles.length > 0 && (
        <div className="absolute bottom-5 right-2 z-[1000] rounded-lg bg-white px-3 py-2 text-xs shadow-md">
          <p className="mb-1 font-semibold text-gray-700">Categorías</p>
          {categoriasVisibles.map((o) => (
            <div key={o.id} className="flex items-center gap-1.5 leading-relaxed">
              <span
                style={{ background: COLORES_CATEGORIA[o.id] ?? COLOR_DEFAULT }}
                className="inline-block h-2.5 w-2.5 flex-shrink-0 rounded-full border border-white shadow-sm"
              />
              <span className="text-gray-700">{o.icono} {o.etiqueta}</span>
            </div>
          ))}
        </div>
      )}
    <MapContainer
      center={[ubicacion.lat, ubicacion.lng]}
      zoom={14}
      scrollWheelZoom
      className={`h-full w-full ${modoSeleccionUbicacion ? "cursor-crosshair" : ""}`}
    >
      <AjustarVista ubicacion={ubicacion} puntos={puntos} />
      <SelectorUbicacion activo={modoSeleccionUbicacion} onElegir={onElegirUbicacion} />
      <TileLayer
        attribution='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
      />
      <Marker position={[ubicacion.lat, ubicacion.lng]} icon={iconoUsuario}>
        <Popup>Tu ubicación</Popup>
      </Marker>
      {puntos.map((p) => {
        const info = posiciones.get(p.id) ?? { posicion: [p.lat, p.lng] as [number, number], tamanoGrupo: 1 };
        const elegido = puntosElegidosIds.includes(p.id);
        const objetoId = puntoAObjetoId.get(p.id);
        const objeto = OBJETOS_RAEE.find((o) => o.id === objetoId);
        const color = (objetoId && COLORES_CATEGORIA[objetoId]) ?? COLOR_DEFAULT;
        return (
          <Marker
            key={p.id}
            position={info.posicion}
            icon={crearIcono(objetoId, elegido)}
            eventHandlers={{ click: () => onSeleccionarPunto?.(p.id) }}
          >
            <Popup>
              <div style={{ fontSize: "13px", minWidth: "160px" }}>
                <strong>{p.nombre}</strong>
                <br />
                {objeto && (
                  <span
                    style={{
                      display: "inline-block",
                      marginTop: "3px",
                      padding: "1px 7px",
                      borderRadius: "10px",
                      background: color,
                      color: "white",
                      fontSize: "11px",
                    }}
                  >
                    {objeto.icono} {objeto.etiqueta}
                  </span>
                )}
                <br />
                <span style={{ color: "#6b7280", fontSize: "12px" }}>{p.ciudad}</span>
                {info.tamanoGrupo > 1 && (
                  <>
                    <br />
                    <span style={{ fontSize: "11px", color: "#92400e" }}>
                      Hay {info.tamanoGrupo} puntos en esta misma dirección.
                    </span>
                  </>
                )}
                <br />
                <Link href={`/punto/${p.id}`} className="text-emerald-700 underline">
                  Ver detalle y cómo llegar →
                </Link>
              </div>
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
    </div>
  );
}
