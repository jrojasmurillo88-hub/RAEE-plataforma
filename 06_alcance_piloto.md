# 06 · Alcance del piloto de colaboración

Borrador para revisar e insertar en la propuesta cuando tengas espacio — no toca el Word que estás editando ahora.

## Qué incluye

- Integración de los puntos de recolección del sistema de posconsumo en RAEEconecta durante los 3 meses del piloto.
- Visibilidad de esos puntos ante cualquier ciudadano que busque desechar un RAEE cerca de ellos.
- Datos de comportamiento del sistema: selecciones de punto, intención de descarte vs. entregas confirmadas, peso real por categoría entregada.
- Verificación semanal del estado de los puntos (abierto/cerrado, horario) mediante reportes ciudadanos.
- Sesiones de co-diseño para ajustar la visibilización de sus puntos y validar la herramienta con retroalimentación directa del sistema.
- Un NDA bilateral que protege la confidencialidad de los datos compartidos por ambas partes durante el piloto.
- Al finalizar el piloto, un informe con los resultados medidos frente a las metas acordadas (usos, selecciones de punto, entregas confirmadas, kg recolectados).

## Qué NO incluye

- **Mejoras a la plataforma que resulten inviables para un MVP.** Una solicitud de ajuste o mejora se considera inviable dentro del piloto si cumple uno o más de estos criterios:
  1. **Excede el tiempo disponible**: requiere más horas de desarrollo de las que caben en el bloque semanal acordado (~10h/semana, ver plan de trabajo) sin renegociar el alcance o el cronograma.
  2. **Requiere infraestructura nueva no construida**, como integración en tiempo real con sistemas internos del gestor (ERP, inventario, bases de datos propias) o con terceros fuera del control de RAEEconecta.
  3. **Implica recolectar datos personales (PII) del ciudadano** (nombre, cédula, email obligatorio, etc.) — rompe el principio de diseño "sin fricción, sin registro" sobre el que está construida la plataforma.
  4. **Requiere una app nativa** (iOS/Android) en lugar de la web app actual — es un desarrollo de otra escala, no un ajuste de MVP.
  5. **Implica exclusividad o una versión de marca blanca** solo para un sistema — contradice el modelo de plataforma unificada entre sistemas.
  6. **Requiere procesar pagos o transacciones económicas** dentro de la app.
  7. **Exige garantías contractuales de nivel empresarial** (SLA de disponibilidad, soporte 24/7, tiempos de respuesta garantizados) — propias de un contrato de continuidad, no de un piloto de validación.
  8. **Contradice un principio de diseño comportamental ya validado** (por ejemplo, introducir gamificación o recompensas, que el diseño actual evita deliberadamente) sin evidencia que justifique el cambio.
  9. **Depende de una aprobación o desarrollo de un tercero** que el sistema de posconsumo no ha gestionado (ej. una API que ellos no han habilitado, un dato que no tienen digitalizado).

  Si una solicitud cae en alguno de estos puntos, se documenta como fuera de alcance del piloto y se conversa por separado — no se descarta de plano, pero no se compromete dentro de las condiciones ya pactadas.
- **Cesión de la propiedad intelectual de la plataforma.** El código, el diseño, la metodología y la base de datos unificada de RAEEconecta son y siguen siendo propiedad de [nombre / razón social del titular]. El piloto es un acuerdo de uso y colaboración de datos por tiempo definido, no una venta ni transferencia de esos activos.
- **Exclusividad.** Durante el piloto, RAEEconecta puede seguir integrando puntos de otros sistemas de posconsumo — de hecho, es parte del valor: más cobertura para el ciudadano beneficia también a los puntos del sistema aliado.
- **Garantía de un incremento específico de recolección.** El piloto busca medir el efecto real del canal con datos; no garantiza un resultado numérico antes de tenerlos.
- **Desarrollo de funcionalidades a la medida** fuera de lo que se acuerde explícitamente en el plan de trabajo del piloto.
- **Asunción de las obligaciones regulatorias propias del sistema de posconsumo** (REP, reportes ante ANLA, metas de recolección). La plataforma es un canal de apoyo, no un sustituto de esas obligaciones.
- **Continuidad automática después de los 3 meses.** Cualquier contrato posterior a la fecha de cierre del piloto se negocia por separado, con base en los resultados obtenidos.

---

**Pendiente de tu parte:** en el primer punto de "Qué NO incluye" dejé `[nombre / razón social del titular]` — pon ahí a nombre de quién queda la propiedad intelectual (tú a título personal, o una figura legal si ya constituiste algo).
