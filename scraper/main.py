"""
Runner principal. Corre todos los scrapers activos y guarda los resultados en output/.

Uso:
  python main.py                          # corre todos los scrapers
  python main.py lito                     # corre solo el de Lito
  python main.py lito --geo               # scrape + geocodifica con Nominatim
  python main.py lito --geo --gmaps KEY   # scrape + geocodifica con Google Maps primero
  python main.py todos --geo              # scrape todos + geocodifica los que no tengan coords
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from scrapers import lito, ecocomputo, pilas, lumina, redverde

output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)

SCRAPERS = {
    "lito":       lito.scrape,
    "ecocomputo": ecocomputo.scrape,
    "pilas":      pilas.scrape,
    "lumina":     lumina.scrape,
    "redverde":   redverde.scrape,
}


def correr(nombre: str, geocodificar: bool = False, gmaps_key: str | None = None):
    print(f"\n{'=' * 50}")
    print(f"Corriendo scraper: {nombre}")
    print(f"{'=' * 50}")
    try:
        puntos = SCRAPERS[nombre]()
        if not puntos:
            print(f"[{nombre}] Sin puntos — revisar selectores o conectividad.")
            return

        datos = [p.to_dict() for p in puntos]

        if geocodificar:
            from geocoder import geocodificar_puntos
            datos = geocodificar_puntos(datos, gmaps_key=gmaps_key)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sufijo = "_geo" if geocodificar else ""
        ruta = output_dir / f"{nombre}{sufijo}_{timestamp}.json"
        ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[{nombre}] Guardado: {ruta} ({len(datos)} puntos)")

    except Exception as e:
        print(f"[{nombre}] ERROR: {e}")
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sistema", nargs="?", default="todos",
                        help=f"Sistema a scrapear: {', '.join(SCRAPERS)} | todos")
    parser.add_argument("--geo", action="store_true",
                        help="Geocodificar puntos sin coordenadas después del scraping")
    parser.add_argument("--gmaps", metavar="API_KEY",
                        help="API key de Google Maps para geocodificación (opcional)")
    args = parser.parse_args()

    seleccion = args.sistema.lower()

    if seleccion == "todos":
        for nombre in SCRAPERS:
            correr(nombre, geocodificar=args.geo, gmaps_key=args.gmaps)
    elif seleccion in SCRAPERS:
        correr(seleccion, geocodificar=args.geo, gmaps_key=args.gmaps)
    else:
        print(f"Sistema desconocido: {seleccion}")
        print(f"Opciones: {', '.join(SCRAPERS)} | todos")
        sys.exit(1)


if __name__ == "__main__":
    main()
