-- ============================================================
-- Check-in post-entrega (cierre del loop, ver 04_capa_comportamiento.md sección 3)
-- ============================================================

CREATE TABLE IF NOT EXISTS entregas (
    id          SERIAL PRIMARY KEY,
    punto_id    INT NOT NULL REFERENCES puntos(id) ON DELETE CASCADE,
    ciudad      TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_entregas_ciudad_fecha ON entregas(ciudad, created_at);
