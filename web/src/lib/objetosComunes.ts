// Lista de objetos cotidianos mapeados a su categoría — para el usuario que no
// sabe en qué grupo entra lo que quiere desechar (ver 04_capa_comportamiento.md:
// "la interfaz muestra objetos, no categorías técnicas").

export interface ObjetoComun {
  nombre: string;
  objetoId: string;
}

export const OBJETOS_COMUNES: ObjetoComun[] = [
  // Equipos electrónicos
  { nombre: "Celular", objetoId: "equipos_electronicos" },
  { nombre: "Tablet", objetoId: "equipos_electronicos" },
  { nombre: "Computador / Portátil", objetoId: "equipos_electronicos" },
  { nombre: "Monitor / Pantalla", objetoId: "equipos_electronicos" },
  { nombre: "Impresora", objetoId: "equipos_electronicos" },
  { nombre: "Teclado / Mouse", objetoId: "equipos_electronicos" },
  { nombre: "Cargador / Cable", objetoId: "equipos_electronicos" },
  { nombre: "Audífonos", objetoId: "equipos_electronicos" },
  { nombre: "Parlante", objetoId: "equipos_electronicos" },
  { nombre: "Cámara", objetoId: "equipos_electronicos" },
  { nombre: "Consola de videojuegos", objetoId: "equipos_electronicos" },
  { nombre: "Radio", objetoId: "equipos_electronicos" },

  // Electrodomésticos pequeños
  { nombre: "Licuadora", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Plancha", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Tostadora", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Cafetera", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Ventilador", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Secador de pelo", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Olla arrocera", objetoId: "electrodomesticos_pequenos" },
  { nombre: "Batidora", objetoId: "electrodomesticos_pequenos" },

  // Electrodomésticos grandes
  { nombre: "Nevera", objetoId: "electrodomesticos_grandes" },
  { nombre: "Lavadora", objetoId: "electrodomesticos_grandes" },
  { nombre: "Microondas", objetoId: "electrodomesticos_grandes" },
  { nombre: "Aire acondicionado", objetoId: "electrodomesticos_grandes" },
  { nombre: "Secadora de ropa", objetoId: "electrodomesticos_grandes" },
  { nombre: "Estufa", objetoId: "electrodomesticos_grandes" },

  // Bombillos
  { nombre: "Bombillo / Foco", objetoId: "bombillos" },
  { nombre: "Lámpara", objetoId: "bombillos" },
  { nombre: "Tubo fluorescente", objetoId: "bombillos" },

  // Pilas
  { nombre: "Pila AA / AAA", objetoId: "pilas" },
  { nombre: "Batería de control remoto", objetoId: "pilas" },
  { nombre: "Batería recargable", objetoId: "pilas" },
  { nombre: "Pila botón", objetoId: "pilas" },

  // Baterías de carro
  { nombre: "Batería de carro", objetoId: "bateria_carro" },
  { nombre: "Batería de moto", objetoId: "bateria_carro" },
];
