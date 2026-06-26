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
    context = browser.new_context(
        permissions=["geolocation"],
        geolocation={"latitude": 4.6486, "longitude": -74.2479},
        locale="es-CO",
    )
    page = context.new_page()
    page.on("console", log_console)

    # Saltar onboarding
    page.goto(BASE + "/", wait_until="networkidle")
    page.evaluate(
        "window.localStorage.setItem('raee_onboarding_v1', JSON.stringify("
        "{ciudad:'Bogotá', intencion:'explorando', completadoEn: new Date().toISOString()}))"
    )
    page.reload(wait_until="networkidle")
    page.wait_for_timeout(300)

    # Ir directo al mapa de Celular
    page.goto(BASE + "/mapa?tipos=Celular", wait_until="networkidle")
    page.wait_for_timeout(4000)

    # Click en "Cómo llegar" (single tipo -> botón con ese texto, abre pestaña nueva)
    with context.expect_page() as nueva_pagina_info:
        page.click("a:has-text('Cómo llegar')")
    nueva = nueva_pagina_info.value
    nueva.close()

    pendientes = page.evaluate("window.localStorage.getItem('raee_checkins_pendientes_v1')")
    resultados["steps"].append({"paso": "checkin_registrado", "valor": pendientes})

    # Simular que pasaron 25 horas: reescribir el timestamp directamente
    hace_25h = (datetime.now(timezone.utc) - timedelta(hours=25)).isoformat()
    page.evaluate(
        f"""
        const datos = JSON.parse(window.localStorage.getItem('raee_checkins_pendientes_v1'));
        datos.forEach(c => c.creadoEn = '{hace_25h}');
        window.localStorage.setItem('raee_checkins_pendientes_v1', JSON.stringify(datos));
        """
    )

    # Recargar cualquier página -> debe aparecer el modal de check-in
    page.goto(BASE + "/", wait_until="networkidle")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUT}/checkin_1_pregunta.png", full_page=True)
    pregunta_visible = page.locator("text=¿Pudiste entregar en").count() > 0
    resultados["steps"].append({"paso": "modal_pregunta_visible", "ok": pregunta_visible})

    # Responder "Sí, lo entregué"
    page.click("button:has-text('Sí, lo entregué')")
    page.wait_for_timeout(4000)
    page.screenshot(path=f"{OUT}/checkin_2_impacto.png", full_page=True)
    impacto_visible = page.locator("text=Entregaste aproximadamente").count() > 0
    resultados["steps"].append({"paso": "modal_impacto_visible", "ok": impacto_visible})

    page.click("button:has-text('Cerrar')")
    page.wait_for_timeout(500)
    modal_cerrado = page.locator("text=¿Pudiste entregar en").count() == 0
    resultados["steps"].append({"paso": "modal_cerrado_tras_click", "ok": modal_cerrado})

    context.close()
    browser.close()

print(json.dumps(resultados, ensure_ascii=False, indent=2))
