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
    page.wait_for_timeout(400)
    page.screenshot(path=f"{OUT}/cat_1_inicio.png", full_page=True)

    categorias_esperadas = [
        "Equipos electrónicos", "Electrodomésticos pequeños", "Electrodomésticos grandes",
        "Bombillos", "Pilas", "Baterías de carro",
    ]
    for c in categorias_esperadas:
        resultados["steps"].append({"categoria": c, "visible": page.locator(f"text={c}").count() > 0})

    # Probar el buscador "no sé en qué categoría está"
    page.click("text=¿No sabes en qué categoría está tu objeto?")
    page.fill("input[placeholder*='licuadora']", "licuadora")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{OUT}/cat_2_buscador.png", full_page=True)
    page.click("button:has-text('Licuadora')")
    page.wait_for_timeout(300)
    confirmacion = page.locator("text=ya la").count() > 0
    resultados["steps"].append({"paso": "buscador_confirma_categoria", "ok": confirmacion})
    page.screenshot(path=f"{OUT}/cat_3_buscador_resultado.png", full_page=True)

    # Ahora "Electrodomésticos pequeños" + "Equipos electrónicos" deberían estar ambos marcados
    boton_texto = page.locator("button:has-text('Buscar puntos para')").inner_text()
    resultados["steps"].append({"paso": "boton_multi", "texto": boton_texto})

    page.click("button:has-text('Buscar puntos para')")
    page.wait_for_url("**/mapa*")
    page.wait_for_timeout(5000)
    page.screenshot(path=f"{OUT}/cat_4_mapa_dedup.png", full_page=True)

    # Verificar deduplicación: el encabezado combinado debe existir si comparten puntos
    encabezado_combinado = page.locator("h2:has-text(' + ')").count()
    resultados["steps"].append({"paso": "secciones_combinadas", "cantidad": encabezado_combinado})

    # Probar "Buscar desde otro punto"
    page.click("text=📍 Buscar desde otro punto")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{OUT}/cat_5_modo_reubicar.png", full_page=True)
    aviso_reubicar = page.locator("text=Toca un punto del mapa").count() > 0
    resultados["steps"].append({"paso": "modo_reubicar_visible", "ok": aviso_reubicar})

    mapa_box = page.locator(".leaflet-container").first.bounding_box()
    page.mouse.click(mapa_box["x"] + mapa_box["width"] / 2, mapa_box["y"] + mapa_box["height"] / 2)
    page.wait_for_timeout(5000)
    page.screenshot(path=f"{OUT}/cat_6_tras_reubicar.png", full_page=True)
    modo_cerrado = page.locator("text=Toca un punto del mapa").count() == 0
    resultados["steps"].append({"paso": "modo_reubicar_se_cierra_tras_click", "ok": modo_cerrado})

    context.close()
    browser.close()

print(json.dumps(resultados, ensure_ascii=False, indent=2))
