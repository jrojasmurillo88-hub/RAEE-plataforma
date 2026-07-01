// Lista de objetos cotidianos mapeados a su categoría — para el usuario que no
// sabe en qué grupo entra lo que quiere desechar (ver 04_capa_comportamiento.md:
// "la interfaz muestra objetos, no categorías técnicas").
// Electrodomésticos grandes: clasificación basada en el infográfico de Red Verde.

export interface ObjetoComun {
  nombre: string;
  objetoId: string;
}

export const OBJETOS_COMUNES: ObjetoComun[] = [
  // ── Equipos electrónicos ─────────────────────────────────────────────
  { nombre: "Celular", objetoId: "equipos_electronicos" },
  { nombre: "Tablet", objetoId: "equipos_electronicos" },
  { nombre: "Computador", objetoId: "equipos_electronicos" },
  { nombre: "Portátil", objetoId: "equipos_electronicos" },
  { nombre: "Monitor", objetoId: "equipos_electronicos" },
  { nombre: "Pantalla", objetoId: "equipos_electronicos" },
  { nombre: "Impresora", objetoId: "equipos_electronicos" },
  { nombre: "Teclado", objetoId: "equipos_electronicos" },
  { nombre: "Mouse", objetoId: "equipos_electronicos" },
  { nombre: "Cargador", objetoId: "equipos_electronicos" },
  { nombre: "Cable USB", objetoId: "equipos_electronicos" },
  { nombre: "Audífonos", objetoId: "equipos_electronicos" },
  { nombre: "Parlante", objetoId: "equipos_electronicos" },
  { nombre: "Cámara", objetoId: "equipos_electronicos" },
  { nombre: "Consola de videojuegos", objetoId: "equipos_electronicos" },
  { nombre: "TV", objetoId: "equipos_electronicos" },
  { nombre: "Televisor", objetoId: "equipos_electronicos" },
  { nombre: "Radio", objetoId: "equipos_electronicos" },
  { nombre: "DVD", objetoId: "equipos_electronicos" },
  { nombre: "Equipo de sonido", objetoId: "equipos_electronicos" },
  { nombre: "Grabadora", objetoId: "equipos_electronicos" },
  { nombre: "Tocadiscos", objetoId: "equipos_electronicos" },
  { nombre: "Reloj de pulsera", objetoId: "equipos_electronicos" },

  // ── Electrodomésticos pequeños ────────────────────────────────────────
  // Enseres menores de cocina
  { nombre: "Licuadora", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Batidora", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Procesadora de alimentos", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Picadora", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Peladora de papas", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Exprimidor eléctrico", objetoId: "electrodomesticos_pequenos" },
  // Enseres menores de calentamiento
  { nombre: "Tostadora", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Cafetera", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Olla arrocera", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Freidora de aire", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Sanduchera", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Waflera", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Plancha de ropa", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Deshidratador de frutas", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Calentador de agua", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Calentador de ambiente", objetoId: "electrodomesticos_pequenos" },
  // Enseres menores personales
  { nombre: "Secador de pelo", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Plancha de pelo", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Rizador", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Afeitadora eléctrica", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Masajeador", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Máquina de ejercicio", objetoId: "electrodomesticos_pequenos" },
  // Enseres menores de hogar
  { nombre: "Ventilador", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Aspiradora", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Brilladora", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Máquina de coser", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Lavaplatos eléctrico", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Campana de cocina", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Báscula eléctrica", objetoId: "electrodomesticos_pequenos" },
  // Herramientas para el hogar
  { nombre: "Taladro", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Pulidora", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Soldadora", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Lijadora", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Herramienta eléctrica", objetoId: "electrodomesticos_pequenos" },

  // ── Electrodomésticos grandes (Red Verde, recogida a domicilio) ────────
  // Enseres mayores de hogar
  { nombre: "Lavadora", objetoId: "electrodomesticos_grandes" },
  { nombre: "Secadora de ropa", objetoId: "electrodomesticos_grandes" },
  // Refrigeración
  { nombre: "Nevera", objetoId: "electrodomesticos_grandes" },
  { nombre: "Congelador", objetoId: "electrodomesticos_grandes" },
  { nombre: "Vinero eléctrico", objetoId: "electrodomesticos_grandes" },
  { nombre: "Dispensador de agua", objetoId: "electrodomesticos_grandes" },
  // Cocinas y hornos
  { nombre: "Microondas", objetoId: "electrodomesticos_grandes" },
  { nombre: "Horno eléctrico", objetoId: "electrodomesticos_grandes" },
  { nombre: "Estufa eléctrica", objetoId: "electrodomesticos_grandes" },
  { nombre: "Cubierta eléctrica", objetoId: "electrodomesticos_grandes" },
  // Climatización
  { nombre: "Aire acondicionado", objetoId: "electrodomesticos_grandes" },
  { nombre: "Calefacción", objetoId: "electrodomesticos_grandes" },
  { nombre: "Asador eléctrico", objetoId: "electrodomesticos_grandes" },
  { nombre: "Parrilla eléctrica", objetoId: "electrodomesticos_grandes" },

  // ── Bombillos ─────────────────────────────────────────────────────────
  { nombre: "Bombillo", objetoId: "bombillos" },
  { nombre: "Bombilla", objetoId: "bombillos" },
  { nombre: "Lámpara", objetoId: "bombillos" },
  { nombre: "Tubo fluorescente", objetoId: "bombillos" },
  { nombre: "Foco LED", objetoId: "bombillos" },
  { nombre: "Luminaria", objetoId: "bombillos" },

  // ── Pilas ─────────────────────────────────────────────────────────────
  { nombre: "Pila AA", objetoId: "pilas" },
  { nombre: "Pila AAA", objetoId: "pilas" },
  { nombre: "Pila botón", objetoId: "pilas" },
  { nombre: "Batería de control remoto", objetoId: "pilas" },
  { nombre: "Batería recargable", objetoId: "pilas" },

  // ── Baterías de carro ─────────────────────────────────────────────────
  { nombre: "Batería de carro", objetoId: "bateria_carro" },
  { nombre: "Batería de moto", objetoId: "bateria_carro" },
  { nombre: "Batería de plomo", objetoId: "bateria_carro" },
];
