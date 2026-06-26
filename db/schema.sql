-- ============================================================
-- RAEE Colombia — Schema PostgreSQL + PostGIS
-- Ejecutar en Supabase: SQL Editor → New query → pegar y correr
-- ============================================================

-- PostGIS viene habilitado por defecto en Supabase.
-- Si usás PostgreSQL local: CREATE EXTENSION IF NOT EXISTS postgis;

-- ── Sistemas de posconsumo ─────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS sistemas (
    id          SERIAL PRIMARY KEY,
    nombre      TEXT NOT NULL UNIQUE,
    url_fuente  TEXT,
    activo      BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── Tipos de RAEE ──────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS tipos_raee (
    id      SERIAL PRIMARY KEY,
    nombre  TEXT NOT NULL UNIQUE,
    icono   TEXT
);

-- ── Relación sistema ↔ tipos RAEE aceptados ────────────────────────────────

CREATE TABLE IF NOT EXISTS sistemas_raee (
    sistema_id   INT NOT NULL REFERENCES sistemas(id) ON DELETE CASCADE,
    tipo_raee_id INT NOT NULL REFERENCES tipos_raee(id) ON DELETE CASCADE,
    PRIMARY KEY (sistema_id, tipo_raee_id)
);

-- ── Puntos de recolección ──────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS puntos (
    id                  SERIAL PRIMARY KEY,
    sistema_id          INT NOT NULL REFERENCES sistemas(id) ON DELETE CASCADE,
    nombre              TEXT NOT NULL,
    direccion_texto     TEXT,
    ciudad              TEXT,
    departamento        TEXT,
    coordenadas         GEOGRAPHY(POINT, 4326),
    horario             TEXT,
    activo              BOOLEAN DEFAULT TRUE,
    -- 0 = sin dato, 1 = geocodificado automáticamente, 2 = verificado manualmente
    confianza_coords    SMALLINT DEFAULT 0,
    fuente_url          TEXT,
    ultima_verificacion TIMESTAMPTZ,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

-- Índice espacial — obligatorio para que ST_DWithin sea rápido
CREATE INDEX IF NOT EXISTS idx_puntos_coordenadas
    ON puntos USING GIST(coordenadas);

CREATE INDEX IF NOT EXISTS idx_puntos_ciudad
    ON puntos(ciudad);

CREATE INDEX IF NOT EXISTS idx_puntos_activo
    ON puntos(activo);

-- ── Registro de scraping runs ──────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS scraping_runs (
    id                  SERIAL PRIMARY KEY,
    sistema_id          INT REFERENCES sistemas(id),
    inicio              TIMESTAMPTZ DEFAULT NOW(),
    fin                 TIMESTAMPTZ,
    puntos_nuevos       INT DEFAULT 0,
    puntos_actualizados INT DEFAULT 0,
    puntos_desactivados INT DEFAULT 0,
    error               TEXT
);

-- ── Reportes ciudadanos ────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS reportes (
    id         SERIAL PRIMARY KEY,
    punto_id   INT NOT NULL REFERENCES puntos(id) ON DELETE CASCADE,
    tipo       TEXT NOT NULL CHECK (
                   tipo IN ('cerrado', 'horario_incorrecto', 'direccion_incorrecta', 'otro')
               ),
    detalle    TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── Datos semilla: sistemas y tipos de RAEE ────────────────────────────────

INSERT INTO sistemas (nombre, url_fuente) VALUES
    ('Puntos Verdes Lito',    'https://puntosverdeslito.com/puntos-de-recoleccion/'),
    ('EcoCómputo',            'https://ecocomputo.com/puntos-de-recoleccion/'),
    ('Pilas con el Ambiente', 'https://www.pilascolombia.com/puntos')
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO tipos_raee (nombre) VALUES
    ('Celular'),
    ('Tablet'),
    ('Computador'),
    ('Monitor'),
    ('Impresora'),
    ('Teclado'),
    ('Periférico'),
    ('Cable'),
    ('Electrodoméstico'),
    ('Nevera'),
    ('Lavadora'),
    ('Microondas'),
    ('Aire acondicionado'),
    ('Pila'),
    ('Batería doméstica'),
    ('Acumulador'),
    ('Batería de plomo-ácido'),
    ('Luminaria'),
    ('Bombilla')
ON CONFLICT (nombre) DO NOTHING;

-- Relaciones sistema ↔ tipos RAEE
INSERT INTO sistemas_raee (sistema_id, tipo_raee_id)
SELECT s.id, t.id
FROM sistemas s, tipos_raee t
WHERE s.nombre = 'Puntos Verdes Lito'
  AND t.nombre IN ('Celular','Tablet','Computador','Monitor','Impresora',
                   'Teclado','Periférico','Cable','Electrodoméstico')
ON CONFLICT DO NOTHING;

INSERT INTO sistemas_raee (sistema_id, tipo_raee_id)
SELECT s.id, t.id
FROM sistemas s, tipos_raee t
WHERE s.nombre = 'EcoCómputo'
  AND t.nombre IN ('Computador','Monitor','Tablet','Impresora','Celular','Teclado','Periférico')
ON CONFLICT DO NOTHING;

INSERT INTO sistemas_raee (sistema_id, tipo_raee_id)
SELECT s.id, t.id
FROM sistemas s, tipos_raee t
WHERE s.nombre = 'Pilas con el Ambiente'
  AND t.nombre IN ('Pila','Batería doméstica','Acumulador')
ON CONFLICT DO NOTHING;

-- ── Vista útil: puntos con su sistema ─────────────────────────────────────

CREATE OR REPLACE VIEW v_puntos AS
SELECT
    p.id,
    p.nombre,
    p.direccion_texto,
    p.ciudad,
    p.horario,
    p.activo,
    p.confianza_coords,
    p.ultima_verificacion,
    ST_X(p.coordenadas::geometry) AS lng,
    ST_Y(p.coordenadas::geometry) AS lat,
    s.nombre AS sistema,
    s.url_fuente
FROM puntos p
JOIN sistemas s ON p.sistema_id = s.id;
