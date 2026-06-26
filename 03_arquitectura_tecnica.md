# 03 · Arquitectura Técnica

## Criterios de selección de stack

El stack se elige para un solo desarrollador construyendo un prototipo funcional que pueda mostrarse a inversores. Los criterios son:

- **Velocidad de prototipado** sobre optimización prematura
- **Ecosistema maduro** para scraping geoespacial y mobile
- **Costos de infraestructura cercanos a cero** en fase inicial
- **Un solo lenguaje de scripting** para scraping y backend (reduce contexto mental)

---

## Stack seleccionado

| Capa | Tecnología | Razón |
|---|---|---|
| Scraping | Python + Playwright | Único stack maduro para sitios dinámicos JS; Playwright supera a Selenium en velocidad y manejo de SPAs |
| Backend / API | Python + FastAPI | Mismo lenguaje que scraping; rápido de desarrollar; genera documentación automática (útil para alianzas futuras con sistemas posconsumo) |
| Base de datos | PostgreSQL + extensión PostGIS | Consultas geoespaciales nativas (`ST_DWithin` para "puntos cercanos"); estándar de la industria para datos de localización |
| Geocodificación | Google Maps Geocoding API (con fallback Nominatim/OSM) | Necesaria para convertir direcciones textuales en coordenadas; Nominatim es gratis pero menos preciso en Colombia |
| Web | Next.js (React) | Renderizado híbrido (SSR + CSR); ecosistema React comparte conocimiento con la capa mobile; fácil deploy en Vercel |
| Mobile | Expo (React Native) | Comparte lógica y componentes con la web (React); una sola codebase para iOS y Android; Expo Go permite testear sin compilar |
| Mapas | Mapbox GL JS (web) / react-native-maps (mobile) | Mapbox tiene buen soporte para Colombia y tier gratuito generoso; alternativa libre: MapLibre + tiles de OpenStreetMap |

---

## Arquitectura del sistema

```
┌─────────────────────────────────────────────────┐
│                 CAPA DE INGESTA                  │
│                                                  │
│  Playwright scraper  →  Parser / Normalizador    │
│  (por sistema)           (Python)                │
│       ↓                       ↓                  │
│  Scheduler (cron)      Geocodificador            │
│                        (GMaps API / Nominatim)   │
└──────────────────────┬──────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────┐
│              BASE DE DATOS                       │
│                                                  │
│  PostgreSQL + PostGIS                            │
│  tablas: puntos, sistemas, tipos_raee,           │
│          scraping_runs, reportes_usuarios        │
└──────────────────────┬──────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────┐
│              API (FastAPI)                       │
│                                                  │
│  GET /puntos?lat=&lng=&radio=&raee=              │
│  GET /puntos/{id}                                │
│  GET /tipos-raee                                 │
│  POST /reportes   (punto cerrado / dato malo)    │
└───────────────┬─────────────────┬───────────────┘
                │                 │
                ↓                 ↓
┌──────────────────┐   ┌─────────────────────────┐
│   Web (Next.js)  │   │   Mobile (Expo /         │
│   + Mapbox GL    │   │   React Native)          │
│   Vercel deploy  │   │   + react-native-maps    │
└──────────────────┘   └─────────────────────────┘
```

---

## 1. Pipeline de ingesta de datos

### Flujo completo de un punto nuevo

```
1. Playwright abre la página del sistema
2. Itera por cada ciudad disponible (o llama el endpoint AJAX identificado)
3. Extrae: nombre_establecimiento, dirección_texto, ciudad, sistema_id
4. Normalizador estandariza la dirección (mayúsculas, abreviaciones)
5. Geocodificador convierte dirección → (lat, lng)
6. Upsert en PostgreSQL: si el punto ya existe (por dirección), actualiza; si es nuevo, inserta
7. Registra timestamp del scraping_run
```

### Estrategia por fuente (ver 02_fuentes_de_datos.md)

| Fuente | Método | Notas |
|---|---|---|
| Puntos Verdes Lito | requests + BeautifulSoup | Contenido estático; el más simple |
| EcoCómputo | Playwright (headless) o API reversa | Inspeccionar Network tab para identificar endpoint JSON |
| Pilas con el Ambiente | Playwright (headless) o API reversa | Igual que EcoCómputo; posible backend compartido (Grupo Retorna) |
| Red Verde | Por determinar post-verificación | Puede compartir infraestructura con Grupo Retorna |
| Recoenergy | Por determinar post-verificación | Protección activa; evaluar contacto directo |
| ArcGIS Grupo Retorna | REST API de ArcGIS (JSON) | Si el Feature Service es público, devuelve GeoJSON sin scraping |

### Scheduler de actualización automática

El scraper no se corre manualmente — se programa para ejecutarse periódicamente y mantener la base de datos sincronizada con los cambios que hagan los sistemas posconsumo en sus páginas.

**Frecuencia por tipo de fuente:**

| Fuente | Frecuencia | Justificación |
|---|---|---|
| Puntos Verdes Lito (estático) | Semanal | Cambios poco frecuentes; página actualizada manualmente |
| EcoCómputo / Pilas (dinámico) | Semanal | Mismo criterio; los sistemas no actualizan en tiempo real |
| Red Verde / Recoenergy | Semanal (cuando estén integrados) | Idem |

**Implementación:**

Para el MVP, un job de Python con `APScheduler` o un cron del SO es suficiente — no se necesita Celery ni Redis. El job corre cada domingo a las 3am, registra el resultado en `scraping_runs`, y envía un email de alerta si algún scraper falla (indicador de que el sitio cambió su estructura).

```python
# Lógica del job
for sistema in sistemas_activos:
    try:
        puntos = scraper[sistema].extraer()
        db.upsert(puntos)
        db.log_run(sistema, exitoso=True)
    except Exception as e:
        db.log_run(sistema, exitoso=False, error=str(e))
        alertar_por_email(sistema, e)  # el scraper se rompió — revisar manualmente
```

**Detección de puntos eliminados:**

Cuando un punto deja de aparecer en el scraping de su fuente por 2 semanas consecutivas, se marca como `activo = FALSE` automáticamente en lugar de eliminarse. Esto preserva el historial y permite reactivarlo si fue un error de scraping transitorio.

---

## 2. Base de datos

### Modelo de datos central

```sql
-- Sistemas de posconsumo
CREATE TABLE sistemas (
    id          SERIAL PRIMARY KEY,
    nombre      TEXT NOT NULL,
    url_fuente  TEXT,
    activo      BOOLEAN DEFAULT TRUE
);

-- Tipos de RAEE
CREATE TABLE tipos_raee (
    id      SERIAL PRIMARY KEY,
    nombre  TEXT NOT NULL,  -- "Computador", "Pila", "Nevera", etc.
    icono   TEXT            -- nombre del ícono para la UI
);

-- Relación sistema ↔ tipos RAEE aceptados
CREATE TABLE sistemas_raee (
    sistema_id   INT REFERENCES sistemas(id),
    tipo_raee_id INT REFERENCES tipos_raee(id),
    PRIMARY KEY (sistema_id, tipo_raee_id)
);

-- Puntos de recolección
CREATE TABLE puntos (
    id                  SERIAL PRIMARY KEY,
    sistema_id          INT REFERENCES sistemas(id),
    nombre              TEXT NOT NULL,
    direccion_texto     TEXT,
    ciudad              TEXT,
    departamento        TEXT,
    coordenadas         GEOGRAPHY(POINT, 4326),  -- PostGIS
    horario             TEXT,                    -- NULL para la mayoría en MVP
    activo              BOOLEAN DEFAULT TRUE,
    confianza_horario   SMALLINT DEFAULT 0,      -- 0=sin dato, 1=inferido, 2=verificado
    ultima_verificacion TIMESTAMPTZ,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

-- Índice espacial (obligatorio para consultas de cercanía rápidas)
CREATE INDEX idx_puntos_coordenadas ON puntos USING GIST(coordenadas);

-- Registro de scraping runs
CREATE TABLE scraping_runs (
    id          SERIAL PRIMARY KEY,
    sistema_id  INT REFERENCES sistemas(id),
    inicio      TIMESTAMPTZ,
    fin         TIMESTAMPTZ,
    puntos_nuevos   INT DEFAULT 0,
    puntos_actualizados INT DEFAULT 0,
    error       TEXT
);

-- Reportes de usuarios (punto cerrado, dato incorrecto)
CREATE TABLE reportes (
    id          SERIAL PRIMARY KEY,
    punto_id    INT REFERENCES puntos(id),
    tipo        TEXT CHECK (tipo IN ('cerrado', 'horario_incorrecto', 'direccion_incorrecta', 'otro')),
    detalle     TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
```

### Consulta clave — puntos cercanos por tipo de RAEE

```sql
SELECT p.id, p.nombre, p.direccion_texto, p.ciudad,
       p.horario, s.nombre AS sistema,
       ST_Distance(p.coordenadas, ST_MakePoint($lng, $lat)::geography) AS distancia_metros
FROM puntos p
JOIN sistemas s ON p.sistema_id = s.id
JOIN sistemas_raee sr ON s.id = sr.sistema_id
JOIN tipos_raee tr ON sr.tipo_raee_id = tr.id
WHERE tr.nombre = $tipo_raee
  AND p.activo = TRUE
  AND ST_DWithin(p.coordenadas, ST_MakePoint($lng, $lat)::geography, $radio_metros)
ORDER BY distancia_metros
LIMIT 10;
```

---

## 3. API (FastAPI)

### Endpoints del MVP

```
GET  /tipos-raee
     → Lista todos los tipos de RAEE con id, nombre e ícono

GET  /puntos?lat=&lng=&radio=5000&raee_id=
     → Puntos cercanos filtrados por tipo de RAEE
     → radio en metros, default 5000 (5 km)
     → Devuelve: id, nombre, dirección, ciudad, sistema, distancia, horario, última_verificación

GET  /puntos/{id}
     → Detalle completo de un punto

POST /reportes
     → Body: { punto_id, tipo, detalle }
     → Registra reporte ciudadano de dato incorrecto o punto cerrado
```

### Lo que FastAPI da gratis

- Documentación interactiva en `/docs` (Swagger) — útil para mostrar a posibles aliados técnicos
- Validación de parámetros automática (Pydantic)
- Async por defecto (compatible con consultas PostGIS sin bloquear)

---

## 4. Frontend web (Next.js)

### Páginas del MVP

| Ruta | Función |
|---|---|
| `/` | Pantalla de inicio — selector de tipo de RAEE (ver archivo 04 para diseño comportamental) |
| `/mapa` | Mapa con puntos filtrados por tipo y ubicación |
| `/punto/[id]` | Detalle de un punto: dirección, cómo llegar, RAEE que acepta, horario si existe |
| `/reportar/[id]` | Formulario de reporte de dato incorrecto |

### Consideración de renderizado

Las páginas de mapa son client-side (CSR) por naturaleza. Las páginas de detalle de punto pueden ser SSR/ISR para SEO — útil si queremos que alguien que busca "dónde botar celular Bogotá" encuentre la app por Google.

---

## 5. App móvil (Expo / React Native)

### Decisión de arquitectura

La app comparte la misma API que el web. No hay lógica de negocio duplicada — solo una capa UI diferente.

Para el MVP, la app mobile tiene una sola ventaja crítica sobre el web que justifica construirla: **acceso nativo a GPS** para geolocalización precisa sin fricción de permiso de browser. El flujo "abrí la app → ya sé dónde estás → estos son los puntos más cercanos" es más fluido que en web móvil.

### Pantallas del MVP

1. **Inicio** — selector de qué RAEE tengo (mismo flujo que web, ver archivo 04)
2. **Mapa** — puntos cercanos con mi ubicación centrada
3. **Detalle del punto** — dirección, cómo llegar (deep link a Google Maps / Waze), RAEE aceptado
4. **Reportar** — formulario corto si el punto está cerrado o el dato es incorrecto

---

## 6. Infraestructura y costos del MVP

| Componente | Servicio | Costo estimado |
|---|---|---|
| Base de datos PostgreSQL + PostGIS | Supabase (free tier: 500 MB, PostGIS incluido) | $0 |
| Backend FastAPI | Render (free tier: 750 hs/mes) o Railway ($5/mes) | $0–5/mes |
| Frontend web | Vercel (free tier) | $0 |
| Scraping scheduler | Mismo servidor del backend o GitHub Actions (cron) | $0 |
| Geocodificación | Google Maps Geocoding API ($5 por 1000 requests) | ~$5–20 para carga inicial |
| Mapas web | Mapbox (free: 50.000 loads/mes) | $0 en MVP |
| App mobile | Expo Go para testing; build con EAS (gratis para proyectos personales) | $0 |

**Costo total estimado fase MVP**: menos de $25/mes, probablemente $0–5.

---

## 7. Secuencia de construcción recomendada

El orden minimiza tiempo antes de tener algo funcional y mostrable:

```
Semana 1-2:  Scraper de Lito (el más simple, contenido estático)
             + modelo de BD + inserción básica
             → primer dataset de ~200 puntos en Bogotá

Semana 3-4:  API FastAPI con endpoint /puntos
             + geocodificación de las direcciones de Lito

Semana 5-6:  Web Next.js con mapa funcional
             → prototipo mostrable a usuarios para feedback

Semana 7-8:  Scrapers de EcoCómputo y Pilas (dinámicos)
             + ingeniería inversa de sus APIs

Semana 9-10: App Expo con geolocalización nativa
             + flujo completo desde selector hasta navegación

Semana 11+:  Resolver Red Verde / Recoenergy
             + reporte ciudadano
             + scraping automático (scheduler)
```

---

## 8. Deuda técnica conocida y límites del MVP

| Limitación | Impacto | Decisión |
|---|---|---|
| Sin horarios en casi ningún punto | Alto (ver archivo 04) | Aceptada para MVP; mitigación: badge "horario no verificado" |
| Scraping puede romperse si los sitios cambian su estructura | Medio | Monitoreo de errores en scraping_run + alertas simples por email |
| Sin autenticación en la API | Bajo en MVP | No se necesita para lectura pública; sí para el endpoint de reportes (añadir rate limiting) |
| App mobile no publicada en stores | Bajo en MVP | Expo Go es suficiente para validación; publicación posterior |
| Geocodificación de direcciones colombianas es imprecisa | Medio | Revisión manual para puntos con baja confianza (campo `confianza_horario` reutilizable) |
