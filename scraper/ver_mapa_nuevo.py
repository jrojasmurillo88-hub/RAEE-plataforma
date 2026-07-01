from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(
        permissions=["geolocation"],
        geolocation={"latitude": 4.684, "longitude": -74.043},
        locale="es-CO",
    )
    page = context.new_page()
    page.goto("http://localhost:3000/mapa?tipos=Pila", wait_until="networkidle")
    page.wait_for_timeout(4000)
    page.screenshot(path=r"C:\Users\jroja\raee-colombia-producto\scraper\output\mapa_carto.png")
    browser.close()
