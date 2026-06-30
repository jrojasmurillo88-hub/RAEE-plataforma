import json
from playwright.sync_api import sync_playwright

BASE = "https://raee-plataforma.vercel.app"
OUT = r"C:\Users\jroja\raee-colombia-producto\scraper\output"

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(
        permissions=["geolocation"],
        geolocation={"latitude": 4.684, "longitude": -74.043},  # Calle 103 con Cra 19, Bogota
        locale="es-CO",
    )
    page = context.new_page()

    page.goto(BASE + "/", wait_until="networkidle")
    page.evaluate(
        "window.localStorage.setItem('raee_onboarding_v1', JSON.stringify("
        "{ciudad:'Bogotá', intencion:'explorando', completadoEn: new Date().toISOString()}))"
    )
    page.reload(wait_until="networkidle")
    page.wait_for_timeout(500)

    page.goto(BASE + "/mapa?tipos=Pila", wait_until="networkidle")
    page.wait_for_timeout(6000)
    page.screenshot(path=f"{OUT}/verif_colsubsidio_1.png", full_page=True)

    # Revisar el texto completo de la seccion de tarjetas (lista)
    texto_lista = page.locator("section").first.inner_text()
    print("=== Lista visible (tarjetas) ===")
    for nombre in ["COLSUBSIDIO", "MABE", "GAES"]:
        print(f"{nombre} en lista: {nombre in texto_lista.upper()}")

    # Revisar los popups de TODOS los marcadores del mapa (no solo los primeros 5)
    marcadores = page.locator(".leaflet-marker-icon").all()
    print(f"\nTotal marcadores renderizados en el mapa: {len(marcadores)}")

    nombres_en_mapa = []
    for m in marcadores:
        m.click(force=True)
        page.wait_for_timeout(150)
        popup = page.locator(".leaflet-popup-content")
        if popup.count() > 0:
            nombres_en_mapa.append(popup.first.inner_text())

    print("\n=== Nombres encontrados en popups del mapa ===")
    for n in nombres_en_mapa:
        print(" -", n.replace("\n", " | "))

    browser.close()
