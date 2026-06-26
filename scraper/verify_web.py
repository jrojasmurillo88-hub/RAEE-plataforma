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

    # Paso 1: inicio
    page.goto(BASE + "/", wait_until="networkidle")
    page.screenshot(path=f"{OUT}/verif_1_inicio.png", full_page=True)
    botones = page.locator("a:has-text('Celular')").count()
    resultados["steps"].append({"paso": "inicio", "boton_celular_visible": botones > 0})

    # Paso 2: click en Celular -> mapa
    page.click("a:has-text('Celular')")
    page.wait_for_url("**/mapa*")
    page.wait_for_timeout(4000)  # esperar geolocalización + fetch
    page.screenshot(path=f"{OUT}/verif_2_mapa.png", full_page=True)
    tarjetas = page.locator("text=min caminando").count()
    resultados["steps"].append({"paso": "mapa", "tarjetas_con_tiempo": tarjetas})

    # Paso 3: click primer punto -> detalle
    primer_link = page.locator("a[href^='/punto/']").first
    href = primer_link.get_attribute("href")
    primer_link.click()
    page.wait_for_url("**/punto/**")
    page.wait_for_timeout(1500)
    page.screenshot(path=f"{OUT}/verif_3_detalle.png", full_page=True)
    cta = page.locator("a:has-text('Cómo llegar')").count()
    reportar = page.locator("a:has-text('Reportar dato incorrecto')").count()
    resultados["steps"].append({
        "paso": "detalle",
        "url": href,
        "cta_como_llegar": cta,
        "link_reportar": reportar,
    })

    # Paso 4: click reportar -> formulario -> enviar
    page.click("a:has-text('Reportar dato incorrecto')")
    page.wait_for_url("**/reportar/**")
    page.wait_for_timeout(1000)
    page.screenshot(path=f"{OUT}/verif_4_reportar.png", full_page=True)
    page.click("label:has-text('El punto está cerrado')")
    page.fill("textarea", "Prueba automatizada de verificación")
    page.click("button:has-text('Enviar reporte')")
    page.wait_for_timeout(1500)
    page.screenshot(path=f"{OUT}/verif_5_confirmacion.png", full_page=True)
    confirmacion = page.locator("text=Gracias por avisarnos").count()
    resultados["steps"].append({"paso": "reportar", "confirmacion_visible": confirmacion > 0})

    browser.close()

print(json.dumps(resultados, ensure_ascii=False, indent=2))
