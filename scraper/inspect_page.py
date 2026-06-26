"""
Herramienta de diagnóstico para ver el HTML renderizado de una página dinámica.

Uso:
  python inspect_page.py https://ecocomputo.com/puntos-de-recoleccion/
  python inspect_page.py https://www.pilascolombia.com/puntos

Genera dos archivos en output/:
  - <dominio>_rendered.html  → HTML completo después de que JS corre
  - <dominio>_network.txt    → Llamadas de red (XHR/fetch) capturadas durante la carga

Con esos archivos podés:
1. Abrir el .html en el navegador y usar Ctrl+F para buscar "select", "ciudad", etc.
2. Ver en _network.txt si hay endpoints de API que devuelvan los puntos en JSON.
"""

import sys
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)


def inspeccionar(url: str):
    dominio = urlparse(url).netloc.replace("www.", "").replace(".", "_")
    llamadas_api: list[dict] = []

    def capturar_request(request):
        if request.resource_type in ("xhr", "fetch"):
            llamadas_api.append({
                "url": request.url,
                "method": request.method,
                "resource_type": request.resource_type,
            })

    def capturar_response(response):
        if response.request.resource_type in ("xhr", "fetch"):
            content_type = response.headers.get("content-type", "")
            for entrada in llamadas_api:
                if entrada["url"] == response.url:
                    entrada["status"] = response.status
                    entrada["content_type"] = content_type
                    # Intentar guardar el body si es JSON (puede contener los puntos)
                    if "json" in content_type:
                        try:
                            body = response.json()
                            entrada["body_preview"] = str(body)[:500]
                        except Exception:
                            pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.on("request", capturar_request)
        page.on("response", capturar_response)

        print(f"Abriendo: {url}")
        page.goto(url, wait_until="networkidle", timeout=30_000)
        page.wait_for_timeout(2000)  # espera extra por si hay renders tardíos

        html = page.content()
        browser.close()

    # Guardar HTML renderizado
    html_path = output_dir / f"{dominio}_rendered.html"
    html_path.write_text(html, encoding="utf-8")
    print(f"HTML guardado en: {html_path}")

    # Guardar llamadas de red
    net_path = output_dir / f"{dominio}_network.txt"
    with net_path.open("w", encoding="utf-8") as f:
        f.write(f"Llamadas XHR/fetch capturadas para: {url}\n")
        f.write("=" * 60 + "\n\n")
        if not llamadas_api:
            f.write("No se capturaron llamadas XHR/fetch.\n")
            f.write("Los datos pueden estar embebidos en el HTML o cargarse con interacción del usuario.\n")
        for llamada in llamadas_api:
            f.write(f"[{llamada.get('method', '?')}] {llamada['url']}\n")
            f.write(f"  Status: {llamada.get('status', '?')}\n")
            f.write(f"  Content-Type: {llamada.get('content_type', '?')}\n")
            if "body_preview" in llamada:
                f.write(f"  Body (primeros 500 chars): {llamada['body_preview']}\n")
            f.write("\n")
    print(f"Llamadas de red guardadas en: {net_path}")

    # Resumen en consola: selects y posibles endpoints
    print("\n--- Selects encontrados en el HTML ---")
    selects = re.findall(r'<select[^>]*>', html)
    for s in selects:
        print(" ", s[:200])

    print("\n--- Llamadas a APIs (JSON) ---")
    apis_json = [c for c in llamadas_api if "json" in c.get("content_type", "")]
    if apis_json:
        for api in apis_json:
            print(f"  {api['url']}")
            if "body_preview" in api:
                print(f"    Preview: {api['body_preview'][:200]}")
    else:
        print("  Ninguna capturada en carga inicial.")
        print("  Probá abrir el HTML renderizado, seleccionar una ciudad manualmente")
        print("  y observar el Network tab en DevTools para capturar la llamada.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python inspect_page.py <URL>")
        sys.exit(1)
    inspeccionar(sys.argv[1])
