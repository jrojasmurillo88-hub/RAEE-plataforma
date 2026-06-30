from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:3000/mapa?tipos=Pila", wait_until="networkidle", timeout=20000)
    page.wait_for_timeout(1500)
    boton = page.locator("button:has-text('Buscar desde otro punto')")
    boton.screenshot(path="output/boton_zoom.png")
    browser.close()
