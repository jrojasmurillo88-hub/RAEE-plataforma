const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface TipoRaee {
  id: number;
  nombre: string;
}

export interface PuntoCercano {
  id: number;
  nombre: string;
  direccion_texto: string | null;
  ciudad: string | null;
  horario: string | null;
  sistema: string;
  distancia_metros: number;
  lat: number;
  lng: number;
  confianza_coords: number;
  ultima_verificacion: string | null;
}

export interface PuntoDetalle {
  id: number;
  nombre: string;
  direccion_texto: string | null;
  ciudad: string | null;
  horario: string | null;
  activo: boolean;
  confianza_coords: number;
  ultima_verificacion: string | null;
  lng: number;
  lat: number;
  sistema: string;
  url_fuente: string | null;
}

export type TipoReporte =
  | "cerrado"
  | "horario_incorrecto"
  | "direccion_incorrecta"
  | "otro";

const TIMEOUT_MS = 300000; // 5 min — Render free puede tardar >90s en despertar

async function obtenerJson<T>(url: string, init?: RequestInit): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const resp = await fetch(url, { ...init, signal: controller.signal });
    if (!resp.ok) {
      throw new Error(`Error ${resp.status} consultando ${url}`);
    }
    return await resp.json();
  } finally {
    clearTimeout(timer);
  }
}

export function fetchTiposRaee(): Promise<TipoRaee[]> {
  return obtenerJson(`${API_URL}/tipos-raee`);
}

export function fetchPuntosCercanos(params: {
  lat: number;
  lng: number;
  radio?: number;
  tipo?: string;
}): Promise<PuntoCercano[]> {
  const qs = new URLSearchParams({
    lat: String(params.lat),
    lng: String(params.lng),
    radio: String(params.radio ?? 5000),
  });
  if (params.tipo) qs.set("tipo", params.tipo);
  return obtenerJson(`${API_URL}/puntos?${qs.toString()}`);
}

export function fetchPunto(id: number | string): Promise<PuntoDetalle> {
  return obtenerJson(`${API_URL}/puntos/${id}`);
}

export function postReporte(body: {
  punto_id: number;
  tipo: TipoReporte;
  detalle?: string;
}): Promise<{ ok: boolean }> {
  return obtenerJson(`${API_URL}/reportes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

export function postEntrega(body: {
  punto_id: number;
}): Promise<{ ok: boolean; conteo_zona: number }> {
  return obtenerJson(`${API_URL}/entregas`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}
