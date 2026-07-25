"""
Catálogo de ítems de RAEE con su peso aproximado en gramos.

Reemplaza la estimación por sistema (pesoEstimadoGramos) por una estimación
real: el usuario dice qué entregó específicamente, y sumamos el peso de cada
ítem. Los pesos son estimaciones gruesas de referencia de la industria —
no provienen de datos oficiales de los sistemas de posconsumo colombianos.
Ajustar si algún sistema (EcoCómputo, Pilas con el Ambiente, etc.) entrega
cifras propias de peso promedio por aparato.

Los ids deben coincidir exactamente con web/src/lib/itemsRaee.ts
"""

PESO_POR_ITEM_GRAMOS: dict[str, int] = {
    # equipos_electronicos
    "celular": 150,
    "tablet": 400,
    "laptop": 2000,
    "computador_escritorio": 8000,
    "monitor": 4000,
    "impresora": 5000,
    "teclado_mouse": 200,
    "cables_cargadores": 100,
    "otro_equipo_electronico": 300,
    # electrodomesticos_pequenos
    "licuadora_batidora": 1200,
    "plancha": 1000,
    "ventilador": 2000,
    "cafetera": 1500,
    "otro_electrodomestico_pequeno": 1000,
    # bombillos
    "bombillo_led": 100,
    "tubo_fluorescente": 200,
    # pilas
    "pila_aa_aaa": 20,
    "pila_boton": 5,
    "bateria_recargable": 50,
}

PESO_DEFAULT_GRAMOS = 150


def calcular_peso_total(items: list[str]) -> int:
    """Suma el peso de cada ítem entregado. Ítems desconocidos usan el default."""
    return sum(PESO_POR_ITEM_GRAMOS.get(item, PESO_DEFAULT_GRAMOS) for item in items)
