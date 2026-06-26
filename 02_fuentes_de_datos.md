# 02 · Fuentes de Datos

## Alcance del inventario

**En scope**: residuos de aparatos eléctricos y electrónicos (RAEE) — equipos de cómputo, electrodomésticos, pilas, baterías industriales, luminarias.
**Fuera de scope (MVP)**: llantas (Rueda Verde), plaguicidas domésticos (Cierra el Ciclo).

---

## 1. Inventario de sistemas activos

### Grupo Retorna — alianza de 6 sistemas (ANDI)

Grupo Retorna no tiene mapa unificado público. Cada sistema opera su propia página y base de puntos. Los sistemas en scope son:

| Sistema | RAEE aceptado | URL puntos de recolección | Estructura técnica |
|---|---|---|---|
| **EcoCómputo** | Computadores, tablets, impresoras, monitores, periféricos | ecocomputo.com/puntos-de-recoleccion/ | Dinámica — formulario JS con selector de ciudad y radio; datos cargados post-búsqueda via AJAX |
| **Pilas con el Ambiente** | Pilas y acumuladores domésticos | pilascolombia.com/puntos | Dinámica — selector de ciudad + geolocalización + Google Street View; sin HTML estático |
| **Red Verde** | Línea blanca: neveras, lavadoras, microondas, aires acondicionados | redverde.co (sección puntos por confirmar) | No verificada — sitio con errores de conexión al momento del análisis |
| **Recoenergy** | Baterías de plomo-ácido (industriales, de vehículos) | recoenergy.com.co | No verificada — sitio con protección anti-bot activa |

### Fuera de Grupo Retorna

| Sistema | RAEE aceptado | URL puntos de recolección | Estructura técnica |
|---|---|---|---|
| **Puntos Verdes Lito** | RAEE general (electrónicos, electrodomésticos) | puntosverdeslito.com/puntos-de-recoleccion/ | **Estática** — listas de texto por ciudad con nombre de establecimiento y dirección |
| **Lúmina** | Bombillas y tubos fluorescentes | Por confirmar | Por confirmar |

---

## 2. Análisis técnico por tipo de fuente

### Tipo A — Contenido estático (scraping directo)

**Sistema**: Puntos Verdes Lito

**Lo que expone la página:**
- Lista de puntos agrupados por ciudad
- Ciudades cubiertas: Barranquilla, Bogotá, Bucaramanga, Cali, Manizales, Medellín, Popayán
- Nombre del establecimiento + dirección (calle/carrera/número)
- Subcategoría identificada: "Contenedores de EcoCómputo operados por Lito"

**Lo que NO expone:**
- Horarios de atención por punto
- Coordenadas geográficas
- Teléfono del punto individual

**Estrategia de extracción**: requests + BeautifulSoup. Parsear listas HTML por sección de ciudad. Geocodificar direcciones post-extracción (Google Maps Geocoding API o Nominatim).

**Frecuencia de actualización estimada**: baja (páginas estáticas actualizadas manualmente). Rescraping semanal o quincenal es suficiente.

---

### Tipo B — Contenido dinámico (headless browser o API reversa)

**Sistemas**: EcoCómputo, Pilas con el Ambiente

**Comportamiento observado:**
- La página carga un formulario de búsqueda vacío
- Los puntos se renderizan solo después de que el usuario selecciona ciudad y/o activa geolocalización
- Sin HTML estático con datos de puntos

**Estrategia de extracción (opción 1 — headless browser):**
Playwright o Puppeteer automatiza la selección de cada ciudad disponible, espera la respuesta, extrae el DOM renderizado. Más lento pero no requiere ingeniería reversa.

**Estrategia de extracción (opción 2 — API reversa):**
Interceptar las llamadas de red (Network tab en DevTools) durante una búsqueda manual para identificar el endpoint AJAX y sus parámetros. Si el endpoint responde JSON, extracción directa sin browser. Más eficiente, más frágil ante cambios de backend.

**Riesgo**: ambos sistemas pertenecen a Grupo Retorna — es posible que compartan backend. Confirmar si la misma API sirve ambos reduciría el trabajo de extracción significativamente.

---

### Tipo C — Sitios con protección activa (estado por verificar)

**Sistemas**: Red Verde, Recoenergy

**Comportamiento observado:**
- Red Verde: error de conexión (ECONNREFUSED) al momento del análisis — puede ser temporal o indicar bloqueo por IP
- Recoenergy: pantalla de verificación ("One moment, please...") — protección tipo Cloudflare o similar

**Estrategia de extracción**: verificar manualmente primero. Si tienen protección activa, opciones son: (a) contacto directo con el sistema para acuerdo de datos, (b) scraping con rotación de user-agents + delays, (c) entrada manual de puntos como fallback para MVP.

---

## 3. Fuentes complementarias

| Fuente | Tipo | Utilidad | URL |
|---|---|---|---|
| **RPCAEE (VUCE)** | Registro oficial | Inventario de productores obligados — base para identificar sistemas faltantes | vuce.gov.co/servicios/rpcaee |
| **ANLA** | Regulador | Lista de sistemas autorizados y sanciones activas | anla.gov.co |
| **Mapa ArcGIS Grupo Retorna** | Mapa embebido | Podría exponer datos geoespaciales en formato consultable (REST API de ArcGIS) | arcgis.com/apps/View/?appid=07ca65a606704e5cb6913ccb0b998b5b |
| **Secretaría Distrital de Ambiente Bogotá** | Datos públicos | Jornadas de recolección y puntos temporales para Bogotá | ambientebogota.gov.co |

**Nota sobre ArcGIS**: los mapas publicados con ArcGIS Online suelen tener una REST API consultable en la URL del Feature Service subyacente. Inspeccionar el appid mencionado puede revelar un endpoint que devuelve todos los puntos en GeoJSON, sin necesidad de scraping.

---

## 4. Campos de datos objetivo por punto

Cada punto de recolección en la base de datos unificada debe tener idealmente:

| Campo | Obligatorio MVP | Fuente posible |
|---|---|---|
| Nombre del establecimiento | Sí | Scraping |
| Dirección textual | Sí | Scraping |
| Ciudad / Municipio | Sí | Scraping |
| Coordenadas (lat/lng) | Sí | Geocodificación post-extracción |
| Sistema posconsumo | Sí | Metadato de extracción |
| Tipos de RAEE aceptados | Sí | Metadato del sistema + scraping |
| Horario de atención | Deseable | Escaso en fuentes actuales — gap conocido |
| Teléfono / contacto | Deseable | Escaso en fuentes actuales |
| Fecha de última verificación | Sí | Timestamp del scraping |
| Estado (activo / sin verificar / inactivo) | Sí | Lógica de negocio |

---

## 5. Gaps conocidos y plan de mitigación

| Gap | Impacto | Mitigación |
|---|---|---|
| Horarios ausentes en casi todas las fuentes | Alto — un punto sin horario genera visitas fallidas (destruye confianza, ver archivo 04) | Contacto directo con establecimientos para los top-N puntos de Bogotá en MVP |
| Red Verde y Recoenergy no verificadas | Medio | Verificación manual + contacto directo con sistemas |
| Lúmina sin URL confirmada | Bajo (luminarias son RAEE de nicho) | Búsqueda específica + posible ingreso manual |
| Sin coordenadas en ninguna fuente | Alto — la app depende de mapas y cercanía | Geocodificación automática por dirección; validación manual para puntos con dirección ambigua |
| Actualización manual de los sistemas | Alto — información desactualizada destruye la propuesta de valor | Pipeline de rescraping automático + sistema de reporte de puntos por parte de usuarios |

---

## 6. Priorización de extracción para MVP

**Fase 1 — Bogotá, datos disponibles hoy:**
1. Puntos Verdes Lito (estático, inmediato)
2. EcoCómputo vía headless browser o API reversa
3. Pilas con el Ambiente vía headless browser o API reversa

**Fase 2 — Ampliar cobertura:**
4. Red Verde y Recoenergy (una vez resuelta la estrategia de acceso)
5. ArcGIS de Grupo Retorna (si el REST API es consultable)
6. Lúmina

**Fuera del MVP técnico:**
- Integración con RPCAEE para detección automática de nuevos sistemas
- Módulo de reporte ciudadano de puntos nuevos o cerrados
