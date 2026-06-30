from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto("https://www.pilascolombia.com/puntos", wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(3000)

    todos = page.evaluate("""
        () => allMarkers.map(m => {
            try {
                return {
                    lat: m.getPosition ? m.getPosition().lat() : (m.position ? m.position.lat : null),
                    lng: m.getPosition ? m.getPosition().lng() : (m.position ? m.position.lng : null),
                    title: m.getTitle ? m.getTitle() : (m.title || null),
                };
            } catch (e) {
                return null;
            }
        }).filter(m => m && m.lat && m.lng && m.lat !== 0)
    """)

    print("Total marcadores con coordenadas validas:", len(todos))

    # Zona amplia: Bogota norte, lat 4.65-4.75, lng -74.10 a -74.00 (cubre Calle 100-116, Santa Barbara, Chico)
    zona = [m for m in todos if 4.65 <= m["lat"] <= 4.75 and -74.10 <= m["lng"] <= -74.00]
    print(f"Marcadores en zona norte de Bogota (lat 4.65-4.75, lng -74.10 a -74.00): {len(zona)}")
    for m in sorted(zona, key=lambda x: x["lat"]):
        print(f"  {m['lat']:.6f}, {m['lng']:.6f}  -  {m['title']}")

    with open("output/marcadores_vivos_completos.json", "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

    browser.close()
