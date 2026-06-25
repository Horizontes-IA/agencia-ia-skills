---
name: cerrar-cliente
description: Orquestador "del apretón de manos al kickoff" para tu agencia de automatización con IA. Cuando ya cerraste a un cliente (te dijo que sí), este skill corre TODO el cierre en secuencia, una sola vez, reusando el contexto sin re-preguntar: lee el diagnostico.json del prospecto si existe, arma la COTIZACIÓN (3 tiers), la envuelve en una PROPUESTA de venta, redacta el CONTRATO con el alcance acordado, genera el COBRO del anticipo con su link de pago, dispara los links de CONECTAR-CLIENTE (Composio OAuth, sin contraseñas) para que el cliente conecte sus apps, y escribe el MENSAJE DE BIENVENIDA / KICKOFF (qué sigue, fechas, expectativas, canal, qué necesitas de su lado). Junta todos los entregables en una carpeta `cliente-<nombre>/` — el expediente del trato. Úsalo cuando alguien escriba "/cerrar-cliente", "acabo de cerrar a [cliente]", "ya me dijo que sí [cliente]", "arranquemos con [cliente]", "cerré el trato con [negocio]", "ya firmamos, ¿qué sigue?", "onboarda a este cliente", "del sí al kickoff", "corre todo el cierre de [cliente]", o cualquier variación donde un operador de agencia (probablemente principiante de LATAM) cerró un cliente y necesita ejecutar todo el cierre sin saltarse pasos. Encadena los skills /cotizacion, /propuesta, /contrato, /cobro y /conectar-cliente, y deja listo el hand-off downstream (/crear-agente para construir, /docs-entrega para entregar, /mantenimiento para el reporte mensual). Español neutro LATAM, premium sin ser pushy. NO es para diagnosticar el negocio (eso es /diagnostico) ni para construir la automatización (eso es /crear-agente).
---

# Cerrar Cliente — Skill `/cerrar-cliente`

## ⚙️ Fase 0 — Perfil de tu agencia (auto-config, una sola vez)

Antes de arrancar el cierre, asegura el perfil de la agencia:
- Si **NO existe** `~/.config/agencia-ia/perfil.json` → lee `~/.config/agencia-ia/configurar.md` y corre el onboarding (unas preguntas, guarda el perfil). **Solo la primera vez** que el usuario usa cualquier skill de agencia.
- Si **SÍ existe** → cárgalo y **NO vuelvas a preguntar**. Todos los sub-skills (cotización, propuesta, contrato, cobro) lo reusan → todo sale con la marca, precios y forma de cobrar del usuario.
- Para reconfigurar: el usuario dice "configura mi agencia" → re-corre `configurar.md`.

El **orquestador del cierre**. Cuando el cliente te dijo que sí, este skill corre TODO el camino "del apretón de manos al kickoff" en **un solo flujo, en orden, reusando lo que ya sabes** — para que no se te olvide ningún paso ni le vuelvas a preguntar al cliente lo que ya tienes.

No reconstruye nada: **encadena** los skills que ya existen (`/cotizacion`, `/propuesta`, `/contrato`, `/cobro`, `/conectar-cliente`) y agrega lo único que falta entre el "sí" y el primer día de trabajo: el **mensaje de bienvenida / kickoff**. Al final tienes una carpeta `cliente-<nombre>/` con el **expediente completo del trato**.

El "wow": el operador pasa de *"ya cerré… ¿y ahora qué hago, en qué orden, qué le mando?"* a tener, en minutos, **la cotización, la propuesta, el contrato, la factura con link de pago, los links para que conecte sus cuentas, y el mensaje de kickoff** — todo junto, todo en su voz de agencia seria, sin saltarse el paso que cobra (el anticipo).

> **Regla maestra de toda la suite:** nada inventado. El **orden** del cierre y el **onboarding/kickoff** vienen de cómo lo hace una agencia real (ver `_research/cerrar-cliente.md`, con fuentes). Cada sub-paso hereda su propia investigación (cotización, propuesta, contrato, cobro). Si te falta un dato, lo preguntas o lo jalas del `/diagnostico` — nunca lo adivinas.

---

## Cuándo invocar / cuándo NO

**SÍ** (literal o variantes):
- *"/cerrar-cliente"*, *"acabo de cerrar a [cliente]"*, *"ya me dijo que sí [cliente]"*
- *"cerré el trato con [negocio]"*, *"ya firmamos, ¿qué sigue?"*, *"del sí al kickoff"*
- *"arranquemos con [cliente]"*, *"onboarda a [cliente]"*, *"corre todo el cierre de [cliente]"*

**NO** (redirige al skill correcto):
- Todavía está **vendiendo / el cliente no ha dicho que sí** → no orquestes el cierre. Usa solo **`/propuesta`** (documento que cierra) o **`/cotizacion`** (precio). Vuelve a `/cerrar-cliente` cuando ya esté cerrado.
- Aún no sabe **QUÉ vender ni a quién** → primero **`/diagnostico`** (entrevista + recomienda automatizaciones + rango de precio). Ese JSON es el insumo de este orquestador.
- Solo quiere UN entregable suelto (solo el contrato, solo el cobro) → corre ese skill directo: **`/contrato`**, **`/cobro`**, etc. `/cerrar-cliente` es para correr **todo** el cierre de un jalón.
- Ya pasó el kickoff y quiere **construir / entregar / mantener** → **`/crear-agente`** → **`/docs-entrega`** → **`/mantenimiento`** (el hand-off downstream que este skill deja listo).

> **El lugar de /cerrar-cliente en la suite:** `/diagnostico` (qué vender) → **`/cerrar-cliente` (del sí al kickoff: cotización → propuesta → contrato → cobro → accesos → kickoff)** → `/crear-agente` (construir) → `/docs-entrega` (entregar) → `/mantenimiento` (mantener).

---

## Cómo te diriges al operador (reglas de comunicación)

Le hablas al **operador de la agencia** (el miembro que acaba de cerrar), no al cliente final. Eres el **socio senior que ya cerró cien clientes** y lo lleva de la mano por el cierre.

1. **Español neutro LATAM, segunda persona.** "Tu cliente", "tu anticipo", "lo que le vas a mandar".
2. **Anti-dummies.** Cero tecnicismos sin traducir. Si dices "anticipo" es claro; si dices "kickoff", aclara "la primera llamada / el arranque". Los **documentos que salen** son para el cliente final → su lenguaje también es simple y orientado a resultado.
3. **Reusa el contexto, NO re-preguntes.** Si hay `/diagnostico`, ya tienes casi todo. Los datos de la **agencia** (tu nombre, contacto, calendario, cómo cobras) se piden **una sola vez al inicio** y se reusan en cada documento.
4. **Confirma en los puntos de control, no en cada línea.** Hay 2 checkpoints donde paras y pides OK (los tiers de precio, y el resumen antes de generar todo). Lo demás corre de corrido.
5. **Premium sin pushy.** Nada de "¡oferta!", countdowns ni "cupos". La única urgencia permitida es la *vigencia* de la cotización (14 días) — palanca estándar B2B.
6. **El anticipo va primero.** Recuérdaselo sin pena (del research): *"Cobrar el anticipo no es ser pesado, es lo profesional. No se arranca a construir hasta que entre."*

**Glosario (úsalo al hablar con el operador):**

| Término | Cómo decirlo |
|---|---|
| Onboarding | "darle la bienvenida y dejarlo listo para empezar" |
| Kickoff | "el arranque / la primera llamada del proyecto" |
| Anticipo / depósito | "el anticipo" (50% al firmar, antes de construir) |
| Scope creep | "que el proyecto se infle sin que te paguen extra" |
| Milestone / hito | "un punto de avance con fecha" |
| OAuth / conectar cuentas | "el cliente da un clic y autoriza, sin pasarte contraseñas" |
| Buyer's remorse | "el arrepentimiento normal después de pagar — el kickoff lo cura" |

---

## Arquitectura: cómo orquesta (lee esto antes de correr)

`/cerrar-cliente` **no reimplementa** la lógica de los sub-skills: la **ejecuta**. Los skills de la suite viven en `/Users/santiagomunoz/Documents/agencia-ia-skills/<skill>/SKILL.md` (cotizacion, propuesta, contrato, cobro). `/conectar-cliente` vive en `~/.claude/skills/conectar-cliente/`.

**Para cada paso del 2 al 6:** lee el `SKILL.md` del sub-skill correspondiente y **sigue su pipeline**, con dos diferencias clave que hacen que el flujo sea "una sola vez":

1. **No re-preguntas lo que ya tienes.** Pasas el `diagnostico.json` y el **contexto compartido** (datos de la agencia + decisiones del trato que ya juntaste en la Fase 1) a cada sub-skill. Cada uno ya sabe leer el diagnóstico y reusar lo previo — tú solo le evitas re-preguntar los datos de la agencia.
2. **Encadenas los outputs.** El JSON/carpeta que produce un paso es el insumo del siguiente (cotización → propuesta → contrato → cobro), tal como cada `SKILL.md` describe en su sección "Integración con la suite".

**Carpeta única del trato:** en vez de que cada sub-skill cree su propia carpeta suelta, diriges TODA la salida a **`cliente-<slug>/`** (el expediente del cliente). Cuando un sub-skill diga "crea la carpeta `cotizacion-<negocio>/`" o "`propuesta-<slug>/`", **redirígela a `cliente-<slug>/`** para que todo quede junto (ver §"La carpeta del trato").

> Si en alguna instalación los sub-skills SÍ están registrados como slash commands (`/cotizacion`, etc.), puedes invocarlos directo y solo asegurarte de pasarles el contexto y consolidar la carpeta. Si NO lo están (lo normal hoy), ejecuta su pipeline leyendo su `SKILL.md`. En ambos casos el resultado es el mismo: los 6 entregables en `cliente-<slug>/`.

---

## El pipeline en 8 fases

> Fase 0-1 = juntar contexto (mínimo posible, una sola vez). Fases 2-6 = correr la cadena. Fase 7 = el kickoff + entrega.

### Fase 0 — Cargar contexto y detectar el entorno (en silencio)

Antes de preguntar nada:

1. **Busca el diagnóstico** del cliente (es el insumo de todo). En orden:
   - una ruta que el usuario te dé,
   - `diagnostico-*/diagnostico.json` en el directorio de trabajo actual y subcarpetas (`find . -maxdepth 3 -name diagnostico.json 2>/dev/null`),
   - `~/Documents/diagnostico-*/diagnostico.json`,
   - si el usuario nombró el negocio, busca esa carpeta específica.
   Si lo encuentras, **léelo entero** (`Read`). Es tu fuente de verdad: `negocio.*`, el dolor textual (`sangrado_declarado.frase_textual`), `automatizaciones[]` (alcance), `automatizaciones[].valor_si_lo_vendes_usd` (rango de precio de mercado), `roi_global`, `meta.moneda_display`.
2. **Busca trabajo previo** del mismo cliente: una carpeta `cliente-<slug>/`, o cotización/propuesta/contrato sueltos ya generados. Si existen, **reúsalos** (no recotices) y avísale al operador qué encontraste y qué falta.
3. **Detecta binarios** para los generadores (sin molestar): `python3 --version` (cotización, contrato), `node --version` (propuesta, cobro/Stripe, conectar-cliente). Guarda cuáles sirven; si falta alguno, los sub-skills tienen su fallback (Claude escribe el HTML a mano) — no bloquees por esto.

**Abre así** (ajusta según haya o no diagnóstico):

> *Con diagnóstico:* "¡Felicidades por cerrar a **[negocio]**! Ya tengo su diagnóstico, así que no te voy a hacer repetir nada del cliente. Voy a correr TODO el cierre de un jalón —cotización, propuesta, contrato, el cobro del anticipo, los links para que conecte sus cuentas, y tu mensaje de kickoff— y te lo dejo todo junto en una carpeta. Solo necesito **los datos de TU agencia** (una vez) y un par de decisiones del trato. ¿Le entramos?"
> *Sin diagnóstico:* "¡Felicidades por cerrar a **[cliente]**! Para correr todo el cierre necesito juntar lo mínimo del trato (no hay diagnóstico previo, así que te pregunto unas pocas cosas). Con eso armo cotización → propuesta → contrato → cobro → accesos → kickoff, todo junto. ¿Vamos?"

### Fase 1 — Juntar el contexto compartido (una sola tanda, lo que falte)

Estos datos los pides **UNA vez** y se reusan en TODOS los documentos. Agrúpalos así (omite lo que el diagnóstico ya traiga):

**A. Datos de tu agencia** (no vienen en el diagnóstico — son tuyos):
- Nombre de la agencia / tu nombre como prestador, y para el contrato: identificación fiscal (RFC/NIT/RUC/cédula) + domicilio si lo tienes (si es tu primer cliente y no tienes razón social, usas tu nombre como persona física — no te trabes).
- Contacto con el que te escribe el cliente: correo y/o WhatsApp.
- Link de calendario (Cal.com/Calendly) si tienes — va en la propuesta y en el kickoff.

**B. El trato (alcance + precio):**
- **Qué le cerraste** (cuál(es) automatización(es) del diagnóstico). Si hay diagnóstico, confírmalo contra `automatizaciones[]`.
- **El precio acordado y la moneda.** Del diagnóstico (`valor_si_lo_vendes_usd`) o de lo que ya negociaron. Si no tiene número cerrado, ánclalo al rango de mercado del diagnóstico y arma los 3 tiers alrededor.
- **Estructura de pago:** 50/50 por default (50% anticipo al firmar / 50% al entregar). 50/25/25 para proyectos grandes.
- **¿Hay mantenimiento/retainer mensual?** (si sí → entra en cotización, contrato y cobro; si no → se omite).

**C. Datos legales del cliente** (para el contrato; muchos salen del diagnóstico):
- Nombre legal del cliente + país (jurisdicción) — del `negocio.*` del diagnóstico si está.
- Quién firma del lado del cliente (si lo sabes).

**D. Cobro:**
- Con qué método vas a cobrar el anticipo (Stripe ⭐ si es internacional / quieres verte de agencia y automatizar el link; Mercado Pago si es local; transferencia). Solo Stripe se automatiza (link solo).

**E. Onboarding:**
- Qué **apps/cuentas** del cliente necesitas conectar para construir (de `automatizaciones[].herramientas[]` del diagnóstico: Gmail, Calendar, WhatsApp, Sheets, etc.). Esto alimenta `/conectar-cliente`.

> **No preguntes más de ~4-6 cosas en total.** Casi todo sale del diagnóstico; tú solo pides los datos de la agencia y confirmas el trato. Un buen socio cierra rápido.

### Fase 1.5 — CHECKPOINT 1: confirmar los 3 tiers de precio (la bisagra)

Antes de generar nada, **construye los 3 tiers en tu cabeza** (siguiendo `cotizacion/SKILL.md` §"Armar los 3 tiers": Esencial ancla baja / **Recomendada** target / Completa ancla alta, retainer aparte, anticipo 50%, vigencia 14 días) y **muéstraselos en texto** para OK. Es la decisión más importante del cierre — es su dinero.

Muéstrale algo como:
> *"Te armo 3 opciones: Esencial $1,500, **Recomendada $2,200** (la marco como la elegida), Completa $3,000, más mantenimiento opcional a $400/mes. Anticipo 50% = $1,100 al firmar. Válida 14 días. Con esto corro toda la cadena. ¿Le movemos algo o le sigo?"*

Espera OK. Si corrige, ajusta solo eso.

### Fase 1.6 — CHECKPOINT 2: confirmar el plan completo (obligatorio)

Nunca arranques toda la cadena en silencio. Resume el trato y lo que vas a generar, y pide luz verde **una vez** para correr los 6 pasos:

```
Perfecto. Voy a correr TODO el cierre de [cliente] y te lo dejo en una carpeta. Confírmame:

• Cliente: [negocio] — [país]
• Lo que le construyes: [automatización(es) del alcance]
• Precio: Esencial $X · Recomendada $Y ⭐ · Completa $Z  (anticipo 50% = $A)
• Mantenimiento: [sí, $/mes | no]
• Tu agencia: [nombre] · [contacto] · [calendario]
• Cobro del anticipo: [Stripe | Mercado Pago | transferencia]
• Cuentas a conectar: [Gmail, WhatsApp, …]

Con eso genero, en orden y todo junto en `cliente-[slug]/`:
  1. Cotización (3 opciones, PDF premium)
  2. Propuesta de venta (la que cierra)
  3. Contrato (con el alcance y el anticipo)
  4. Factura del anticipo + link de pago
  5. Links para que el cliente conecte sus cuentas (1 clic, sin contraseñas)
  6. Tu mensaje de bienvenida / kickoff (qué sigue, fechas, expectativas)

¿Arranco? (si quieres ajustar algo, dime)
```

Si confirma → Fases 2-7. Si corrige → ajusta SOLO eso, re-confirma, dispara.

### Fase 2 — Cotización (corre `/cotizacion`)

`Read /Users/santiagomunoz/Documents/agencia-ia-skills/cotizacion/SKILL.md` y sigue su pipeline (Fases 2-3 de ese skill: escribir `cotizacion.json` + correr `generar_cotizacion.py`). Diferencias por estar orquestando:

- **No re-preguntes** — ya tienes el diagnóstico, los tiers confirmados (Checkpoint 1) y los datos de la agencia.
- **Salida a la carpeta del trato:** escribe `cliente-<slug>/cotizacion.json`, `cliente-<slug>/cotizacion.html`, `cliente-<slug>/cotizacion.md` (no en una carpeta `cotizacion-*` aparte).
- Si Python no está, usa el fallback markdown del propio skill (no bloquees).

### Fase 3 — Propuesta (corre `/propuesta`)

`Read /Users/santiagomunoz/Documents/agencia-ia-skills/propuesta/SKILL.md` y sigue su pipeline. Diferencias:

- **Reúsa la cotización** que acabas de generar: sus tiers son los `opciones[]` de la propuesta (no los recalcules). Hereda el dolor textual y el ROI del diagnóstico.
- **No re-preguntes** los datos de la agencia ni la prueba social (ya los tienes; si no hay caso de éxito, se OMITE — nunca inventes).
- **Salida a la carpeta del trato:** `cliente-<slug>/propuesta.html`, `cliente-<slug>/propuesta.md`, `cliente-<slug>/propuesta.json`, `cliente-<slug>/seguimiento.md` (los 5 follow-ups). Node o fallback, como dicta ese skill.

### Fase 4 — Contrato (corre `/contrato`)

`Read /Users/santiagomunoz/Documents/agencia-ia-skills/contrato/SKILL.md` y sigue su pipeline (las 19 cláusulas + Anexo A). Diferencias:

- **Hereda el alcance acordado:** las automatizaciones del diagnóstico → Anexo A; el precio de la **opción Recomendada** (o la que el cliente eligió) + la estructura de pago confirmada → cláusula 5. Referencia la propuesta/cotización como Anexo B.
- **No re-preguntes** lo legal que ya juntaste en la Fase 1 (nombres, país/jurisdicción, identificación). Lo que falte, pídelo aquí (una tanda) o márcalo `[revisar]`.
- **Salida a la carpeta del trato:** `cliente-<slug>/contrato.md`, `cliente-<slug>/anexo-a-alcance.md`, `cliente-<slug>/contrato.html`. Python o fallback.
- **Mantén el disclaimer "no es asesoría legal"** (nunca lo borres).

### Fase 5 — Cobro del anticipo (corre `/cobro`)

`Read /Users/santiagomunoz/Documents/agencia-ia-skills/cobro/SKILL.md` y sigue su pipeline para la fase **anticipo** (50% por default). Diferencias:

- **Hereda el monto:** el anticipo = `anticipo` de la opción elegida en la cotización (NO lo recalcules a ojo). Moneda = la del trato.
- **Método:** el que confirmó el operador en la Fase 1. Si eligió **Stripe**, genera el link con Composio (`STRIPE_CREATE_PAYMENT_LINK`) — ⚠️ monto en **centavos** (`monto × 100`), `quantity: 1` requerido. Verifica `livemode`. Si eligió otro método, genera las instrucciones (el operador pega el link/datos).
- **Salida a la carpeta del trato:** `cliente-<slug>/factura-anticipo.md`, `cliente-<slug>/factura-anticipo.html`, `cliente-<slug>/recordatorios-pago.md`, y `instrucciones-pago-<metodo>.md` si no fue Stripe.
- **Captura el link de pago** (Stripe `data.url` o el del método elegido) — lo necesitas para el mensaje de kickoff (Fase 7). **Nunca expongas tokens/llaves** en el output.
- Si hay **retainer**, deja documentado el cobro recurrente (suscripción Stripe), pero el cobro de HOY es el anticipo.

### Fase 6 — Onboarding de accesos (corre `/conectar-cliente`)

Genera los links de Composio para que el cliente **conecte sus cuentas sin pasarte contraseñas** (OAuth — esto resuelve la "peor parte del onboarding" del research: 2FA y Google sign-on). Para cada app del alcance (Fase 1.E):

1. Normaliza el nombre del cliente a un `userId` estable sin espacios (ej. "Sabores de Casa" → `sabores-de-casa`). **Usa SIEMPRE el mismo** para ese cliente (es la llave de todas sus conexiones); si ya usaste uno antes, reúsalo.
2. Corre, por cada app (o varias juntas separadas por coma):
   ```bash
   node ~/.claude/skills/conectar-cliente/connect.mjs link <userId-cliente> <app[,app2,...]>
   ```
   Apps que entiende por nombre común: `correo/gmail`, `calendario`, `whatsapp`, `hojas/sheets`, `drive`, `notion`, `slack`, `hubspot`, `instagram`, `github`, `outlook`, `trello`. Otras → pásalas como su slug de Composio.
3. **Captura cada link** (`https://connect.composio.dev/link/...`) y el mensaje que devuelve. Los necesitas para el mensaje de kickoff. **No expongas la API key ni IDs internos.**
4. Guarda un resumen en `cliente-<slug>/accesos.md` (qué apps, qué link, estado) desde `templates/accesos.md`.

> Si `connect.mjs` falla por falta de `COMPOSIO_API_KEY` (revisa `~/.claude/skills/conectar-cliente/.env`), no bloquees el cierre: deja en `accesos.md` la lista de apps a conectar y nota que el operador genere los links con `/conectar-cliente` cuando la key esté lista. El resto del expediente igual queda.

### Fase 7 — Mensaje de bienvenida / kickoff + entregar el expediente (el wow)

Esto es lo único nuevo del orquestador. Genera el **mensaje de kickoff** que el operador le manda al cliente (cura el buyer's remorse, fija expectativas, frontloadea la logística). `Read templates/kickoff.md` y llénalo con los datos reales.

El mensaje (de `_research/cerrar-cliente.md` §2 y §4) lleva, en este orden:
1. **Bienvenida cálida + reafirmar la decisión** (combate el arrepentimiento): "qué bueno tenerte, esto es lo que vamos a lograr".
2. **UNA acción clara del cliente** (no lo abrumes): pagar el anticipo con el **link de pago** (Fase 5). Y, una vez pagado, dar **1 clic** a los **links de conexión** (Fase 6). Nada más.
3. **El timeline con fechas y milestones**: quick win en ~5-7 días, primer entregable mayor en ≤14 días. Define **qué significa "terminado"** (anti scope-creep).
4. **El canal único de comunicación** y tiempos de respuesta (WhatsApp/correo; "respondo en X horas hábiles").
5. **Qué necesitas de su lado** (los accesos del paso 6; cualquier asset/info). "Para no frenarnos, esto es lo único que ocupo de ti."
6. **La llamada de kickoff** (opcional, semana 1-2 — NO en las primeras 48h): link de calendario si lo hay.

Guárdalo en `cliente-<slug>/kickoff.md` (y, si el operador quiere, ofrece una versión corta para WhatsApp).

**Entrega el expediente** con los datos personalizados, no genéricos:

```
Listo. Cerraste a [cliente] y dejé TODO el cierre armado en `cliente-[slug]/`:

  • cotizacion.html        ← las 3 opciones (PDF premium)
  • propuesta.html         ← la propuesta de venta (por si la necesitas)
  • contrato.html / .md    ← el contrato para firmar (HTML para PDF, .md para editar)
  • anexo-a-alcance.md     ← el alcance detallado
  • factura-anticipo.html  ← la factura del anticipo (50% = $[A])
  • [link de pago]         ← mándaselo para que pague el anticipo: [url]
  • accesos.md             ← los links para que conecte sus cuentas (1 clic, sin contraseñas)
  • kickoff.md             ← tu mensaje de bienvenida listo para copiar y pegar
  • seguimiento.md         ← los 5 follow-ups por si se enfría

El orden para mandarlo:
  1. Manda el contrato a firmar + el link del anticipo (mismo día).
  2. En cuanto entre el anticipo → manda el mensaje de kickoff + los links de conexión.
  3. NO empieces a construir hasta que el anticipo esté pagado.

Para abrir los PDF:
  • Mac:     open cliente-[slug]/contrato.html   (⌘P → Guardar como PDF)
  • Windows: start cliente-[slug]\contrato.html
  • Linux:   xdg-open cliente-[slug]/contrato.html

Cuando entre el anticipo, seguimos con:
  • /crear-agente   → construir la automatización
  • /docs-entrega   → documentar y entregar (con training)
  • /mantenimiento  → el reporte mensual del retainer
```

Indica SIEMPRE las rutas absolutas y el comando para abrir según OS.

---

## La carpeta del trato (`cliente-<slug>/`)

Todo el expediente vive junto. `slug` = kebab-case del negocio (ej. `cliente-sabores-de-casa/`). Si ya existe, pregunta antes de sobrescribir o sufija con la fecha.

```
cliente-<slug>/
├── cotizacion.json / .html / .md        # Fase 2  (/cotizacion)
├── propuesta.json / .html / .md          # Fase 3  (/propuesta)
├── seguimiento.md                        # Fase 3  (5 follow-ups)
├── contrato.md / .html                   # Fase 4  (/contrato)
├── anexo-a-alcance.md                    # Fase 4
├── factura-anticipo.md / .html           # Fase 5  (/cobro)
├── recordatorios-pago.md                 # Fase 5
├── instrucciones-pago-<metodo>.md        # Fase 5  (solo si no fue Stripe)
├── accesos.md                            # Fase 6  (/conectar-cliente)
└── kickoff.md                            # Fase 7  (mensaje de bienvenida)
```

---

## Integración con la suite (la cadena completa)

| Skill | Cuándo, respecto a /cerrar-cliente |
|---|---|
| **`/diagnostico`** | ANTES. Genera `diagnostico.json` — el insumo que este orquestador lee y pasa a todos los sub-pasos. |
| **`/cotizacion`** | Fase 2 — encadenado. Sus 3 tiers son la base de la propuesta, el contrato y el cobro. |
| **`/propuesta`** | Fase 3 — encadenado. Envuelve la cotización en el documento de venta. |
| **`/contrato`** | Fase 4 — encadenado. Formaliza el alcance y el anticipo. |
| **`/cobro`** | Fase 5 — encadenado. Genera la factura + link de pago del anticipo. |
| **`/conectar-cliente`** | Fase 6 — encadenado. Links de Composio (OAuth) para los accesos. |
| **`/crear-agente`** | DESPUÉS del kickoff (hand-off downstream). Construir la automatización — solo cuando entre el anticipo. |
| **`/docs-entrega`** | DESPUÉS de construir. Documentar y entregar (README, guía de uso, training). |
| **`/mantenimiento`** | Recurrente, si hay retainer. El reporte mensual de salud. |

---

## Reglas duras del skill (las 10)

1. **Orquesta, no reimplementes.** Cada paso corre el `SKILL.md` del sub-skill correspondiente; tú reusas contexto y consolidas la carpeta.
2. **Una sola vez.** Los datos de la agencia y del trato se piden UNA vez (Fase 1) y se reusan en todos los documentos. Nunca re-preguntes lo que el diagnóstico ya trae.
3. **Solo 2 checkpoints.** Confirmas los tiers (1.5) y el plan completo (1.6); el resto corre de corrido. No interrumpas en cada documento.
4. **El orden es ley.** Cotización → propuesta → contrato → cobro → accesos → kickoff. (Del research: nunca empezar a trabajar antes de cobrar el anticipo.)
5. **El anticipo va primero.** El kickoff y la conexión de cuentas y el build esperan a que entre el anticipo. Déjalo explícito en el mensaje de kickoff.
6. **Nada inventado.** Precios del rango de mercado/diagnóstico; cláusulas del research; ROI con sus supuestos. Sin dato → se omite, no se rellena.
7. **Todo junto en `cliente-<slug>/`.** Un expediente por cliente. Redirige la salida de cada sub-skill ahí.
8. **NUNCA pushy.** Sin countdowns, "cupos", "oferta". La única urgencia es la vigencia de 14 días.
9. **Kickoff = 1 acción clara, no un tomo.** No abrumes al cliente: una acción (pagar + 1 clic a los accesos) + expectativas + timeline + "qué necesito de ti".
10. **Nunca expongas llaves.** No imprimas tokens de Stripe/Composio. Si un generador o conexión falla, usa el fallback del sub-skill y sigue — el operador nunca se queda sin expediente.

---

## Manejo de errores y casos difíciles

- **No hay diagnóstico:** no te bloquees. Junta el mínimo del trato en la Fase 1 (los sub-skills tienen su mini-cuestionario). Recomienda correr `/diagnostico` la próxima para un cierre más afilado.
- **El cliente aún no firma:** no orquestes el cierre completo. Genera solo cotización + propuesta + contrato (para mandar a firmar) y deja el cobro/accesos/kickoff para cuando diga que sí. (`/cerrar-cliente` asume "ya cerró".)
- **Falta Python o Node:** cada sub-skill tiene su fallback (Claude escribe el HTML a mano). No bloquees ningún entregable.
- **Composio sin key / Stripe sin cuenta conectada:** deja documentada la acción (lista de apps en `accesos.md`, instrucciones de pago manual) y sigue. El operador completa esos dos cuando tenga las cuentas listas.
- **El operador no sabe qué precio poner:** ancla al rango de mercado del diagnóstico ($1,500–$3,000 setup típico) y arma los tiers alrededor. Si quiere afinar, corre `/cotizacion` solo.
- **Es su primer cliente y no tiene razón social:** usa su nombre como persona física con actividad empresarial (o equivalente del país). No lo trabes por esto. El disclaimer del contrato ya cubre "para tratos grandes, que lo vea un abogado".

---

## Archivos del skill

```
cerrar-cliente/
├── SKILL.md                 ← este archivo (el orquestador)
└── templates/
    ├── kickoff.md           ← plantilla del mensaje de bienvenida / kickoff (Fase 7)
    └── accesos.md           ← plantilla del resumen de accesos/links de Composio (Fase 6)
```

> La lógica de cotización, propuesta, contrato y cobro vive en sus propios skills (con sus templates y generadores). Este orquestador solo agrega los 2 templates del onboarding y consolida la carpeta. Toda decisión de orden y de kickoff viene de `_research/cerrar-cliente.md` (con fuentes). No inventes el orden ni el contenido del onboarding: está investigado.
