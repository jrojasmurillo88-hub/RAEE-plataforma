export function formatDistancia(metros: number): string {
  if (metros < 1000) return `${Math.round(metros)} m`;
  return `${(metros / 1000).toFixed(1)} km`;
}

export function minutosCaminando(metros: number): number {
  const VELOCIDAD_M_MIN = 80; // ~4.8 km/h
  return Math.max(1, Math.round(metros / VELOCIDAD_M_MIN));
}

export type NivelConfianza = "verde" | "amarillo" | "rojo";

export function nivelConfianza(ultimaVerificacion: string | null): NivelConfianza {
  if (!ultimaVerificacion) return "rojo";
  const dias =
    (Date.now() - new Date(ultimaVerificacion).getTime()) / (1000 * 60 * 60 * 24);
  if (dias <= 7) return "verde";
  if (dias <= 30) return "amarillo";
  return "rojo";
}

export function textoConfianza(ultimaVerificacion: string | null): string {
  if (!ultimaVerificacion) return "Sin verificación reciente — llamar antes de ir";
  const dias = Math.floor(
    (Date.now() - new Date(ultimaVerificacion).getTime()) / (1000 * 60 * 60 * 24)
  );
  if (dias <= 0) return "Información verificada hoy";
  if (dias === 1) return "Información verificada hace 1 día";
  if (dias <= 30) return `Información verificada hace ${dias} días`;
  const meses = Math.floor(dias / 30);
  return `Información verificada hace ${meses} ${meses === 1 ? "mes" : "meses"}`;
}

export const COLOR_CONFIANZA: Record<NivelConfianza, string> = {
  verde: "🟢",
  amarillo: "🟡",
  rojo: "🔴",
};
