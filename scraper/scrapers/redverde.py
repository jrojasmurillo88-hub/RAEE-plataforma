"""
Scraper para Red Verde (línea blanca: neveras, lavadoras, microondas, aires
acondicionados, electrodomésticos en general).
URL: https://www.redverde.co/localiza-contenedor-mas-cercano/
Tipo: contenido estático — requests + BeautifulSoup.

Cada punto está en un <details class="e-n-accordion-item"> con un <p> de
campos etiquetados:
  <strong>TIPO DE CONTENEDOR</strong><br>...
  <strong>NOMBRE DE LA ENTIDAD</strong><br>...
  <strong>DIRECCIÓN</strong><br>...
  <strong>DEPARTAMENTO</strong><br>...
  <strong>MUNICIPIO</strong><br>...

No incluye coordenadas — requiere geocodificación posterior.
"""

import requests
from bs4 import BeautifulSoup
from models import PuntoRecoleccion

URL = "https://www.redverde.co/localiza-contenedor-mas-cercano/"
SISTEMA = "Red Verde"
TIPOS_RAEE = ["Nevera", "Lavadora", "Microondas", "Aire acondicionado", "Electrodoméstico"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
}


def _parsear_campos(parrafo) -> dict[str, str]:
    campos: dict[str, str] = {}
    etiqueta_actual = None
    buffer: list[str] = []

    for nodo in parrafo.children:
        nombre_nodo = getattr(nodo, "name", None)
        if nombre_nodo == "strong":
            if etiqueta_actual:
                campos[etiqueta_actual] = " ".join(buffer).strip()
            etiqueta_actual = nodo.get_text(strip=True).upper()
            buffer = []
        elif nombre_nodo == "br":
            continue
        else:
            texto = nodo.get_text(strip=True) if hasattr(nodo, "get_text") else str(nodo).strip()
            if texto:
                buffer.append(texto)

    if etiqueta_actual:
        campos[etiqueta_actual] = " ".join(buffer).strip()

    return campos


def scrape() -> list[PuntoRecoleccion]:
    print(f"[Red Verde] Descargando {URL}")
    with requests.Session() as sesion:
        resp = sesion.get(URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    resp.encoding = "utf-8"

    soup = BeautifulSoup(resp.text, "html.parser")
    items = soup.select("details.e-n-accordion-item")

    if not items:
        print("[Red Verde] AVISO: no se encontraron contenedores — el HTML puede haber cambiado.")
        print("  Corré: python inspect_page.py https://www.redverde.co/localiza-contenedor-mas-cercano/")
        return []

    puntos: list[PuntoRecoleccion] = []
    for item in items:
        parrafo = item.find("p")
        if not parrafo:
            continue

        campos = _parsear_campos(parrafo)
        nombre = campos.get("NOMBRE DE LA ENTIDAD", "").strip()
        direccion = campos.get("DIRECCIÓN", "").strip()
        ciudad = campos.get("MUNICIPIO", "").strip()
        departamento = campos.get("DEPARTAMENTO", "").strip()

        if not nombre:
            continue

        direccion_completa = ", ".join(filter(None, [direccion, ciudad, departamento]))

        puntos.append(PuntoRecoleccion(
            sistema=SISTEMA,
            nombre=nombre,
            direccion=direccion_completa or direccion,
            ciudad=ciudad,
            tipos_raee=TIPOS_RAEE,
            fuente_url=URL,
        ))

    print(f"[Red Verde] {len(puntos)} puntos extraídos")
    return puntos
