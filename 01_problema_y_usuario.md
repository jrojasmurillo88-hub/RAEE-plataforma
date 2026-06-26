# 01 · Problema y Usuario

## 1. Enunciado del problema

Los sistemas de posconsumo de RAEE en Colombia operan en silos: cada empresa (Lito, Ecocomputo, RedVerde, Pilas por el Ambiente, entre otras) publica sus puntos de recolección en su propia plataforma web, con distintos niveles de actualización y formatos. Un ciudadano que quiere disponer correctamente un residuo debe saber qué sistema lo recoge, encontrar su sitio web, navegar su interfaz, y repetir ese proceso por cada tipo de RAEE que tenga.

El resultado es un costo de búsqueda y decisión tan alto que la conducta de disposición correcta no ocurre — no porque el ciudadano no quiera, sino porque el ambiente de decisión no la facilita.

## 2. Brecha comportamental

| Nivel | Diagnóstico |
|---|---|
| **Conocimiento** | Parcial. En contextos urbanos hay exposición a la existencia del sistema, pero no claridad sobre cómo operarlo. |
| **Intención** | Generalmente presente en el segmento objetivo (ciudadano urbano con algún nivel de conciencia ambiental). |
| **Acción** | Bloqueada por fricción logística: fragmentación de fuentes, interfaz dispersa, incertidumbre sobre qué sistema acepta qué. |

La intervención no requiere cambiar actitudes — requiere reducir la fricción entre intención y acción.

## 3. Solución núcleo

Una plataforma web y app que agrega, normaliza y mantiene actualizada la información de puntos de disposición RAEE de todos los sistemas de posconsumo activos en Colombia, presentada desde la perspectiva del residuo que el usuario tiene en mano.

**Flujo de uso mínimo viable:**
1. Usuario indica qué dispositivo quiere desechar
2. La app muestra los puntos de entrega más cercanos que lo aceptan, con información operativa actualizada
3. Usuario va al punto

## 4. Usuario Primario — Ciudadano Urbano

**Descripción**: persona en ciudad con uno o más RAEE para desechar (celular viejo, pila, electrodoméstico pequeño). Tiene intención de disposición correcta pero no sabe cómo ejecutarla de forma eficiente.

**Contexto de activación**: el momento de decisión ocurre típicamente al hacer limpieza del hogar, cambiar un dispositivo, o cuando un objeto deja de funcionar.

**Barreras específicas:**
- No sabe qué sistema acepta qué tipo de RAEE
- No conoce los puntos cercanos a su rutina
- Las páginas de los sistemas son difíciles de navegar
- No tiene certeza de que la información esté vigente

**Ciudades de inicio**: centros urbanos con mayor densidad de puntos de recolección señalizados (hipótesis de trabajo: Bogotá como primer contexto).

**Perfil de adopción temprana**: persona que ya intentó disponer correctamente pero abandonó el proceso por la complejidad. Tiene motivación intrínseca preexistente — la app solo necesita no fallarle.

## 5. Usuario Secundario — Municipios y Gestores

**Descripción**: entidades municipales o gestores ambientales que necesitan monitorear cobertura territorial de puntos de recolección y tasas de disposición.

**Necesidad diferencial**: visibilidad agregada (mapas de calor, tendencias), no navegación punto a punto.

**Prioridad de desarrollo**: posterior al lanzamiento ciudadano. Su valor depende de que el producto ciudadano ya tenga datos de uso.

## 6. Validación de contexto

El equipo fundador cuenta con un año de trabajo directo en intervenciones RAEE en Colombia. Esto implica:
- Conocimiento de los sistemas de posconsumo activos y sus páginas
- Comprensión del comportamiento de disposición en campo
- Red de contactos en el ecosistema (sistemas, gestores, puntos)

El riesgo de "construir para un usuario imaginario" es bajo. El riesgo a validar es de ejecución técnica y adopción a escala.

## 7. Métricas de éxito

| Métrica | Descripción | Nivel |
|---|---|---|
| **Tasa de disposición por peso** | Kilogramos de RAEE recolectados en puntos vinculados a la app | Impacto real |
| **Viajes iniciados** | Usuarios que buscan un punto y llegan a confirmación de ruta | Indicador de intención |
| **Retención a 30 días** | Usuarios que vuelven después de su primera disposición | Indicador de hábito |
| **Cobertura de puntos** | % de puntos de posconsumo activos en Colombia incluidos en la plataforma | Calidad del producto |

La métrica de peso conecta el uso de la app con impacto ambiental medible — relevante para narrativa de inversores y para alianzas con sistemas de posconsumo.

## 8. Principios de diseño comportamental derivados del diagnóstico

Estos principios deben cruzar transversalmente los archivos de arquitectura técnica y capa de comportamiento:

- **Reducción de fricción en el punto de decisión**: la búsqueda debe comenzar desde el objeto, no desde el sistema
- **Defaults hacia la acción**: la ubicación, el tipo de RAEE más probable, y el punto más cercano deben aparecer sin que el usuario los busque activamente
- **Fiabilidad como prerequisito de adopción**: un punto cerrado o con horario incorrecto destruye la confianza más que cualquier diseño puede construirla
- **Retroalimentación de impacto**: mostrar al usuario el peso estimado de lo que entregó y su equivalente ambiental (cierra el loop comportamental)
- **Norma descriptiva**: cuántas personas en su zona usaron la app este mes (activa la norma social sin requerir gamificación forzada)
