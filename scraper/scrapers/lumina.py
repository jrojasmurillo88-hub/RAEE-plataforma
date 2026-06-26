"""
Scraper para Lúmina (luminarias y equipos de iluminación).
Usa el plugin Google Maps Elementor (gme_get_excel_data):
  POST /wp-admin/admin-ajax.php  action=gme_get_excel_data

Respuesta: { "success": true, "data": { "locations": [...] } }
Cada location: { departamento, ciudad, nombre, direccion, corriente, lat, lng }
"""

import requests
from models import PuntoRecoleccion

API_URL  = "https://lumina.com.co/wp-admin/admin-ajax.php"
SISTEMA  = "Lúmina"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://lumina.com.co/",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
}


def scrape() -> list[PuntoRecoleccion]:
    print("[Lúmina] Consultando API de puntos...")

    resp = requests.post(
        API_URL,
        data={"action": "gme_get_excel_data"},
        headers=HEADERS,
        timeout=20,
    )
    resp.raise_for_status()

    payload = resp.json()
    if not payload.get("success"):
        print(f"[Lúmina] Respuesta no exitosa: {str(payload)[:200]}")
        return []

    locations = payload.get("data", {}).get("locations", [])
    if not isinstance(locations, list):
        print(f"[Lúmina] 'locations' no es una lista: {type(locations)}")
        return []

    puntos: list[PuntoRecoleccion] = []
    for item in locations:
        nombre = (item.get("nombre") or "").strip()
        if not nombre:
            continue

        corriente = (item.get("corriente") or "").strip()
        tipos = [corriente] if corriente else []

        try:
            lat = float(item["lat"]) if item.get("lat") not in (None, "", 0) else None
            lng = float(item["lng"]) if item.get("lng") not in (None, "", 0) else None
        except (ValueError, TypeError):
            lat, lng = None, None

        puntos.append(PuntoRecoleccion(
            sistema=SISTEMA,
            nombre=nombre,
            direccion=(item.get("direccion") or "").strip() or None,
            ciudad=(item.get("ciudad") or "").strip() or None,
            tipos_raee=tipos,
            lat=lat,
            lng=lng,
            fuente_url="https://lumina.com.co/",
        ))

    print(f"[Lúmina] {len(puntos)} puntos extraídos")
    return puntos
