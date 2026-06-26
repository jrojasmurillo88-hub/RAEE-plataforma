# 04 · Capa de Comportamiento

## Marco de referencia

El diagnóstico del archivo 01 establece que el usuario primario tiene intención pero no ejecuta la conducta. La intervención no busca motivar — busca eliminar la fricción entre intención y acción. Las decisiones de diseño en este archivo se organizan usando el modelo **COM-B** (Capacidad, Oportunidad, Motivación → Comportamiento) como mapa de dónde intervenir, y principios de diseño comportamental como herramientas específicas.

**Diagnóstico COM-B aplicado al usuario primario:**

| Componente | Estado | Implicación de diseño |
|---|---|---|
| **Capacidad física** | Alta — el usuario puede ir a un punto si sabe dónde está | No intervenir aquí |
| **Capacidad psicológica** | Media — no sabe qué sistema acepta qué RAEE | Reducir carga cognitiva: la app decide por él |
| **Oportunidad física** | Media — los puntos existen pero no están en la ruta habitual | Mostrar puntos en el camino, no solo los más cercanos al hogar |
| **Oportunidad social** | Baja — disposición correcta es invisible socialmente | Activar norma descriptiva |
| **Motivación reflectiva** | Alta — intención declarada presente | No necesita intervención directa |
| **Motivación automática** | Baja — no hay hábito ni señal de contexto que dispare la conducta | Construir una señal de contexto (ver sección de activación) |

---

## 1. Flujo de usuario diseñado para máxima conversión

El flujo mínimo viable tiene que completarse en menos de 3 interacciones desde que el usuario abre la app hasta que tiene una dirección y puede salir.

### Pantalla 1 — ¿Qué querés desechar?

**Problema a resolver**: el usuario no sabe en qué categoría entra su objeto. "Celular" no es una categoría obvia en un sistema diseñado por gestores de residuos.

**Decisión de diseño**: la interfaz muestra objetos, no categorías técnicas.

```
❌  "Equipos de cómputo y periféricos"
✅  "Celular / Tablet"   "Computador"   "Cargador / Cable"
❌  "Residuos de aparatos de temperatura"
✅  "Nevera"   "Lavadora"   "Microondas"
```

Categorías ordenadas por frecuencia esperada de uso (celulares primero), no alfabéticamente ni por categoría técnica del gestor.

**Default conductual**: la pantalla de inicio no muestra texto vacío — muestra el objeto más frecuentemente desechado como selección sugerida. El usuario puede cambiarla, pero el camino de menor resistencia ya está orientado hacia la acción.

---

### Pantalla 2 — Puntos cercanos

**Problema a resolver**: mostrar una lista de puntos sin contexto no es accionable. El usuario necesita saber si el punto es realista para él hoy.

**Decisiones de diseño:**

**a) Ordenar por distancia desde la ubicación actual, no desde el hogar.** El mejor momento para ir a un punto es cuando el usuario ya está en movimiento. Un punto a 200m del trabajo vale más que uno a 500m de la casa.

**b) Mostrar tiempo estimado a pie / en carro**, no solo distancia en metros. "8 minutos caminando" es más accionable que "700 metros".

**c) Badge de confianza en el dato:**

```
🟢  Información verificada hace 3 días
🟡  Información verificada hace 3 semanas
🔴  Sin verificación reciente — llamar antes de ir
```

Este badge tiene doble función: construye confianza cuando el dato es reciente, y gestiona expectativas (reduce frustración) cuando no lo es. Un usuario que llega a un punto cerrado sin aviso abandona para siempre; uno que llegó avisado de que el dato podía estar desactualizado lo acepta como parte del sistema.

**d) Si no hay horario disponible, decirlo explícitamente:**

```
❌  [campo vacío]
✅  "Horario no disponible — se recomienda verificar antes de ir"
```

El silencio sobre datos faltantes genera expectativas incorrectas. La honestidad sobre la limitación es menos costosa que el viaje fallido.

---

### Pantalla 3 — Detalle del punto + acción

**Un solo CTA principal**: "Cómo llegar" (deep link a Google Maps / Waze con las coordenadas del punto).

**Información secundaria accesible pero no prominente**: RAEE aceptados, sistema posconsumo, reportar dato incorrecto.

**Fricción intencional en "Reportar"**: el botón de reporte no está en la pantalla principal del punto — está como opción secundaria. Esto evita reportes accidentales y asegura que quien reporta tiene una razón activa.

---

## 2. Activación en el momento correcto

El comportamiento de disposición correcta tiene una señal de contexto natural: **el momento en que el usuario adquiere un dispositivo nuevo**. Ese es el momento en que el objeto anterior queda obsoleto — pero la mayoría de la gente lo guarda en un cajón y lo olvida.

**Intervención de implementación intencional:**

Cuando el usuario usa la app por primera vez, antes de mostrar el mapa:

```
"¿Tenés un dispositivo que cambiar próximamente?
 Si querés, te recordamos dónde entregarlo."
 
 [Sí, en los próximos días]  [Sí, en el próximo mes]  [Solo estoy explorando]
```

Si elige una de las primeras opciones, la app agenda una notificación push para ese período. La notificación aparece como:

```
"Tu celular viejo sigue en el cajón?
 El punto más cercano para entregarlo está a X minutos de donde estás ahora."
```

La notificación usa la ubicación actual en el momento de envío, no la del hogar. Esto maximiza la relevancia contextual.

**Por qué funciona**: la implementación intencional ("si X, entonces Y") es una de las intervenciones de cambio de comportamiento con mayor respaldo empírico. Convertir una intención vaga ("voy a botarlo bien") en un plan concreto ("cuando me avisen, voy al punto del centro comercial que queda de camino") aumenta significativamente la probabilidad de ejecución.

---

## 3. Retroalimentación de impacto (cierre del loop)

Después de que el usuario llega a un punto y entrega su RAEE, la app no sabe con certeza que lo entregó — no hay integración con los sistemas de los gestores. La solución es un **check-in voluntario**.

### Flujo post-entrega

24 horas después de que el usuario abrió el detalle de un punto y presionó "Cómo llegar", la app envía una notificación:

```
"¿Pudiste entregar tu [celular viejo]?"
[Sí, lo entregué]  [No pude ir]  [El punto estaba cerrado]
```

Si responde "Sí, lo entregué":

```
🌱 Entregaste aproximadamente 150g de residuos electrónicos.
   Eso es 1 de los 6.000 toneladas que Colombia recupera por año.
   
   En tu zona, X personas entregaron RAEE este mes.
```

**Elementos comportamentales en esta pantalla:**
- **Retroalimentación de impacto**: el peso estimado hace tangible una acción que de otro modo es abstracta. El equivalente ambiental conecta la acción individual con el sistema.
- **Norma descriptiva local**: "X personas en tu zona" activa comparación social positiva sin ser competitiva. El número debe ser real (calculado de check-ins en la misma zona) — si es bajo, no se muestra.
- **No hay puntos, badges ni gamificación**: en contextos de motivación intrínseca alta, la gamificación extrínseca puede erosionar la motivación existente (efecto de sobreJustificación). El feedback es informativo, no recompensador.

### Si responde "El punto estaba cerrado":

```
"Gracias por avisarnos. Vamos a verificar la información de ese punto."
[¿Querés buscar otro punto cercano ahora?]
```

Este flujo convierte una experiencia negativa en dato útil para la base de datos (actualiza `reportes`) y ofrece recuperación inmediata en lugar de dejar al usuario varado.

---

## 4. Normas sociales — implementación específica

Las normas descriptivas funcionan cuando son locales, concretas y creíbles. "Millones de personas reciclan" no mueve la conducta. "47 personas en Chapinero entregaron RAEE este mes" sí tiene potencial.

**Regla de implementación**: la norma solo se muestra si hay datos reales de esa zona. Si los check-ins de un barrio son < 5 en el último mes, no se muestra ninguna cifra — el silencio es mejor que una norma que normaliza la inacción.

**Dónde aparece la norma:**
- Pantalla de resultado post check-in (ver sección 3)
- Opcionalmente: en el detalle del punto, como "X personas entregaron RAEE aquí en los últimos 30 días"

**Dónde NO aparece:**
- En la pantalla de inicio (es información irrelevante para alguien que todavía no usó el servicio)
- En notificaciones push (el contexto no es el adecuado)

---

## 5. Reducción de fricción en puntos críticos del flujo

| Momento de fricción | Riesgo conductual | Intervención |
|---|---|---|
| El usuario no sabe en qué categoría entra su objeto | Abandono en la primera pantalla | Objetos visuales, no categorías técnicas |
| El usuario activa la app y la geolocalización no está permitida | No puede ver puntos cercanos; posible abandono | Pedir permiso con explicación de para qué se usa; fallback: búsqueda por barrio o dirección |
| Horario no disponible en el punto | Viaje fallido → abandono permanente | Badge de confianza + advertencia explícita de dato no verificado |
| El punto más cercano queda lejos de la ruta habitual | Percepción de que "no vale la pena" | Mostrar también puntos cercanos a lugares frecuentes (trabajo, centro comercial habitual) — requiere onboarding opcional de 1 pregunta |
| El usuario entrega el RAEE y no pasa nada | El comportamiento queda sin refuerzo | Check-in voluntario + feedback de impacto (sección 3) |
| El usuario intenta por segunda vez y el sistema falló antes | Desconfianza acumulada | Mostrar fecha de última verificación del punto prominentemente |

---

## 6. Onboarding — mínimo viable

El onboarding no debe pedir más de lo estrictamente necesario. Cada campo adicional reduce la tasa de completación.

**Lo que se pregunta al entrar por primera vez:**

```
Pantalla 1: "¿En qué ciudad estás?"
            (selector; se puede omitir si el GPS ya está activo)

Pantalla 2: "¿Tenés algún dispositivo que querés desechar próximamente?"
            [Sí]  [No, solo estoy explorando]
            (si Sí → opción de recordatorio, ver sección 2)
```

**Lo que NO se pregunta:**
- Nombre
- Email (hasta que haya una razón real para pedirlo — el MVP no la tiene)
- Cuántos dispositivos tiene
- Frecuencia con que cambia dispositivos

La cuenta de usuario es opcional y se propone solo cuando hay un beneficio concreto para el usuario: "Creá una cuenta para guardar tus puntos favoritos y ver tu historial de entregas."

---

## 7. Principios de diseño comportamental — checklist para decisiones futuras

Cada nueva funcionalidad debe pasar por estas preguntas antes de implementarse:

1. **¿Reduce o aumenta la fricción en el camino hacia la entrega?** Si aumenta, justificar explícitamente.
2. **¿El default lleva hacia la acción o hacia la inacción?** (ej: notificaciones activadas por defecto, no desactivadas)
3. **¿El feedback es informativo o recompensador?** Preferir informativo para no erosionar motivación intrínseca.
4. **¿La norma social mostrada es real y local?** Si los datos no lo soportan, no mostrar la norma.
5. **¿El mensaje de error o dato faltante gestiona expectativas honestamente?** No dejar campos vacíos donde el usuario podría asumir que hay información.
