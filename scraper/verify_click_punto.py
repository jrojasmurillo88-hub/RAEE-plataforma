import json
from playwright.sync_api import sync_playwright

BASE = "http://localhost:3000"
OUT = r"C:\Users\jroja\raee-colombia-producto\scraper\output"

resultados = {"console_errors": [], "steps": []}


def log_console(msg):
    if msg.type == "error":
        resultados["console_errors"].append(msg.text)


with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(
        permissions=["geolocation"],
        geolocation={"latitude": 4.6486, "longitude": -74.2479},
        locale="es-CO",
    )
    page = context.new_page()
    page.on("console", log_console)

    page.goto(BASE + "/", wait_until="networkidle")
    page.evaluate(
        "window.localStorage.setItem('raee_onboarding_v1', JSON.stringify("
        "{ciudad:'Bogotá', intencion:'explorando', completadoEn: new Date().toISOString()}))"
    )
    page.reload(wait_until="networkidle")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{OUT}/idioma_1_inicio.png", full_page=True)

    page.goto(BASE + "/mapa?tipos=Celular", wait_until="networkidle")
    page.wait_for_timeout(4000)

    # Click en un marcador del mapa
    marcador = page.locator(".leaflet-marker-icon").nth(1)  # 0 = usuario, 1 = primer punto
    marcador.click()
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUT}/click_1_marcador.png", full_page=True)

    popup_visible = page.locator(".leaflet-popup").count() > 0
    resultados["steps"].append({"paso": "popup_visible_tras_click_marcador", "ok": popup_visible})
    if popup_visible:
        texto_popup = page.locator(".leaflet-popup-content").inner_text()
        resultados["steps"].append({"paso": "texto_popup", "valor": texto_popup})

    context.close()
    browser.close()

print(json.dumps(resultados, ensure_ascii=False, indent=2))
