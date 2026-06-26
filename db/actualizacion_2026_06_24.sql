-- ============================================================
-- Actualización 2026-06-24
-- 1. Corrige el orden de puntos_cercanos (estaba ordenando por id, no por distancia)
-- 2. Nuevos tipos de RAEE: Multirresiduo, Audífono
-- 3. Nuevo sistema Red Verde (sin puntos propios — opera por solicitud telefónica)
-- 4. Relaciones sistema ↔ tipo para los nuevos datos
-- ============================================================

-- 1. Función corregida (ahora sí ordena por distancia real)
CREATE OR REPLACE FUNCTION puntos_cercanos(
    _lat          float,
    _lng          float,
    _radio_metros int  DEFAULT 5000,
    _tipo_raee    text DEFAULT NULL
)
RETURNS TABLE (
    id                  int,
    nombre              text,
    direccion_texto     text,
    ciudad              text,
    horario             text,
    sistema             text,
    distancia_metros    float,
    lat                 float,
    lng                 float,
    confianza_coords    smallint,
    ultima_verificacion timestamptz
) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM (
        SELECT DISTINCT ON (p.id)
            p.id,
            p.nombre,
            p.direccion_texto,
            p.ciudad,
            p.horario,
            s.nombre AS sistema,
            ROUND(ST_Distance(
                p.coordenadas,
                ST_MakePoint(_lng, _lat)::geography
            )::numeric, 0)::float AS distancia_metros,
            ST_Y(p.coordenadas::geometry)::float AS lat,
            ST_X(p.coordenadas::geometry)::float AS lng,
            p.confianza_coords,
            p.ultima_verificacion
        FROM puntos p
        JOIN sistemas s ON p.sistema_id = s.id
        LEFT JOIN sistemas_raee sr ON s.id = sr.sistema_id
        LEFT JOIN tipos_raee tr    ON sr.tipo_raee_id = tr.id
        WHERE p.activo = TRUE
          AND p.coordenadas IS NOT NULL
          AND ST_DWithin(
                p.coordenadas,
                ST_MakePoint(_lng, _lat)::geography,
                _radio_metros
              )
          AND (_tipo_raee IS NULL OR tr.nombre = _tipo_raee)
        ORDER BY p.id, distancia_metros
    ) puntos_unicos
    ORDER BY distancia_metros
    LIMIT 20;
END;
$$ LANGUAGE plpgsql;

-- 2. Nuevos tipos de RAEE
INSERT INTO tipos_raee (nombre) VALUES
    ('Multirresiduo'),
    ('Audífono')
ON CONFLICT (nombre) DO NOTHING;

-- 3. Nuevo sistema Red Verde — sí tiene contenedores fijos (39), además de recolección a domicilio
INSERT INTO sistemas (nombre, url_fuente) VALUES
    ('Red Verde', 'https://www.redverde.co/localiza-contenedor-mas-cercano/')
ON CONFLICT (nombre) DO NOTHING;

-- 4a. Pilas con el Ambiente también acepta Luminaria y Multirresiduo (vía sus contenedores)
INSERT INTO sistemas_raee (sistema_id, tipo_raee_id)
SELECT s.id, t.id
FROM sistemas s, tipos_raee t
WHERE s.nombre = 'Pilas con el Ambiente'
  AND t.nombre IN ('Luminaria', 'Multirresiduo')
ON CONFLICT DO NOTHING;

-- 4b. Audífonos se reciben en los mismos puntos que celulares (Lito y EcoCómputo)
INSERT INTO sistemas_raee (sistema_id, tipo_raee_id)
SELECT s.id, t.id
FROM sistemas s, tipos_raee t
WHERE s.nombre IN ('Puntos Verdes Lito', 'EcoCómputo')
  AND t.nombre = 'Audífono'
ON CONFLICT DO NOTHING;

-- 4c. Red Verde — línea blanca (sin puntos, solo referencia informativa)
INSERT INTO sistemas_raee (sistema_id, tipo_raee_id)
SELECT s.id, t.id
FROM sistemas s, tipos_raee t
WHERE s.nombre = 'Red Verde'
  AND t.nombre IN ('Nevera', 'Lavadora', 'Microondas', 'Aire acondicionado', 'Electrodoméstico')
ON CONFLICT DO NOTHING;
