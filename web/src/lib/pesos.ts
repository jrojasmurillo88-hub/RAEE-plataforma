// Peso aproximado en gramos de un RAEE típico entregado en cada sistema.
// Son estimaciones gruesas solo para el mensaje de impacto — no buscan precisión.
const PESO_POR_SISTEMA: Record<string, number> = {
  "Puntos Verdes Lito": 150,
  "EcoCómputo": 150,
  "Pilas con el Ambiente": 20,
  "Lúmina": 50,
  "Red Verde": 25000,
};

const PESO_DEFAULT = 150;

export function pesoEstimadoGramos(sistema: string): number {
  return PESO_POR_SISTEMA[sistema] ?? PESO_DEFAULT;
}
