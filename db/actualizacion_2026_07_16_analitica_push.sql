-- ============================================================
-- Actualización 2026-07-16 — Analítica de comportamiento + notificaciones push
-- 1. Tabla de eventos: selección de punto e intención de descarte
-- 2. Peso real por ítem entregado (reemplaza la estimación por sistema)
-- 3. Suscripciones push y notificaciones programadas (check-in 24h)
-- ============================================================

-- ── 1. Eventos de comportamiento ───────────────────────────────────────────
-- Sirve para responder: "¿cuánta gente selecciona qué puntos?" y
-- "¿cuánta gente dice que va a botar un RAEE vs. cuánta lo bota realmente?"

CREATE TABLE IF NOT EXISTS eventos (
    id          SERIAL PRIMARY KEY,
    tipo        TEXT NOT NULL CHECK (tipo IN ('seleccion_punto', 'intencion_descarte')),
    punto_id    INT REFERENCES puntos(id) ON DELETE SET NULL,
    tipo_raee   TEXT,
    session_id  TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_eventos_tipo_punto  ON eventos(tipo, punto_id);
CREATE INDEX IF NOT EXISTS idx_eventos_tipo_fecha   ON eventos(tipo, created_at);

-- Puntos más seleccionados (consulta de referencia, no una vista obligatoria):
--   SELECT punto_id, COUNT(*) FROM eventos WHERE tipo='seleccion_punto'
--   GROUP BY punto_id ORDER BY COUNT(*) DESC;
--
-- Conversión intención → entrega real (consulta de referencia):
--   SELECT
--     (SELECT COUNT(*) FROM eventos WHERE tipo='intencion_descarte') AS intenciones,
--     (SELECT COUNT(*) FROM entregas) AS entregas_confirmadas;

-- ── 2. Peso real por ítem entregado ────────────────────────────────────────
-- Antes: pesoEstimadoGramos(sistema) — una sola cifra fija por sistema.
-- Ahora: el usuario dice qué entregó específicamente, y el peso se calcula
-- sumando el peso de cada ítem (catálogo vive en el backend, ver main.py).

ALTER TABLE entregas ADD COLUMN IF NOT EXISTS items JSONB;
ALTER TABLE entregas ADD COLUMN IF NOT EXISTS peso_gramos INT;

-- ── 3. Notificaciones push ──────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS push_subscriptions (
    id          SERIAL PRIMARY KEY,
    endpoint    TEXT NOT NULL UNIQUE,
    p256dh      TEXT NOT NULL,
    auth        TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS notificaciones_programadas (
    id                SERIAL PRIMARY KEY,
    endpoint          TEXT NOT NULL REFERENCES push_subscriptions(endpoint) ON DELETE CASCADE,
    punto_id          INT REFERENCES puntos(id) ON DELETE SET NULL,
    nombre_punto      TEXT,
    fire_at           TIMESTAMPTZ NOT NULL,
    enviada           BOOLEAN DEFAULT FALSE,
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_notif_pendientes
    ON notificaciones_programadas(enviada, fire_at)
    WHERE enviada = FALSE;

-- ── 4. RLS ──────────────────────────────────────────────────────────────────
-- Sin políticas: bloquea por defecto cualquier acceso con la anon key.
-- El backend usa la service_role key, que ignora RLS, así que esto no le
-- afecta — solo cierra la puerta si la anon key se filtrara alguna vez.

ALTER TABLE eventos ENABLE ROW LEVEL SECURITY;
ALTER TABLE push_subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE notificaciones_programadas ENABLE ROW LEVEL SECURITY;
