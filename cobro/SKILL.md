---
name: cobro
description: Genera el cobro de un proyecto de automatización con IA y el link de pago listo para mandárselo al cliente — factura/recibo profesional (markdown + HTML que imprime a PDF, con acento cyan de Horizontes IA), link de pago real (Stripe vía Composio, o instrucciones para Mercado Pago / PayPal / transferencia) y la cadena de recordatorios de pago tardío. Úsalo cuando alguien escriba "/cobro", "cobra a este cliente", "genera el cobro", "hazme la factura", "arma la factura del anticipo", "genera el link de pago", "mándale el link de cobro", "cobra el anticipo", "cobra el saldo", "cobra la mensualidad", "factura el retainer", "cómo le cobro a mi cliente", "ya firmó, ¿cómo le saco el dinero?", o cualquier variación donde el operador de una agencia de automatización con IA (LATAM, probablemente principiante) ya cerró/firmó y necesita COBRARLE de verdad. El skill lee el `diagnostico-<negocio>/diagnostico.json` si existe para no re-pedir datos, pregunta el proveedor de pago y la estructura (anticipo+saldo 50/50, hitos, o retainer mensual), genera el documento de factura, dispara el link de Stripe con Composio (`STRIPE_CREATE_PAYMENT_LINK`) cuando aplica, y deja lista la secuencia de recordatorios por si el cliente se atrasa. Español neutro LATAM, premium sin ser pushy. Cero tecnicismos sin traducir.
---

# Cobro — Skill `/cobro`

## ⚙️ Fase 0 — Perfil de tu agencia (auto-config, una sola vez)

Antes de generar nada, asegura el perfil de la agencia:
- Si **NO existe** `~/.config/agencia-ia/perfil.json` → lee `~/.config/agencia-ia/configurar.md` y corre el onboarding (unas preguntas, guarda el perfil). **Solo la primera vez** que el usuario usa cualquier skill de agencia.
- Si **SÍ existe** → cárgalo y **NO vuelvas a preguntar**. Personaliza TODO con él: nombre de la agencia, datos, precios, **proveedor y link/datos de pago** (cobro), color de acento (HTML), tono.
- Para reconfigurar: el usuario dice "configura mi agencia" → re-corre `configurar.md`.

El perfil es el DEFAULT, no una jaula: si para ESTE cliente el monto o la estructura cambian, ajústalo para ese trato sin tocar el perfil.

Skill que toma un proyecto **ya cerrado** (el cliente dijo que sí, firmó la propuesta o el contrato) y genera **todo lo necesario para cobrarle de verdad**: una factura/recibo que se ve de agencia seria con sus **datos/instrucciones de pago** (transferencia o un link que tú generes), y la cadena de recordatorios por si se atrasa.

> **La factura NO embebe un botón de "Pagar".** La mayoría cobra por transferencia, o genera su propio link (Stripe / Mercado Pago) y lo comparte aparte. Por eso la factura muestra el **método + las instrucciones/datos de pago** y, si hay link, como **texto** — no un botón. Si el usuario quiere un link de Stripe, el skill se lo genera (Fase 3) y va dentro de esas instrucciones.

El "wow" no es el documento bonito. Es que el operador —que casi siempre es principiante y nunca le ha cobrado a un negocio— pase de *"ya cerré… ¿y ahora cómo le saco el dinero?"* a tener, en minutos, **un link que le manda al cliente y el dinero entrando a su cuenta**, con la estructura correcta (anticipo primero, nunca arrancar gratis) y sin verse improvisado.

> Regla de oro de este skill (de la investigación): **SIEMPRE se cobra un anticipo antes de construir.** Quien no paga el anticipo no iba a pagar el saldo. El default es **50% al firmar / 50% al entregar**. Nunca propongas arrancar sin cobrar.

---

## Cuándo invocar / cuándo NO

**SÍ** (literal o variantes):
- *"/cobro"*, *"cobra a este cliente"*, *"genera el cobro"*
- *"hazme la factura"*, *"arma la factura del anticipo"*, *"factura el retainer"*
- *"genera el link de pago"*, *"mándale el link de cobro"*, *"link de Stripe para el cliente"*
- *"cobra el anticipo"*, *"cobra el saldo"*, *"cobra la mensualidad"*
- *"ya firmó, ¿cómo le cobro?"*, *"cómo le saco el dinero a mi cliente"*

**NO** (redirige, no abras este pipeline):
- Todavía no hay precio ni alcance cerrado → primero **`/cotizacion`** (precio + tiers) o **`/propuesta`** (documento que cierra).
- Todavía no firman / falta el acuerdo → primero **`/contrato`** (define anticipo, pago tardío, PI tras pago).
- Solo quiere saber *cuánto* cobrar, no *cómo* cobrarlo → eso es **`/cotizacion`** (modelos de precio y rangos de mercado).
- El cliente ya pagó y quiere documentar/entregar el proyecto → eso es **`/docs-entrega`** y luego **`/mantenimiento`**.

> El orden natural de la suite es: **/diagnostico → /cotizacion → /propuesta → /contrato → /cobro → /conectar-cliente → /crear-agente → /docs-entrega → /mantenimiento.** /cobro es el momento en que entra el dinero.

---

## Cómo dirigirte a la persona (reglas de comunicación)

Le hablas como un **socio que ya cobró cien veces y le está enseñando al que cobra por primera vez.** Tranquilo, seguro, sin tecnicismos, sin presión.

1. **Español neutro LATAM, segunda persona, siempre.** "Tu cliente", "tu anticipo", "el link que le mandas" — nunca tercera persona ni tono de manual.
2. **UNA pregunta a la vez.** Nunca sueltes 5 preguntas juntas. Preguntas → escuchas → confirmas → sigues.
3. **Traduce todo.** El operador no sabe qué es un *payment link*, un *line item* ni *net-15*. Dilo en cristiano: "el link que le mandas para que pague", "los conceptos de la factura", "le das 15 días para pagar". Nombres propios (Stripe, Mercado Pago, PayPal, Wise, Composio) se quedan como son.
4. **Reasegura el miedo a cobrar.** El principiante tiene pena de pedir dinero. Recuérdale: *"Cobrar el anticipo no es ser pesado, es lo profesional. Quien va en serio paga sin problema; quien no paga el anticipo no iba a pagarte nunca."*
5. **Cero improvisación frente al cliente.** El documento que sale de aquí lo ve un negocio real. Tiene que verse impecable: folio, fecha, conceptos claros, total, link.
6. **Nunca prometas lo que no controlas.** No digas "el dinero entra hoy" — depende del banco del cliente. Di "en cuanto pague te llega la notificación de Stripe".

---

## El pipeline en 6 fases

### Fase 0 — Cargar contexto (lee el diagnóstico si existe)

Antes de preguntar nada, **busca el `diagnostico.json`** para no re-pedir datos que ya existen.

1. Busca en el directorio de trabajo (y un nivel arriba) una carpeta `diagnostico-*/diagnostico.json`. Si el usuario te pasó una ruta o nombre de negocio, úsalo.
   ```bash
   find . .. -maxdepth 2 -name "diagnostico.json" -path "*diagnostico-*" 2>/dev/null | head
   ```
2. Si existe, **léelo** y extrae (mapeo exacto del esquema canónico de `/diagnostico`):
   - `negocio.nombre_negocio` → nombre del cliente en la factura
   - `negocio.nombre_persona` → contacto / a quién va dirigida
   - `negocio.pais` → ayuda a sugerir el método de pago (local vs internacional) y la moneda
   - `negocio.tipo` → contexto del concepto
   - `meta.moneda_display` (ej. `"USD"`) → moneda de cobro por default
   - `automatizaciones[]` → cada una tiene `titulo` y `valor_si_lo_vendes_usd` = **`[min, max]`** (rango de mercado). De ahí sale el **monto del proyecto** (concepto + precio). Si hay varias, suma las que entran en el alcance vendido o pregunta cuál(es) se cerraron.
3. Si **NO** existe diagnóstico, pregunta lo mínimo en orden, una por una:
   - Nombre del negocio del cliente + a quién va dirigida (persona de contacto).
   - País del cliente (para sugerir método de pago).
   - Qué le vendiste (una línea: "asistente de WhatsApp que cotiza", etc.).
   - El monto total cerrado y en qué moneda.

> Si el diagnóstico trae un **rango** (`[1500, 3000]`) y el usuario aún no fijó el número final, recuérdale lo que ya quedó en `/cotizacion`/`/propuesta`. Si no lo tiene a la mano, propón el **punto medio del rango** como sugerencia, dejando claro que es solo eso: *"según tu diagnóstico esto se vende entre $1,500 y $3,000; si ya cerraste un número, dímelo; si no, te sugiero $2,250 como referencia."* **Nunca inventes un precio fuera del rango investigado.**

### Fase 1 — Elegir la estructura de cobro

Pregunta cómo se va a repartir el cobro. Explica cada opción en una línea y **recomienda el default**:

| Estructura | Cómo se reparte | Cuándo |
|---|---|---|
| **50/50** ⭐ (default) | 50% ahora (anticipo, al firmar) + 50% al entregar | Proyecto chico-mediano, 1-2 automatizaciones, $1,500–$3,000. **El recomendado para empezar.** |
| **Hitos 50/25/25** | 50% ahora + 25% en revisión intermedia + 25% al entregar | Proyecto más grande o por fases. |
| **Tercios 33/33/33** | inicio / mitad / entrega | Cuando el cliente empuja por pagar menos al inicio. |
| **Retainer mensual** | mensualidad por adelantado (suscripción) | Mantenimiento/monitoreo después de entregar. Se cobra **al inicio de cada mes**, no al final. |

Reglas que le explicas:
- **El anticipo siempre va primero**, antes de construir. No se arranca sin él.
- **No entregas el acceso/deploy final hasta que el saldo esté pagado.** (entregas credenciales contra pago).
- El **retainer** es donde está la recurrencia: si vendiste mantenimiento, se cobra por adelantado cada mes, idealmente como **suscripción automática** para no andar persiguiendo el pago.

Luego pregunta **qué fase vas a cobrar ahora** (lo más común: el **anticipo**). El skill genera la factura de esa fase; las demás quedan documentadas para después.

### Fase 2 — Elegir el método de pago

Pregunta con qué va a cobrar y **recomienda según el cliente** (de la investigación de pasarelas LATAM):

| Método | Comisión típica | Cuándo recomendarlo |
|---|---|---|
| **Stripe** ⭐ | 2.9% + $0.30 (cross-border puede subir a ~4.9%) | Cliente internacional o que quieres verte de agencia seria, cobro recurrente. **Es el único que el skill automatiza** (genera el link solo vía Composio). Requiere entidad US/Atlas o estar en MX/BR. |
| **Mercado Pago** | ~3.79% + fijo | Cliente **local** que paga en moneda local (AR, BR, CL, CO, MX, UY, PE). Máxima aceptación, pero comisión más alta. |
| **PayPal** | ~6.5%–8.4% | Último recurso / cliente que solo tiene PayPal. El más caro, retenciones frecuentes. |
| **Transferencia / SPEI / PIX** | ~0% | Cliente local que ya confía, montos grandes. Sin link automático, más fricción. |
| **Wise** | 0.35%–2% FX | **No es para cobrarle con tarjeta** — es para *recibir/mover* el dinero a tasa real. Combo ganador: **cobras por Stripe → retiras a Wise** para convertir a moneda local barato. |

Reglas:
- Si el cliente es **internacional / B2B** → empuja **Stripe** (el skill le arma el link solo).
- Si es **local pequeño** → **Mercado Pago** (link) o **transferencia + factura**.
- **Evita PayPal** salvo que el cliente lo exija (es el más caro).
- Menciona el **combo Stripe + Wise** si va a recibir USD y vive en LATAM.

### Fase 3 — Generar el link de pago

#### Si eligió Stripe → automatízalo con Composio

Usa el toolkit **`stripe`** vía la CLI de Composio. El slug principal es **`STRIPE_CREATE_PAYMENT_LINK`**.

**Antes de ejecutar**, dos cuidados confirmados por la investigación:
- ⚠️ **El monto va en la unidad mínima (centavos).** $1,500.00 USD → `unit_amount: 150000`. **NO** pongas `1500`. Multiplica el monto por 100.
- ⚠️ `line_items[].quantity` es **requerido** (normalmente `1`). Sin él, Stripe responde error 400.

Verifica la conexión y el schema primero (sin ejecutar):
```bash
~/.composio/composio execute STRIPE_CREATE_PAYMENT_LINK --get-schema
```
Si no hay cuenta de Stripe conectada en Composio, el CLI te lo dirá. En ese caso, dile al usuario que conecte Stripe (lo mismo que hace `/conectar-cliente`, pero para SU propia cuenta de cobro) o usa el script `scripts/crear-link-stripe.mjs` que envuelve el flujo.

Ejecuta el cobro (ejemplo — **anticipo del 50%** de un proyecto de $1,500):
```bash
~/.composio/composio execute STRIPE_CREATE_PAYMENT_LINK -d '{
  "line_items": [{
    "quantity": 1,
    "price_data": {
      "currency": "usd",
      "unit_amount": 75000,
      "product_data": { "name": "Anticipo 50% — Asistente de WhatsApp que cotiza · Sabores de Casa" }
    }
  }],
  "metadata": { "cliente": "Sabores de Casa", "fase": "anticipo", "proyecto": "asistente-whatsapp" }
}'
```
- `unit_amount: 75000` = $750.00 (la mitad de $1,500, en centavos).
- `metadata` te sirve para identificar el pago después (cliente, fase). Opcional pero recomendado.
- Captura el **`data.url`** de la respuesta: **ese es el link que le mandas al cliente.**

**Verifica** que quedó activo:
```bash
~/.composio/composio execute STRIPE_GET_PAYMENT_LINK -d '{ "payment_link": "plink_xxx" }'
```
Confirma `data.active: true`. Revisa `data.livemode`: si es `false`, estás en modo de prueba (test) — avísale al usuario que ese link NO cobra dinero real hasta que active el modo *live* en su cuenta de Stripe.

**Para el retainer mensual (suscripción):**
1. Crea un precio recurrente con `STRIPE_CREATE_PRICE` (`recurring.interval: "month"`, `unit_amount` en centavos, `currency`).
2. Pasa ese `price` (ID `price_xxx`) como `line_items[].price` en `STRIPE_CREATE_PAYMENT_LINK`.
3. ⚠️ Para suscripciones **omite** `invoice_creation`/`customer_creation` (chocan con precios recurrentes).
4. El link resultante crea una **suscripción que cobra sola cada mes** — adiós cobranza manual del retainer.

> El script `scripts/crear-link-stripe.mjs` envuelve todo esto: recibe monto, moneda, descripción, metadata y (opcional) `--recurring month`, hace la conversión a centavos por ti, ejecuta Composio y te devuelve el link. Úsalo para no equivocarte con los centavos.

#### Si eligió otro método → instrucciones + link manual

Genera el documento `instrucciones-pago-<metodo>.md` desde la plantilla `templates/instrucciones-pago.md` con los pasos exactos para ese método:
- **Mercado Pago**: cómo crear un *link de pago* desde su panel (Tu negocio → Link de pago / Cobrar → generar link por el monto) y pegarlo en la factura.
- **PayPal**: `paypal.me/<usuario>/<monto>` o "Solicitar dinero" → email del cliente.
- **Transferencia / SPEI / PIX**: poner los datos bancarios (CLABE/cuenta/alias) directo en la factura + pedir comprobante.

En todos estos, el **link/datos los pega el usuario** en la factura (Stripe es el único que el skill genera solo).

### Fase 4 — Generar la factura/recibo (markdown + HTML que imprime a PDF)

Esto es lo que **ve el cliente**, así que va doble: markdown editable + HTML profesional.

1. Llena la plantilla `templates/factura.md` con los datos. Campos clave (todos con placeholder claro):
   - **Folio consecutivo** (ej. `HZ-2026-001`). Llévale el conteo al usuario: pregúntale cuál fue el último folio o arranca en `001`.
   - **Fecha de emisión** y **fecha de vencimiento** (para el anticipo, "pago inmediato / al firmar"; para el saldo, según los términos — net-15 sano, net-30 máximo).
   - **Datos del cliente** (negocio, contacto, país; RFC/RUT/CUIT solo si el usuario lo tiene y aplica fiscalmente).
   - **Datos del emisor** (el operador / su marca de agencia).
   - **Conceptos (line items)**: descripción clara (ej. "Anticipo 50% — Asistente de WhatsApp que cotiza"), cantidad, precio unitario, subtotal.
   - **Totales**: subtotal, impuestos si aplica, **total a pagar** de esta factura, y **saldo pendiente del proyecto** (lo que falta de las otras fases).
   - **Condiciones de pago**: método, a qué corresponde (anticipo/saldo/mensualidad), términos.
   - **Datos / instrucciones de pago**: el método (transferencia, etc.) y los datos para pagar. Si el usuario generó un link (Stripe/Mercado Pago), va en `link_pago` y la factura lo muestra **como texto**, NO como botón.
2. Genera el **HTML self-contained** con `scripts/factura-html.mjs` (acento de la marca, A4, sin botón de "Pagar"). El script recibe un JSON con los mismos campos y escupe el `.html`.
3. **Generar el PDF (automático).** Corre el conversor compartido (multi-OS):
   ```bash
   python3 ~/.config/agencia-ia/html2pdf.py <ruta>/factura.html
   ```
   `PDF: <ruta>` → quedó `factura.pdf` junto al HTML. `NO_PDF:` → el usuario abre el `.html` y hace **Cmd/Ctrl+P → Guardar como PDF**.
4. *(opcional)* Si el usuario quiere, **súbelo a Google Docs** con la CLI `gws` (autenticada) para que lo edite/comparta. No es obligatorio.

Guarda los entregables junto al cliente: idealmente dentro de `diagnostico-<negocio>/cobro/` (o `cobro-<negocio>/` si no hay diagnóstico):
- `factura-<fase>.md`
- `factura-<fase>.html`
- `instrucciones-pago-<metodo>.md` (si no es Stripe)
- `recordatorios-pago.md`

### Fase 5 — Dejar lista la cobranza de pago tardío

Genera `recordatorios-pago.md` desde `templates/recordatorios-pago.md` — la **cadena educada que escala** si el cliente se atrasa (de la investigación):

1. **Día de vencimiento**: recordatorio amable + el link otra vez.
2. **+3 días**: "¿algún problema con el pago?".
3. **+7 días**: recordatorio firme, mencionar pausa del servicio/retainer.
4. **+14 días**: pausar monitoreo/retainer hasta regularizar.

Reglas que le explicas al usuario:
- **Tu mejor defensa es el anticipo**: con 50/50 nunca entregas sin haber cobrado la mitad; el riesgo se limita al saldo.
- **No liberes el acceso/deploy final hasta que el saldo entre.**
- El **recargo por mora** y la **pausa del servicio** deben estar en el contrato (eso lo cubre `/contrato`) — aquí solo ejecutas la cobranza, citándolo.
- Para el retainer, el **cobro recurrente automático** (suscripción Stripe) elimina casi toda la cobranza manual.

### Fase 6 — Cierre (qué le entregas y qué sigue)

Resume en lenguaje simple:
- ✅ "Aquí está tu **factura** (markdown editable + HTML para mandar como PDF)."
- ✅ "Aquí está el **link de pago** — mándaselo al cliente por WhatsApp/correo: `<url>`." *(o las instrucciones del método elegido)*
- ✅ "Si se atrasa, ya tienes los **recordatorios** listos para copiar y pegar."
- 👉 Siguiente paso: **en cuanto pague el anticipo**, pasa a **`/conectar-cliente`** (que el cliente conecte sus cuentas sin darte contraseñas) y luego a **`/crear-agente`** para construir. **No construyas antes de que entre el anticipo.**

---

## Reglas duras del skill (las 10)

1. **Anticipo SIEMPRE primero.** Nunca propongas arrancar a construir sin cobrar. Default 50/50.
2. **Stripe en centavos.** `unit_amount = monto × 100`. Nunca pasar el monto "normal" — error clásico que cobra de menos.
3. **`quantity` requerido** en cada `line_item` (normalmente `1`).
4. **No inventes precios.** El monto sale del `valor_si_lo_vendes_usd` del diagnóstico (rango investigado) o de lo que el usuario ya cerró en `/cotizacion`/`/propuesta`. Si solo hay rango, sugiere el punto medio, marcándolo como sugerencia.
5. **Stripe es el único automatizado.** Para Mercado Pago / PayPal / transferencia, generas instrucciones; el link/datos los pega el usuario.
6. **Verifica `livemode`.** Si el link salió en modo test, avísale que no cobra dinero real todavía.
7. **No entregar contra nada.** El acceso/deploy final se libera contra pago del saldo, no antes.
8. **Folio consecutivo y fechas reales.** Una factura sin folio ni vencimiento se ve improvisada.
9. **Nunca expongas llaves.** No imprimas tokens de Stripe/Composio en el output al usuario. Si Composio falla por conexión, dile que conecte su cuenta, no le pegues credenciales.
10. **El documento del cliente se ve de agencia.** Markdown editable + HTML cyan que imprime a PDF. Nada de texto suelto sin formato para el cliente.

---

## Manejo de errores y casos difíciles

- **Composio dice que no hay cuenta de Stripe conectada** → el usuario necesita conectar SU Stripe (su cuenta de cobro). Guíalo: es el mismo gesto que `/conectar-cliente` pero para su propia cuenta. Si no quiere/puede, cae a método manual (Mercado Pago/transferencia) sin bloquear el cobro.
- **El usuario no está en US ni tiene Atlas y quiere Stripe** → Stripe opera directo en MX y BR; en Chile está en preview y Colombia aún no oficial. Si no aplica su país, recomiéndale **Mercado Pago** (local) o Stripe Atlas (LLC Delaware ~$500) si va a escalar a clientes internacionales.
- **Error 400 al crear el link** → casi siempre es (a) falta `quantity`, o (b) `unit_amount` no está en centavos. Revisa esos dos primero.
- **El cliente solo tiene PayPal** → úsalo pero adviértele de la comisión alta (6.5–8.4%) y las retenciones; documenta el link manual.
- **No hay diagnóstico ni precio cerrado** → no inventes. Pídele el monto que ya acordó con el cliente, o mándalo a `/cotizacion` si todavía no tiene número.
- **Quiere factura fiscal (CFDI en México)** → el skill genera la factura "de agencia" (comercial), no el CFDI fiscal. Para CFDI automático al cobrar Stripe/PayPal existe **gigstack** — menciónalo como herramienta aparte, no lo prometas dentro del skill.

---

## Archivos del skill (qué `Read` y cuándo)

- `templates/factura.md` — la factura/recibo que ve el cliente (markdown). Llénala en la Fase 4.
- `templates/instrucciones-pago.md` — pasos por método (Mercado Pago / PayPal / transferencia) cuando NO es Stripe. Fase 3.
- `templates/recordatorios-pago.md` — la cadena de cobranza de pago tardío. Fase 5.
- `scripts/crear-link-stripe.mjs` — envuelve `STRIPE_CREATE_PAYMENT_LINK` vía Composio (convierte a centavos por ti, soporta `--recurring`). Fase 3.
- `scripts/factura-html.mjs` — convierte los datos de la factura en un HTML self-contained (cyan, A4, imprime a PDF). Fase 4.

> Toda la lógica de estructura de cobro, métodos de pago, slugs de Stripe y cadencia de recordatorios viene de `_research/cobro.md` (agencias reales + guía de pasarelas LATAM + search real de Composio). No inventes estructura ni comisiones: están investigadas.
