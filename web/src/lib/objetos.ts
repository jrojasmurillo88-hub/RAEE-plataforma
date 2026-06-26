// Objetos del día a día, no categorías técnicas del gestor de residuos.
// Orden por frecuencia esperada de uso (ver 04_capa_comportamiento.md).

export interface ContactoFallback {
  mensaje: string;
  lineaCelular: string;
  lineaFija: string;
}

export interface ObjetoRaee {
  id: string;
  etiqueta: string;
  icono: string;
  tipoRaee: string; // debe coincidir con tipos_raee.nombre en la BD
  contacto?: ContactoFallback; // si existe, se prioriza sobre la búsqueda de puntos
}

export const CONTACTO_LINEA_BLANCA: ContactoFallback = {
  mensaje:
    "Los electrodomésticos grandes no se dejan en un punto — Red Verde los recoge en tu casa.",
  lineaCelular: "317 405 0510",
  lineaFija: "(601) 443 1940",
};

export const CONTACTO_BATERIA_CARRO: ContactoFallback = {
  mensaje: "Las baterías de carro se recogen directamente, no se dejan en un punto.",
  lineaCelular: "310 750 5865",
  lineaFija: "604 322 4414",
};

export const OBJETOS_RAEE: ObjetoRaee[] = [
  { id: "celular", etiqueta: "Celular", icono: "📱", tipoRaee: "Celular" },
  { id: "auriculares", etiqueta: "Auriculares", icono: "🎧", tipoRaee: "Audífono" },
  { id: "cargador", etiqueta: "Cargador / Cable", icono: "🔌", tipoRaee: "Cable" },
  { id: "pila", etiqueta: "Pila / Batería", icono: "🔋", tipoRaee: "Pila" },
  { id: "computador", etiqueta: "Computador", icono: "💻", tipoRaee: "Computador" },
  { id: "pantalla", etiqueta: "Pantalla / Monitor", icono: "🖥️", tipoRaee: "Monitor" },
  { id: "bombilla", etiqueta: "Bombilla / Luminaria", icono: "💡", tipoRaee: "Bombilla" },
  {
    id: "electrodomestico",
    etiqueta: "Electrodomésticos",
    icono: "🧺",
    tipoRaee: "Electrodoméstico",
    contacto: CONTACTO_LINEA_BLANCA,
  },
  {
    id: "nevera",
    etiqueta: "Nevera",
    icono: "🧊",
    tipoRaee: "Nevera",
    contacto: CONTACTO_LINEA_BLANCA,
  },
  {
    id: "bateria_carro",
    etiqueta: "Batería de carro",
    icono: "🔧",
    tipoRaee: "Batería de plomo-ácido",
    contacto: CONTACTO_BATERIA_CARRO,
  },
];

export const OBJETO_DEFAULT_ID = "celular";

export function buscarObjetoPorTipo(tipoRaee: string): ObjetoRaee | undefined {
  return OBJETOS_RAEE.find((o) => o.tipoRaee === tipoRaee);
}
