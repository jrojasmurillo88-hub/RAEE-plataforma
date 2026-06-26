# 05 · Modelo de Negocio

## Lógica central

El producto tiene dos horizontes de valor que coexisten desde el inicio y no se contradicen:

1. **Horizonte operativo**: sostenibilidad financiera propia — el producto genera ingresos suficientes para mantenerse y crecer sin depender de donaciones permanentes.
2. **Horizonte estratégico**: el producto como activo transferible — la plataforma, los datos y la metodología pueden venderse o licenciarse a un actor institucional (PNUD, MinAmbiente, ANDI) como parte de un proceso de consultoría.

La narrativa de impacto es el activo que habilita ambos horizontes. Sin datos reales de uso y disposición, ninguno de los dos funciona.

---

## 1. Propuesta de valor por actor

| Actor | Problema que resuelve la plataforma | Disposición a pagar |
|---|---|---|
| **Ciudadano** | Dónde botar qué, sin buscar en 6 páginas diferentes | Baja — el servicio debe ser gratuito para maximizar adopción y datos |
| **Sistemas de posconsumo** (EcoCómputo, Lito, etc.) | Sus puntos no son encontrados por los ciudadanos; sus metas de recolección dependen del volumen que llega | Media-alta — dependen de la afluencia para cumplir metas regulatorias |
| **Empresas con obligación REP** | Deben demostrar ante ANLA que sus productos tienen sistema de recolección activo; necesitan datos de disposición para sus reportes | Alta — el incumplimiento tiene sanciones económicas |
| **Municipios y CAR** | Necesitan monitorear cobertura territorial y tasas de disposición para reportes ambientales | Media — depende del presupuesto disponible |
| **Actores institucionales** (PNUD, GEF, cooperación internacional) | Necesitan infraestructura de datos para proyectos de economía circular; no quieren construirla desde cero | Alta — si el producto ya tiene datos y metodología probada |

---

## 2. Modelo de ingresos — horizonte operativo

### Capa gratuita (ciudadano)

El ciudadano nunca paga. Esta es una restricción de diseño, no una decisión financiera: cobrar al ciudadano añade fricción en el eslabón más débil de la cadena y reduce los datos de uso que son el activo central del negocio.

### Fuente 1 — Visibilidad premium para sistemas de posconsumo

Los sistemas de posconsumo pagan una suscripción mensual/anual para:
- Aparecer destacados en los resultados de búsqueda del usuario
- Acceder a un dashboard con métricas de su red de puntos (visitas, check-ins, reportes ciudadanos)
- Recibir alertas cuando un punto de su red recibe reportes negativos

**Precio referencia**: $200–500 USD/mes por sistema. Con 4–5 sistemas suscritos, cubre costos operativos básicos.

**Por qué pagarían**: su modelo de negocio depende de que los ciudadanos lleven RAEE a sus puntos. La plataforma es un canal de adquisición directo hacia su meta de recolección.

### Fuente 2 — Datos de disposición para empresas con obligación REP

Las empresas importadoras y fabricantes registradas en RPCAEE deben reportar anualmente a la ANLA cuánto RAEE de sus productos fue recolectado. Hoy eso es difícil de medir.

La plataforma puede ofrecer:
- Informes de disposición por marca/categoría de producto, basados en check-ins y datos de los sistemas
- Certificado de participación en el sistema de recolección para sus reportes de sostenibilidad

**Precio referencia**: $500–2.000 USD/año por empresa. Este segmento escala bien porque el número de empresas obligadas es grande (todo importador/fabricante de AEE en Colombia).

**Advertencia**: este modelo requiere que los datos de check-in tengan suficiente volumen para ser estadísticamente útiles. Es una fuente de ingresos de Fase 2, no del MVP.

### Fuente 3 — Dashboard institucional para municipios y CAR

Versión de la plataforma orientada a gestores territoriales: mapa de cobertura, brechas de puntos por localidad, evolución temporal de disposición.

**Precio referencia**: $1.000–5.000 USD/año por entidad. Licitaciones o contratos de prestación de servicios.

**Advertencia**: el ciclo de venta institucional es largo (6–18 meses). Esta fuente es de Fase 3. En MVP, se puede preparar la narrativa y los datos, pero no depender de estos ingresos.

---

## 3. Modelo de exit / consultoría — horizonte estratégico

### El activo que se vende

No es solo el código — es la combinación de:
- **Base de datos unificada de puntos RAEE** con historial de verificación
- **Metodología de extracción y actualización** (los scrapers + el pipeline)
- **Datos de comportamiento ciudadano** (patrones de búsqueda, check-ins, reportes)
- **Diseño comportamental** validado en campo
- **Conocimiento del ecosistema** (relaciones con sistemas de posconsumo, comprensión regulatoria)

Ninguno de estos activos existe hoy en Colombia de forma agregada y verificada. Eso es la ventaja.

### Actores compradores potenciales

**PNUD Colombia / PNUMA**
El PNUD tiene programas activos de economía circular y gestión de residuos en América Latina. Una plataforma con datos reales y metodología probada encaja como herramienta de un proyecto regional. El modelo de compra típico es un contrato de consultoría + transferencia de tecnología, no una adquisición tradicional.

**MinAmbiente / ANLA**
El Estado tiene interés en tener visibilidad sobre el sistema RAEE, pero no tiene capacidad técnica para construirlo. Una plataforma ya operativa con datos puede convertirse en herramienta oficial mediante convenio o contrato interadministrativo.

**ANDI / Grupo Retorna**
Los sistemas de posconsumo agrupados en ANDI podrían adquirir la plataforma como infraestructura compartida para toda la alianza, reemplazando sus páginas individuales.

**Fundaciones corporativas con mandato ambiental**
Empresas como Bancolombia, EPM o Bavaria con compromisos de sostenibilidad pueden financiar la operación como parte de su estrategia de impacto, con o sin transferencia de propiedad.

### Condición para que el exit sea posible

El comprador institucional necesita ver:
1. **Datos reales de uso** — no un prototipo en blanco; mínimo 6 meses de operación con usuarios reales
2. **Impacto medible** — kilogramos de RAEE atribuibles a la plataforma, aunque sea de forma aproximada
3. **Metodología documentada** — los archivos de este proyecto son parte de ese activo

Por eso la secuencia correcta es: construir → operar → medir → vender/transferir. No al revés.

---

## 4. Financiamiento de la fase inicial

El MVP no genera ingresos por varios meses. Las opciones para sostener ese período:

| Fuente | Monto potencial | Tiempo de acceso | Condición |
|---|---|---|---|
| **Fondos de innovación social** (iNNpulsa, Apps.co) | $5.000–20.000 USD | 3–6 meses | Aplicación a convocatoria; encaja bien con perfil de impacto |
| **Cooperación internacional** (USAID, GEF Small Grants, UE) | $10.000–50.000 USD | 6–12 meses | Requiere propuesta técnica; los archivos de este proyecto son la base |
| **Aceleradoras de impacto** (Yunus Social Business, Socialab) | Mentorship + $0–15.000 USD | 3–6 meses | Equity o sin equity dependiendo del programa |
| **Autofinanciamiento** (consultoría paralela) | Variable | Inmediato | El fundador sostiene el proyecto con ingresos de consultoría mientras construye el MVP |

**Recomendación de secuencia**: autofinanciamiento + Apps.co para las primeras 10 semanas (construcción del MVP), luego cooperación internacional para la fase de crecimiento una vez haya datos reales.

---

## 5. Métricas de negocio para la narrativa de inversores / compradores

| Métrica | Por qué importa |
|---|---|
| **Kg de RAEE atribuibles a la app** | La métrica de impacto central — es lo que compra un actor institucional |
| **Puntos de recolección indexados** | Muestra cobertura y esfuerzo de construcción del dataset |
| **Usuarios activos mensuales** | Tracción de producto |
| **Tasa de check-in** (usuarios que reportan haber entregado) | Proxy de conversión real, no solo intención |
| **Costo por kg de RAEE** | Eficiencia de la intervención vs. campañas tradicionales |
| **Tiempo de actualización del dato** | Ventaja competitiva sobre páginas estáticas de los sistemas |

El último indicador — tiempo de actualización — es la ventaja estructural frente a cualquier competidor. Un sistema que actualiza semanalmente de forma automática siempre va a tener datos más confiables que una página que actualiza manualmente cuando alguien se acuerda.

---

## 6. Resumen del modelo en una oración por actor

- **Al ciudadano**: gratis, sin fricción.
- **A los sistemas de posconsumo**: más ciudadanos en sus puntos, a cambio de visibilidad pagada.
- **A las empresas REP**: datos que les ayudan a cumplir su obligación regulatoria.
- **Al Estado / PNUD**: infraestructura de datos lista para usar, construida por alguien que entiende el ecosistema.
