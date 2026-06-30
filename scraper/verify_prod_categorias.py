from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://raee-plataforma.vercel.app/", wait_until="networkidle")
    page.evaluate(
        "window.localStorage.setItem('raee_onboarding_v1', JSON.stringify("
        "{ciudad:'Bogotá', intencion:'explorando', completadoEn: new Date().toISOString()}))"
    )
    page.reload(wait_until="networkidle")
    page.wait_for_timeout(800)
    print("Equipos electronicos visible:", page.locator("text=Equipos electrónicos").count() > 0)
    print("Buscador visible:", page.locator("text=No sabes en qué categoría").count() > 0)
    browser.close()
