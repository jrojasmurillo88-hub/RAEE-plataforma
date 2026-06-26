"""
Carga los archivos JSON del scraper en Supabase vía REST API (HTTP).

Requisitos:
  pip install requests  (ya instalado)

Configuración: archivo db/.env con:
  SUPABASE_URL=https://[ref].supabase.co
  SUPABASE_SERVICE_KEY=[service_role_key]

Uso:
  python loader.py                    # carga el archivo más reciente de cada sistema
  python loader.py --archivo path.json
"""

import os
import sys
import json
import argparse
from pathlib import Path

import requests

BATCH_SIZE = 500


# ── Configuración ─────────────────────────────────────────────────────────────

def _leer_env() -> tuple[str, str]:
    env_path = Path(__file__).parent / ".env"
    config = {}
    if env_path.exists():
        for linea in env_path.read_text(encoding="utf-8").splitlines():
            if "=" in linea and not linea.startswith("#"):
                k, v = linea.split("=", 1)
                config[k.strip()] = v.strip()

    url = os.environ.get("SUPABASE_URL") or config.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_SERVICE_KEY") or config.get("SUPABASE_SERVICE_KEY", "")

    if not url or not key:
        print("ERROR: Falta SUPABASE_URL o SUPABASE_SERVICE_KEY en db/.env")
        sys.exit(1)

    return url.rstrip("/"), key


def _headers(key: str) -> dict:
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=ignore-duplicates,return=minimal",
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_sistemas(base_url: str, key: str) -> dict[str, int]:
    resp = requests.get(
        f"{base_url}/rest/v1/sistemas?select=id,nombre",
        headers=_headers(key),
        timeout=10,
    )
    resp.raise_for_status()
    return {s["nombre"]: s["id"] for s in resp.json()}


def _seleccionar_archivos(directorio: Path) -> list[Path]:
    sistemas = ["lito", "ecocomputo", "pilas", "lumina", "redverde"]
    seleccionados = []
    for sistema in sistemas:
        geo = sorted(directorio.glob(f"{sistema}_geo_*.json"), reverse=True)
        sin_geo = [
            f for f in sorted(directorio.glob(f"{sistema}_*.json"), reverse=True)
            if "test" not in f.name and "_geo_" not in f.name
        ]
        if geo:
            seleccionados.append(geo[0])
        elif sin_geo:
            seleccionados.append(sin_geo[0])
    return seleccionados


# ── Carga ─────────────────────────────────────────────────────────────────────

def cargar_archivo(ruta: Path, base_url: str, key: str, sistemas_map: dict) -> dict:
    puntos = json.loads(ruta.read_text(encoding="utf-8-sig"))
    stats = {"insertados": 0, "sin_sistema": 0, "errores": 0, "total": len(puntos)}

    rows = []
    for p in puntos:
        sistema_id = sistemas_map.get(p.get("sistema", ""))
        if not sistema_id:
            stats["sin_sistema"] += 1
            continue

        lat = p.get("lat")
        lng = p.get("lng")

        row = {
            "sistema_id":          sistema_id,
            "nombre":              p.get("nombre", ""),
            "direccion_texto":     p.get("direccion") or None,
            "ciudad":              p.get("ciudad") or None,
            "horario":             p.get("horario"),
            "fuente_url":          p.get("fuente_url"),
            "confianza_coords":    1 if lat is not None else 0,
            "ultima_verificacion": p.get("ultima_verificacion"),
        }

        # PostgREST requiere que todos los objetos del batch tengan las mismas keys
        row["coordenadas"] = f"SRID=4326;POINT({lng} {lat})" if lat is not None and lng is not None else None

        rows.append(row)

    # Insertar en batches
    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        resp = requests.post(
            f"{base_url}/rest/v1/puntos?on_conflict=sistema_id,nombre,ciudad",
            headers=_headers(key),
            json=batch,
            timeout=30,
        )
        if resp.ok:
            stats["insertados"] += len(batch)
            print(f"  Batch {i // BATCH_SIZE + 1}: {len(batch)} puntos OK")
        else:
            stats["errores"] += len(batch)
            print(f"  Batch {i // BATCH_SIZE + 1}: ERROR {resp.status_code} — {resp.text[:200]}")

    return stats


def cargar_todos(archivos: list[Path]):
    base_url, key = _leer_env()
    print(f"Conectando a {base_url}...")

    sistemas_map = _get_sistemas(base_url, key)
    print(f"Sistemas en BD: {list(sistemas_map.keys())}\n")

    for ruta in archivos:
        print(f"{'=' * 50}")
        print(f"Cargando: {ruta.name}")
        print(f"{'=' * 50}")
        stats = cargar_archivo(ruta, base_url, key, sistemas_map)
        print(f"  Total en archivo : {stats['total']}")
        print(f"  Insertados       : {stats['insertados']}")
        print(f"  Sin sistema BD   : {stats['sin_sistema']}")
        print(f"  Errores          : {stats['errores']}\n")

    print("Carga completada.")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--archivo", metavar="PATH")
    group.add_argument("--directorio", metavar="PATH")
    args = parser.parse_args()

    if args.archivo:
        archivos = [Path(args.archivo)]
    else:
        directorio = Path(args.directorio) if args.directorio else Path(__file__).parent.parent / "scraper" / "output"
        archivos = _seleccionar_archivos(directorio)

    if not archivos:
        print("No se encontraron archivos JSON.")
        sys.exit(1)

    print(f"Archivos a cargar ({len(archivos)}):")
    for a in archivos:
        print(f"  {a.name}")
    print()

    cargar_todos(archivos)


if __name__ == "__main__":
    main()
