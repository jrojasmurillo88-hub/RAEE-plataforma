import json
from playwright.sync_api import sync_playwright

BASE = "https://raee-plataforma.vercel.app"
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

    page.goto(BASE + "/", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUT}/prod_1_inicio.png", full_page=True)

    # Si aparece onboarding, lo saltamos rápido eligiendo "explorando"
    if page.locator("text=¿Tienes un dispositivo").count() > 0:
        page.click("button:has-text('Solo estoy explorando')")
        page.wait_for_timeout(300)
        page.click("button:has-text('Continuar')")
        page.wait_for_timeout(500)

    page.screenshot(path=f"{OUT}/prod_2_selector.png", full_page=True)
    selector_visible = page.locator("text=Qué quieres desechar").count() > 0
    resultados["steps"].append({"paso": "selector_visible", "ok": selector_visible})

    page.click("button:has-text('Buscar puntos cercanos')")
    page.wait_for_url("**/mapa*", timeout=15000)
    page.wait_for_timeout(5000)
    page.screenshot(path=f"{OUT}/prod_3_mapa.png", full_page=True)

    tarjetas = page.locator("text=min caminando").count()
    resultados["steps"].append({"paso": "tarjetas_con_resultados", "cantidad": tarjetas})

    context.close()
    browser.close()

print(json.dumps(resultados, ensure_ascii=False, indent=2))
