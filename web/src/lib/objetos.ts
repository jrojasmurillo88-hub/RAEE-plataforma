// Categorías amplias, no objetos individuales — ver 04_capa_comportamiento.md.
// El filtrado real es por sistema (no por punto), así que reutilizamos el tipo
// de RAEE que ya está vinculado a los sistemas correctos en la base de datos.

export interface ContactoFallback {
  mensaje: string;
  lineaCelular: string;
  lineaFija: string;
  linkUrl?: string;
  linkLabel?: string;
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
  linkUrl: "https://www.redverde.co/formulario-recoleccion/",
  linkLabel: "Solicitar recogida en redverde.co",
};

export const CONTACTO_BATERIA_CARRO: ContactoFallback = {
  mensaje: "Las baterías de carro se recogen directamente, no se dejan en un punto.",
  lineaCelular: "310 750 5865",
  lineaFija: "604 322 4414",
};

export const OBJETOS_RAEE: ObjetoRaee[] = [
  {
    id: "equipos_electronicos",
    etiqueta: "Equipos electrónicos",
    icono: "💻",
    tipoRaee: "Celular", // mismos sistemas (Lito, EcoCómputo) para todo equipo electrónico
  },
  {
    id: "electrodomesticos_pequenos",
    etiqueta: "Electrodomésticos pequeños",
    icono: "🧺",
    tipoRaee: "Electrodoméstico",
  },
  {
    id: "electrodomesticos_grandes",
    etiqueta: "Electrodomésticos grandes",
    icono: "🧊",
    tipoRaee: "Nevera",
    contacto: CONTACTO_LINEA_BLANCA,
  },
  { id: "bombillos", etiqueta: "Bombillos", icono: "💡", tipoRaee: "Luminaria" },
  { id: "pilas", etiqueta: "Pilas", icono: "🔋", tipoRaee: "Pila" },
  {
    id: "bateria_carro",
    etiqueta: "Baterías de carro",
    icono: "🔧",
    tipoRaee: "Batería de plomo-ácido",
    contacto: CONTACTO_BATERIA_CARRO,
  },
];

export const OBJETO_DEFAULT_ID = "equipos_electronicos";

export function buscarObjetoPorTipo(tipoRaee: string): ObjetoRaee | undefined {
  return OBJETOS_RAEE.find((o) => o.tipoRaee === tipoRaee);
}

export function buscarObjetoPorId(id: string): ObjetoRaee | undefined {
  return OBJETOS_RAEE.find((o) => o.id === id);
}
