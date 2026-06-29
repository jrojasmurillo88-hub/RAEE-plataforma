import json
from datetime import datetime, timedelta, timezone
from playwright.sync_api import sync_playwright

BASE = "http://localhost:3000"
OUT = r"C:\Users\jroja\raee-colombia-producto\scraper\output"

resultados = {"console_errors": [], "steps": []}


def log_console(msg):
    if msg.type == "error":
        resultados["console_errors"].append(msg.text)


with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(locale="es-CO")
    page = context.new_page()
    page.on("console", log_console)

    # Forzar que la llamada a /entregas falle (simula API caída/dormida)
    page.route("**/entregas", lambda route: route.abort())

    page.goto(BASE + "/", wait_until="networkidle")
    page.evaluate(
        """
        window.localStorage.setItem('raee_onboarding_v1', JSON.stringify(
          {ciudad:'Bogotá', intencion:'explorando', completadoEn: new Date().toISOString()}));
        const hace25h = new Date(Date.now() - 25*60*60*1000).toISOString();
        window.localStorage.setItem('raee_checkins_pendientes_v1', JSON.stringify([
          {puntoId: 6, nombrePunto: 'Doria -Productos Alimenticios Doria S.A.S', sistema: 'EcoCómputo', creadoEn: hace25h, resuelto: false}
        ]));
        """
    )
    page.reload(wait_until="networkidle")
    page.wait_for_timeout(700)

    page.click("button:has-text('Sí, lo entregué')")
    page.wait_for_timeout(2000)
    page.screenshot(path=f"{OUT}/checkin_error_1.png", full_page=True)

    error_visible = page.locator("text=No pudimos conectar con el servidor").count() > 0
    falso_exito = page.locator("text=Entregaste aproximadamente").count() > 0
    boton_reintentar = page.locator("button:has-text('Reintentar')").count() > 0
    resultados["steps"].append({"paso": "muestra_error_real", "ok": error_visible})
    resultados["steps"].append({"paso": "NO_muestra_falso_exito", "ok": not falso_exito})
    resultados["steps"].append({"paso": "boton_reintentar_visible", "ok": boton_reintentar})

    # Verificar que el check-in sigue pendiente (no se marcó resuelto falsamente)
    pendientes = page.evaluate(
        "JSON.parse(window.localStorage.getItem('raee_checkins_pendientes_v1'))"
    )
    resultados["steps"].append({"paso": "checkin_sigue_pendiente", "valor": pendientes})

    context.close()
    browser.close()

print(json.dumps(resultados, ensure_ascii=False, indent=2))
