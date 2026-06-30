from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto("https://www.pilascolombia.com/puntos", wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(3000)

    info = page.evaluate("""
        () => {
            try {
                const total = allMarkers.length;
                const muestra = allMarkers.slice(0, 3).map(m => {
                    try {
                        return {
                            lat: m.getPosition ? m.getPosition().lat() : (m.position ? m.position.lat : null),
                            lng: m.getPosition ? m.getPosition().lng() : (m.position ? m.position.lng : null),
                            title: m.getTitle ? m.getTitle() : (m.title || null),
                        };
                    } catch (e) {
                        return { error: String(e) };
                    }
                });
                return { total, muestra };
            } catch (e) {
                return { error: String(e) };
            }
        }
    """)
    print(json.dumps(info, ensure_ascii=False, indent=2))
    browser.close()
