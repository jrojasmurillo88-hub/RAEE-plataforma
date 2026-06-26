"""
Scraper para Puntos Verdes Lito.
URL: https://puntosverdeslito.com/puntos-de-recoleccion/
Tipo: contenido estático — requests + BeautifulSoup.

Estructura real del HTML (Elementor tabs):
  div.elementor-tab-title.elementor-tab-desktop-title[aria-controls="elementor-tab-content-15XX"]
    → texto = nombre de la ciudad
  div#elementor-tab-content-15XX
    → ul > li con formato "Nombre – Dirección"
    → p > strong para separadores de subcategoría (no son puntos)
"""

import requests
from bs4 import BeautifulSoup
from models import PuntoRecoleccion

URL = "https://puntosverdeslito.com/puntos-de-recoleccion/"
SISTEMA = "Puntos Verdes Lito"
TIPOS_RAEE = ["Computador", "Celular", "Tablet", "Electrodoméstico", "Cable", "Periférico"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
}


def _parsear_li(texto: str, ciudad: str) -> PuntoRecoleccion | None:
    texto = texto.strip()
    if not texto:
        return None

    for sep in [" – ", " — ", "–", " - "]:
        if sep in texto:
            partes = texto.split(sep, 1)
            return PuntoRecoleccion(
                sistema=SISTEMA,
                nombre=partes[0].strip(),
                direccion=partes[1].strip(),
                ciudad=ciudad,
                tipos_raee=TIPOS_RAEE,
                fuente_url=URL,
            )

    return PuntoRecoleccion(
        sistema=SISTEMA,
        nombre=texto,
        direccion="",
        ciudad=ciudad,
        tipos_raee=TIPOS_RAEE,
        fuente_url=URL,
    )


def scrape() -> list[PuntoRecoleccion]:
    print(f"[Lito] Descargando {URL}")
    with requests.Session() as sesion:
        resp = sesion.get(URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    resp.encoding = "utf-8"

    soup = BeautifulSoup(resp.text, "html.parser")
    puntos: list[PuntoRecoleccion] = []

    # Cada tab de ciudad tiene un título y un contenido vinculados por aria-controls / id
    titulos = soup.select("div.elementor-tab-title.elementor-tab-desktop-title")

    if not titulos:
        print("[Lito] AVISO: no se encontraron tabs de ciudad — el HTML puede haber cambiado.")
        print("  Corré: python inspect_page.py https://puntosverdeslito.com/puntos-de-recoleccion/")
        return []

    for titulo in titulos:
        ciudad = titulo.get_text(strip=True)
        contenido_id = titulo.get("aria-controls")
        if not contenido_id:
            continue

        contenido_div = soup.find("div", {"id": contenido_id})
        if not contenido_div:
            continue

        print(f"[Lito] Ciudad: {ciudad}")
        items = contenido_div.select("li")
        for item in items:
            texto = item.get_text(strip=True)
            punto = _parsear_li(texto, ciudad)
            if punto:
                puntos.append(punto)

    print(f"[Lito] {len(puntos)} puntos extraídos")
    return puntos
