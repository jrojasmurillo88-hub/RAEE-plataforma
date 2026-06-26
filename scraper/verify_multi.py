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
        geolocation={"latitude": 4.6486, "longitude": -74.2479},  # Bogotá, Fontibón
        locale="es-CO",
    )
    page = context.new_page()
    page.on("console", log_console)

    # Saltar onboarding manualmente vía localStorage
    page.goto(BASE + "/", wait_until="networkidle")
    page.evaluate(
        "window.localStorage.setItem('raee_onboarding_v1', JSON.stringify("
        "{ciudad:'Bogotá', intencion:'explorando', completadoEn: new Date().toISOString()}))"
    )
    page.reload(wait_until="networkidle")
    page.wait_for_timeout(300)

    # Paso 1: seleccionar Celular (default) + Computador + Nevera
    page.click("button:has-text('Computador')")
    page.click("button:has-text('Nevera')")
    page.screenshot(path=f"{OUT}/multi_1_seleccion.png", full_page=True)

    boton_texto = page.locator("button:has-text('Buscar puntos para')").inner_text()
    resultados["steps"].append({"paso": "seleccion_multiple", "texto_boton": boton_texto})

    page.click("button:has-text('Buscar puntos para')")
    page.wait_for_url("**/mapa*")
    page.wait_for_timeout(5000)
    page.screenshot(path=f"{OUT}/multi_2_mapa.png", full_page=True)

    secciones = page.locator("h2:has-text('Celular'), h2:has-text('Computador'), h2:has-text('Nevera')").count()
    tarjeta_contacto = page.locator("text=Llama a la línea").count()
    boton_ruta = page.locator("a:has-text('Planear ruta'), a:has-text('Cómo llegar')").count()
    resultados["steps"].append({
        "paso": "mapa_multi",
        "secciones_encontradas": secciones,
        "tarjeta_contacto_visible": tarjeta_contacto > 0,
        "boton_ruta_visible": boton_ruta > 0,
    })

    href_ruta = None
    if boton_ruta > 0:
        href_ruta = page.locator("a:has-text('Planear ruta'), a:has-text('Cómo llegar')").first.get_attribute("href")
    resultados["steps"].append({"paso": "url_ruta", "href": href_ruta})

    context.close()
    browser.close()

print(json.dumps(resultados, ensure_ascii=False, indent=2))
