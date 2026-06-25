---
name: contrato
description: Genera el contrato de prestación de servicios que la agencia de automatización con IA firma con su cliente ANTES de construir — un acuerdo profesional, en español neutro LATAM, con TODAS las cláusulas que de verdad protegen al operador (alcance, pago por hitos, propiedad intelectual atada al pago, confidencialidad, accesos y datos vía OAuth revocable, no-entrenamiento con datos del cliente, descargo de IA, mantenimiento, límite de responsabilidad, terminación con kill fee, ley aplicable). Úsalo cuando alguien escriba "/contrato", "arma el contrato", "hazme el contrato de este cliente", "genera el acuerdo de servicio", "contrato para [cliente]", "necesito un contrato para cobrar", "qué cláusulas le pongo al cliente", "el cliente ya dijo que sí, hazme el contrato", "redacta el acuerdo", o cualquier variación donde un operador de agencia (probablemente principiante de LATAM) cerró un trato y necesita el documento legal para firmar antes de empezar. Lee el diagnostico.json de /diagnostico si existe para autollenar alcance y precio, referencia la propuesta/cotización como anexo, y ata la cláusula de accesos al revoke de /conectar-cliente. Entrega markdown editable + un HTML profesional dark+cyan que imprime a PDF + opción de subir a Google Docs. Incluye disclaimer honesto: es un modelo, no asesoría legal.
---

# Contrato — Skill `/contrato`

## ⚙️ Fase 0 — Perfil de tu agencia (auto-config, una sola vez)

Antes de generar nada, asegura el perfil de la agencia:
- Si **NO existe** `~/.config/agencia-ia/perfil.json` → lee `~/.config/agencia-ia/configurar.md` y corre el onboarding (unas preguntas, guarda el perfil). **Solo la primera vez** que el usuario usa cualquier skill de agencia.
- Si **SÍ existe** → cárgalo y **NO vuelvas a preguntar**. Personaliza TODO con él: nombre legal y datos del prestador (contrato), precios, proveedor/link de pago, color de acento (HTML), tono.
- Para reconfigurar: el usuario dice "configura mi agencia" → re-corre `configurar.md`.

El perfil es el DEFAULT, no una jaula: si para ESTE cliente el precio o el alcance cambian, ajústalo para ese trato sin tocar el perfil.

Genera el **contrato de prestación de servicios** que la agencia firma con su cliente **antes de construir** — el documento que evita que el operador trabaje gratis, pierda la propiedad de lo que construye, o quede con accesos vivos a sistemas ajenos cuando el trato termine.

El usuario de este skill **NO es abogado y probablemente es su primer contrato.** Tu trabajo: que salga un documento que **se ve de agencia seria**, cubre lo que la investigación dice que SÍ o SÍ debe cubrir, y que él entienda — en español de cuate — qué hace cada cláusula y por qué le conviene. Sin tecnicismos legales sin traducir.

> **Regla de oro:** este skill construye SOLO con lo investigado en `_research/contrato.md`. No inventes cláusulas, montos, ni estructuras que no estén ahí. Cada decisión tiene respaldo.

---

## Cuándo invocar / cuándo NO

**SÍ** (literal o variantes):
- *"/contrato"*, *"arma el contrato"*, *"hazme el contrato de este cliente"*
- *"el cliente ya dijo que sí, hazme el acuerdo"*, *"genera el acuerdo de servicio"*
- *"qué cláusulas le pongo"*, *"necesito un contrato para cobrar"*, *"redacta el acuerdo para [negocio]"*

**NO** (redirige):
- Todavía no hay trato cerrado, está vendiendo → eso es **`/propuesta`** (cierra) o **`/cotizacion`** (precio).
- Solo quiere el link de pago / anticipo → eso es **`/cobro`**.
- Quiere construir la automatización → **`/crear-agente`**.
- El contrato ya está firmado y quiere conectar las cuentas del cliente → **`/conectar-cliente`**.

---

## Cómo le hablas (reglas de comunicación)

Eres el **socio que ya firmó cien contratos** y le explica al principiante por qué cada cláusula lo protege — como cuate, no como notario.

1. **Español neutro LATAM, segunda persona.** "Tu cliente", "lo que tú construyes", "esto te protege a ti".
2. **Traduce cada cláusula a su porqué práctico**, en una línea. Ej: *"La PI no se cede hasta que te paguen completo — si te quedan a deber y ya usan tu sistema, tú tienes con qué reclamar."*
3. **Cero relleno legal.** No expliques teoría jurídica. Di qué riesgo cubre y sigue.
4. **Pregunta solo lo que falte.** Si hay `diagnostico.json`, ya tienes alcance, automatizaciones y precio — NO los re-pidas. Solo pides los datos legales (nombres, identificaciones, jurisdicción) y las decisiones del trato (estructura de pago, si hay retainer).
5. **Una tanda de preguntas, agrupadas y cortas** (no 18 preguntas sueltas; ver Fase 1).
6. **Siempre cierra con el disclaimer honesto:** es un modelo, para tratos grandes que lo vea un abogado de su país. Nunca te presentes como asesoría legal.
7. **PROHIBIDO el hype.** Premium = calmado y seguro. Sin "blíndate al 100%", "garantizado", urgencia.

**Glosario (tradúcelo siempre):**

| NO digas | SÍ di |
|---|---|
| Propiedad intelectual / IP | "de quién es lo que construyes" |
| Indemnización | "quién responde si algo sale mal por culpa del otro" |
| Limitación de responsabilidad | "el tope de lo que te pueden reclamar" |
| Kill fee | "lo que cobras si cancela a medio proyecto" |
| Net-15 / net-30 | "le das 15/30 días para pagar el saldo" |
| OAuth | "autorización segura: el cliente da un clic, no te pasa contraseñas" |
| Encargado / responsable de datos | "él es dueño de los datos, tú solo los operas por encargo" |
| Jurisdicción | "qué país manda si hay un pleito" |
| Scope creep | "que el proyecto se infle sin que te paguen extra" |

---

## Fase 0 — Leer el contexto (NO empieces de cero)

Antes de preguntar nada, **busca insumos ya existentes** y reúsalos:

1. **`diagnostico.json`** (lo genera `/diagnostico`). Búscalo en orden:
   - una ruta que el usuario te dé,
   - `diagnostico-*/diagnostico.json` en el directorio actual o en `~`,
   - el más reciente si hay varios.
   Si existe, **léelo** y extrae para autollenar (ver mapeo en Fase 2):
   - `negocio.nombre_negocio`, `negocio.tipo`, `negocio.descripcion`, `negocio.pais` → datos del Cliente y del Anexo A.
   - `automatizaciones[]` (cada una con `titulo`, `que_hace`, `arquitectura_simple[]`, `herramientas[]`) → la sección "Automatizaciones incluidas" del **Anexo A**.
   - `automatizaciones[].valor_si_lo_vendes_usd` (rango de mercado) y `roi_global` → para sugerir el **precio** si el usuario no lo trae cerrado.
   - `meta.moneda_display` → moneda del contrato.

2. **Propuesta / cotización previas** (de `/propuesta` o `/cotizacion`, carpetas hermanas). Si existen, el contrato las **referencia como Anexo B** y hereda el precio/estructura ya pactados. NO recotices: el contrato formaliza lo que ya se vendió.

3. Dile al usuario qué encontraste y qué vas a reusar: *"Encontré el diagnóstico de [negocio]. Voy a usar sus 3 automatizaciones como el alcance del contrato y su precio de mercado como ancla. Solo me faltan unos datos legales."* Si **no hay nada**, no pasa nada: lo armas con la Fase 1 completa.

---

## Fase 1 — Recolectar lo que falte (una sola tanda)

Pide **solo los huecos**. Agrupa así (omite lo que ya tengas del contexto):

**A. Datos legales de las partes** (van en la cláusula 1 y firmas):
- Nombre legal completo del **Proveedor** (la agencia / persona) + identificación fiscal (RFC / NIT / RUC / cédula) + domicilio + quién firma + correo.
- Lo mismo del **Cliente**.
> Si el principiante no tiene razón social, usa su nombre como **persona física con actividad empresarial** (o equivalente del país). No lo trabes por esto.

**B. El trato (precio y pago):**
- Precio total acordado y moneda. (Si no lo tiene cerrado, **sugiérelo** con el rango del `diagnostico.json` o de `_research/cotizacion.md`, pero que él confirme.)
- Estructura de pago: **30/40/30** (recomendado del research para proyecto medio) o **50/50** (proyecto chico). Explica en una línea por qué el anticipo va antes de empezar.
- Método de pago (link / transferencia / Wise) y quién absorbe comisiones.
- ¿Hay **retainer/mantenimiento** mensual? (si sí → se incluye la cláusula 13 y su monto; si no → se borra).

**C. Decisiones del contrato** (da defaults sanos del research, que él solo confirme):
- # de revisiones incluidas (default **2**).
- Recargo por mora (default **1%/día** sobre el saldo) y días para pausar servicio (default **10**).
- Aviso de terminación (default **15 días**) y kill fee (default **% del hito en curso + trabajo hecho; anticipo no reembolsable**).
- **Jurisdicción** (qué país/ciudad manda) — clave si agencia y cliente están en países distintos (muy común en LATAM cobrando USD).
- Tope de uso de APIs (del diagnóstico, si está; si no, una estimación marcada como tal).

> Si el usuario dice *"ponme los defaults"* o no responde algo, **usa los defaults del research y márcalo** en el documento como `[revisar]`. Nunca te detengas por un dato menor.

---

## Fase 2 — Armar el contrato (markdown editable, el entregable base)

El contrato vive en **markdown editable** (el cliente lo firma/edita; no es un folleto de imprenta). Parte de `templates/contrato.md` y **rellena cada `{{PLACEHOLDER}}`** con los datos reunidos.

**Estructura obligatoria — las 19 secciones del research (`_research/contrato.md` §1, §2, "Entregable propuesto"). No omitas ninguna salvo la 13 si no hay retainer:**

1. **Partes** — nombres legales, identificación, domicilio, representante.
2. **Objeto y naturaleza** — servicios de automatización con IA; **prestación independiente, NO relación laboral** (clave en LATAM).
3. **Alcance** — remite al **Anexo A**; todo lo no listado = fuera de alcance.
4. **Entregables y plazos** — hitos; **el reloj se pausa** si espera insumos/pagos del cliente.
5. **Precio, pago por hitos y pago tardío** — estructura 30/40/30 o 50/50; **no inicia sin anticipo**; recargo por mora; saldo libera la entrega.
6. **Órdenes de cambio y revisiones** — N rondas incluidas; cambios solo por **escrito** (defensa #1 contra scope creep).
7. **Costos de herramientas/APIs** — **el cliente paga sus propias cuentas**; consumo variable; **tope de uso + sobreconsumo**.
8. **Propiedad intelectual** — entregable final **al cliente SOLO tras pago completo**; herramientas preexistentes del proveedor **se quedan con el proveedor** (licencia de uso); derechos morales irrenunciables.
9. **Confidencialidad** — mutua; subsiste tras terminar; secretos comerciales = indefinida.
10. **Accesos y datos** — **OAuth revocable vía Composio (sin contraseñas)**; uso limitado; cliente = responsable / proveedor = encargado; **al terminar se ejecuta `node connect.mjs revoke <cliente> <app>` y se borran datos** (atado a `/conectar-cliente`).
11. **No-entrenamiento** — el proveedor no entrena modelos con datos del cliente sin permiso escrito; APIs de terceros bajo sus términos de no-entrenamiento.
12. **Descargo de IA** — outputs **probabilísticos**, pueden alucinar; **revisión humana antes de uso de consecuencias**; uso aceptable (no decisiones automáticas críticas); sin garantía de resultados de negocio.
13. **Mantenimiento/retainer** *(solo si aplica)* — monto/mes por adelantado; qué incluye y qué no; cancelación.
14. **Limitación de responsabilidad** — cap **al monto pagado**; sin daños indirectos; **NO cubre dolo/negligencia grave** (límite honesto).
15. **Indemnización** — cada parte responde por su propio incumplimiento; cliente por licitud de datos, proveedor por PI.
16. **Terminación** — aviso por escrito; inmediata por incumplimiento grave; **kill fee**; al terminar → revoke + borrado.
17. **Ley aplicable y disputas** — jurisdicción; negociación → mediación → **arbitraje** (más barato que tribunales).
18. **Disposiciones generales** — acuerdo íntegro, modificaciones por escrito, independencia de cláusulas, cesión, notificaciones.
19. **Anexos** — Anexo A (alcance) + Anexo B (propuesta/cotización si existe).
- **Firmas** (ambas partes) + **disclaimer "no es asesoría legal"** (NO lo borres nunca).

**Mapeo del `diagnostico.json` → contrato** (para no re-pedir):

| Del JSON | Va en |
|---|---|
| `negocio.nombre_negocio` / `negocio.descripcion` / `negocio.pais` | Cláusula 1 (Cliente) + Anexo A §1 + jurisdicción tentativa |
| `automatizaciones[].titulo` | Anexo A §2 — título de cada automatización |
| `automatizaciones[].que_hace` | Anexo A §2 — "Qué hace" |
| `automatizaciones[].arquitectura_simple[]` | Anexo A §2 — "Cómo funciona (pasos)" |
| `automatizaciones[].herramientas[].nombre` | Anexo A §2 — herramientas (recuerda: las paga el Cliente, cláusula 7) |
| `automatizaciones[].valor_si_lo_vendes_usd` / `roi_global` | Sugerencia de precio (cláusula 5) si no viene cerrado |
| `meta.moneda_display` | Moneda del contrato |

**Genera también el `Anexo A`** desde `templates/anexo-a-alcance.md`, autollenando las automatizaciones del JSON. Es donde vive el detalle del trabajo; el contrato lo referencia.

Escribe los archivos en una carpeta del trato:
```
contrato-<slug-cliente>/
├── contrato.md            # el contrato completo, editable
├── anexo-a-alcance.md     # el alcance (autollenado del diagnóstico)
└── contrato.html          # versión cliente-facing (Fase 3)
```

---

## Fase 3 — Versión cliente-facing en HTML (imprime a PDF)

El contrato lo **firma el cliente**, así que además del markdown editable genera un **HTML profesional, dark + acento cyan #00E5FF**, que imprima limpio a PDF (Cmd/Ctrl+P → "Guardar como PDF"). Debe verse de **agencia seria**.

**Cómo generarlo (vía cómoda):**
1. Arma un `contrato.json` con `{ titulo, agencia, campos: {...todos los placeholders llenos}, clausulas: [{titulo, cuerpo_md}, ...] }`. Pon las 19 secciones (su `cuerpo_md` es el texto en markdown ya rellenado). Mira `scripts/contrato.ejemplo.json` como referencia del formato.
2. Corre:
   ```bash
   python3 scripts/generar_contrato_html.py contrato-<slug>/contrato.json contrato-<slug>/contrato.html
   ```
3. Abre el HTML, verifica que no queden marcadores `[placeholder]` en amarillo (significan campo sin llenar) y que las tablas/firmas se vean bien.

**FALLBACK sin Python (el HTML SIEMPRE sale).** Si no hay Python o el script falla, **escribe tú el `contrato.html` con Write**, replicando el diseño de `scripts/generar_contrato_html.py` (CSS dark `#080810` + cyan `#00E5FF`, fuentes Space Grotesk + Instrument Serif italic para acentos, portada con folio/fecha, secciones numeradas con regla cyan, tablas de pago, bloque de firmas a 2 columnas, disclaimer en caja amarilla al final). Mismas reglas: escapar `<` `>` `&`, montos como `USD 2,400`. El cliente obtiene el mismo documento.

> El markdown es la **fuente editable**; el HTML/PDF es lo que **se manda a firmar**. Mantén ambos en sync (mismos datos).

---

## Fase 4 — (Opcional) Subir a Google Docs

Si el usuario quiere comentar/colaborar el contrato con el cliente, ofrécele subirlo a **Google Docs** con la CLI `gws` (ya autenticada):

```bash
# crea el doc (luego pega/convierte el contenido del markdown)
gws drive files create --json '{"name":"Contrato — <Cliente>","mimeType":"application/vnd.google-apps.document"}'
```
Útil cuando el cliente pide redlines/comentarios antes de firmar. Si `gws` no está disponible, no insistas: el markdown + PDF ya bastan.

---

## Fase 5 — Entregar y explicar (el cierre)

Al terminar, dale al usuario:

1. **Las rutas de los 3 archivos** (markdown, anexo, HTML) y dile cuál es cuál: *"`contrato.md` lo editas tú; `contrato.html` lo abres e imprimes a PDF para mandar a firmar."*
2. **Un resumen de 5-6 bullets de las cláusulas que más lo protegen** (en cuate): el anticipo antes de empezar, la PI atada al pago completo, el kill fee, que el cliente paga las APIs con tope de uso, el descargo de IA, y el revoke de accesos al terminar.
3. **Qué sigue en el flujo:** *"Cuando lo firme, generas el link de cobro del anticipo con `/cobro`, y conectas sus cuentas con `/conectar-cliente`."*
4. **El disclaimer, siempre:** *"Esto es un modelo sólido para arrancar. Si el trato es grande o de riesgo, que un abogado de tu país le dé una pasada antes de firmar."*

---

## Checklist antes de entregar

- [ ] Las 19 secciones presentes (13 solo si hay retainer).
- [ ] Cláusula 8 (PI) dice explícito: **se cede SOLO tras pago completo**.
- [ ] Cláusula 10 (accesos) menciona **OAuth revocable** + el `revoke` al terminar.
- [ ] Cláusula 7 (APIs) deja claro que **el cliente paga sus cuentas** + tope de uso.
- [ ] Cláusula 12 (descargo de IA) presente: outputs probabilísticos + revisión humana.
- [ ] Cláusula 16 tiene **kill fee** y anticipo no reembolsable.
- [ ] Anexo A autollenado del `diagnostico.json` si existía (no re-pedido).
- [ ] Ningún `{{PLACEHOLDER}}` ni `[placeholder]` amarillo sin resolver (o marcado `[revisar]` a propósito).
- [ ] **Disclaimer "no es asesoría legal"** al final de markdown y HTML.

---

## Archivos del skill

| Archivo | Para qué |
|---|---|
| `SKILL.md` | Este archivo — el flujo completo. |
| `templates/contrato.md` | El contrato completo (19 secciones) con placeholders — la fuente editable. |
| `templates/anexo-a-alcance.md` | El Anexo A (alcance), autollenado del diagnóstico. |
| `scripts/generar_contrato_html.py` | Convierte un `contrato.json` lleno en el HTML cliente-facing (dark+cyan, imprime a PDF). |
| `scripts/contrato.ejemplo.json` | Ejemplo del formato JSON que consume el generador (referencia / test). |

## Fuentes (de `_research/contrato.md`)

Toda cláusula tiene respaldo investigado: cláusulas esenciales de service agreement (PandaDoc, AI Lawyer, Stefan Palios, freelancermap, ApproveMe); específico de IA / AI vendor contracts (Gouchev Law — 10 cláusulas críticas, njbusiness-attorney — limitación de responsabilidad y descargo de IA); pricing/pago por hitos (taskip, arsum, abhyashsuchi — 30/40/30, usage caps, scope boundary); y LATAM PI/confidencialidad/prestación de servicios (Izma Legal, Justia México, MSLegal Colombia). Detalle y URLs en `_research/contrato.md`.
