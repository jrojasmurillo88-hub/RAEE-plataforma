-- ============================================================
-- Función: puntos_cercanos
-- Llamada desde la API vía: POST /rest/v1/rpc/puntos_cercanos
-- ============================================================

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
