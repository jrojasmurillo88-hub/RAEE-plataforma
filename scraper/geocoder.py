"""
Módulo de geocodificación para puntos sin coordenadas.

Proveedores (en orden de prioridad):
  1. Nominatim / OpenStreetMap — gratuito, sin API key, límite 1 req/seg
  2. Google Maps Geocoding API — mayor precisión, requiere API key

Uso standalone:
  python geocoder.py output/lito_*.json                   # geocodifica con Nominatim
  python geocoder.py output/lito_*.json --gmaps TU_KEY    # usa Google Maps

Uso desde código:
  from geocoder import geocodificar_puntos
  puntos_enriquecidos = geocodificar_puntos(puntos)

El módulo guarda un caché en output/geocode_cache.json para no repetir
llamadas entre ejecuciones. Si una dirección ya fue geocodificada, usa
el resultado guardado sin hacer una nueva petición.
"""

import sys
import time
import json
import argparse
from pathlib import Path

import requests

CACHE_PATH = Path(__file__).parent / "output" / "geocode_cache.json"

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
GMAPS_URL = "https://maps.googleapis.com/maps/api/geocode/json"

HEADERS_NOMINATIM = {
    "User-Agent": "raee-colombia-app/1.0 (jrojasmurillo88@gmail.com)"
}


# ── Caché ─────────────────────────────────────────────────────────────────────

def _cargar_cache() -> dict:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def _guardar_cache(cache: dict):
    CACHE_PATH.parent.mkdir(exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def _cache_key(direccion: str, ciudad: str) -> str:
    return f"{ciudad.lower().strip()}|{direccion.lower().strip()}"


# ── Proveedores ───────────────────────────────────────────────────────────────

def _nominatim(direccion: str, ciudad: str) -> tuple[float, float] | None:
    query = f"{direccion}, {ciudad}, Colombia"
    params = {
        "q": query,
        "format": "json",
        "limit": 1,
        "countrycodes": "co",
    }
    try:
        resp = requests.get(NOMINATIM_URL, params=params, headers=HEADERS_NOMINATIM, timeout=10)
        resp.raise_for_status()
        resultados = resp.json()
        if resultados:
            return float(resultados[0]["lat"]), float(resultados[0]["lon"])
    except Exception as e:
        print(f"    [Nominatim] Error: {e}")
    return None


def _gmaps(direccion: str, ciudad: str, api_key: str) -> tuple[float, float] | None:
    query = f"{direccion}, {ciudad}, Colombia"
    params = {"address": query, "key": api_key, "region": "co"}
    try:
        resp = requests.get(GMAPS_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "OK" and data.get("results"):
            loc = data["results"][0]["geometry"]["location"]
            return loc["lat"], loc["lng"]
        if data.get("status") not in ("OK", "ZERO_RESULTS"):
            print(f"    [GMaps] Status inesperado: {data.get('status')} — {data.get('error_message', '')}")
    except Exception as e:
        print(f"    [GMaps] Error: {e}")
    return None


# ── Función principal ─────────────────────────────────────────────────────────

def geocodificar_puntos(
    puntos: list[dict],
    gmaps_key: str | None = None,
    delay: float = 1.1,
) -> list[dict]:
    """
    Recibe una lista de dicts (formato to_dict() de PuntoRecoleccion).
    Devuelve la misma lista con lat/lng rellenados donde faltaban.

    delay: segundos entre llamadas a Nominatim (mínimo 1.0 por los ToS).
    """
    cache = _cargar_cache()
    sin_coords = [p for p in puntos if p.get("lat") is None or p.get("lng") is None]
    con_coords = [p for p in puntos if p.get("lat") is not None and p.get("lng") is not None]

    print(f"[Geocoder] {len(con_coords)} puntos ya tienen coordenadas.")
    print(f"[Geocoder] {len(sin_coords)} puntos a geocodificar.")

    nuevas_llamadas = 0
    exitos = 0
    fallos = 0

    for i, punto in enumerate(sin_coords):
        direccion = punto.get("direccion", "").strip()
        ciudad = punto.get("ciudad", "").strip()

        if not direccion and not ciudad:
            fallos += 1
            continue

        key = _cache_key(direccion, ciudad)

        # Usar caché si existe
        if key in cache:
            resultado = cache[key]
            if resultado:
                punto["lat"], punto["lng"] = resultado
                exitos += 1
            continue

        # Llamada real al proveedor
        nuevas_llamadas += 1
        resultado = None

        if gmaps_key:
            resultado = _gmaps(direccion, ciudad, gmaps_key)

        if resultado is None:
            resultado = _nominatim(direccion, ciudad)
            if nuevas_llamadas > 1:
                time.sleep(delay)  # respetar rate limit de Nominatim

        if resultado:
            punto["lat"], punto["lng"] = resultado
            cache[key] = list(resultado)
            exitos += 1
            print(f"  [{i+1}/{len(sin_coords)}] OK  {punto.get('nombre', '')} -> {resultado[0]:.5f}, {resultado[1]:.5f}")
        else:
            cache[key] = None  # guardar fallo para no reintentar
            fallos += 1
            print(f"  [{i+1}/{len(sin_coords)}] --- {punto.get('nombre', '')} ({ciudad}, {direccion[:50]})")

        # Guardar caché periódicamente (cada 20 llamadas)
        if nuevas_llamadas % 20 == 0:
            _guardar_cache(cache)

    _guardar_cache(cache)

    total = len(puntos)
    print(f"\n[Geocoder] Resultado: {exitos + len(con_coords)}/{total} con coordenadas "
          f"({exitos} nuevas, {fallos} sin resultado, {nuevas_llamadas} llamadas a API)")

    return con_coords + sin_coords


# ── CLI standalone ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Geocodifica puntos sin coordenadas en archivos JSON.")
    parser.add_argument("archivos", nargs="+", help="Archivos JSON de puntos a geocodificar")
    parser.add_argument("--gmaps", metavar="API_KEY", help="API key de Google Maps (opcional)")
    args = parser.parse_args()

    for patron in args.archivos:
        # Soportar globs desde línea de comandos
        rutas = sorted(Path(".").glob(patron)) if "*" in patron else [Path(patron)]
        for ruta in rutas:
            if not ruta.exists():
                print(f"Archivo no encontrado: {ruta}")
                continue

            print(f"\n{'=' * 50}")
            print(f"Procesando: {ruta.name}")
            print(f"{'=' * 50}")

            puntos = json.loads(ruta.read_text(encoding="utf-8-sig"))
            puntos_enriquecidos = geocodificar_puntos(puntos, gmaps_key=args.gmaps)

            ruta_salida = ruta.with_stem(ruta.stem + "_geo")
            ruta_salida.write_text(
                json.dumps(puntos_enriquecidos, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"Guardado: {ruta_salida}")


if __name__ == "__main__":
    main()
