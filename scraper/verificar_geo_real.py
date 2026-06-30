from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(
        permissions=["geolocation"],
        geolocation={"latitude": 4.684, "longitude": -74.043},
        locale="es-CO",
    )
    page = context.new_page()
    page.goto("https://raee-plataforma.vercel.app/", wait_until="networkidle")

    resultado = page.evaluate("""
        () => new Promise((resolve) => {
            navigator.geolocation.getCurrentPosition(
                (pos) => resolve({lat: pos.coords.latitude, lng: pos.coords.longitude}),
                (err) => resolve({error: err.message})
            );
        })
    """)
    print("Geolocalizacion reportada por el navegador:", resultado)
    browser.close()
