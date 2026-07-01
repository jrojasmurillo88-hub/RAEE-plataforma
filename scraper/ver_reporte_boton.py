from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://raee-plataforma.vercel.app/punto/1", wait_until="networkidle")
    page.wait_for_timeout(2000)
    boton = page.locator("a:has-text('Reportar dato incorrecto')")
    boton.screenshot(path=r"C:\Users\jroja\raee-colombia-producto\scraper\output\boton_reporte_rojo.png")
    browser.close()
