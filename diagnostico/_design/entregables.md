# Entregables del Skill `/diagnostico` — Spec del Paquete + Reporte HTML

> **Para:** el ingeniero que escribe `scripts/generar_reporte.py` y los templates de `templates/`.
> **Qué es esto:** el contrato visual y de contenido del paquete que el pipeline genera tras la entrevista. El generador consume `diagnostico.json` (esquema canónico en `_design/schema.md`) y escupe **un reporte HTML premium + 4 entregables markdown**. El reporte es el artefacto "wow": debe sentirse como abrir un PDF de consultoría de ~$2,000 con el nombre del negocio del usuario, no como un output de IA.
>
> **Norte de diseño (de la data real, `.funnel-analysis/FINAL-REPORT.md`):**
> - El usuario está **paralizado** ("no sé por dónde empezar", 50%) — el reporte debe dar **una sola cosa que hacer HOY**, no un menú de 20 opciones.
> - Su victoria es **recuperar su tiempo** — dejar de sangrar horas en tareas repetitivas y ver su primer proceso corriendo solo. Todo entregable debe LADDER hacia eso.
> - Su metáfora mental es **contratar un empleado, no comprar software**. El lenguaje de las automatizaciones usa esa metáfora ("tu empleado que cotiza solo 24/7").
> - Es **pre-monetización** (88% factura <$2k/mes) y llega con **poco stack** (muchos solo ChatGPT) → los costos deben ser bajos y reales, el quick-win debe ser usable HOY sin instalar nada caro.

---

## 0. Principios rectores (los 7 mandamientos del paquete)

1. **El reporte HTML es el héroe.** Los 4 markdown son soporte. El 90% del "wow" vive en `reporte.html`: una persona lo abre, lo imprime a PDF, lo guarda como su mapa de automatización. Debe verse caro.
2. **Personalizado hasta la médula.** El nombre del negocio aparece en la portada, en headers, en el footer. Cada número (ahorro, ROI, costo) sale de SU data, no de promedios. Si dice "Tacos El Güero", el reporte dice "Tacos El Güero" en 6+ lugares.
3. **Una decisión, no un buffet.** Hay UNA automatización #1 destacada (la `quick_win`). Las otras 2 son "lo que sigue". Combate la parálisis: el CTA primario del reporte es *empezar la #1 hoy*.
4. **Números que el usuario cree.** Ahorro en horas/semana → en dinero (con su tarifa o un proxy LATAM conservador). ROI con payback en semanas. Nada inflado: si no hay data para un número, se omite o se marca "estimado conservador". El mercado huele el humo.
5. **Premium SIN pushy.** Cero countdowns, cero "oferta limitada", cero "solo hoy". El cierre invita a la comunidad como *el siguiente paso natural*, después de haber entregado valor real. (Regla de marca de Santi.)
6. **Self-contained, cero dependencias.** Python stdlib puro. HTML con **todo CSS inline en un `<style>`**, fuentes vía `@import` de Google Fonts con **fallback a system-ui** (para que imprima bien offline), logo como **SVG inline**. Cero assets externos, cero `<img src>`. Corre igual en Mac/Win/Linux.
7. **Imprime a PDF perfecto.** `@media print` cuida saltos de página (cada automatización en su página, roadmap sin cortar a la mitad), colores que sobreviven (`-webkit-print-color-adjust: exact`), márgenes A4. El usuario hará `Cmd/Ctrl+P → Guardar como PDF` y el resultado debe ser indistinguible de un deliverable de agencia.

---

## 1. El SET DE ENTREGABLES (qué archivos produce el pipeline)

Tras la entrevista, `generar_reporte.py <diagnostico.json> <output_dir>` crea esta carpeta:

```
<output_dir>/  (ej. ~/Desktop/diagnostico-tacos-el-guero/)
├── reporte.html              ← ★ EL ARTEFACTO WOW (self-contained, imprime a PDF)
├── 01-procesos-y-roi.md      ← los 3 procesos a automatizar con ROI, en texto editable
├── 02-plan-90-dias.md        ← roadmap accionable semana a semana
├── 03-stack-recomendado.md   ← herramientas exactas + costos reales + por qué cada una
├── 04-quick-win.md           ← ★ el entregable USABLE HOY: prompt/plantilla real de la automatización #1
└── README.txt                ← "qué es cada archivo y por dónde empezar" (3 líneas, plano)
```

> **Por qué markdown además del HTML:** el HTML es para VER/imprimir/impresionar. Los `.md` son para COPIAR-PEGAR-EDITAR — el usuario abre `04-quick-win.md`, copia el prompt y lo pega en Claude/ChatGPT al instante. El markdown es el "úsalo ahora", el HTML es el "siéntete dueño de algo caro". Ambos salen del **mismo** `diagnostico.json`.

### Tabla maestra de entregables

| Archivo | Propósito | Fuente en el JSON | Tono / longitud |
|---|---|---|---|
| `reporte.html` | El paquete completo, visual, imprimible. El "wow". | todo el JSON | Premium, escaneable, visual |
| `01-procesos-y-roi.md` | Justificar QUÉ automatizar y por qué, con números. | `procesos[]`, `automatizaciones[]`, `roi` | Consultor, ~1.5 pág |
| `02-plan-90-dias.md` | El orden exacto, semana a semana. Mata la parálisis. | `roadmap[]` | Imperativo, checklist |
| `03-stack-recomendado.md` | Las herramientas mínimas + costo real + free tier. | `stack[]` | Tabla + notas |
| `04-quick-win.md` | El recurso ejecutable HOY de la automatización #1. | `quick_win` | Copy-paste, cero relleno |
| `README.txt` | Onboarding de 3 líneas al paquete. | `negocio`, `quick_win.titulo` | Plano, directo |

---

### 1.1 `reporte.html` — ver §2 (la sección grande)

### 1.2 `01-procesos-y-roi.md` — "Qué automatizar y por qué"

**Propósito:** la lógica de negocio detrás de la recomendación. Es el documento que el usuario podría reenviar a un socio para justificar la inversión de tiempo.

**Contenido (de `templates/01-procesos-y-roi.md`):**
- **H1:** `# Diagnóstico de automatización — {negocio.nombre}`
- **Intro (2-3 frases):** resume el negocio en palabras del usuario + la tesis ("Hay 3 procesos que hoy te roban ~{horas_total}h/semana. Automatizarlos en este orden te devuelve ~{horas}h/semana.").
- **Tabla de procesos (mapa de calor textual):** una fila por `proceso`: nombre · frecuencia · horas/semana · dolor (cita literal del usuario si existe) · **score de automatización 0-100** · veredicto (🟢 automatizar ya / 🟡 después / ⚪ no vale la pena aún).
- **Las 3 automatizaciones recomendadas:** por cada una, sub-sección con: qué resuelve, cómo funciona en 1 frase (metáfora de empleado), ahorro estimado (h/sem → $/mes), esfuerzo de montaje, herramientas.
- **Tabla ROI consolidada:** ver §2.7 (misma data, formato markdown).
- Cierre: "La #1 es `{quick_win.titulo}` — empieza por ahí. El archivo `04-quick-win.md` ya tiene lo que necesitas para arrancar hoy."

### 1.3 `02-plan-90-dias.md` — "Tu ruta, semana a semana"

**Propósito:** el antídoto directo al dolor #1 ("desorden de mil tutoriales"). NO es una lista de temas; es una secuencia de **acciones con resultado**.

**Estructura:** 3 bloques (Mes 1 / Mes 2 / Mes 3), cada uno con 2-4 hitos semanales. Cada hito = `[ ] acción concreta → resultado tangible`. Ejemplo:
```
## Mes 1 — Tu primer proceso corriendo solo
- [ ] Semana 1: Montar el agente de cotizaciones (usa 04-quick-win.md) → dejas de perder medio día respondiendo.
- [ ] Semana 2: Conectarlo a WhatsApp → responde a tus clientes sin que tú estés.
...
## Mes 3 — Tu operación trabajando sola
- [ ] Semana 9: Montar la automatización #3 → tus 3 procesos clave corriendo sin que tú estés.
```
- **El Mes 3 SIEMPRE aterriza en el objetivo a 90 días del usuario** (`meta_90_dias`): su operación corriendo sola, con las horas recuperadas ya medidas. Esa es la victoria.
- Tono imperativo, segunda persona, cálido. Sin jerga sin traducir.

### 1.4 `03-stack-recomendado.md` — "Las herramientas exactas"

**Propósito:** quitar la fricción de "¿qué uso?". Stack **mínimo viable**, no exhaustivo. El usuario llega con poco (solo ChatGPT) → cada herramienta extra se justifica y se prioriza el free tier.

**Contenido:**
- Tabla: herramienta · para qué (en lenguaje de negocio) · costo real (`gratis` / `$X/mes` / `$X una vez`) · free tier sí/no · alternativa más barata.
- **Costo total mensual estimado** destacado (debe ser bajo: el público es pre-monetización).
- Nota por herramienta solo si no es obvia. Nombres propios en inglés (Cloudflare, OpenAI, Claude), todo lo demás traducido.
- Si el diagnóstico recomienda construir un agente en la nube → nota: *"Para construir esto paso a paso sin programar, usa el skill `/crear-agente`."* (hand-off explícito, ver §4).

### 1.5 `04-quick-win.md` — ★ EL ENTREGABLE USABLE HOY

**Propósito:** ESTE es el quick win de "día 1". El usuario lo abre y en <5 min tiene un resultado real, sin instalar nada. Es lo que convierte "leí un reporte" en "ya hice algo".

**Qué es:** un recurso **ejecutable** de la automatización #1, elegido por tipo según `quick_win.tipo`:
- `prompt` → un **prompt maestro listo para pegar** en Claude/ChatGPT que hace el 80% del trabajo del proceso #1 hoy mismo (ej. "Plantilla de cotización automática: pega los datos del cliente y este prompt te genera la cotización con tu formato"). Con variables `[ENTRE CORCHETES]` que el usuario rellena + 1 ejemplo ya lleno.
- `plantilla` → una estructura lista (ej. tabla de seguimiento de leads, guion de respuesta) en markdown copiable.
- `outline` → el plano paso-a-paso de la automatización para construirla (puente directo a `/crear-agente`).

**Reglas del quick-win:**
- **Cero teoría.** Empieza con "Copia esto y pégalo en Claude:" o "Pega tus datos aquí:". El valor es inmediato.
- **Personalizado:** usa el nombre del negocio, su nicho, su dolor literal. El ejemplo lleno usa SU caso.
- **Un solo quick-win**, no tres. Combate la parálisis.
- Termina con: "Cuando esto te funcione, el siguiente paso es automatizarlo del todo (ver `02-plan-90-dias.md`)."

### 1.6 `README.txt`

```
DIAGNÓSTICO DE AUTOMATIZACIÓN — {negocio.nombre}
Generado por Horizontes IA · {fecha}

Empieza aquí:
1. Abre reporte.html (doble clic) — tu diagnóstico completo. Para PDF: Cmd/Ctrl+P → Guardar como PDF.
2. Abre 04-quick-win.md — algo que puedes usar HOY mismo, en 5 minutos.
3. El resto son tu plan a 90 días, los procesos con ROI y el stack de herramientas.
```

---

## 2. EL REPORTE HTML — diseño detallado (`reporte.html`)

> El artefacto wow. Documento de **una sola columna, scroll vertical**, ancho de lectura ~820px centrado sobre fondo near-black. Pensado para leerse en pantalla Y para imprimirse a PDF A4. Cada sección es un "bloque" con respiración generosa.

### 2.0 Sistema de diseño (tokens — el ingeniero los define como CSS variables)

Tomado del DNA de marca real de Santi (`generate-ad-cards.mjs`, landings):

```css
:root{
  --bg:        #0a0a0c;   /* near-black, fondo base */
  --surface:   #111317;   /* tarjetas / superficies elevadas */
  --surface-2: #16191f;   /* hover / sub-superficie */
  --border:    rgba(255,255,255,.08);
  --text:      #e6e6e6;   /* texto principal */
  --muted:     #8b93a1;   /* texto secundario */
  --cyan:      #00E5FF;   /* ACENTO de marca Horizontes IA */
  --cyan-2:    #22d3ee;   /* cyan secundario (gradientes) */
  --cyan-soft: rgba(0,229,255,.10);  /* fills suaves, badges */
  --good:      #34d399;   /* verde — ahorro, scores altos */
  --warn:      #fbbf24;   /* ámbar — scores medios */
  --dim:       #64748b;   /* gris — scores bajos / "no aún" */
  --radius:    16px;
  --radius-sm: 10px;
  --shadow:    0 20px 60px -20px rgba(0,0,0,.7);
  --glow:      0 0 40px -8px rgba(0,229,255,.35);
}
```

**Tipografía:**
- Cuerpo / UI / números: **Space Grotesk** (400/500/600/700). Fallback: `system-ui, -apple-system, sans-serif`.
- Acentos editoriales (el toque "caro"): **Instrument Serif italic** — solo para el subtítulo de portada, los números grandes de KPI y los headers de sección decorativos. Fallback: `Georgia, serif`.
- `@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap');`
- Escala: portada h1 ~52px, section h2 ~30px, card h3 ~20px, body ~16px/1.65, micro/label ~12px tracking 0.14em uppercase.

**Detalles "premium" (lo que separa $2k de un output de IA):**
- Líneas de acento cyan finas (2px) bajo los títulos de sección, no cajas pesadas.
- Números clave en serif italic grande con el cyan — se sienten "editoriales".
- Mucho espacio en blanco (negro). Padding generoso (40-56px en bloques).
- Sombras suaves y un glow cyan sutil SOLO en el CTA y la tarjeta del quick-win (jerarquía: el ojo va al quick-win).
- Un grano/gradiente radial muy sutil en el fondo de la portada (CSS `radial-gradient`, sin imagen).

### 2.1 Estructura de secciones (orden de scroll)

```
┌─ A. PORTADA ────────────────────────────── (full viewport, página 1 en PDF)
├─ B. RESUMEN EJECUTIVO ───────────────────── (la tesis en 4 frases + 3 KPIs)
├─ C. MAPA DE PROCESOS ────────────────────── (barras de score por proceso)
├─ D. LAS 3 AUTOMATIZACIONES ──────────────── (3 tarjetas; la #1 destacada/glow)
├─ E. TABLA DE ROI ────────────────────────── (ahorro $ + payback)
├─ F. QUICK-WIN DESTACADO ─────────────────── (★ tarjeta cyan, lo usable hoy)
├─ G. ROADMAP 90 DÍAS ─────────────────────── (timeline 3 meses)
├─ H. STACK RECOMENDADO ───────────────────── (chips + costo total)
└─ I. CIERRE / SIGUIENTE PASO ─────────────── (CTA suave a comunidad)
```

---

### A. PORTADA `<section class="cover">`

El primer impacto. Debe gritar "esto es para MÍ y es caro".

- **Layout:** full-height (`min-height: 100vh` en pantalla; página propia en print). Centrado vertical, alineado a la izquierda dentro del ancho de lectura. Fondo: `--bg` + `radial-gradient` cyan muy tenue arriba-izquierda.
- **Lockup superior:** logo SVG inline de Horizontes IA (ver §3.3) + wordmark "HORIZONTES IA" en micro-label cyan uppercase tracking. A la derecha, fecha (`negocio.fecha`).
- **Eyebrow:** `DIAGNÓSTICO DE AUTOMATIZACIÓN` (micro-label, cyan, tracking 0.18em).
- **Título (lo más grande de todo el doc):** el **nombre del negocio** del usuario en Space Grotesk 700, ~52px. Ej. *"Tacos El Güero"*.
- **Subtítulo en Instrument Serif italic** (~26px, muted→text): una frase que sintetiza su realidad y promesa, generada del JSON. Ej. *"Un mapa para que tu negocio empiece a trabajar solo."*
- **Meta-fila (3 mini-datos):** "Preparado para {negocio.nombre_persona} · Sector: {negocio.sector} · {negocio.ubicacion}". En muted, separados por puntos cyan.
- **Banda de 3 KPI-teaser** abajo de la portada (preview del valor): `{horas_recuperables}h/semana recuperables` · `${ahorro_mensual}/mes de ahorro estimado` · `{payback_semanas} sem para recuperar la inversión`. Números en serif italic cyan grande, label debajo en micro uppercase.
- Print: esta sección es la página 1 completa (`break-after: page`).

### B. RESUMEN EJECUTIVO `<section>`

La tesis del consultor. Quien solo lee esto, ya entendió el valor.

- **Header de sección:** `Resumen ejecutivo` (h2) con línea cyan debajo.
- **Párrafo-tesis (3-5 frases, `resumen.tesis` del JSON):** en lenguaje del usuario. Estructura: "Tu negocio hace X. Hoy pierdes ~Yh/semana en {proceso doloroso}. Las 3 automatizaciones de este reporte recuperan esas horas y te acercan a {su victoria}. Empieza por {quick_win.titulo}."
- **3 KPI cards** (grid 3-col, colapsa a 1-col en print/móvil) — los mismos KPIs de portada pero ahora como tarjetas con contexto:
  - Card: número grande (serif italic cyan) + label + 1 línea de contexto. Borde sutil, fondo `--surface`.
  - KPI 1: **Horas/semana recuperables** (suma de ahorro de las 3 autom.).
  - KPI 2: **Ahorro mensual estimado en $** (horas × tarifa o proxy).
  - KPI 3: **Payback** (semanas para que el ahorro pague el costo de montar).
- **Bloque "Tu mayor oportunidad ahora mismo":** callout con borde-izquierdo cyan que nombra la automatización #1 y dice por qué es la primera. Tease al quick-win.

### C. MAPA DE PROCESOS `<section>` — barras de score visuales

El "diagnóstico" tangible: muestra que se analizó SU operación, no genérico.

- **Header:** `Mapa de tus procesos` + sub: "Cada proceso, calificado por qué tan automatizable es y cuánto tiempo te devuelve."
- **Lista de filas-proceso** (una por `procesos[]`), cada fila es un componente **score-bar**:
  ```
  ┌──────────────────────────────────────────────────────────┐
  │ Responder cotizaciones            🟢 Automatizar ya       │
  │ ████████████████████░░░░  82/100                          │
  │ 10h/sem · diario · "se me va medio día en esto"           │
  └──────────────────────────────────────────────────────────┘
  ```
  - **Nombre del proceso** (h3, izquierda) + **badge de veredicto** (derecha): 🟢 Automatizar ya (score ≥70) / 🟡 Después (40-69) / ⚪ No aún (<40). Badge = pill con color por tier.
  - **Barra de score:** track `--surface-2`, fill con gradiente cyan (`--cyan-2`→`--cyan`), ancho = `score%`, altura 10px, redondeada. Número `score/100` al final en Space Grotesk 600.
  - **Meta-línea (muted):** `{horas}h/sem · {frecuencia} · "{cita literal del dolor}"`. La cita es lo que personaliza — usa las palabras del usuario.
- Las filas se ordenan por score descendente (lo más automatizable arriba = lo que debe hacer primero).
- **Print color fix** obligatorio en las barras (`-webkit-print-color-adjust: exact; print-color-adjust: exact;`).

### D. LAS 3 AUTOMATIZACIONES `<section>` — tarjetas de arquitectura

El corazón del entregable. 3 tarjetas; la **#1 con glow cyan y badge "EMPIEZA AQUÍ"**, las otras 2 atenuadas como "lo que sigue".

- **Header:** `Las 3 automatizaciones que te recomiendo` + sub: "En orden. No intentes las tres a la vez — domina la primera."
- **Por cada `automatizaciones[]`, una tarjeta** (apilada vertical, cada una su página en print):
  ```
  ┌─ #1 ─────────────────────────────────  [★ EMPIEZA AQUÍ] ─┐  ← borde+glow cyan
  │  🤖 Tu empleado que cotiza solo                          │
  │  "Responde cada solicitud de cotización en segundos,     │
  │   con tu formato, sin que tú muevas un dedo."            │
  │                                                          │
  │  ┌─ Cómo funciona (arquitectura) ──────────────────────┐ │
  │  │  Cliente escribe → IA lee → genera cotización →      │ │  ← mini "diagrama"
  │  │  te avisa → tú apruebas y se envía                   │ │     (cadena con flechas →)
  │  └─────────────────────────────────────────────────────┘ │
  │                                                          │
  │  HERRAMIENTAS   Claude · WhatsApp · Cloudflare           │  ← chips
  │  COSTO          ~$3/mes        ESFUERZO   1 tarde        │  ← stat row
  │  AHORRO         10h/sem ≈ $480/mes                       │  ← stat destacado verde
  └──────────────────────────────────────────────────────────┘
  ```
  - **Header de tarjeta:** número de orden (`#1` en pill cyan), título con metáfora de empleado (h3), badge `★ EMPIEZA AQUÍ` solo en la #1 (las demás sin badge o "Después"). Una frase de promesa en serif italic.
  - **Bloque "Cómo funciona":** la arquitectura en lenguaje de negocio como **cadena con flechas →** (NO diagrama técnico): `paso → paso → paso`. Renderizado con chips/pills conectados por flechas cyan. Esto es lo que se ve "de arquitecto" sin asustar.
  - **Chips de herramientas:** pills con `--cyan-soft` fill, borde cyan tenue. Nombres propios en inglés.
  - **Stat row:** Costo · Esfuerzo · **Ahorro** (el ahorro en verde `--good`, destacado, formato `Xh/sem ≈ $Y/mes`).
  - **#1 destacada:** `box-shadow: var(--glow)`, borde `1px solid var(--cyan)`. #2 y #3: borde normal `--border`, ligeramente atenuadas (opacity .92) para jerarquía.
  - Si una automatización es "construir un agente en la nube" → micro-nota al pie de la tarjeta: *"Esto se construye con el skill `/crear-agente`"*.
- Print: cada tarjeta `break-inside: avoid`; la #1 idealmente abre página.

### E. TABLA DE ROI `<section>`

El número que el usuario pre-monetización necesita ver para creer.

- **Header:** `El retorno de tu inversión` + sub: "Tiempo y dinero, en frío. Estimaciones conservadoras."
- **Tabla** (`--surface`, header row cyan-soft, zebra sutil):

  | Automatización | Horas/sem | Ahorro/mes | Costo montaje | Costo/mes | Payback |
  |---|---|---|---|---|---|
  | #1 Cotizaciones | 10h | $480 | 1 tarde | $3 | <1 sem |
  | #2 … | … | … | … | … | … |
  | #3 … | … | … | … | … | … |
  | **TOTAL** | **{Σ}h** | **${Σ}/mes** | — | **${Σ}/mes** | — |

  - Fila TOTAL en bold, fondo `--cyan-soft`, números en cyan.
  - Columna "Ahorro/mes" en verde `--good`.
  - **Nota al pie (importante para credibilidad):** "Ahorro = horas recuperadas × tu tarifa (`{tarifa}`/h). Conservador. No incluye los ingresos extra que recuperas al responder más rápido y dejar de perder clientes."
- Print: `break-inside: avoid`.

### F. QUICK-WIN DESTACADO `<section class="quickwin">` — ★ el ancla de acción

La sección con **más peso visual de todo el reporte** (junto al CTA final). Es "haz esto HOY".

- **Tarjeta full-width con fondo `--cyan-soft` + borde cyan + glow.** El ojo cae aquí.
- **Eyebrow:** `★ TU QUICK WIN — ÚSALO HOY` (cyan, bold).
- **Título:** `quick_win.titulo` (h2). Ej. *"Plantilla de cotización automática para Tacos El Güero"*.
- **Una frase de promesa:** "En 5 minutos, sin instalar nada, deja de escribir cotizaciones desde cero."
- **El recurso en sí, renderizado según `quick_win.tipo`:**
  - Si `prompt`/`plantilla`/`outline` → bloque `<pre>` con el contenido **monospace**, fondo `--bg` (oscuro dentro del cyan), borde, esquinas redondeadas, **scrolleable horizontal si hace falta**, y un micro-label arriba "Copia esto:". Render literal del `quick_win.contenido` (preservar saltos de línea, escapar HTML).
  - Variables `[ASÍ]` resaltadas en cyan dentro del bloque.
- **3 mini-pasos de uso** debajo (numerados, lo mínimo): "1. Copia el texto. 2. Pégalo en Claude/ChatGPT. 3. Rellena lo que está [entre corchetes]."
- **Línea de continuidad:** "El archivo `04-quick-win.md` tiene esto mismo para copiar fácil. Cuando funcione → automatízalo del todo (roadmap)."
- Print: `break-inside: avoid` si cabe; si el contenido es largo, permitir corte pero mantener el header con el bloque.

### G. ROADMAP 90 DÍAS `<section>` — timeline

La ruta que mata la parálisis. Visual de línea de tiempo, no lista plana.

- **Header:** `Tu ruta a 90 días` + sub: "El orden exacto. Una cosa a la vez."
- **3 columnas-mes** (o filas apiladas en print/móvil): Mes 1 / Mes 2 / Mes 3, cada uno con un **encabezado-objetivo** (ej. "Mes 1 — Tu primer proceso corriendo solo").
- **Dentro de cada mes, hitos** como items de timeline con un **punto cyan + línea vertical conectora**:
  ```
  Mes 1 · Tu primer proceso corriendo solo
   ●─ Semana 1: Monta el agente de cotizaciones → dejas de perder medio día
   │
   ●─ Semana 2: Conéctalo a WhatsApp → responde sin que estés
  ```
  - Punto cyan (`●`), línea conectora `--border`, texto del hito: **acción** (bold) `→` **resultado** (muted).
- **El Mes 3 culmina en un hito destacado** (verde o cyan, con ícono ✦): el objetivo a 90 días del usuario cumplido (su operación corriendo sola, las horas recuperadas). Visualmente es la "meta" del timeline.
- Print: cada mes `break-inside: avoid`.

### H. STACK RECOMENDADO `<section>`

Las herramientas, sin abrumar.

- **Header:** `Tu stack` + sub: "Lo mínimo para arrancar. Casi todo tiene plan gratis."
- **Grid de chips/cards de herramientas** (`stack[]`): cada una = card chica con nombre (Space Grotesk 600), "para qué" (1 línea muted), y un badge de costo (`GRATIS` verde / `$X/mes` muted / `$X una vez`).
- **Banda de costo total:** "Costo total para empezar: **${total}/mes**" en serif italic cyan grande. Refuerza que es accesible.
- Si hay agente en la nube → nota cyan: *"¿Listo para construir? El skill `/crear-agente` te guía paso a paso, sin programar."*

### I. CIERRE / SIGUIENTE PASO `<section class="closing">`

El CTA suave. Premium, no pushy. Ladder a la comunidad DESPUÉS de haber entregado.

- **Tarjeta cierre** (`--surface`, borde cyan tenue, centrada).
- **Título (serif italic):** *"Ya tienes el mapa. El siguiente paso es construir."*
- **Párrafo (cálido, 2-3 frases):** "Este diagnóstico es tuyo — imprímelo, compártelo, úsalo. Empieza HOY por tu quick-win. Y cuando quieras construir las automatizaciones completas con gente que va en tu mismo camino, te esperamos en la comunidad." (CERO urgencia, cero "limitado").
- **CTA primario (pill cyan con glow):** "Empieza tu quick-win →" (apunta conceptualmente al archivo; en print queda como referencia). 
- **CTA secundario (texto/ghost):** "Conoce la comunidad de Horizontes IA →" `https://www.skool.com/horizontes-ia-9992`.
- **Footer del documento:** logo Horizontes IA mini + "Diagnóstico generado por Horizontes IA · {fecha} · Hecho para {negocio.nombre}". Micro, muted, centrado.
- Print: página final propia.

---

### 2.7 Componentes reutilizables (catálogo para el ingeniero)

El generador construye el HTML con estos componentes (helpers de Python que devuelven strings de HTML):

| Componente | HTML/CSS | Dónde se usa |
|---|---|---|
| `kpi_card(numero, label, contexto)` | número serif-italic cyan grande + label uppercase + contexto muted. Card `--surface`. | Portada, Resumen |
| `score_bar(nombre, score, meta, veredicto)` | nombre + badge veredicto + track/fill gradiente + `score/100`. | Mapa de procesos |
| `verdict_badge(score)` | pill: 🟢≥70 `--good` / 🟡40-69 `--warn` / ⚪<40 `--dim`. | Score bars |
| `automation_card(idx, data, destacada)` | tarjeta con header, cadena-arquitectura, chips, stat row. Glow si `destacada`. | Sección D |
| `arch_chain(pasos[])` | pills conectados por flechas `→` cyan, wrap responsive. | Dentro de automation_card |
| `tool_chip(nombre)` | pill `--cyan-soft`, borde cyan tenue, Space Grotesk 600. | Automatizaciones, Stack |
| `cost_badge(valor)` | pill: `GRATIS` verde / `$X/mes` muted. | Stack |
| `roi_table(rows[], total)` | tabla con header cyan-soft, zebra, fila TOTAL destacada, col ahorro verde. | Sección E |
| `timeline_month(titulo, hitos[])` | encabezado-mes + items con punto cyan + línea conectora. | Roadmap |
| `code_block(texto, label)` | `<pre>` monospace, fondo `--bg`, escape HTML, variables `[X]` en cyan. | Quick-win |
| `section_header(titulo, sub)` | h2 + línea cyan 2px + sub muted. | Todas las secciones |

**Helper crítico:** una función `esc(s)` que escape `< > & "` para todo texto que venga del JSON (es input de usuario / IA) antes de inyectarlo al HTML. **Obligatorio** — el `reason`/nombre del negocio puede traer caracteres que rompan el HTML.

---

## 3. Principios de implementación (HTML+CSS inline, self-contained)

### 3.1 Estructura del archivo
- **Un solo `.html`**: `<!DOCTYPE html>` → `<head>` con `<meta charset utf-8>`, `<meta viewport>`, `<title>Diagnóstico — {negocio}</title>`, `@import` de fuentes + **todo el CSS en un `<style>`** → `<body>` con las 9 secciones.
- **Cero JS** (no se necesita; todo es estático). Cero `<img>` externos. Logo = SVG inline.
- El generador es **string templating con stdlib** (f-strings / `.format` / `string.Template`). No Jinja, no deps. Recomendado: helpers que devuelven fragmentos de HTML y se concatenan.

### 3.2 Print CSS (`@media print`) — no negociable
```css
@media print {
  :root { /* mantener colores */ }
  * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  @page { size: A4; margin: 16mm; }
  body { background: var(--bg); }       /* el negro debe imprimirse */
  .cover { break-after: page; min-height: auto; }
  section { break-inside: avoid; }       /* default: no cortar secciones */
  .automation-card { break-inside: avoid; }
  .automation-card.featured { break-before: page; } /* la #1 abre página */
  .timeline-month { break-inside: avoid; }
  .roi-table, .quickwin { break-inside: avoid; }
  .closing { break-before: page; }
  /* ocultar nada interactivo; subir contraste de muted para tinta */
}
```
- Fondo oscuro al imprimir es intencional (es la identidad). `print-color-adjust: exact` lo garantiza. Si el ingeniero detecta que algún navegador lo ignora, dejar el negro igual — el usuario que quiera fondo blanco lo decide en el diálogo de print; el default debe verse premium dark.
- Verificar que el ancho de lectura (~820px) + márgenes A4 no corten contenido a la derecha. Usar `max-width` en `%`/`mm`-friendly, no px fijos enormes.

### 3.3 Logo SVG inline (Horizontes IA)
- Un mark geométrico simple en cyan que evoque "horizonte" (ej. arco/línea de horizonte + sol, o las iniciales). Inline en el HTML como `<svg>`, color `--cyan`. ~28px en lockups, ~20px en footer. (El ingeniero puede tomar el SVG real de `public/logo.svg` del repo scraperskool si está disponible y simplificarlo a path inline; si no, un placeholder geométrico cyan limpio.)

### 3.4 Robustez de datos (el generador no debe romper)
- **Defaults para todo campo opcional.** Si falta `tarifa` → usar proxy LATAM conservador (ej. $12 USD/h) y marcar "estimado". Si falta una cita de dolor → omitir la línea, no poner placeholder vacío. Si hay <3 automatizaciones → renderizar las que haya. Si falta `quick_win` → omitir la sección F pero el resto se genera (degradación elegante).
- **Números formateados** legibles: `$480/mes`, `10h/sem`, `<1 sem`. Helper `money()`, `hrs()`.
- **Nunca** dejar `{variable}` sin reemplazar visible en el output. Validar contra el esquema de `_design/schema.md`.
- El generador imprime en stdout la ruta final (`✅ Reporte generado: <output_dir>/reporte.html`) y NO abre el browser solo (cross-platform; el SKILL.md le dirá al usuario cómo abrirlo).

### 3.5 Consistencia con el esquema canónico
- Este spec asume que `diagnostico.json` tiene (al menos) estos bloques — **el esquema canónico manda; si difiere, gana `_design/schema.md`**:
  - `negocio`: `nombre`, `nombre_persona`, `sector`, `ubicacion`, `fecha`, `tarifa?`
  - `resumen`: `tesis`, `kpis` (`horas_recuperables`, `ahorro_mensual`, `payback_semanas`)
  - `procesos[]`: `nombre`, `frecuencia`, `horas_semana`, `dolor?` (cita), `score`, `veredicto`
  - `automatizaciones[]` (ordenadas, [0] = la #1): `titulo`, `promesa`, `arquitectura[]` (pasos), `herramientas[]`, `costo_mensual`, `esfuerzo`, `ahorro_horas`, `ahorro_mensual`, `usa_crear_agente?` (bool)
  - `roi`: filas derivables de `automatizaciones[]` + `total`
  - `quick_win`: `titulo`, `tipo` (`prompt`|`plantilla`|`outline`), `contenido`, `promesa`
  - `roadmap[]`: `mes`, `objetivo`, `hitos[]` (`semana`, `accion`, `resultado`, `es_meta?`)
  - `stack[]`: `nombre`, `para_que`, `costo`, `gratis?`, `total_mensual`
- El generador **deriva** la tabla ROI y los KPI sumando `automatizaciones[]` cuando sea posible (no confiar en que la IA sume bien) — recalcular `horas_recuperables` y `ahorro_mensual` server-side desde las partes.

---

## 4. Sinergia con `/crear-agente` (hand-off de construcción)

El reporte y los entregables **invitan a construir**, y cuando una automatización es "un agente en la nube", pasan la batuta:
- En la tarjeta de automatización (§D), `03-stack-recomendado.md` y `H. Stack`, si `automatizaciones[i].usa_crear_agente == true` → micro-nota: *"Esto se construye con el skill `/crear-agente` — te guía paso a paso, sin programar."*
- Esto es lo que el SKILL.md ofrecerá EJECUTAR ahí mismo tras generar el reporte ("¿quieres que construyamos la #1 ahora? → invoco `/crear-agente`"). El paquete de entregables es el "plano"; `/crear-agente` es la "construcción". El `04-quick-win.md` es el puente: valor inmediato hoy, construcción completa después.

---

## 5. Checklist de aceptación del entregable (para QA del generador)

- [ ] `reporte.html` abre en Chrome/Safari/Firefox sin assets externos rotos (offline OK salvo fuentes, que tienen fallback).
- [ ] El nombre del negocio aparece ≥6 veces (portada, headers, ROI nota, quick-win, footer).
- [ ] `Cmd/Ctrl+P → PDF`: portada = pág 1, automatización #1 abre página, ningún bloque se corta a la mitad, los colores/barras se imprimen (no salen blancos).
- [ ] Las barras de score reflejan los scores del JSON (ancho = score%) y los colores de veredicto coinciden con los tiers.
- [ ] La automatización #1 tiene glow + badge "EMPIEZA AQUÍ"; las otras 2 atenuadas.
- [ ] La tabla ROI suma correctamente (recalculada server-side, no copiada de la IA).
- [ ] El quick-win renderiza el contenido literal sin romper HTML (escape OK), variables `[X]` resaltadas.
- [ ] El roadmap termina en un hito destacado: el objetivo a 90 días cumplido (operación corriendo sola / horas recuperadas).
- [ ] Los 4 `.md` + `README.txt` se generan con la misma data y son copy-paste-ables.
- [ ] Sin un solo `{placeholder}` sin reemplazar en ningún output.
- [ ] Cero countdown / "oferta limitada" / urgencia en ningún archivo (regla de marca).
- [ ] Corre con `python3 scripts/generar_reporte.py ejemplo/diagnostico.json /tmp/out` sin errores y sin deps externas.
