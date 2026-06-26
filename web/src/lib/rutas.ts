export interface Coordenada {
  lat: number;
  lng: number;
}

export function construirUrlRutaGoogleMaps(
  origen: Coordenada,
  destinos: Coordenada[]
): string {
  if (destinos.length === 0) return "";

  const ultimo = destinos[destinos.length - 1];
  const intermedios = destinos.slice(0, -1);

  const params = new URLSearchParams({
    api: "1",
    origin: `${origen.lat},${origen.lng}`,
    destination: `${ultimo.lat},${ultimo.lng}`,
    travelmode: "driving",
  });

  if (intermedios.length > 0) {
    params.set("waypoints", intermedios.map((p) => `${p.lat},${p.lng}`).join("|"));
  }

  return `https://www.google.com/maps/dir/?${params.toString()}`;
}
