"use client";

import { MapContainer, TileLayer, Marker, Popup, useMap, useMapEvents } from "react-leaflet";
import L from "leaflet";
import { useEffect } from "react";
import Link from "next/link";
import type { PuntoCercano } from "@/lib/api";

const iconoPunto = L.divIcon({
  className: "",
  html: `<div style="
    width:14px; height:14px; border-radius:50%;
    background:#10b981; border:2px solid white;
    box-shadow:0 1px 3px rgba(0,0,0,.4);
  "></div>`,
  iconSize: [14, 14],
  iconAnchor: [7, 7],
});

const iconoPuntoElegido = L.divIcon({
  className: "",
  html: `<div style="
    width:18px; height:18px; border-radius:50%;
    background:#047857; border:3px solid white;
    box-shadow:0 1px 4px rgba(0,0,0,.5);
  "></div>`,
  iconSize: [18, 18],
  iconAnchor: [9, 9],
});

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
  modoSeleccionUbicacion = false,
  onElegirUbicacion,
  onSeleccionarPunto,
}: {
  puntos: PuntoCercano[];
  ubicacion: { lat: number; lng: number };
  puntosElegidosIds?: number[];
  modoSeleccionUbicacion?: boolean;
  onElegirUbicacion?: (lat: number, lng: number) => void;
  onSeleccionarPunto?: (id: number) => void;
}) {
  return (
    <MapContainer
      center={[ubicacion.lat, ubicacion.lng]}
      zoom={14}
      scrollWheelZoom
      className={`h-full w-full ${modoSeleccionUbicacion ? "cursor-crosshair" : ""}`}
    >
      <AjustarVista ubicacion={ubicacion} puntos={puntos} />
      <SelectorUbicacion activo={modoSeleccionUbicacion} onElegir={onElegirUbicacion} />
      <TileLayer
        attribution="© OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[ubicacion.lat, ubicacion.lng]} icon={iconoUsuario}>
        <Popup>Tu ubicación</Popup>
      </Marker>
      {puntos.map((p) => (
        <Marker
          key={p.id}
          position={[p.lat, p.lng]}
          icon={puntosElegidosIds.includes(p.id) ? iconoPuntoElegido : iconoPunto}
          eventHandlers={{
            click: () => onSeleccionarPunto?.(p.id),
          }}
        >
          <Popup>
            <strong>{p.nombre}</strong>
            <br />
            {p.ciudad}
            <br />
            <Link href={`/punto/${p.id}`} className="text-emerald-700 underline">
              Ver detalle y cómo llegar →
            </Link>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
