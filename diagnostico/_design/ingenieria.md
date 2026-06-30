# Ingeniería del Skill `/diagnostico`

> Spec técnico del skill. Define la estructura del `SKILL.md`, el enfoque del generador de reporte (Python stdlib → HTML), instalación/distribución, y manejo de la carpeta de salida. Pensado para que los demás agentes (entrevista, schema, generador, plantillas, ejemplo, README) construyan piezas que encajan sin fricción.
>
> Fuentes de verdad que este spec respeta:
> - Patrón de skill de Santi: `~/.claude/skills/crear-agente/` (frontmatter, fases, install.sh/ps1, README, tono).
> - Data de audiencia: `scraperskool/.funnel-analysis/FINAL-REPORT.md` (dolor #1 "no sé por dónde empezar" 50%, deseo "empleado 24/7", beginner 69% / operator 20%).
> - Best practices Claude Code Skills (ver §6).

---

## 0. Filosofía del skill en una línea

El usuario instala el skill, dice "diagnostica mi negocio", y el skill lo **entrevista como un consultor senior**, luego **ejecuta un pipeline completo** (investiga → diagnostica → calcula ROI → escribe `diagnostico.json` → corre `generar_reporte.py` → escribe docs markdown → presenta) que termina en una **carpeta `diagnostico-<negocio>/` con un `reporte.html` premium** dark+cyan, y ofrece **construir la automatización #1 ahí mismo** (scaffolding o hand-off a `/crear-agente`).

El "wow" NO es texto: es recibir un **paquete de consultoría de ~$2,000 en minutos**, con su nombre/negocio, que mata su dolor #1 (parálisis "no sé por dónde empezar").

**Regla rectora anti-pushy**: entregar valor real PRIMERO, siempre. El CTA a la comunidad es la última línea, suave, opcional. A quien claramente no califica (hobby, sin negocio), no se le empuja Skool — se le da igual su diagnóstico y se le sugiere YouTube. Espejo de la regla `low → YouTube` del funnel.

---

## 1. Contrato de archivos (la "shape" del skill instalado)

Estructura final del repo `santmun/diagnostico-skill` (= lo que vive en `~/.claude/skills/diagnostico/` tras instalar):

```
diagnostico-skill/
├── SKILL.md                      ← EL CEREBRO (frontmatter + pipeline). <500 líneas.
├── README.md                     ← qué es + install 1-comando + ejemplo
├── LICENSE                       ← MIT (igual que crear-agente)
├── install.sh                    ← instala a ~/.claude/skills/diagnostico (Mac/Linux)
├── install.ps1                   ← idem Windows PowerShell
├── .gitignore
├── scripts/
│   └── generar_reporte.py        ← stdlib-only, JSON → reporte.html self-contained
├── templates/
│   ├── reporte.html.template      ← plantilla HTML del reporte (Python rellena placeholders)
│   ├── 01-procesos-y-roi.md       ← entregable markdown (procesos detectados + ROI)
│   ├── 02-plan-90-dias.md         ← entregable markdown (roadmap 90 días)
│   ├── 03-stack-recomendado.md    ← entregable markdown (router de herramientas: n8n/Make/Claude Code)
│   ├── 04-quick-win.md            ← spec de la automatización #1 / quick-win (handoff a /crear-agente)
│   └── README.txt                 ← índice del paquete que ve el usuario en su carpeta
├── ejemplo/
│   └── diagnostico.json           ← caso realista lleno (para testear el generador)
├── reference/
│   ├── entrevista.md              ← guion de la entrevista (cargado on-demand)
│   ├── catalogo-automatizaciones.md ← biblioteca de automatizaciones por tipo de negocio + ROI base
│   └── playbook-roi.md            ← cómo estimar horas/$ ahorrados de forma defendible
└── _design/
    ├── ingenieria.md             ← este archivo
    └── schema.md                 ← esquema canónico de diagnostico.json (lo escribe el agente de schema)
```

**Nota de progressive disclosure**: `SKILL.md` NO contiene el guion completo de la entrevista ni el catálogo de ROI. Solo el flujo orquestador y punteros (`reference/entrevista.md`, `reference/catalogo-automatizaciones.md`, `reference/playbook-roi.md`). Claude los lee con `Read` solo cuando entra a esa fase. Esto mantiene `SKILL.md` < 500 líneas y el arranque barato (solo name+description en contexto hasta que se invoca).

**`diagnostico.json`** es el formato pivote: lo PRODUCE la entrevista+diagnóstico (Claude lo escribe), lo CONSUME `generar_reporte.py` y las plantillas markdown. Su esquema canónico vive en `_design/schema.md` (otro agente) — el generador y las plantillas DEBEN leerlo de ahí, no inventar campos. Si schema.md aún no existe cuando construyes, asume el contrato mínimo de §3.

---

## 2. SKILL.md — estructura completa

### 2.1 Frontmatter

```yaml
---
name: diagnostico
description: Diagnostica un negocio o proyecto como un consultor senior de automatización con IA y entrega, en minutos, un paquete de consultoría completo (reporte HTML premium + plan de 90 días + stack recomendado + la automatización #1 lista para construir). Úsalo cuando alguien escriba "/diagnostico", "diagnostica mi negocio", "qué puedo automatizar", "auditá mi negocio", "por dónde empiezo con IA", "ayúdame a saber qué automatizar primero", "haz un diagnóstico de mi negocio", "no sé por dónde empezar con IA", "qué proceso de mi negocio puedo automatizar", "analiza mi negocio y dime qué automatizar", o cualquier variación donde alguien (probablemente principiante LATAM, sin saber programar) está paralizado sin saber qué automatizar primero. El skill entrevista a la persona en lenguaje natural (negocio, tareas repetitivas, horas perdidas, meta de ingresos), detecta cuándo ya tiene data suficiente, investiga su industria, calcula el ROI en horas y dinero, identifica las 3 automatizaciones de mayor impacto, y genera una carpeta con un reporte HTML de consultoría con su nombre/negocio, un plan de 90 días, y el spec de la automatización #1 — con opción de construirla ahí mismo o pasar a /crear-agente. Español neutro LATAM, cero tecnicismos sin traducir.
---
```

Notas de diseño del frontmatter (alineadas a best practices §6):
- **Tercera persona** ("Diagnostica…", "El skill entrevista…"), no segunda — la consistencia de POV mejora el matching y evita under-triggering.
- **Description rica y "pushy"** (~1000 chars, bajo el límite de 1024): describe QUÉ hace Y CUÁNDO usarlo, con muchas frases-gatillo en lenguaje literal del cliente (sacadas de los `reasons` del funnel: "no sé por dónde empezar", "qué automatizar primero"). Esto combate la tendencia a under-trigger.
- `name: diagnostico` (lowercase, sin tildes, ≤64 chars, sin palabras reservadas).

### 2.2 Cuerpo — secciones (en orden)

1. **Título + qué es** (3-4 líneas).
2. **Cuándo invocar / cuándo NO** — espejo de crear-agente:
   - SÍ: persona quiere saber qué automatizar, está paralizada, quiere auditar su negocio.
   - NO: ya sabe exactamente qué construir y quiere construirlo → mandar directo a `/crear-agente`. Solo quiere teoría → explicación normal. No tiene negocio ni idea de negocio y solo es curiosidad → diagnóstico ligero igual, pero sin empujar nada.
3. **Cómo dirigirte a la persona** — reglas de comunicación + glosario de traducción (reusar el de crear-agente: API key→"llave de acceso", deploy→"publicar en internet", cron→"calendario automático", etc.). Tono: cálido, experto, segunda persona, español neutro LATAM, premium SIN pushy (PROHIBIDO: countdowns, "oferta limitada", "cupos"). Una pregunta a la vez. Confirmar lo entendido.
4. **El pipeline en 7 fases** (§2.3) — el corazón.
5. **Detectar "data suficiente"** (§2.4).
6. **Hand-off de construcción** (§2.5).
7. **Manejo de errores y fallbacks** — incluye el fallback de Python (§4.4).
8. **Reglas duras del skill** (§2.6).
9. **Archivos del skill** — índice con una línea por archivo (para que Claude sepa qué `Read` y cuándo).

### 2.3 El pipeline en 7 fases

> El `SKILL.md` describe cada fase con: objetivo, qué hace Claude, qué archivo `Read` si aplica, y qué le dice al usuario. Las fases 0-1 son conversacionales; 2-6 son ejecución (Claude trabaja, el usuario espera y luego recibe el wow).

**Fase 0 — Bienvenida + encuadre del valor**
Mensaje de apertura que ancla el valor antes de pedir nada (espejo del tono de crear-agente). Plantea: "te voy a hacer unas preguntas como lo haría un consultor que cobra $2,000 por esto, y en minutos te entrego un paquete completo: un reporte de tu negocio, tu plan de 90 días, y la automatización #1 lista para construir". Verifica `python3 --version` en silencio (para decidir generador vs fallback en Fase 4) — NO molestar al usuario con esto; si falla, se usa el fallback sin que lo note.

**Fase 1 — Entrevista (conversacional, lenguaje natural)**
Claude `Read reference/entrevista.md` y conduce la entrevista UNA pregunta a la vez. El guion detallado vive en `reference/entrevista.md` (otro agente lo diseña). El `SKILL.md` solo lista los **ejes mínimos que la entrevista DEBE cubrir** para llenar `diagnostico.json`:
   - Negocio / proyecto (qué vende, a quién, dónde — país).
   - Segmento auto-detectado: beginner (está arrancando su propio negocio/emprendimiento o tiene una idea) / operator (ya tiene negocio en marcha, quiere automatizar interno). Esto bifurca TODO el diagnóstico.
   - Tareas repetitivas que le roban tiempo (la mina de oro — aquí sale "se me va medio día respondiendo cotizaciones").
   - Horas/semana en esas tareas + valor aproximado de su hora (para el ROI).
   - Stack actual (qué herramientas usa — casi siempre "solo ChatGPT").
   - Meta de ingresos / qué haría diferente su vida (ancla la meta del propio negocio).
   - Nivel técnico declarado (para calibrar el lenguaje, no para juzgar).
Después de cada respuesta importante: confirmar lo entendido. No avanzar a Fase 2 hasta tener "data suficiente" (§2.4).

**Fase 2 — Investigación (Claude trabaja)**
Con el negocio claro, Claude investiga: benchmarks de la industria, automatizaciones típicas para ese tipo de negocio, rangos de precio que el mercado paga por esos sistemas. Fuentes: `reference/catalogo-automatizaciones.md` (biblioteca curada por tipo de negocio) + WebSearch si está disponible (opcional, con fallback al catálogo si no hay red). Output interno: lista candidata de automatizaciones con impacto estimado.

**Fase 3 — Diagnóstico + cálculo de ROI (Claude trabaja)**
Claude `Read reference/playbook-roi.md` y:
   - Prioriza las 3 automatizaciones de mayor impacto (matriz impacto × esfuerzo).
   - Para cada una calcula ROI defendible: horas/semana ahorradas → horas/mes → $ ahorrados/mes (horas × valor de la hora) → $ ahorrados/año.
   - Identifica LA automatización #1 (la que Claude recomienda construir primero — usualmente la que mata el dolor textual #1 del segmento: "responder cotizaciones/leads 24/7").
   - Construye la "ruta a recuperar X horas/mes" del propio negocio según segmento.

**Fase 4 — Escribir `diagnostico.json` + correr el generador (Claude trabaja)**
   - Claude escribe `diagnostico-<slug-negocio>/diagnostico.json` siguiendo el esquema de `_design/schema.md` (§3 si no existe aún).
   - Corre: `python3 scripts/generar_reporte.py <ruta>/diagnostico.json <ruta>/` → produce `reporte.html`.
   - Si Python falla o no existe → **fallback** (§4.4): Claude genera `reporte.html` directo leyendo `templates/reporte.html.template` y rellenando los placeholders él mismo con los datos del JSON. El usuario nunca se queda sin reporte.

**Fase 5 — Escribir los docs markdown (Claude trabaja)**
Claude rellena las plantillas de `templates/` con los datos del diagnóstico y las escribe en la carpeta:
   - `01-procesos-y-roi.md` (procesos detectados + ROI)
   - `02-plan-90-dias.md` (roadmap 90 días)
   - `03-stack-recomendado.md` (router de herramientas: n8n/Make/Claude Code)
   - `04-quick-win.md` (spec de la automatización #1 / quick-win — el puente a la construcción)
   - `README.txt` (índice de la carpeta que ve el usuario)

**Fase 6 — Presentar el paquete (el wow)**
Claude resume en chat lo que generó, con los NÚMEROS personalizados (no genéricos): "tu negocio pierde ~X horas/mes en [tarea] = ~$Y/mes. La automatización #1 te recupera eso. Te dejé todo en la carpeta `diagnostico-<negocio>/` — abre `reporte.html` para verlo bonito." Indica explícitamente cómo abrir el HTML (`open reporte.html` en Mac, doble clic en Win). Cierra con el hand-off (Fase 7).

**Fase 7 — Hand-off de construcción** → §2.5.

### 2.4 Detectar "data suficiente"

`SKILL.md` define un check explícito que Claude evalúa tras cada respuesta de la entrevista. Hay data suficiente para pasar a Fase 2 cuando se tienen, como mínimo:
- [ ] Tipo de negocio/proyecto + país.
- [ ] Segmento (beginner/operator) inferido con confianza.
- [ ] Al menos 1 tarea repetitiva concreta + estimado de horas.
- [ ] Meta (ingresos o ahorro de tiempo).

Si falta algo crítico (típicamente la tarea repetitiva concreta o las horas), Claude hace UNA pregunta de seguimiento dirigida, no una lista. Si el usuario es vago ("no sé, lo que sea"), Claude ofrece ejemplos de su industria para destrabar (ataca el dolor #1 "no sé por dónde empezar" en vivo). Tope de seguridad: máximo ~6-8 intercambios antes de ejecutar igual con lo que haya, marcando supuestos en el reporte — nunca dejar al usuario atrapado en preguntas infinitas.

### 2.5 Hand-off de construcción (el cierre que conecta con la construcción)

Tras presentar el paquete, Claude ofrece (sin presionar):

```
Tu automatización #1 — [nombre, ej. "el agente que responde cotizaciones por ti"] —
está especificada en 04-quick-win.md. ¿Quieres que la construyamos ahora mismo?

  1. Sí, constrúyela conmigo  → [hand-off]
  2. Solo quiero el diagnóstico por ahora  → cierre suave
```

- **Si dice que sí** y la automatización es un agente en la nube (lo más común: "que responda/cotice solo 24/7") → **pasar la batuta a `/crear-agente`**, pasándole el contexto ya capturado (negocio, tarea, fuentes, destino, notificación) para que arranque desde Fase 1 sin re-entrevistar. Esto es la sinergia explícita del ecosistema de skills de Santi.
- **Si la automatización no es un agente Cloudflare** (ej. una landing, un CRM, un menú digital) → Claude hace scaffolding básico él mismo o sugiere el skill adecuado.
- **Cierre suave** (siempre, independientemente de la respuesta): UNA línea opcional hacia la comunidad, atada al valor, no a la venta. Ej: "Si quieres que te acompañe a implementar esto en tu negocio, en mi comunidad (Horizontes IA) lo trabajamos juntos." A quien NO calificó (sin negocio, hobby) → NO mencionar Skool; sugerir YouTube. Espejo `high/medium → Skool`, `low → YouTube`.

### 2.6 Reglas duras del skill (las 10)

1. **Entrega valor PRIMERO, siempre.** El paquete se genera completo antes de cualquier CTA.
2. **NUNCA pushy.** Prohibido: countdowns, "oferta", "cupos limitados", urgencia falsa. Premium = calmado.
3. **Números personalizados, nunca genéricos.** El ROI usa los datos REALES de la entrevista. Nada de "ahorra hasta un 80%".
4. **Una pregunta a la vez** en la entrevista. No abrumar.
5. **Confirma lo entendido** tras cada respuesta importante.
6. **Cero tecnicismos sin traducir.** Glosario obligatorio.
7. **El reporte SIEMPRE se genera**, aunque Python falle (fallback) o falten datos (supuestos marcados).
8. **Bifurca por segmento.** Beginner ≠ operator: el diagnóstico, el ROI y la ruta cambian.
9. **CTA atado a calificación.** Califica → Skool suave. No califica → YouTube. Nunca al revés.
10. **Carpeta auto-contenida.** Todo el paquete vive en `diagnostico-<negocio>/`; el `reporte.html` abre sin internet.

---

## 3. Contrato mínimo de `diagnostico.json` (si `schema.md` aún no existe)

El esquema canónico lo define `_design/schema.md`. Mientras tanto, el generador y las plantillas pueden asumir este contrato mínimo (top-level keys). El agente de schema debe ser superset de esto:

```jsonc
{
  "meta": {
    "generado": "ISO-8601",
    "version_skill": "1.0.0",
    "slug": "barberia-carlos"            // usado para nombrar la carpeta
  },
  "negocio": {
    "nombre": "Barbería de Carlos",
    "tipo": "barbería",
    "pais": "México",
    "descripcion": "...",
    "segmento": "operator",              // beginner | operator
    "nivel_tecnico": "principiante",
    "stack_actual": ["ChatGPT", "WhatsApp"]
  },
  "persona": {
    "nombre": "Carlos",                  // se usa en el saludo del reporte
    "valor_hora_usd": 12,                // base del cálculo de ROI
    "meta": "recuperar 10h/semana en mi negocio",
    "meta_tipo": "ingresos"              // ingresos | tiempo
  },
  "dolores": [                            // las tareas repetitivas detectadas
    { "tarea": "responder cotizaciones por WhatsApp", "horas_semana": 10,
      "cita_literal": "se me va medio día respondiendo casi lo mismo" }
  ],
  "roi": {
    "horas_mes_recuperables": 40,
    "ahorro_mensual_usd": 480,
    "ahorro_anual_usd": 5760,
    "valor_paquete_consultoria_usd": 2000   // el "wow" anchor
  },
  "automatizaciones": [                   // 3, ordenadas por impacto
    {
      "rank": 1,
      "nombre": "Agente que responde cotizaciones 24/7",
      "que_hace": "...",
      "impacto": "alto", "esfuerzo": "medio",
      "horas_mes_ahorradas": 40,
      "ahorro_mensual_usd": 480,
      "como_construir": "Cloudflare Agents SDK + OpenAI + WhatsApp",
      "handoff": "crear-agente"           // crear-agente | scaffold | manual
    }
  ],
  "plan_90_dias": [
    { "ventana": "Días 1-30", "objetivo": "...", "pasos": ["...", "..."] }
  ],
  "supuestos": ["si faltó algún dato, se anota aquí"],
  "cta": {
    "califica": true,                      // true → Skool; false → YouTube
    "destino": "https://www.skool.com/horizontes-ia-9992"
  }
}
```

**Regla de oro para el generador**: tolerante a campos faltantes. Cualquier key opcional ausente → sección se omite o muestra un placeholder elegante, NUNCA crashea. Ver §4.3.

---

## 4. El generador: `scripts/generar_reporte.py`

### 4.1 Firma exacta y comportamiento

```
python3 scripts/generar_reporte.py <ruta/al/diagnostico.json> <directorio_salida>
```

- **Argumentos**:
  - `argv[1]` = ruta al `diagnostico.json` de entrada (obligatorio).
  - `argv[2]` = directorio de salida (obligatorio). El script escribe `<dir>/reporte.html`.
- **Stdout en éxito**: ruta absoluta del HTML generado, una línea (`/.../diagnostico-x/reporte.html`). Así Claude la captura para decirle al usuario qué abrir.
- **Exit codes**: `0` éxito; `1` error de uso (args faltantes); `2` JSON inválido/no encontrado; `3` error al escribir el HTML. Cada error imprime a **stderr** un mensaje en español claro Y una marca machine-readable (`FALLBACK_NEEDED`) para que el SKILL.md detecte el fallo y active el fallback de Claude (§4.4) sin ambigüedad.

### 4.2 Restricciones técnicas (duras)

- **SOLO stdlib.** Imports permitidos: `sys`, `json`, `os`, `pathlib`, `html`, `datetime`, `re`. CERO pip installs. Corre en cualquier Mac/Win/Linux con Python 3.8+ out-of-the-box.
- **`python3` Y `python`**: el SKILL.md intenta `python3` primero; si no existe, `python`. El script no asume el binario.
- **HTML self-contained**: un solo `.html`, **CSS inline en `<style>`**, cero CDNs, cero JS externo, cero fuentes remotas (usar font-stack del sistema con fallback a las de marca si están; NO `@import` de Google Fonts porque debe abrir offline). Imágenes: ninguna requerida; si se quiere el logo, embeber como data-URI SVG inline (opcional). Debe abrir con doble clic sin internet.
- **Imprimible a PDF**: incluir `@media print` que fije A4, evite cortes feos (`break-inside: avoid` en tarjetas), y oculte cualquier elemento interactivo. El usuario hace Cmd/Ctrl+P → "Guardar como PDF" y obtiene un entregable de consultoría.
- **Determinista**: misma entrada → mismo HTML (salvo el timestamp de `meta.generado`). Facilita testing con `ejemplo/diagnostico.json`.

### 4.3 Estructura interna (cómo escribirlo, sin sobre-ingeniería)

KISS. Una función por sección, escape SIEMPRE de strings del usuario con `html.escape()` (el nombre del negocio puede traer `&`, `<`). Patrón:

```
load_json(path)         → dict, valida y normaliza (defaults para keys faltantes)
fmt_money(n)            → "$480 USD"
fmt_hours(n)            → "40 h/mes"
section_hero(d)         → str HTML (saludo con persona.nombre + el anchor $2,000)
section_dolor(d)        → str HTML (la tarea + cita literal del usuario)
section_roi(d)          → str HTML (las tarjetas de números: h/mes, $/mes, $/año)
section_automatizaciones(d) → str HTML (las 3 tarjetas, #1 destacada en cyan)
section_plan(d)         → str HTML (timeline 90 días)
section_cta(d)          → str HTML (Skool o YouTube según d.cta.califica)
render(d)               → ensambla la plantilla con todas las secciones
main()                  → parse args, try/except por exit code, escribe archivo, print ruta
```

**Dos enfoques válidos para la plantilla** (elige uno, documenta cuál):
- (A) **Plantilla externa** `templates/reporte.html.template` con placeholders `{{HERO}}`, `{{ROI}}`, etc. → el script lee el template, hace `.replace()`. Ventaja: el fallback de Claude usa el MISMO template (un solo lugar de verdad para el HTML). **Recomendado.**
- (B) HTML embebido como f-string en el `.py`. Más simple pero duplica el HTML entre Python y el fallback.

→ **Usar (A)**. El `.template` es la única fuente del HTML; tanto Python como el fallback de Claude lo rellenan. El placeholder usa un marcador que no colisione con CSS (`{{...}}`, no `{...}`).

### 4.4 Fallback sin Python (crítico — el reporte SIEMPRE sale)

El `SKILL.md`, en Fase 4, instruye:

> Corre `python3 scripts/generar_reporte.py <json> <dir>`. Si el comando falla (exit≠0, imprime `FALLBACK_NEEDED`, o `python3`/`python` no existen), NO te detengas: lee `templates/reporte.html.template`, rellena cada placeholder (`{{HERO}}`, `{{ROI}}`, …) tú mismo con los datos del `diagnostico.json` aplicando las mismas reglas de formato (`$X USD`, `Y h/mes`, escapar `<`,`>`,`&`), y escribe el `reporte.html` resultante con la herramienta Write. El usuario obtiene exactamente el mismo entregable.

Esto hace al skill **robusto en cualquier máquina**: si el alumno no tiene Python (común en Windows fresco), el reporte igual se genera por Claude. La plantilla externa (enfoque A) es lo que hace este fallback trivial — un solo HTML que se rellena por dos caminos.

### 4.5 Testing del generador

`ejemplo/diagnostico.json` es el fixture. Test manual de aceptación:

```
python3 scripts/generar_reporte.py ejemplo/diagnostico.json /tmp/test-diag
open /tmp/test-diag/reporte.html   # Mac
```

Criterios de aceptación: (1) exit 0; (2) `reporte.html` existe y abre offline; (3) muestra el nombre/negocio del ejemplo; (4) las tarjetas de ROI muestran los números del JSON; (5) Cmd+P se ve como un PDF de consultoría limpio; (6) borrar una key opcional del JSON NO crashea (degradación elegante).

---

## 5. Diseño visual del reporte (dark + cyan, premium)

Identidad Horizontes IA. El HTML debe SENTIRSE de $2,000.

- **Paleta**: fondo near-black `#080810`; texto `#E8E8F0`; acento cyan `#00E5FF` (números clave, automatización #1, líneas); cyan tenue `rgba(0,229,255,.12)` para fondos de tarjeta; amarillo highlight `#FFE632` muy puntual.
- **Tipografía**: stack del sistema con fallback a marca, p.ej. `font-family: 'Space Grotesk', -apple-system, 'Segoe UI', system-ui, sans-serif;` (si la fuente no está, el sistema toma el fallback — abre offline igual). Acentos en serif italic opcional.
- **Layout**: ancho máx ~820px centrado (legible + imprime A4). Secciones en orden del wow:
  1. Hero: "Diagnóstico de [Negocio]" + saludo a [persona.nombre] + el anchor "Equivalente a una consultoría de ~$2,000 USD".
  2. El dolor en sus palabras (cita literal — espejo emocional).
  3. Los números (3 tarjetas grandes: horas/mes, $/mes, $/año recuperables) — esto es el gut-punch.
  4. Las 3 automatizaciones (la #1 en tarjeta cyan destacada con badge "Empieza por aquí").
  5. Tu plan de 90 días (timeline).
  6. CTA suave (Skool o YouTube según `cta.califica`).
- **Detalles premium**: tarjetas con `border: 1px solid rgba(0,229,255,.2)`, `border-radius: 14px`, sombras suaves, números en `font-size` grande y peso 700. Una barra de acento cyan a la izquierda de cada sección. `@media print` que aplana a tinta sobre blanco si conviene para PDF, o mantiene el dark (decisión del agente generador; preferir mantener dark pero garantizar contraste).
- **Sin JS.** Todo estático. Cero dependencias.

---

## 6. Best practices de Claude Code Skills aplicadas (resumen accionable)

De la doc oficial y guías 2026:
- **Frontmatter = el único contrato de descubrimiento.** Solo `name`+`description` se cargan al arranque (unos pocos tokens). El cuerpo se lee on-demand al invocar. → invertir en una `description` rica.
- **Tercera persona, action-oriented, con frases-gatillo.** Mejora el matching de intención.
- **Combatir under-triggering siendo "pushy"** en la description (muchos sinónimos/variaciones del trigger). Claude tiende a NO invocar skills cuando debería.
- **Cuerpo < 500 líneas.** Si crece, partir en archivos y referenciarlos (progressive disclosure). Por eso entrevista/catálogo/ROI van en `reference/` y se `Read` solo en su fase.
- **Mantener paths separados** para contextos mutuamente excluyentes (no cargar el catálogo de ROI mientras solo se conversa).
- **Scripts ejecutables para trabajo determinista** (generar el HTML) en vez de pedirle a Claude que produzca HTML largo a mano — más barato y consistente; el fallback cubre el caso sin Python.

Fuentes:
- [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Agent Skills — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skill authoring best practices — Claude Docs](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [anthropics/skills — skill-creator/SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- [Equipping agents for the real world with Agent Skills — Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Claude Code Skills: Progressive Disclosure Step by Step — Daniel Avila](https://medium.com/@dan.avila7/claude-code-skills-progressive-disclosure-step-by-step-3ca02a4a9f60)

---

## 7. Instalación y distribución

Espejo EXACTO de `crear-agente` (mismo público, misma mecánica, consistencia de marca).

- **Repo**: `github.com/santmun/diagnostico-skill` (público, para que el comando 1-liner funcione vía raw).
- **Destino de instalación**: `~/.claude/skills/diagnostico/` (carpeta = `name` del frontmatter).
- **`install.sh`** (Mac/Linux): adaptar el de crear-agente — variables `SKILL_NAME="diagnostico"`, `REPO_URL="https://github.com/santmun/diagnostico-skill.git"`, `TARGET="$HOME/.claude/skills/diagnostico"`. Mismo flujo: detecta OS, verifica `git` y `~/.claude`, `git clone --depth 1`, quita `.git`, mueve a `TARGET`, mensaje final con cómo usarlo y CTA suave a Skool/Twitter. **Diferencia**: NO requiere Node (el skill no construye nada por sí mismo); verificar `python3`/`python` es **opcional** (si falta, el skill usa el fallback) — el instalador puede avisarlo como "recomendado, no obligatorio".
- **`install.ps1`** (Windows): equivalente PowerShell, igual que crear-agente.
- **Comando 1-liner** en README:
  - Mac/Linux: `curl -fsSL https://raw.githubusercontent.com/santmun/diagnostico-skill/main/install.sh | bash`
  - Windows: `irm https://raw.githubusercontent.com/santmun/diagnostico-skill/main/install.ps1 | iex`
- **`README.md`** (estructura espejo de crear-agente): badge cyan; "¿Qué hace?" con ejemplos en bullets ("descubre qué automatizar primero", "calcula cuánto tiempo/dinero pierdes", "te arma tu plan de 90 días", "te recomienda el stack para empezar"); sección Instalación (los 2 comandos); "Cómo usarlo" (`/diagnostico` o "diagnostica mi negocio"); un ejemplo de output (screenshot/descripción del reporte); qué genera (la carpeta + reporte.html); FAQ corto (¿necesito Python? no es obligatorio; ¿necesito saber programar? no); CTA suave a la comunidad. Todo en español, dark+cyan en branding visual.

---

## 8. Manejo de la carpeta de salida

- Claude crea `diagnostico-<slug>/` en el **directorio de trabajo actual** del usuario (donde corre Claude Code), NO dentro del skill. `slug` = `meta.slug` del JSON (kebab-case del nombre del negocio; ej. `diagnostico-barberia-carlos/`).
- Contenido de la carpeta tras el pipeline:
  ```
  diagnostico-barberia-carlos/
  ├── reporte.html          ← el entregable estrella (abrir esto)
  ├── diagnostico.json      ← la data cruda (fuente de verdad, re-generable)
  ├── 01-procesos-y-roi.md
  ├── 02-plan-90-dias.md
  ├── 03-stack-recomendado.md
  ├── 04-quick-win.md       ← el spec que /crear-agente puede consumir
  └── README.txt            ← índice: "abre reporte.html primero"
  ```
- Si la carpeta ya existe (re-diagnóstico), Claude pregunta antes de sobrescribir o sufija con fecha (`-2026-06-23`).
- El último mensaje de Fase 6 SIEMPRE dice la ruta exacta y el comando para abrir el HTML según OS (`open`, `start`, `xdg-open`).

---

## 9. Checklist de implementación (orden sugerido para los demás agentes)

1. `_design/schema.md` — esquema canónico de `diagnostico.json` (superset de §3). **Bloquea a casi todos.**
2. `reference/entrevista.md` — guion de entrevista que llena el schema.
3. `reference/catalogo-automatizaciones.md` + `reference/playbook-roi.md` — la inteligencia del diagnóstico.
4. `templates/reporte.html.template` — el HTML con placeholders `{{...}}` (única fuente del HTML).
5. `scripts/generar_reporte.py` — rellena el template desde el JSON (stdlib-only, §4).
6. `templates/*` — los entregables (01-procesos-y-roi, 02-plan-90-días, 03-stack-recomendado, 04-quick-win + README.txt).
7. `ejemplo/diagnostico.json` — fixture realista (caso operator barbería) para testear 4-5.
8. `SKILL.md` — orquesta todo (§2). Se escribe al final, cuando los archivos a referenciar existen.
9. `README.md`, `install.sh`, `install.ps1`, `LICENSE`, `.gitignore` — distribución (§7), espejo de crear-agente.
