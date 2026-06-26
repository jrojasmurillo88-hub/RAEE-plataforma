"""
Scraper para EcoCómputo.
Usa el endpoint del plugin WordPress Store Locator:
  GET /wp-admin/admin-ajax.php?action=store_search&lat=...&lng=...&max_results=...&search_radius=...

El endpoint ignora max_results/search_radius y siempre limita la respuesta
a los 50 puntos más cercanos al lat/lng enviado (cap fijo del servidor).
Por eso se consulta desde varios centros urbanos repartidos por Colombia
y se combinan los resultados, deduplicando por el campo "id" de cada tienda.
"""

import re
import requests
from models import PuntoRecoleccion

API_URL = "https://ecocomputo.com/wp-admin/admin-ajax.php"
SISTEMA = "EcoCómputo"
TIPOS_RAEE = ["Computador", "Monitor", "Tablet", "Impresora", "Celular", "Periférico", "Teclado"]

# Centros urbanos repartidos por Colombia para cubrir el cap de 50 resultados por consulta
CENTROS = [
    ("Bogotá",       4.7110, -74.0721),
    ("Medellín",     6.2442, -75.5812),
    ("Cali",         3.4516, -76.5320),
    ("Barranquilla", 10.9685, -74.7813),
    ("Cartagena",    10.3910, -75.4794),
    ("Bucaramanga",  7.1193, -73.1227),
    ("Pereira",      4.8087, -75.6906),
    ("Manizales",    5.0689, -75.5174),
    ("Ibagué",       4.4389, -75.2322),
    ("Villavicencio", 4.1420, -73.6266),
    ("Pasto",        1.2136, -77.2811),
    ("Cúcuta",       7.8939, -72.5078),
    ("Santa Marta",  11.2408, -74.1990),
    ("Montería",     8.7479, -75.8814),
    ("Neiva",        2.9273, -75.2819),
    ("Popayán",      2.4448, -76.6147),
    ("Tunja",        5.5353, -73.3678),
    ("Armenia",      4.5339, -75.6811),
    ("Sincelejo",    9.3047, -75.3978),
    ("Riohacha",     11.5444, -72.9072),
    ("Valledupar",   10.4631, -73.2532),
    ("Quibdó",       5.6947, -76.6611),
    ("Florencia",    1.6144, -75.6062),
    ("Yopal",        5.3378, -72.3959),
    ("San Andrés",   12.5847, -81.7006),
    ("Leticia",      -4.2153, -69.9406),
    ("Arauca",       7.0902, -70.7617),
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://ecocomputo.com/puntos-de-recoleccion/",
}


def _limpiar_horario(html: str | None) -> str | None:
    if not html:
        return None
    texto = re.sub(r"<tr>", "\n", html)
    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto or None


def _consultar(lat: float, lng: float) -> list[dict]:
    params = {
        "action": "store_search",
        "lat": lat,
        "lng": lng,
        "max_results": 500,
        "search_radius": 2000,
        "autoload": 1,
    }
    resp = requests.get(API_URL, params=params, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    datos = resp.json()
    return datos if isinstance(datos, list) else []


def scrape() -> list[PuntoRecoleccion]:
    print(f"[EcoCómputo] Consultando API desde {len(CENTROS)} centros urbanos...")

    vistos: dict[str, dict] = {}
    for ciudad, lat, lng in CENTROS:
        try:
            datos = _consultar(lat, lng)
        except requests.RequestException as e:
            print(f"[EcoCómputo] Error consultando desde {ciudad}: {e}")
            continue
        for item in datos:
            clave = item.get("id") or f"{item.get('store')}|{item.get('address')}"
            vistos[clave] = item

    puntos: list[PuntoRecoleccion] = []
    for item in vistos.values():
        nombre = item.get("store", "").strip()
        direccion = " ".join(filter(None, [
            item.get("address", "").strip(),
            item.get("address2", "").strip(),
        ]))
        ciudad = item.get("city", "").strip()

        if not nombre:
            continue

        try:
            lat = float(item["lat"]) if item.get("lat") else None
            lng = float(item["lng"]) if item.get("lng") else None
        except (ValueError, TypeError):
            lat, lng = None, None

        puntos.append(PuntoRecoleccion(
            sistema=SISTEMA,
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            tipos_raee=TIPOS_RAEE,
            horario=_limpiar_horario(item.get("hours")),
            lat=lat,
            lng=lng,
            fuente_url="https://ecocomputo.com/puntos-de-recoleccion/",
        ))

    print(f"[EcoCómputo] {len(puntos)} puntos únicos extraídos")
    return puntos
