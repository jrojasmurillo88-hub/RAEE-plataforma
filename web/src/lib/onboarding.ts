const STORAGE_KEY = "raee_onboarding_v1";

export type IntencionDescarte = "pronto" | "mes" | "explorando";

export interface OnboardingData {
  ciudad: string | null;
  intencion: IntencionDescarte;
  completadoEn: string;
}

export function obtenerOnboarding(): OnboardingData | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as OnboardingData) : null;
  } catch {
    return null;
  }
}

export function guardarOnboarding(data: Omit<OnboardingData, "completadoEn">) {
  if (typeof window === "undefined") return;
  const completo: OnboardingData = { ...data, completadoEn: new Date().toISOString() };
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(completo));
}
