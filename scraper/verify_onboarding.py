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

    # --- Caso 1: sin permisos de geolocalización otorgados -> debe pedir ciudad ---
    context = browser.new_context(locale="es-CO")
    page = context.new_page()
    page.on("console", log_console)
    page.goto(BASE + "/", wait_until="networkidle")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUT}/onboard_1_ciudad.png", full_page=True)
    tiene_selector_ciudad = page.locator("text=¿En qué ciudad estás?").count() > 0
    resultados["steps"].append({"paso": "ciudad_visible", "ok": tiene_selector_ciudad})

    page.select_option("select", "Bogotá")
    page.click("button:has-text('Continuar')")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUT}/onboard_2_intencion.png", full_page=True)
    tiene_intencion = page.locator("text=¿Tenés un dispositivo que cambiar próximamente?").count() > 0
    resultados["steps"].append({"paso": "intencion_visible", "ok": tiene_intencion})

    page.click("button:has-text('Sí, en los próximos días')")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{OUT}/onboard_3_confirmacion.png", full_page=True)
    nota_honesta = page.locator("text=Pronto vamos a poder recordártelo").count() > 0
    resultados["steps"].append({"paso": "nota_honesta_visible", "ok": nota_honesta})

    page.click("button:has-text('Continuar')")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUT}/onboard_4_inicio.png", full_page=True)
    selector_objetos = page.locator("text=¿Qué querés desechar?").count() > 0
    resultados["steps"].append({"paso": "selector_objetos_tras_onboarding", "ok": selector_objetos})

    almacenado = page.evaluate("window.localStorage.getItem('raee_onboarding_v1')")
    resultados["steps"].append({"paso": "localStorage_guardado", "valor": almacenado})

    # --- Recargar: el onboarding no debe repetirse ---
    page.reload(wait_until="networkidle")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUT}/onboard_5_recarga.png", full_page=True)
    no_repite = page.locator("text=¿Qué querés desechar?").count() > 0
    resultados["steps"].append({"paso": "no_se_repite_tras_reload", "ok": no_repite})

    context.close()

    # --- Caso 2: con geolocalización ya otorgada -> debe saltar paso de ciudad ---
    context2 = browser.new_context(
        permissions=["geolocation"],
        geolocation={"latitude": 4.6486, "longitude": -74.2479},
        locale="es-CO",
    )
    page2 = context2.new_page()
    page2.on("console", log_console)
    page2.goto(BASE + "/", wait_until="networkidle")
    page2.wait_for_timeout(800)
    page2.screenshot(path=f"{OUT}/onboard_6_gps_salta_ciudad.png", full_page=True)
    salto_ciudad = page2.locator("text=¿Tenés un dispositivo que cambiar próximamente?").count() > 0
    no_pidio_ciudad = page2.locator("text=¿En qué ciudad estás?").count() == 0
    resultados["steps"].append({
        "paso": "gps_activo_salta_paso_ciudad",
        "fue_directo_a_intencion": salto_ciudad,
        "no_mostro_ciudad": no_pidio_ciudad,
    })

    context2.close()
    browser.close()

print(json.dumps(resultados, ensure_ascii=False, indent=2))
