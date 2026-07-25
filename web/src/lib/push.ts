import { postPushProgramar, postPushSuscribir } from "@/lib/api";

const VAPID_PUBLIC_KEY = process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY || "";

function base64UrlAUint8Array(base64Url: string): BufferSource {
  const padding = "=".repeat((4 - (base64Url.length % 4)) % 4);
  const base64 = (base64Url + padding).replace(/-/g, "+").replace(/_/g, "/");
  const raw = window.atob(base64);
  const bytes = new ArrayBuffer(raw.length);
  const vista = new Uint8Array(bytes);
  for (let i = 0; i < raw.length; i++) vista[i] = raw.charCodeAt(i);
  return bytes;
}

// Pide permiso de notificaciones y registra la suscripción en el backend.
// Devuelve el endpoint de la suscripción, o null si el usuario no dio permiso
// o el navegador no soporta push (falla silenciosamente — nunca bloquea el flujo).
export async function suscribirseAPush(): Promise<string | null> {
  if (typeof window === "undefined") return null;
  if (!("serviceWorker" in navigator) || !("PushManager" in window)) return null;
  if (!VAPID_PUBLIC_KEY) return null;

  try {
    if (Notification.permission === "denied") return null;
    if (Notification.permission === "default") {
      const permiso = await Notification.requestPermission();
      if (permiso !== "granted") return null;
    }

    const registro = await navigator.serviceWorker.register("/sw.js");
    await navigator.serviceWorker.ready;

    let suscripcion = await registro.pushManager.getSubscription();
    if (!suscripcion) {
      suscripcion = await registro.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: base64UrlAUint8Array(VAPID_PUBLIC_KEY),
      });
    }

    const json = suscripcion.toJSON();
    if (!json.endpoint || !json.keys?.p256dh || !json.keys?.auth) return null;

    await postPushSuscribir({
      endpoint: json.endpoint,
      keys: { p256dh: json.keys.p256dh, auth: json.keys.auth },
    });

    return json.endpoint;
  } catch {
    return null;
  }
}

// Programa el recordatorio de check-in 24h después de que el usuario pidió la ruta.
// Si no se pudo suscribir a push, no pasa nada — el check-in dentro de la app sigue
// funcionando igual cuando el usuario vuelva a abrir la página.
export async function programarRecordatorioPush(
  puntoId: number,
  nombrePunto: string
): Promise<void> {
  const endpoint = await suscribirseAPush();
  if (!endpoint) return;
  try {
    await postPushProgramar({ endpoint, punto_id: puntoId, nombre_punto: nombrePunto });
  } catch {
    // si falla, el recordatorio dentro de la app (checkins.ts) sigue siendo el respaldo
  }
}
