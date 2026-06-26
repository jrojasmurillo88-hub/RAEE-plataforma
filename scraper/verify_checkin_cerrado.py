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
    page.screenshot(path=f"{OUT}/checkin_cerrado_1.png", full_page=True)

    page.click("button:has-text('El punto estaba cerrado')")
    page.wait_for_timeout(2000)
    page.screenshot(path=f"{OUT}/checkin_cerrado_2.png", full_page=True)
    gracias_visible = page.locator("text=Gracias por avisarnos").count() > 0
    resultados["steps"].append({"paso": "mensaje_gracias_visible", "ok": gracias_visible})

    context.close()
    browser.close()

print(json.dumps(resultados, ensure_ascii=False, indent=2))
