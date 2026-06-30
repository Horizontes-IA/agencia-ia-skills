---
name: propuesta
description: Arma la PROPUESTA que cierra al cliente de tu agencia de automatización con IA — el documento que GANA la decisión, no la cotización seca. Toma el dolor del cliente en SUS palabras, lo enmarca como narrativa de cierre (problema → solución como transformación → alcance → entregables → timeline → inversión con 3 opciones → prueba social → términos → siguiente paso), y lo entrega como markdown editable + un HTML cliente-facing premium que imprime a PDF (limpio, acento cyan, de agencia seria). Lee el diagnostico.json de /diagnostico si existe y REUSA la cotización si ya se generó, para no empezar de cero ni re-preguntar. Úsalo cuando alguien escriba "/propuesta", "hazme una propuesta", "arma la propuesta para este cliente", "propuesta para [negocio]", "necesito mandarle una propuesta a mi cliente", "cómo le presento esto al cliente", "envuelve la cotización en una propuesta", "documento para cerrar al cliente", "propuesta de automatización", o cualquier variación donde un operador de agencia (probablemente principiante de LATAM) necesita un documento profesional para CERRAR a un prospecto. Español neutro LATAM, segunda persona, premium sin ser pushy. Cada decisión de estructura/precio viene de la investigación, no inventada. NO es la cotización (lista de precios — eso es /cotizacion), NO es el contrato (eso es /contrato), NO es el link de cobro (eso es /cobro).
---

# Propuesta — Skill `/propuesta`

## ⚙️ Fase 0 — Perfil de tu agencia (auto-config, una sola vez)

Antes de generar nada, asegura el perfil de la agencia:
- Si **NO existe** `~/.config/agencia-ia/perfil.json` → lee `~/.config/agencia-ia/configurar.md` y corre el onboarding (unas preguntas, guarda el perfil). **Solo la primera vez** que el usuario usa cualquier skill de agencia.
- Si **SÍ existe** → cárgalo y **NO vuelvas a preguntar**. Personaliza TODO con él: nombre de la agencia, nombre legal y datos (contrato), precios (cotización), proveedor/link de pago (cobro), color de acento (HTML), tono.
- **Contenido a la medida de la agencia** (clave en la propuesta): `agencia.metodologia` → arma la sección "cómo trabajamos / nuestro proceso" y el timeline; `agencia.propuesta_valor` → el ángulo de cierre (por qué con esta agencia); `agencia.que_hace` y `agencia.nicho` → encuadran el problema y la prueba social en el lenguaje del sector; `agencia.construye_con` → con qué se construye la solución.
- Para reconfigurar: el usuario dice "configura mi agencia" → re-corre `configurar.md`.

El perfil es el DEFAULT, no una jaula: si para ESTE cliente el precio o el alcance cambian, ajústalo para ese trato sin tocar el perfil.

Skill que arma **la propuesta que cierra a un prospecto** de una agencia de automatización con IA. No es una lista de precios: es el documento de venta que **gana la decisión** antes del "sí". Toma todo lo que ya sabes del cliente (del `/diagnostico` y/o `/cotizacion`), lo re-empaqueta como una narrativa de cierre, y lo entrega listo para mandar: **markdown editable + un HTML cliente-facing premium que imprime a PDF**.

**El dato que justifica este skill:** mandar una **propuesta** estructurada cierra ~**38%**; mandar una **cotización** seca cierra ~**23%** (sendtrumpet). Y una propuesta **personalizada** cierra **32% más** que una genérica (cobl.ai / adai). Por eso este skill NUNCA es una plantilla rígida copiada: personaliza con los datos reales del cliente.

> **El "wow" no es el texto bonito.** Es que el prospecto **se reconozca** ("este entiende MI problema, me leyó la mente") antes de ver un solo número, y que decir "sí" se sienta de bajo riesgo. Eso es lo que cierra.

---

## Cuándo invocar / cuándo NO

**SÍ** (literal o variantes):
- *"/propuesta"*, *"hazme una propuesta"*, *"arma la propuesta para [cliente]"*
- *"necesito mandarle una propuesta a mi cliente"*, *"cómo le presento esto"*
- *"envuelve la cotización en una propuesta"*, *"documento para cerrar"*

**NO** (redirige al skill correcto de la suite):
- Solo quiere el **precio / la lista de items** (negociación, ya decidido) → **`/cotizacion`**.
- Ya cerró y quiere el **contrato / acuerdo de alcance** → **`/contrato`**.
- Ya firmó y quiere el **link de cobro del anticipo** → **`/cobro`**.
- Aún no sabe QUÉ vender ni a quién → **`/diagnostico`** primero (genera el insumo de esta propuesta).

> **El lugar de /propuesta en la cadena:** `/diagnostico` (qué vender) → **`/propuesta` (GANAR el negocio)** → `/cotizacion` (precio fino en negociación) → `/contrato` (cerrar) → `/cobro` (anticipo). La propuesta es el documento que abre el cierre.

---

## Cómo te diriges al usuario del skill (el operador de la agencia)

El que usa este skill es **tu cliente: un operador de agencia, casi siempre principiante de LATAM**. Le hablas como un socio senior de ventas que ya cerró esto mil veces.

1. **Español neutro LATAM, segunda persona.** "Tu cliente", "tu propuesta", "lo que le vas a mandar".
2. **Cero tecnicismos sin traducir.** Si dices "anclaje de precio", explícalo en una frase ("poner la opción cara primero para que la de en medio se vea razonable").
3. **Una pregunta a la vez** cuando falte info. Nunca un formulario de 8 campos de golpe.
4. **Conservador y defendible > impresionante y falso.** Ningún número de ROI o precio que no venga del diagnóstico/cotización o que el operador no confirme. Si no hay dato, se omite — no se inventa.
5. **PROHIBIDO el hype.** En la propuesta y en cómo hablas: sin "¡garantizado!", "secreto", countdowns, "cupos". La urgencia única permitida es la **vigencia de 14 días** (real). Premium = calmado y seguro.

**Glosario (úsalo si el operador no lo conoce):**

| Término | Cómo lo explicas |
|---|---|
| Propuesta vs cotización | "la cotización dice cuánto cuesta; la propuesta convence de por qué TÚ y por qué ahora" |
| Anclaje / 3 tiers | "3 opciones: una cara que ancla, la de en medio que quieres que elija, una barata de salida" |
| Scope creep | "que el proyecto se infle con cosas que no cotizaste" |
| Anticipo / depósito | "el 50% que cobras al firmar, antes de empezar a trabajar" |
| ROI | "cuánto le regresa al cliente por lo que invierte" |
| SOW / acuerdo de alcance | "el documento que define exactamente qué entregas (lo hace el skill /contrato)" |

---

## La anatomía de la propuesta (7 secciones, en ESTE orden — y por qué)

El orden **replica la psicología del prospecto**: primero le pruebas que entiendes su problema, luego le das confianza en la solución, luego justificas el precio, y al final le das una acción clara. (digitalapplied).

> ⚠️ **Regla de oro del orden: el PROBLEMA va primero, tus CREDENCIALES van al final.** "A los prospectos no les importa tu background hasta que creen que entiendes su problema." Liderar con credenciales es el error #1 del consultor solo.

| # | Sección | Qué hace (de la investigación) |
|---|---|---|
| 1 | **Resumen ejecutivo** | El gancho de 30s. Re-enuncia el dolor con SUS palabras + cuantifica el costo mensual + adelanta entregables y rango de inversión. Debe **cerrar solo** (el decisor lee <4 min y escanea). |
| 2 | **El problema (en sus palabras)** | Lo que te separa de una cotización genérica. Repite la situación específica del cliente; cita su frase literal del diagnóstico. Lidera con **empatía, no credenciales**. |
| 3 | **La solución (3 fases)** | Vende **transformación, no una herramienta**. 3 fases: Descubrimiento → Construcción → Handoff. Ataca el **trust gap de IA**: demuestra que la IA es una herramienta que controlas, no una caja negra (privacidad + control humano). |
| 4 | **Entregables** | Formatos y cantidades **específicas** (elimina ambigüedad) + rondas de revisión incluidas + qué NO incluye (anti scope-creep). |
| 5 | **Timeline** | Semana por semana, con hitos. Incluye **lenguaje protector** ("el reloj se pausa si no recibimos X de tu lado"). Vende rollout gradual con **wins inmediatos**. |
| 6 | **Inversión (3 opciones)** | Anclaje psicológico (§Precios). Las 3 a la vez, con una **recomendada**. Ata el precio al **costo del problema**. |
| 7 | **Prueba social → Sobre ti → Siguiente paso** | Credibilidad **al final**. Casos con métrica concreta. CTA de **máx 3 pasos** + vigencia 14 días + link de calendario. |

---

## Precios: cómo armar los 3 tiers (anclaje) — de la investigación

Tres opciones explotan el **anclaje**: el tier alto ancla, el de en medio es el target (lo elige 55-65%), el bajo es la salida legítima de menor costo (no un "no" total). Estructura de referencia del nicho (digitalapplied):

- **Esencial / Starter** — red de seguridad. Precio **bajo** del rango. Lo elige 10-20%.
- **Recomendado / Professional** — **el target de conversión** (`"recomendada": true`). Precio **medio**. Lo elige 55-65%.
- **Completo / Enterprise** — ancla alta. Precio **alto** que hace ver al medio razonable. Lo elige 20-25%.

**Cómo calibrar los montos a ESTE cliente (no inventar):**
- Si hay `diagnostico.json`: el rango de mercado sale de `automatizaciones[].valor_si_lo_vendes_usd` (ej. `[1500, 3000]`). Ancla los 3 tiers a ese rango.
- Si hay una **cotización ya generada** (carpeta `cotizacion-<negocio>/` o `propuesta-<negocio>/cotizacion.*`): **reúsala tal cual** — sus tiers YA son los `opciones[]`. No los recalcules.
- Rango global del nicho que confirman las fuentes: **$1,500–$6,000 por engagement** (consistente con el $1,500–$3,000 de setup de la agencia objetivo). Setup más mensualidad opcional (`retainer_mes_usd`).
- **Estructura de pago:** 50/50 (50% al firmar, 50% a la entrega). El tier alto puede ir 40-30-30.

**Anclaje en la llamada (díselo al operador):** "cuando presentes los tiers en vivo, menciona PRIMERO el Completo (el caro). Así el Recomendado se siente un punto medio razonable." Y manejo de "está caro": ata el precio al costo mensual del problema ("esto te cuesta ~$X/mes") — nunca descuento seco; ofrece un piloto/rollout por fases.

---

## El pipeline en 6 fases

> Fase 0-1 = recolección (lee lo que ya existe, pregunta solo lo que falte). Fases 2-5 = construcción (trabajas, generas, verificas). Lee el archivo indicado al ENTRAR a cada fase.

### Fase 0 — Localiza el insumo (trabajas en silencio)

Antes de preguntar nada, **busca lo que ya existe** en el directorio de trabajo actual del usuario:

1. **Diagnóstico** — busca `diagnostico-*/diagnostico.json` (lo genera `/diagnostico`). Si existe, **léelo completo** — trae negocio, dolor en sus palabras (`sangrado_declarado.frase_textual`), procesos, automatizaciones, ROI y `valor_si_lo_vendes_usd`. Es la materia prima de TODA la propuesta. Mapeo campo-por-campo en `templates/propuesta.schema.md`.
2. **Cotización** — busca `cotizacion-*/` o un `cotizacion.json` / `cotizacion.md`. Si existe, sus tiers de precio son tus `opciones[]` — **reúsalos, no los recalcules**.
3. Si encuentras uno o ambos, confírmaselo al operador: *"Encontré tu diagnóstico de [negocio] — voy a armar la propuesta con eso, no te vuelvo a preguntar lo que ya sé."*

> Detecta también en silencio el binario disponible para el generador: prueba `node --version`. Guárdalo para la Fase 4. (Si no hay Node, el reporte igual sale por el fallback de la Fase 4.)

### Fase 1A — Si HAY diagnóstico/cotización: confirma y completa lo mínimo

No re-entrevistes. Solo necesitas lo que el diagnóstico no tiene (son **datos de la AGENCIA**, no del cliente):

- **Datos de tu agencia** (`agencia.*`): nombre, contacto (email / WhatsApp / link de calendario), tagline. Pregúntalos juntos UNA vez: *"Para personalizar la propuesta, ¿cómo se llama tu agencia y con qué correo o WhatsApp te contacta el cliente? Y si tienes link de calendario (Cal.com/Calendly), mándalo."*
- **Prueba social** (`prueba_social`): *"¿Tienes algún caso de un cliente parecido con un número concreto que pueda citar? Si aún no, no pasa nada — lo dejo fuera, no inventamos casos."* (Si no hay, se OMITE — nunca inventar.)
- **Confirma los 3 tiers**: muéstrale los precios que vas a poner (del diagnóstico/cotización) y pide luz verde o ajuste.

### Fase 1B — Si NO hay nada: mini-cuestionario (lo mínimo para una buena propuesta)

Si no existe diagnóstico ni cotización, levanta lo esencial — **una pregunta a la vez**, reflejando cada respuesta. Lo mínimo:

1. **El negocio del cliente** y a qué se dedica.
2. **El dolor #1, en SUS palabras** — *"¿cuál es la frase exacta con la que tu cliente describe su problema? Eso va literal en la propuesta, es lo que más cierra."*
3. **Qué le vas a construir** (la automatización / sistema) y qué resuelve.
4. **El costo del problema** — *"¿cuánto le cuesta hoy ese problema? Horas perdidas, leads que se caen, dinero que se va. Aunque sea aproximado."* (No inventes — si no sabe, se omite el número.)
5. **Tu precio** — *"¿en cuánto piensas venderlo? Te ayudo a armar 3 opciones alrededor de eso."* (Si duda, ancla al mercado: $1,500–$3,000 setup; sugiérele correr `/cotizacion` para el precio fino.)
6. **Datos de tu agencia** (nombre, contacto, calendario) — como en 1A.
7. **Prueba social** (opcional) — como en 1A.

> Tope: ~5-7 intercambios. Un buen vendedor cierra rápido. Si el operador da todo de golpe, extrae y refleja en bloque, no re-preguntes.

### Fase 1.5 — Confirma antes de construir (obligatoria)

Nunca generes en silencio. Resume y pide luz verde:

```
Listo, ya tengo lo necesario para armarte una propuesta que cierra.
Déjame confirmar:

• Tu cliente: [negocio]
• Su dolor (en sus palabras): "[cita literal]"
• Lo que le vas a construir: [solución]
• Tus 3 opciones de precio: [Esencial $X] · [Recomendado $Y] ⭐ · [Completo $Z]
• Tu agencia: [nombre] · [contacto]

Con esto armo la propuesta completa (problema en sus palabras → solución →
entregables → timeline → inversión → prueba social → siguiente paso) y te la
entrego en markdown editable + un PDF premium para mandarle.

¿Le atino? Si sí, arranco. (Si quieres ajustar algo, dime.)
```

Si confirma → Fases 2-5. Si corrige → ajusta SOLO eso, re-confirma, dispara.

### Fase 2 — Redacta la propuesta (trabajas)

Construye el contenido de las 7 secciones siguiendo la **anatomía** de arriba. Reglas de redacción que cierran:

- **Resumen ejecutivo**: empieza por el dolor del cliente con SUS palabras, no por ti. Mete 2-3 KPIs (del ROI del diagnóstico). Cierra adelantando entregable + rango de inversión.
- **Problema**: cita la `frase_textual` del diagnóstico LITERAL. 2-4 puntos de dolor cuantificados (de `procesos[]` + `score_rationale`). Empatía, no credenciales.
- **Solución**: 3 fases. Lenguaje de **transformación y de empleado** ("como una recepcionista que cotiza sola"), no de features técnicas. **Obligatorio** el `nota_confianza_ia` (privacidad + control humano — ataca el "¿es una caja negra?").
- **Entregables**: específicos, con cantidades. Incluye `revisiones` y `fuera_de_alcance` (anti scope-creep).
- **Timeline**: hitos semanales + `nota_pausa` protectora.
- **Inversión**: 3 tiers calibrados (§Precios), con `recomendada: true` en el del medio. `ancla_valor` que ata el precio al costo del problema.
- **Prueba social / Sobre ti / CTA**: al final. CTA de **máx 3 pasos** (confirmar tier → firmar alcance → mandar anticipo) + vigencia 14 días + link de calendario.

**Longitud objetivo: equivalente a 3-5 páginas.** El decisor escanea. Que el resumen y la tabla de precios comuniquen solos.

### Fase 3 — Escribe `propuesta.json` (trabajas)

**Lee el contrato:** `Read templates/propuesta.schema.md` — es la fuente de verdad de los nombres de campo. Respétalo al pie de la letra.

1. Carpeta de salida: `propuesta-<slug>/` en el **directorio de trabajo actual del usuario** (NO dentro del skill). `slug` = kebab-case del negocio (ej. `propuesta-sabores-de-casa/`). Si existe, pregunta antes de sobrescribir o sufija con la fecha.
2. Escribe `propuesta-<slug>/propuesta.json` con TODAS las secciones, conforme al schema. Montos en USD (número). `meta.validez_dias = 14`. Listas vacías `[]` donde no haya dato (NO inventar). Marca `"recomendada": true` SOLO en el tier del medio.

### Fase 4 — Genera el HTML cliente-facing + el markdown (trabajas)

1. Corre el generador (usa el binario detectado en Fase 0):
   ```
   node scripts/generar_propuesta.mjs <ruta>/propuesta.json <ruta>/propuesta.html
   ```
   Imprime a stdout la ruta absoluta del `propuesta.html` — captúrala para el mensaje final. Es un documento **claro, premium, imprimible a PDF** (papel blanco, acento de la marca, fuentes Space Grotesk + Instrument Serif). Sin dependencias.
1b. **Generar el PDF (automático).** Tras el `propuesta.html`, corre el conversor compartido (multi-OS, usa el navegador que ya tenga el usuario):
   ```
   python3 ~/.config/agencia-ia/html2pdf.py <ruta>/propuesta.html
   ```
   `PDF: <ruta>` → quedó `propuesta.pdf` junto al HTML (eso le mandas al cliente). `NO_PDF:` → dile que abra el `.html` y haga **Cmd/Ctrl+P → Guardar como PDF**. No bloquees por esto.
2. **FALLBACK sin Node (el HTML SIEMPRE sale).** Si el comando falla o no hay Node: NO te detengas. Escribe tú el `propuesta.html` con Write, replicando la estructura y el CSS del generador (mira `scripts/generar_propuesta.mjs` — el `CSS` y las funciones de cada sección). Documento claro (NO dark), acento cyan, 7 secciones en orden, 3 tiers con el recomendado resaltado, CTA con pasos numerados. Escapa `<` `>` `&`.
3. Genera también el **markdown editable** `propuesta-<slug>/propuesta.md` (rellena `templates/propuesta.md` con los datos reales — quita los placeholders `{{...}}`). Es el robusto/editable, como en /docs-entrega.
4. Genera la **secuencia de seguimiento** `propuesta-<slug>/seguimiento.md` (rellena `templates/seguimiento.md`). Es el activo que de verdad cierra: 5 toques en 21 días.

### Fase 5 — (Opcional) Google Docs + presentar el paquete (el wow)

**Google Docs (opcional, solo si el operador lo pide o aporta):** si quiere comentar/colaborar el cliente, empuja el markdown a un Doc con la CLI `gws` (ya autenticada):
```
gws docs ... (crea un Doc con el contenido de propuesta.md)
```
Si `gws` no está autenticado o falla, NO bloquees — el HTML/PDF es el entregable principal. Solo menciónalo como opción.

**Presenta el paquete** con los NÚMEROS personalizados, no genéricos:

```
Listo. Tu propuesta para [cliente] está armada para cerrar.

Lo que hace que cierre:
• Abre con SU frase: "[cita literal del cliente]" — se va a sentir leído.
• Vende transformación, no una herramienta, y ataca la duda de "¿es una caja negra?".
• 3 opciones con [Recomendado $Y] marcado — la mayoría elige esa.
• Cierra con 3 pasos claros y vigencia de 14 días (urgencia real, no falsa).

Te dejé todo en `propuesta-[slug]/`:
  • propuesta.html      ← el PDF premium para mandarle (ábrelo → imprime a PDF)
  • propuesta.md        ← versión editable por si quieres ajustar algo
  • seguimiento.md      ← los 5 correos de follow-up (recuperan 25-30% de los que se enfrían)
  • propuesta.json      ← los datos (para regenerar o pasar a /contrato)

Para abrir el PDF:
  • Mac:     open propuesta-[slug]/propuesta.html  (luego ⌘P → Guardar como PDF)
  • Windows: start propuesta-[slug]\propuesta.html
  • Linux:   xdg-open propuesta-[slug]/propuesta.html

Cómo presentarla para que cierre (de la investigación):
  1. NO se la mandes en frío por correo — preséntala en una llamada de 15 min y cierra ahí
     (las propuestas por correo se "shopean" y se comparan con la competencia).
  2. En la llamada menciona PRIMERO la opción cara — así la de en medio se siente razonable.
  3. Di el precio con seguridad… y cállate. No te disculpes ni saltes a descuento.
  4. Cierra dando el siguiente paso: "te mando el acuerdo y el link de pago, ¿lo vemos el martes?"

Si cierra: pásame a /contrato para el acuerdo de alcance y a /cobro para el link del anticipo.
```

Indica SIEMPRE la ruta exacta y el comando para abrir según OS.

---

## Reglas duras del skill (las 10)

1. **Es una PROPUESTA, no una cotización.** Vende (problema → transformación → cierre), no lista precios secos. La cotización es `/cotizacion`.
2. **El problema PRIMERO, las credenciales al FINAL.** Siempre. Liderar con tu background mata el cierre.
3. **Cita al cliente LITERAL.** La `frase_textual` del diagnóstico va textual — es lo que más cierra ("me leyó la mente").
4. **3 opciones SIEMPRE**, con el del medio marcado `recomendada`. Calibradas al rango real (diagnóstico/cotización), nunca inventadas.
5. **Ataca el trust gap de IA.** Toda propuesta lleva la nota de "la IA es una herramienta que controlamos, no una caja negra" (privacidad + control humano).
6. **Define el fuera-de-alcance.** Anti scope-creep. Y las rondas de revisión incluidas.
7. **Nada inventado.** Ningún ROI/precio/caso que no venga del diagnóstico/cotización o que el operador confirme. Sin dato → se omite la sección, no se rellena.
8. **NUNCA pushy.** Prohibido countdowns, "cupos", "oferta". La única urgencia es la vigencia de 14 días (real).
9. **Reusa, no recalcules.** Si hay diagnóstico → hereda el dolor y el ROI. Si hay cotización → hereda los tiers. No re-entrevistes lo que ya existe.
10. **Carpeta auto-contenida.** Todo en `propuesta-<slug>/`. El HTML abre e imprime a PDF sin internet (fuentes por CDN; degrada a system fonts si no hay red).

---

## Integración con la suite (la cadena de cierre)

| Skill | Cuándo, respecto a /propuesta |
|---|---|
| **`/diagnostico`** | ANTES. Genera `diagnostico.json` — el insumo que /propuesta lee y re-empaqueta. |
| **`/cotizacion`** | ANTES o EN PARALELO. Sus 3 tiers son los `opciones[]` de la propuesta — /propuesta los reúsa. |
| **`/contrato`** | DESPUÉS de que cierra. El acuerdo de alcance/SOW. (Los `terminos` de la propuesta son un resumen; el contrato es el legal.) |
| **`/cobro`** | DESPUÉS de firmar. El link de pago del anticipo (50%). |
| **`/conectar-cliente`** | En el onboarding tras cerrar — links de Composio para que el cliente conecte cuentas sin dar API keys. |

---

## Manejo de errores y casos difíciles

- **No hay diagnóstico ni cotización:** usa la Fase 1B (mini-cuestionario). No te bloquees, pero recomienda correr `/diagnostico` para una propuesta más afilada.
- **El operador no tiene caso de éxito:** OMITE la sección de prueba social. NUNCA inventes un caso ni una métrica. (Puedes sugerir usar logos de las herramientas de confianza —WhatsApp, Cloudflare— como prueba social ligera.)
- **El operador no sabe qué precio poner:** ancla al mercado ($1,500–$3,000 setup) y sugiere correr `/cotizacion` para el precio fino. No fuerces un número que no defiende.
- **Node no disponible / el generador falla:** usa el fallback de la Fase 4 (Claude escribe el HTML a mano replicando el CSS del generador). El operador nunca se queda sin PDF.
- **`gws` no autenticado:** el Google Doc es opcional — omítelo, el HTML/PDF es el entregable principal. Menciona que puede correr `gws auth login` si lo quiere.
- **Cliente B2B con varios decisores:** recuérdale al operador que incluya al segundo decisor en la llamada de presentación y que NUNCA deje que reenvíen la propuesta sin él (se shopea).

---

## Archivos del skill (qué `Read` y cuándo)

| Archivo | Cuándo leerlo |
|---|---|
| `templates/propuesta.schema.md` | Fase 3 — contrato canónico de `propuesta.json` (la fuente de verdad de los campos) + mapeo desde `diagnostico.json` |
| `templates/propuesta.md` | Fase 4 — plantilla del markdown editable (rellena los `{{...}}`) |
| `templates/seguimiento.md` | Fase 4 — plantilla de los 5 correos de follow-up |
| `templates/ejemplo.propuesta.json` | Referencia — un `propuesta.json` realista lleno (caso "Sabores de Casa"); úsalo para ver el formato o testear el generador |
| `scripts/generar_propuesta.mjs` | Fase 4 — `node scripts/generar_propuesta.mjs <json> <html>` → escribe el HTML premium. Fuente única del HTML (y la referencia para el fallback sin Node) |

---

## Fuentes de la investigación (de `_research/propuesta.md` y `_research/cotizacion.md`)

- **digitalapplied** — anatomía táctica de la propuesta de IA, los números (close 38% vs 23%, tiers, 50% deposit, secuencia de follow-up).
- **Nick (operador, 150+ calls)** — "don't offer a tool, offer a transformation", ROI framing, "name the price and shut up", rollout gradual con wins inmediatos.
- **"$8,400 close"** — manejar objeciones temprano, tono de conversación no de venta.
- **sendtrumpet** — propuesta vs cotización (38% vs 23%). **cobl.ai / adai** — personalizada cierra 32-65% más.
- **freshproposals / HVAC Know It All** — anclaje de 3-4 tiers, +98% revenue. **turbodocx** — cadena propuesta → cotización → SOW.

> Todas las decisiones de estructura, orden, precio y cláusula de este skill vienen de esas fuentes. No hay nada inventado.
