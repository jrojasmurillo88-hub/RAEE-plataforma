// Catálogo de ítems específicos de RAEE, usado en el check-in post-entrega
// para preguntar qué se entregó exactamente (en vez de estimar un peso fijo
// por sistema). Los ids deben coincidir con api/catalogo_pesos.py — el peso
// mostrado aquí es solo para la etiqueta visual, el peso real y autoritativo
// se calcula en el backend a partir del id del ítem.
//
// Pesos: estimaciones gruesas de referencia de la industria, no cifras
// oficiales de los sistemas de posconsumo colombianos.

export interface ItemRaee {
  id: string;
  etiqueta: string;
  pesoGramosAprox: number;
  categoriaId: string; // debe coincidir con ObjetoRaee.id en objetos.ts
}

export const ITEMS_RAEE: ItemRaee[] = [
  // equipos_electronicos
  { id: "celular", etiqueta: "Celular", pesoGramosAprox: 150, categoriaId: "equipos_electronicos" },
  { id: "tablet", etiqueta: "Tablet", pesoGramosAprox: 400, categoriaId: "equipos_electronicos" },
  { id: "laptop", etiqueta: "Computador portátil", pesoGramosAprox: 2000, categoriaId: "equipos_electronicos" },
  { id: "computador_escritorio", etiqueta: "Computador de escritorio", pesoGramosAprox: 8000, categoriaId: "equipos_electronicos" },
  { id: "monitor", etiqueta: "Monitor o pantalla", pesoGramosAprox: 4000, categoriaId: "equipos_electronicos" },
  { id: "impresora", etiqueta: "Impresora", pesoGramosAprox: 5000, categoriaId: "equipos_electronicos" },
  { id: "teclado_mouse", etiqueta: "Teclado o mouse", pesoGramosAprox: 200, categoriaId: "equipos_electronicos" },
  { id: "cables_cargadores", etiqueta: "Cables o cargadores", pesoGramosAprox: 100, categoriaId: "equipos_electronicos" },
  { id: "otro_equipo_electronico", etiqueta: "Otro equipo electrónico", pesoGramosAprox: 300, categoriaId: "equipos_electronicos" },

  // electrodomesticos_pequenos
  { id: "licuadora_batidora", etiqueta: "Licuadora o batidora", pesoGramosAprox: 1200, categoriaId: "electrodomesticos_pequenos" },
  { id: "plancha", etiqueta: "Plancha", pesoGramosAprox: 1000, categoriaId: "electrodomesticos_pequenos" },
  { id: "ventilador", etiqueta: "Ventilador", pesoGramosAprox: 2000, categoriaId: "electrodomesticos_pequenos" },
  { id: "cafetera", etiqueta: "Cafetera", pesoGramosAprox: 1500, categoriaId: "electrodomesticos_pequenos" },
  { id: "otro_electrodomestico_pequeno", etiqueta: "Otro electrodoméstico pequeño", pesoGramosAprox: 1000, categoriaId: "electrodomesticos_pequenos" },

  // bombillos
  { id: "bombillo_led", etiqueta: "Bombillo o ahorrador", pesoGramosAprox: 100, categoriaId: "bombillos" },
  { id: "tubo_fluorescente", etiqueta: "Tubo fluorescente", pesoGramosAprox: 200, categoriaId: "bombillos" },

  // pilas
  { id: "pila_aa_aaa", etiqueta: "Pila AA / AAA", pesoGramosAprox: 20, categoriaId: "pilas" },
  { id: "pila_boton", etiqueta: "Pila botón", pesoGramosAprox: 5, categoriaId: "pilas" },
  { id: "bateria_recargable", etiqueta: "Batería recargable", pesoGramosAprox: 50, categoriaId: "pilas" },
];

export function itemsPorCategorias(categoriaIds: string[]): ItemRaee[] {
  if (categoriaIds.length === 0) return ITEMS_RAEE;
  return ITEMS_RAEE.filter((i) => categoriaIds.includes(i.categoriaId));
}

export function formatearPeso(gramos: number): string {
  return gramos >= 1000 ? `${(gramos / 1000).toFixed(1)} kg` : `${gramos} g`;
}
