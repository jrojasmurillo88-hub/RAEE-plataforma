// Identificador anónimo de sesión — solo para poder cruzar eventos del mismo
// dispositivo (selección → intención → entrega) sin guardar datos personales.
const STORAGE_KEY = "raee_session_id_v1";

export function obtenerSessionId(): string {
  if (typeof window === "undefined") return "";
  try {
    let id = window.localStorage.getItem(STORAGE_KEY);
    if (!id) {
      id = crypto.randomUUID();
      window.localStorage.setItem(STORAGE_KEY, id);
    }
    return id;
  } catch {
    return "";
  }
}
