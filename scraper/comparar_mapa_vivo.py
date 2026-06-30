"""
Carga el mapa real de pilascolombia.com, espera a que los marcadores carguen,
y captura tanto el HTML del mapa como las coordenadas de TODOS los marcadores
visibles (vía la API interna de Google Maps en el navegador), para comparar
directamente contra nuestra base de datos.
"""
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto("https://www.pilascolombia.com/puntos", wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(3000)

    # Intentar extraer todos los marcadores cargados en el objeto del mapa de Google
    marcadores = page.evaluate("""
        () => {
            if (typeof markers !== 'undefined') return markers.length;
            if (typeof window.markers !== 'undefined') return window.markers.length;
            if (typeof map !== 'undefined' && map.markers) return map.markers.length;
            return 'no encontrado en variables globales esperadas';
        }
    """)
    print("Variable 'markers' global encontrada:", marcadores)

    # Listar variables globales relacionadas a mapa/marcadores
    globales = page.evaluate("""
        () => Object.keys(window).filter(k =>
            k.toLowerCase().includes('marker') ||
            k.toLowerCase().includes('map') ||
            k.toLowerCase().includes('punto')
        )
    """)
    print("Variables globales relevantes en window:", globales)

    page.screenshot(path=r"C:\Users\jroja\raee-colombia-producto\scraper\output\mapa_vivo_completo.png", full_page=False)
    browser.close()
