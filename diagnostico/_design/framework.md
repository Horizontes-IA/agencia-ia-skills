# Framework de Diagnóstico — el motor analítico de `/diagnostico`

> Este documento define CÓMO el skill piensa: qué entrevista, cómo rankea procesos, cómo estima ROI sin inventar precisión falsa, y qué investiga en web para sentirse consultoría real y no plantilla. El esquema de datos que produce esto vive en `schema.md` (el contrato con el generador de reporte).

## 0. Principio rector

El usuario instala el skill, lo entrevistan ~6-9 minutos, y recibe un paquete de consultoría de ~$2,000 USD: un diagnóstico de su negocio con sus procesos rankeados, las 3 automatizaciones que más le mueven la aguja (con arquitectura, herramientas, costo y ROI), un quick-win construible HOY, y un roadmap de 90 días. El "wow" no es el texto — es **reconocerse** ("esto es MI negocio, no un ejemplo genérico") y **ver el número** ("recupero 31 horas/mes ≈ $1,240").

Tres reglas que tiñen todo el motor:

1. **Lenguaje del cliente, no del consultor.** La audiencia (n=7,600 leads) dice "se me va medio día respondiendo cotizaciones casi iguales", no "tengo un cuello de botella en mi proceso de pre-venta". El diagnóstico les devuelve SUS palabras estructuradas. Eso es el reconocimiento.
2. **Conservador y defendible > impresionante y falso.** Todo número de ROI lleva un *haircut* explícito y supuestos visibles. Un consultor senior nunca dice "te ahorro 40 horas"; dice "estimando conservador, ~24-31 horas/mes, asumiendo X e Y". Esto construye confianza, no la quema.
3. **Ordena el caos, suave hacia la comunidad.** El dolor #1 (50%) del público es "no sé por dónde empezar". El diagnóstico lo ataca de frente: pone orden con una ruta priorizada y un quick-win construible hoy. Nunca empuja; entrega valor y, al final, abre la puerta a la comunidad como acompañamiento.

---

## 1. Las dimensiones del diagnóstico (qué cubre la entrevista)

Un diagnóstico de consultor real cubre 8 dimensiones. La entrevista NO es un formulario de 8 bloques — es una conversación natural (una pregunta a la vez, estilo `/crear-agente`) que va llenando estas dimensiones. Claude adapta el orden y se salta lo ya respondido. La meta es "data suficiente para ejecutar el pipeline", no rellenar todos los campos.

> Heurística de "data suficiente": se puede ejecutar el pipeline cuando hay **(a)** tipo de negocio + cómo gana dinero, **(b)** al menos 3 procesos descritos con su tiempo/frecuencia aproximados, **(c)** dónde se va más tiempo/dinero (el sangrado), **(d)** stack actual, **(e)** la meta a 90 días. El resto se infiere o se estima con supuestos marcados.

### D1 — Identidad del negocio
Quién es, a qué se dedica, tamaño (solo / con equipo / cuántos), país (afecta moneda, costo hora, herramientas disponibles), y a quién le vende (B2C, B2B, local, online).
*Por qué importa:* todo el reporte se personaliza con esto. El país fija la moneda y el costo-hora de referencia. El tamaño define cómo se encuadra el reporte (un negocio en marcha vs. uno que apenas arranca).

### D2 — Modelo de ingresos + LOS NÚMEROS DUROS (cómo entra el dinero)
Qué vende, ticket promedio, y cómo cobra. Y —el corazón de un ROI **real**— **las cifras duras del negocio** (`negocio.economia`): **ingresos ~mensuales, nómina / costo del equipo, horas trabajadas al mes, leads/mes, ventas/mes (o tasa de cierre), margen grueso y 1-2 KPIs del giro**.
*Por qué importa:* esto es lo que separa un ROI **real** de uno estimado. La nómina ÷ horas da el **costo-hora REAL** del negocio (no un default por país). Los leads × tasa de cierre × ticket dan el **ingreso recuperado REAL**. Sin estos números el modelo cae a supuestos (defaults por país, componente de ingresos omitido) y el diagnóstico se siente genérico.
*Regla:* para **operators** estos números son **data crítica** — la entrevista los pide (con calidez, se pueden estimar). Para **beginners** (aún no facturan) se saltan o se marcan como meta/estimado. **Nunca se inventan**: si el usuario no lo sabe, se deja el campo vacío y el reporte lo dice.

### D3 — Mapa de procesos (el inventario "as-is")
La dimensión central. Se le pide al usuario que liste las tareas repetitivas de su semana: "¿qué haces una y otra vez que se siente mecánico?". Para cada proceso que mencione, Claude indaga 4 atributos mínimos:
- **Frecuencia** (cuántas veces por semana/día)
- **Tiempo por vez** (minutos/horas)
- **Quién lo hace** (el usuario, un empleado, nadie aún)
- **Cómo lo hace hoy** (manual, semi-manual con alguna herramienta)

Áreas a sondear si el usuario no las menciona (checklist mental del consultor, NO se recitan todas):
- **Adquisición / leads**: ¿de dónde llegan clientes? ¿les respondes manual? ¿se te enfrían?
- **Pre-venta / cotización**: ¿cotizas manual? ¿respondes lo mismo muchas veces? *(dolor #1 operativo del dataset)*
- **Atención al cliente / soporte**: ¿contestas las mismas preguntas? ¿WhatsApp/DMs?
- **Entrega / operación**: ¿onboarding manual? ¿reportes? ¿seguimiento?
- **Cobro / facturación / admin**: ¿recordatorios de pago? ¿facturas a mano?
- **Contenido / marketing**: ¿posteas manual? ¿el copy-paste de una app a otra?
- **Datos / reportes**: ¿armas reportes copiando de varios lados?

### D4 — El sangrado (dónde se va el tiempo y el dinero)
La pregunta de oro del consultor: *"Si pudieras clonarte y quitarte UNA tarea de encima para siempre, ¿cuál sería?"* y *"¿qué te hace perder clientes o dinero hoy?"*. Esto revela el dolor emocional, no solo el operativo — y suele ser el quick-win.
*Por qué importa:* el ranking objetivo (§2) se cruza con este "voto emocional" del usuario. Si la fórmula dice A pero el usuario sangra por B, el reporte lo nombra explícitamente y suele elegir B como quick-win por momentum psicológico.

### D5 — Stack actual (qué herramientas ya usa)
Qué apps/herramientas usa hoy (muchos: solo WhatsApp + ChatGPT + Excel/Sheets). Qué sabe usar. Si ya pagó por algo que no usa.
*Por qué importa:* las automatizaciones recomendadas deben **encajar con lo que ya tiene** o ser un salto mínimo. Recomendar Salesforce a quien usa una libreta es mal diagnóstico. También detecta gasto desperdiciado (suscripciones zombi).

### D6 — Nivel técnico y de autonomía
¿Programa? (casi nadie — "no sé programar" ya no es el bloqueo). ¿Quiere construirlo él mismo o que alguien se lo haga? ¿Cuánto tiempo a la semana puede dedicarle a implementar?
*Por qué importa:* calibra la complejidad recomendada y el formato del roadmap. Define si el hand-off natural es "tú lo construyes con `/crear-agente`" o "esto te conviene contratarlo/delegarlo".

### D7 — Restricciones (presupuesto, tiempo, riesgo)
Cuánto puede invertir en herramientas/mes. Cuánto tiempo tiene. Qué NO está dispuesto a automatizar (ej. el trato humano con clientes premium). Sensibilidad a que "suene a bot".
*Por qué importa:* el modelo de costo (§3) y la selección de herramientas deben caber en el presupuesto. Un agente de $200/mes para quien factura $800/mes es irresponsable.

### D8 — La meta a 90 días (el norte)
¿Qué quiere lograr en 3 meses? Las metas reales del público: recuperar X horas, dejar de perder leads, ordenar la operación, crecer sin contratar más gente. Esto orienta TODO el roadmap.
*Por qué importa:* el roadmap de 90 días se construye hacia atrás desde esta meta. Si la meta es "dejar de perder leads", el roadmap arranca por la automatización que captura y responde leads, no por el back-office.

---

## 2. Rúbrico de scoring de procesos (qué automatizar primero)

Cada proceso del inventario (D3) recibe un **Score de Priorización (0-100)**. Es la columna vertebral analítica: convierte una lista subjetiva en un ranking defendible. Inspirado en las matrices impacto×esfuerzo de consultoría pero adaptado a automatización con IA y a negocios pequeños de LATAM.

### Los 5 factores (cada uno 0-5)

| Factor | Qué mide | Cómo se puntúa (0-5) |
|---|---|---|
| **Sangrado** (`bleed`) | Cuánto tiempo/dolor consume hoy = horas/mes que se va | 0 = trivial · 5 = "me come medio día / muchas horas/semana" |
| **Frecuencia** (`frequency`) | Qué tan seguido ocurre (más repetición = más ROI de automatizar) | 0 = esporádico · 3 = semanal · 5 = diario/varias-veces-al-día |
| **Automatabilidad** (`automatability`) | Qué tan factible es automatizarlo con IA/no-code HOY | 0 = requiere juicio humano profundo · 5 = regla clara y repetible (responder, clasificar, cotizar, agendar) |
| **Impacto en ingresos** (`revenue_impact`) | Si automatizar esto gana/protege dinero (no solo ahorra tiempo) | 0 = puro back-office · 3 = ahorra tiempo facturable · 5 = recupera leads/ventas que hoy se pierden |
| **Velocidad a valor** (`speed_to_value`) | Qué tan rápido se ve el resultado (quick-win vs proyecto) | 0 = semanas de setup · 5 = funcionando en un día |

### La fórmula

El score combina dos ideas: **el valor de automatizarlo** (sangrado × frecuencia, ponderado por impacto en ingresos) y **la viabilidad** (automatabilidad × velocidad). Un proceso solo sube si ambas son altas — exactamente la lógica "quick win" de la matriz impacto×esfuerzo.

```
valor      = (bleed × 0.40) + (frequency × 0.25) + (revenue_impact × 0.35)     # 0-5
viabilidad = (automatability × 0.60) + (speed_to_value × 0.40)                  # 0-5

score = round( (valor × 0.60 + viabilidad × 0.40) / 5 × 100 )                   # 0-100
```

- **valor** pesa más (0.60) que **viabilidad** (0.40): preferimos atacar dolor real aunque sea un poco más de esfuerzo, antes que automatizar algo trivial solo porque es fácil.
- Dentro de valor, `bleed` (0.40) y `revenue_impact` (0.35) dominan: el público quiere recuperar tiempo Y ganar dinero, no eficiencia abstracta.
- Dentro de viabilidad, `automatability` (0.60) manda: de nada sirve que sea rápido si en realidad no se puede automatizar bien con las herramientas de hoy.

### Bandas de interpretación (lo que ve el usuario)

| Score | Banda | Etiqueta en el reporte |
|---|---|---|
| 75-100 | 🟢 Automatiza ya | "Esto es lo primero. Máximo retorno, mínimo riesgo." |
| 55-74 | 🟡 Alto potencial | "Vale mucho la pena, en tu fase 2." |
| 35-54 | 🟠 Más adelante | "Buena, pero hay cosas más urgentes primero." |
| 0-34 | ⚪ No prioritario | "No vale la pena automatizar esto aún." |

### Tie-breakers y el voto emocional

- Empate de score → gana mayor `speed_to_value` (momentum psicológico para el público paralizado).
- El **proceso que el usuario nombró en D4** ("la tarea que me quitaría de encima") recibe un flag `user_flagged: true`. Si su score está dentro de 10 puntos del #1, **ese se convierte en el quick-win** aunque no sea el #1 absoluto — porque construir lo que el usuario sangra genera el "wow" y el momentum que el #1 técnico puede no dar.

### Cómo Claude asigna los 0-5 (anti-inventar)

Claude NO inventa los puntajes: los deriva de lo que el usuario dijo en la entrevista. `bleed` y `frequency` salen directos de "tiempo por vez × veces por semana". `automatability` se calibra contra patrones conocidos (responder mensajes/cotizar/agendar/clasificar/generar contenido = alta; negociar/diseñar estrategia/relación humana = baja). `revenue_impact` sube si el proceso toca leads/ventas/cobro. Cada proceso guarda un campo `score_rationale` de una línea explicando el puntaje — esto es lo que hace que se sienta razonado, no aleatorio.

---

## 3. Modelo de ROI (defendible, sin precisión falsa)

El error fatal sería decir "te ahorro 40 horas y $5,000/mes" con falsa precisión. Un consultor senior modela **conservador, con supuestos visibles y en rangos**. Adoptamos la metodología estándar de business case de automatización: baseline → beneficio con *haircut* → costo total → y siempre un escenario conservador.

### 3.1 Horas ahorradas/mes (por proceso automatizado)

```
horas_brutas_mes = (tiempo_por_vez_min × veces_por_semana × 4.33) / 60

# HAIRCUT obligatorio: la automatización casi nunca elimina el 100% de la tarea.
# Sigues revisando, interviniendo, manejando casos raros. El estándar de la
# industria es modelar 50-70% del ahorro teórico. Usamos un factor de captura
# según automatabilidad:

factor_captura =
    0.70  si automatability >= 4   (tarea muy automatizable)
    0.55  si automatability == 3   (semi-automatizable, revisión frecuente)
    0.40  si automatability <= 2   (mucho humano en el loop)

horas_ahorradas_mes = round( horas_brutas_mes × factor_captura, 1 )
```

> Esto es lo que hace defendible el número: el reporte SIEMPRE muestra "de las ~X horas brutas, estimamos recuperar ~Y reales (factor de captura Z%) porque seguirás revisando casos". Honestidad = confianza.

### 3.2 Valor en dinero del tiempo

```
# PRIORIDAD — el número REAL gana; el default por país es el ÚLTIMO recurso:
costo_hora =
    economia.nomina_mes_usd / economia.horas_trabajadas_mes   # 1) REAL — derivado de la nómina del negocio
    || D2.costo_hora_usuario                                   # 2) el número que el usuario dé directo
    || default_por_pais(D1.pais)                               # 3) último recurso (se marca editable en el reporte)

# Se guarda cuál se usó en costo_hora_fuente ("nomina_real" | "dato_usuario" | "default_pais").
# CLAVE: con nómina real el costo-hora NO es un supuesto — es la cifra del negocio, y el reporte
# lo presenta como dato ("tu hora cuesta ~$X, según tu nómina"), no como estimación. SOLO cuando
# cae al #3 el reporte muestra "asumimos ~$X/hora; ajústalo si tu hora vale más".

valor_tiempo_mes = horas_ahorradas_mes × costo_hora
```

**Defaults de costo-hora por país** (USD, conservadores; **solo si el usuario NO dio nómina ni su propio número** — es el fallback, no lo preferido):

| País | Costo-hora default (USD) | Nota |
|---|---|---|
| México | $8 | factura <$2k/mes mayoría |
| Colombia / Perú / Argentina / Ecuador | $6 | |
| US (diáspora latina) | $20 | |
| España | $15 | |
| Otro LATAM | $7 | fallback |

> El reporte marca el costo-hora como **supuesto editable**: *"Asumimos que tu hora vale ~$X. Si vale más, multiplica el ahorro."* Nunca se presenta como hecho.

### 3.3 Valor por ingresos recuperados (solo si `revenue_impact >= 4`)

Para procesos que recuperan leads/ventas perdidas (ej. responder leads que hoy se enfrían), se modela un segundo componente, MUY conservador:

```
# Se ANCLA en los números reales de `economia` (nada inventado):
tasa_cierre   = economia.tasa_cierre_pct / 100
                || (economia.ventas_mes / economia.leads_mes)     # REAL — derivada del embudo del negocio
ticket        = negocio.modelo_ingresos.ticket_promedio_usd        # REAL — el ticket que dio el usuario
leads_perdidos_mes = los que hoy se enfrían por el cuello (ej. "27 pedidos grandes/mes que se te van por tardar")

leads_recuperados_mes  = leads_perdidos_mes × 0.20                 # capturas 1 de cada 5 (haircut conservador)
ingreso_recuperado_mes = leads_recuperados_mes × tasa_cierre × ticket
```

> Cada factor de esta fórmula es un dato que el usuario dio (leads, ventas, ticket). El reporte muestra el desglose ("de los ~27 que se enfrían, recuperas ~5; a tu cierre de X% y ticket de $Y = $Z/mes"). Si falta ALGÚN factor, se omite el componente completo (NO se inventa) y se dice cualitativamente *"además, dejarías de perder leads por no responder a tiempo — no lo cuantificamos por falta de datos, pero suele ser el mayor retorno oculto"*. **Nunca se inventa un número de ingresos.**

### 3.4 Costo de la automatización (TCO mensual)

```
costo_herramientas_mes = suma de tools recomendadas (ver §4 benchmarks de precios)
costo_setup_unico      = estimado en horas-de-construcción × (gratis si lo hace él con Claude Code)
costo_api_mes          = estimado de uso de IA (tokens) — casi siempre <$5/mes a este volumen
```

El reporte distingue **"si lo construyes tú"** (setup ≈ $0, solo herramientas + API) vs **"si lo contratas"** (lo que costaría que alguien te lo construya).

### 3.5 El número headline y el payback

```
ahorro_total_mes = Σ (valor_tiempo_mes + ingreso_recuperado_mes) de las 3 automatizaciones
costo_total_mes  = Σ costo_herramientas_mes + costo_api_mes
neto_mes         = ahorro_total_mes − costo_total_mes
payback_dias     = (costo_setup_unico_usd / max(neto_mes,1)) × 30    # si lo contrata; ≈0 si lo construye él
roi_anual_x      = round( (neto_mes × 12) / max(costo_total_mes × 12, 1), 1 )
```

### 3.6 Tres escenarios (sensibilidad — lo que separa un business case creíble)

El reporte presenta SIEMPRE tres números para el ahorro mensual, no uno:

| Escenario | Cómo se calcula | Mensaje |
|---|---|---|
| **Conservador** | factor_captura − 0.15, costo_hora default | "Aun en el peor caso, recuperas esto." |
| **Base** | factor_captura y costo_hora como en §3.1-3.2 | "Lo más probable." |
| **Optimista** | factor_captura + 0.10 (cap 0.90), costo_hora ×1.3 | "Si lo aprovechas bien." |

Presentar el rango ("entre ~$X y ~$Z al mes, más probable ~$Y") es lo que hace que suene a consultor y no a vendedor.

---

## 4. El paso de INVESTIGACIÓN del pipeline (qué busca Claude en web)

Esto es lo que convierte el diagnóstico de "plantilla bonita" a "esto está investigado para MI industria". Durante la ejecución del pipeline, ANTES de escribir las recomendaciones, Claude corre 3-5 búsquedas web dirigidas. Los hallazgos se guardan en `research[]` del JSON con su fuente, y se citan en el reporte.

### Las 3 búsquedas obligatorias

1. **Benchmark de la industria del usuario**
   `"[tipo de negocio] cuánto tiempo se gasta en [proceso #1] / automatización [industria] 2026"`
   → Para anclar el sangrado en datos externos ("estudios del sector [X] reportan que se gastan ~N horas/semana en [tarea]"). Da autoridad.

2. **Ejemplo de cómo competidores/el sector ya automatizan esto**
   `"how [industria] automate [proceso] AI / casos automatización [vertical] [país]"`
   → Para mostrar que NO es teoría: "negocios como el tuyo ya usan [patrón]". Combate el "¿servirá para MI nicho?" (objeción recurrente del dataset).

3. **Precio real y actual de las herramientas recomendadas**
   `"[herramienta] pricing 2026"` (n8n, Make, Twilio/WhatsApp API, OpenAI/Claude API, etc.)
   → Para que el costo del §3.4 sea REAL y actual, no inventado. Los precios cambian; verificarlos al momento es lo que hace serio el reporte.

### Benchmarks de precios pre-cargados (fallback si la búsqueda falla)

Para que el reporte nunca quede sin números, el skill lleva una tabla base (verificada jun-2026; Claude la actualiza con la búsqueda #3 cuando puede):

| Herramienta | Precio referencia 2026 | Nota |
|---|---|---|
| n8n (cloud) | €24/mo Starter · self-host gratis | unlimited workflows desde abr-2026 |
| Make | ~$9-16/mo planes core | verificar, varía por operaciones |
| Zapier | ~$20/mo | el caro; preferir n8n para LATAM |
| Cloudflare Workers/Agents | ~$5/mo | el patrón barato de `/crear-agente` |
| OpenAI API (gpt-5.x mini/nano) | $0.20-$0.75 /M input | a volumen pyme casi siempre <$5/mes |
| Claude API (Haiku 4.5) | $1 in / $5 out por M tokens | |
| Twilio WhatsApp | número $1-15/mo + por conversación | servicio iniciado por user = gratis |
| Pushover | $5 una vez | notificaciones push |

### Regla de oro de la investigación

Si una búsqueda no devuelve algo específico y citable, Claude **NO inventa una estadística**. Marca el campo como estimado (`"source": "estimación propia"`) y baja la confianza del dato. Una cifra inventada que el usuario detecta destruye todo el "wow". Es preferible "no tengo el dato exacto del sector, pero por tu descripción estimo ~N" que un número falso con falsa autoridad.

---

## 5. El pipeline de ejecución (cómo se encadena todo)

Después de la entrevista, Claude ejecuta este pipeline de forma autónoma (mostrando avance, estilo "déjame trabajar en tu diagnóstico..."):

```
1. NORMALIZAR    → limpia el inventario de procesos, normaliza nombres de tools
                   (n8n/N8N→"n8n", Make.com→"Make", etc.)
2. SCORE         → aplica §2 a cada proceso → ranking 0-100 + bandas + rationale
3. INVESTIGAR    → corre §4 (3-5 búsquedas) → llena research[] con fuentes
4. SELECCIONAR   → toma top-3 procesos por score → diseña 1 automatización por cada uno
                   (arquitectura en lenguaje simple + herramientas + costo + ROI §3)
5. QUICK-WIN     → elige el construible-hoy (mayor speed_to_value entre el top-3,
                   o el user_flagged si aplica regla D4) → instrucciones accionables
6. ROI GLOBAL    → agrega §3.5 + escenarios §3.6 → número headline + payback
7. ROADMAP       → 90 días en 3 fases hacia la meta D8 (back-casting)
8. HAND-OFF      → enruta la #1 por construir_con: n8n/Make (flujo de apps) → curso
                   de la comunidad · claude_code (sistema a la medida) → /crear-agente
9. EMITIR JSON   → escribe diagnostico.json (esquema en schema.md)
10. GENERAR      → python3 scripts/generar_reporte.py diagnostico.json <out> → reporte.html
```

### El hand-off de construcción — un ROUTER, no un funnel

El "wow" final no es solo el reporte — es la oferta de **construir la automatización #1 ahí mismo, con la herramienta que le TOCA** (no siempre Claude Code). Al cerrar, Claude enruta según `construir_con`:

- **`claude_code`** — un sistema/app/agente a la medida (un CRM propio, una app, un agente que razona y corre 24/7, algo que n8n/Make no hace barato o que quiere ser dueño) → *"¿Lo construimos ahora?"* → invoca `/crear-agente` con el contexto ya cargado (no re-entrevista).
- **`n8n` / `make`** — un flujo de conectar apps (cuando pasa X, haz Y; sincronizar, recordatorios, mover datos entre apps) → **NO lo mandes a Claude Code:** oriéntalo al curso y las plantillas de n8n/Make de la comunidad, y esboza el flujo (disparador → pasos → acción).
- **Siempre** → cierra hacia la meta D8 y, suave, hacia la comunidad: *"Esto es el inicio de tu ruta. En Horizontes IA te acompaño a construir las 3 —con la herramienta de cada una—."* Sin presión, sin countdown.

---

## 6. Calibración por segmento (el mismo motor, distinto encuadre)

El motor es uno; el encuadre del reporte cambia según D6/D1 (alineado con los 2 segmentos del público):

- **Beginner** — está arrancando su propio negocio/emprendimiento. El reporte ENFATIZA la ruta ordenada y el quick-win súper accionable. Encuadre: "deja de saltar entre tutoriales, esta es TU secuencia".
- **Operator** — ya tiene un negocio en marcha. El reporte ENFATIZA ahorro de horas internas y ROI en dinero (recupera tu medio día de cotizaciones). Encuadre: "contrata a tu primer empleado digital".

Claude detecta el segmento en la entrevista (D1+D2+D6) y setea `segment` en el JSON; el generador de reporte usa ese campo para elegir copys de encuadre.

---

## 7. Garantías de calidad del motor (checklist antes de emitir)

Antes de escribir el JSON, Claude valida:

- [ ] ≥3 procesos con bleed/frequency reales (no inventados) → si no, sigue entrevistando.
- [ ] Cada proceso top-3 tiene `score_rationale` no vacío.
- [ ] Cada número de ROI tiene su supuesto visible y su haircut aplicado.
- [ ] research[] tiene ≥2 fuentes citables; las no citables marcadas como estimación.
- [ ] El quick-win es realmente construible en ≤1 día con el stack del usuario.
- [ ] Costo total mensual ≤ presupuesto declarado (D7); si no, se ajustan herramientas.
- [ ] Ningún número de ingresos inventado sin datos del usuario.
- [ ] El encuadre coincide con el `segment` detectado.
- [ ] El tono es 2ª persona, español neutro LATAM, cálido-experto, SIN pushy.

---

## Fuentes (metodología de §1-§4)

- Process discovery / discovery playbook de consultoría — [Kognitos](https://www.kognitos.com/blog/process-discovery-guide/), [Navvia](https://navvia.com/blog/understand-your-processes-through-identification-process-discovery), [Consulting Discovery Playbook 2026 (Medium)](https://medium.com/@avery.brooks_59610/consulting-discovery-playbook-2026-the-30-day-framework-top-firms-use-to-standardize-discovery-56a8f305a9c4)
- Identificación de cuellos de botella — [Workato](https://www.workato.com/the-connector/identify-bottlenecks-in-a-process/)
- Modelo de ROI / haircut / sensibilidad — [Auditic ROI Calculator](https://auditic.app/blog/Automation-ROI-Calculator), [SolvSpot: estimar horas antes de construir](https://solvspot.com/blog/ai-automation-roi-estimation), [Wiss: financial justification](https://wiss.com/manufacturing-automation-roi-financial-justification/)
- Matriz de priorización impacto×esfuerzo / 5 criterios — [Action Priority Matrix (MindTools)](https://www.mindtools.com/agst6d0/the-action-priority-matrix/), [Cómo priorizar proyectos de IA 2026 (FountainCity)](https://fountaincity.tech/resources/blog/a-strategic-framework-for-how-to-prioritize-ai-projects/), [NN/g prioritization methods](https://www.nngroup.com/articles/prioritization-methods/)
- Precios de herramientas 2026 — [n8n pricing](https://n8n.io/pricing/), [OpenAI API pricing](https://openai.com/api/pricing/), [Twilio WhatsApp 2026 (Chatarmin)](https://chatarmin.com/en/blog/twilio-whats-app-api)
