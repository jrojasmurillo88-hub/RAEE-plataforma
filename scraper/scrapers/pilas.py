"""
Scraper para Pilas con el Ambiente (pilascolombia.com).
Usa dos endpoints públicos:
  GET /api/get_collection_points.php   → puntos de pilas/baterías (~1500)
  GET /api/get_luminaria_points.php    → puntos de luminarias/multirresiduo (~15)
    Nota: en este segundo endpoint las claves "departamento" y "city" están
    invertidas respecto a su nombre (el header de la propia API lo confirma).

Ambas respuestas incluyen lat/lng — no se requiere geocodificación.
"""

import requests
from models import PuntoRecoleccion

API_PUNTOS = "https://www.pilascolombia.com/api/get_collection_points.php"
API_LUMINARIA = "https://www.pilascolombia.com/api/get_luminaria_points.php"
SISTEMA = "Pilas con el Ambiente"
TIPOS_RAEE = ["Pila", "Batería doméstica", "Acumulador"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
    "Referer": "https://www.pilascolombia.com/puntos",
}


def _coord(valor) -> float | None:
    try:
        f = float(valor)
        return f if f != 0 else None
    except (ValueError, TypeError):
        return None


def _scrape_puntos_pila(sesion: requests.Session) -> list[PuntoRecoleccion]:
    resp = sesion.get(API_PUNTOS, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    datos = resp.json()

    if not isinstance(datos, list):
        print(f"[Pilas] Respuesta inesperada: {type(datos)} — {str(datos)[:200]}")
        return []

    puntos: list[PuntoRecoleccion] = []
    for item in datos:
        if item.get("id") == "0" or item.get("city") == "ciu_munic":
            continue

        nombre = " – ".join(filter(None, [
            item.get("name", "").strip(),
            item.get("venue", "").strip(),
        ]))
        ciudad = item.get("city", "").strip()
        direccion = item.get("full_address", "").strip()

        if not nombre or nombre == " – ":
            continue

        puntos.append(PuntoRecoleccion(
            sistema=SISTEMA,
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            tipos_raee=TIPOS_RAEE,
            lat=_coord(item.get("latitude")),
            lng=_coord(item.get("longitude")),
            fuente_url="https://www.pilascolombia.com/puntos",
        ))
    return puntos


def _scrape_puntos_luminaria(sesion: requests.Session) -> list[PuntoRecoleccion]:
    resp = sesion.get(API_LUMINARIA, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    datos = resp.json()

    if not isinstance(datos, list):
        print(f"[Pilas-Luminaria] Respuesta inesperada: {type(datos)} — {str(datos)[:200]}")
        return []

    puntos: list[PuntoRecoleccion] = []
    for item in datos:
        if item.get("id") == "1" or item.get("name") == "RAZON SOCIAL":
            continue  # fila de encabezado

        nombre = " – ".join(filter(None, [
            item.get("name", "").strip(),
            item.get("venue", "").strip(),
        ]))
        # En esta API "departamento" trae la ciudad y "city" trae el departamento
        ciudad = item.get("departamento", "").strip()
        direccion = item.get("full_address", "").strip()
        tipo_contenedor = (item.get("container_type") or "").strip().upper()
        tipo_raee = "Luminaria" if "LUMINARIA" in tipo_contenedor else "Multirresiduo"

        if not nombre or nombre == " – ":
            continue

        puntos.append(PuntoRecoleccion(
            sistema=SISTEMA,
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            tipos_raee=[tipo_raee],
            lat=_coord(item.get("latitude")),
            lng=_coord(item.get("longitude")),
            fuente_url="https://www.pilascolombia.com/puntos",
        ))
    return puntos


def scrape() -> list[PuntoRecoleccion]:
    print("[Pilas] Consultando API de puntos...")
    with requests.Session() as sesion:
        puntos_pila = _scrape_puntos_pila(sesion)
        print(f"[Pilas] {len(puntos_pila)} puntos de pilas/baterías extraídos")

        puntos_luminaria = _scrape_puntos_luminaria(sesion)
        print(f"[Pilas] {len(puntos_luminaria)} puntos de luminaria/multirresiduo extraídos")

    return puntos_pila + puntos_luminaria
