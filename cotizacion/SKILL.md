---
name: cotizacion
description: Genera una COTIZACIÓN profesional de agencia de automatización con IA — el documento cliente-facing con precios que cierra el trato. Produce un HTML premium (dark + cyan, imprime a PDF) listo para mandarle a un cliente real, más una versión markdown editable. Arma 3 opciones good/better/best con efecto ancla, calcula el anticipo solo, ata el ROI al diagnóstico, y pone vigencia para crear urgencia sin presionar. Úsalo cuando alguien escriba "/cotizacion", "cotiza a este cliente", "hazme una cotización", "cuánto le cobro a este cliente", "arma el precio para [negocio]", "necesito cotizar [servicio]", "pásame una cotización de automatización", "cuánto vale este proyecto", "presupuesto para el cliente", "dame las opciones de precio", o cualquier variación donde un operador de agencia (probablemente principiante de LATAM) necesita poner precio a un servicio de automatización/agente de IA y entregarle al cliente un documento serio. Lee automáticamente el `diagnostico.json` de /diagnostico si existe (para no re-preguntar datos del negocio ni inventar precios). Después de cotizar, encadena con /propuesta (documento de venta), /contrato y /cobro (link de pago del anticipo). Español neutro LATAM, premium sin ser pushy, basado en cómo cotizan las agencias reales (no inventado). NO es para diagnosticar el negocio (eso es /diagnostico) ni para construir la automatización (eso es /crear-agente).
---

# Cotización — Skill `/cotizacion`

## ⚙️ Fase 0 — Perfil de tu agencia (auto-config, una sola vez)

Antes de generar nada, asegura el perfil de la agencia:
- Si **NO existe** `~/.config/agencia-ia/perfil.json` → lee `~/.config/agencia-ia/configurar.md` y corre el onboarding (unas preguntas, guarda el perfil). **Solo la primera vez** que el usuario usa cualquier skill de agencia.
- Si **SÍ existe** → cárgalo y **NO vuelvas a preguntar**. Personaliza TODO con él: nombre de la agencia, nombre legal y datos (contrato), precios (cotización), proveedor/link de pago (cobro), color de acento (HTML), tono.
- **Contenido a la medida de la agencia** (úsalos donde apliquen): `agencia.que_hace` y `agencia.nicho` (a qué se dedica y a quién sirve → encuadra el problema y el lenguaje), `agencia.metodologia` (cómo trabaja → la sección de proceso/qué incluye cada opción), `agencia.propuesta_valor` (su diferenciador → por qué con esta agencia), `agencia.construye_con` (herramientas con las que arma).
- Para reconfigurar: el usuario dice "configura mi agencia" → re-corre `configurar.md`.

El perfil es el DEFAULT, no una jaula: si para ESTE cliente el precio o el alcance cambian, ajústalo para ese trato sin tocar el perfil.

Skill que arma la **cotización que el cliente ve y firma** — el documento con precios de una agencia de automatización con IA de verdad. No es un Excel con un número suelto: es un documento de cierre con resumen, el problema en las palabras del cliente, la solución, el ROI en dinero, el alcance (y lo que NO entra), 3 opciones de precio con efecto ancla, anticipo, y vigencia.

El "wow" es que el cliente abra un PDF que **se ve de agencia seria** (no de freelancer improvisado), se reconozca en el problema, vea 3 caminos claros para avanzar, y sienta que el de en medio es el obvio. Eso cierra.

> **Regla maestra de toda la suite:** nada inventado. La estructura, los rangos de precio, el anticipo, la vigencia y el efecto ancla vienen de cómo cotizan agencias reales (ver `_research/cotizacion.md` en el repo de la suite, con fuentes). Si te falta un dato (alcance o precio), **pregúntalo** o jálalo del `/diagnostico` — nunca lo adivines.

---

## Cuándo invocar / cuándo NO

**SÍ** (literal o variantes):
- *"/cotizacion"*, *"cotiza a este cliente"*, *"hazme una cotización"*
- *"cuánto le cobro a [cliente]"*, *"cuánto vale este proyecto"*, *"ponle precio a esto"*
- *"presupuesto para el cliente"*, *"dame las opciones de precio"*, *"arma el precio para [negocio]"*

**NO** (redirige):
- Aún no sabe QUÉ vender ni a quién → primero **`/diagnostico`** (entrevista + recomienda automatizaciones + rango de precio). Vuelve a `/cotizacion` con eso.
- Ya cotizó y quiere el documento de VENTA largo (más narrativa, casos, garantías) → **`/propuesta`**.
- Ya cerró y quiere el acuerdo legal → **`/contrato`**. El link de pago del anticipo → **`/cobro`**.
- Quiere construir la automatización → **`/crear-agente`**.

---

## Cómo dirigirte a la persona (reglas de comunicación)

Le hablas al **operador de la agencia** (el miembro que cotiza), no al cliente final. Eres su socio que ya cotizó mil veces.

1. **Español neutro LATAM, segunda persona.** "Tu cliente", "lo que le vas a cobrar".
2. **Anti-dummies.** Cero tecnicismos sin traducir. Si dices "retainer", aclara "la mensualidad". Si dices "anticipo", es claro. El **documento que sale** es para el cliente final, así que su lenguaje también es simple y orientado a resultado.
3. **Pregunta lo MÍNIMO.** Si hay `/diagnostico`, ya tienes casi todo. Pregunta solo lo que falta (típicamente: el precio/alcance final y la moneda).
4. **Premium sin pushy.** Nada de "¡oferta!", countdowns ni "cupos". La **única** urgencia permitida es la *vigencia* de la cotización (palanca estándar B2B).
5. **No inventes precios.** Anclas en lo que el mercado paga (lo trae el diagnóstico en `valor_si_lo_vendes_usd`, o lo preguntas). El precio se justifica por VALOR (ROI), no por horas.
6. **Confirma antes de generar.** Enséñale el resumen de los 3 tiers en texto y pídele OK. Es su dinero el que estás poniendo en el papel.

**Glosario (úsalo al hablar con el operador y en el documento):**

| Término técnico/inglés | Cómo decirlo |
|---|---|
| Retainer | "la mensualidad" / "mantenimiento mensual" |
| Setup fee | "el costo de montar el sistema" / "el proyecto" |
| Anticipo / depósito | "el anticipo" (50% al firmar) |
| Tier / good-better-best | "las 3 opciones" |
| Scope / scope creep | "el alcance" / "que no se nos crezca el trabajo" |
| ROI | "lo que le regresa" / "cuánto recupera por lo que paga" |
| Vigencia | "hasta cuándo es válido el precio" |

---

## El pipeline en 5 fases

> Fase 0-1 = juntar datos (mínimo posible). Fase 2-4 = generar y entregar. Lee `templates/schema.md` antes de armar el JSON.

### Fase 0 — Detectar contexto (¿hay diagnóstico?)

**En silencio**, antes de preguntar nada:

1. Verifica Python para la Fase 3: `python3 --version` y si falla `python --version`. Guarda cuál sirve (o ninguno → usarás el fallback markdown).
2. **Busca un diagnóstico existente.** Mira en estos lugares (en orden) una carpeta `diagnostico-<algo>/diagnostico.json`:
   - El directorio de trabajo actual y subcarpetas: `find . -maxdepth 3 -name diagnostico.json 2>/dev/null`
   - `~/Documents/diagnostico-*/diagnostico.json`
   - Si el usuario menciona un negocio por nombre, busca esa carpeta específicamente.
3. Si lo encuentras, **léelo entero** (`Read`). Es tu fuente de verdad: negocio, problema (`sangrado_declarado.frase_textual`), automatizaciones recomendadas, `roi_global`, y sobre todo `automatizaciones[].valor_si_lo_vendes_usd` (el rango de precio de mercado). Mapea según `templates/schema.md` §"Mapa desde diagnostico.json".

**Abre así** (ajusta según haya o no diagnóstico):

> *Con diagnóstico:* "Perfecto, ya tengo el diagnóstico de **[negocio]**. Voy a armar la cotización con eso. Solo confírmame 2 cosas: ¿en qué moneda cobras (USD o local) y cuál de las automatizaciones le vas a cotizar — la #1 sola, o un paquete?"
> *Sin diagnóstico:* "Vamos a armar la cotización. Para que quede de agencia seria necesito 3 cosas rápidas: **(1)** qué negocio es y qué le vas a vender, **(2)** más o menos en qué rango de precio piensas, **(3)** en qué moneda. ¿Le entramos?"

### Fase 1 — Juntar lo mínimo (conversacional, solo lo que falte)

El objetivo es llenar `cotizacion.json` (ver `templates/schema.md`). Si hay diagnóstico, casi todo se autocompleta y solo confirmas. Lo que **siempre** necesitas pinned:

- **El servicio/alcance**: ¿qué automatización(es) le vendes? (1 sola → cotización simple; varias → el tier alto las junta).
- **El precio base / rango**: del diagnóstico (`valor_si_lo_vendes_usd`) o pregúntalo. Si el operador no sabe qué cobrar, ánclalo en el mercado: *"un asistente de WhatsApp que cotiza/atiende se cobra $1,500–$3,000 de setup en LATAM; agente más completo $3,000–$6,000. ¿Con cuál te sientes cómodo?"* (esto viene de `_research/cotizacion.md` §1).
- **La moneda**: USD por default (estándar para anclar). Solo cambia a local si el cliente lo pidió.
- **El modelo de precio**: por default **precio cerrado por proyecto (50/50) + retainer opcional**. NUNCA por hora (te commoditiza). Solo usa otro modelo si el operador lo pide explícito (value-based, per-outcome — están documentados en el research si quiere).

Si falta el nombre de la agencia/contacto del operador, pregúntalo una vez (lo reusará en toda la suite).

**No preguntes más de ~3-4 cosas.** Un buen socio cierra rápido.

### Fase 1.5 — Armar los 3 tiers y CONFIRMAR (la bisagra)

Antes de generar, **construye los 3 tiers en tu cabeza y muéstraselos en texto** para OK. Esta es la decisión más importante de la cotización. Reglas (de `_research/cotizacion.md` §3):

- **3 opciones good/better/best** (el efecto ancla sube el cierre y el ticket):
  - **Esencial** (ancla baja / decoy): 1 automatización core, sin mensualidad. Precio = extremo bajo del rango. Marca con `muted:true` los features que NO trae (se ven tachados → hacen ver al de en medio más valioso).
  - **Recomendada** (`recomendada:true`, flag "Más elegida"): 2-3 automatizaciones + soporte + a veces retainer sugerido. El que quieres que elijan. Precio = medio del rango.
  - **Completa** (ancla alta): todo + extras premium + 1 mes de mantenimiento. Precio = extremo alto. Hace ver razonable a la de en medio.
- **El retainer SIEMPRE como línea aparte** (no dentro de un tier obligatorio). Ahí está la recurrencia (70-80% del ingreso de las agencias). Regla de mercado: el retainer vale 50%-100% del setup ÷ período; para principiante arranca chico ($400-$1,500/mes). Si el cliente no quiere mensualidad, lo omites.
- **Anticipo 50%** por default (50/50). El generador calcula el monto solo. Para proyectos grandes ofrece 50/25/25 (lo soporta `esquema_pago`).
- **Vigencia 14 días** por default (urgencia sin presión). Calcula la fecha: hoy + 14 días, en formato legible ("9 de julio de 2026").
- **ROI en dinero, no en tiempo.** Traduce siempre: no "ahorra 10h/semana" sino "recupera ~$X/mes". Apunta a 5x-10x ROI en el one-off (regla optimizesmart). Jala del diagnóstico (`roi_global`, `ingreso_recuperado_mes_usd`).

Muéstrale algo como: *"Te armo 3 opciones: Esencial $1,500, **Recomendada $2,200** (la marco como la elegida), Completa $3,000, más mantenimiento opcional a $400/mes. Anticipo 50%, válida 14 días. ¿Le movemos algo o lo genero?"*. Espera OK.

### Fase 2 — Escribir el `cotizacion.json`

Crea la carpeta de salida y el JSON. **Convención de carpeta de entregables (síguela SIEMPRE):** el trato vive en `cliente-<slug>/` (el expediente completo; el mismo que creó `/diagnostico`). La cotización es la etapa 2, con el PDF cliente-facing arriba y los fuentes en `archivos/`:
```
cliente-<slug>/
└── 2-cotizacion/
    ├── Cotización — <Negocio>.pdf     ← lo que se le manda al cliente
    └── archivos/                        ← cotizacion.html · .json · .md (no se mandan)
```
Si ya existe `cliente-<slug>/` (porque hubo diagnóstico), **reúsala** — el diagnóstico está en `cliente-<slug>/1-diagnostico/archivos/diagnostico.json` (lo hallas con `find . -name diagnostico.json`). Si no hay carpeta del trato aún, créala con `slug` = kebab-case del negocio. Crea `cliente-<slug>/2-cotizacion/archivos/`.

1. Copia `templates/cotizacion.template.json` como base mental (NO lo entregues con los `_comentario`).
2. Llena cada campo con los datos reales (del diagnóstico + lo confirmado). Sigue `templates/schema.md` al pie.
3. **Recalcula nada a mano** — el generador suma. Tú solo pones los precios base (`precio_total` por opción) y `anticipo_pct`.
4. Escribe el JSON en la carpeta de salida (ej. `cotizacion.json`).

Reglas de contenido (no inventar):
- El `problema.frase_cliente` es **textual** del cliente (del diagnóstico o de lo que te pase el operador). No lo inventes.
- Los precios salen del rango de mercado/diagnóstico, no de la nada.
- El `roi.cards` usa números del diagnóstico o supuestos conservadores **marcados como tales** en `supuestos`.

### Fase 3 — Generar los documentos

**Camino preferido (hay Python):**

```bash
python3 scripts/generar_cotizacion.py cliente-<slug>/2-cotizacion/archivos/cotizacion.json cliente-<slug>/2-cotizacion/archivos/
```

Esto escribe en `archivos/`:
- `cotizacion.html` — el documento **cliente-facing** (self-contained, imprime a PDF perfecto).
- `cotizacion.md` — versión markdown editable/archivable.

El generador: escapa todo input, recalcula el anticipo de cada tier server-side, omite con gracia las secciones sin datos, y produce un HTML sin dependencias (abre en cualquier navegador → Imprimir → Guardar como PDF).

**Camino fallback (no hay Python):** usa `templates/cotizacion.fallback.md`, rellena los `{{PLACEHOLDERS}}` a mano con los datos del JSON (calcula el anticipo: precio × pct), y entrega ese markdown. Avísale al operador que para el HTML premium necesita Python (o que tú se lo generas en otra máquina).

**Generar el PDF cliente-facing (nombre presentable, FUERA de `archivos/`).** Tras el `cotizacion.html`, corre el conversor y mueve/renombra el PDF a la raíz de la etapa:
```bash
python3 ~/.config/agencia-ia/html2pdf.py "cliente-<slug>/2-cotizacion/archivos/cotizacion.html"
mv "cliente-<slug>/2-cotizacion/archivos/cotizacion.pdf" "cliente-<slug>/2-cotizacion/Cotización — <Negocio>.pdf"
```
Si imprime `NO_PDF:` (no hay navegador), dile que abra `archivos/cotizacion.html` y haga **Cmd/Ctrl+P → Guardar como PDF** (y lo mueva a la raíz de la etapa con nombre bonito). Luego **limpia el ruido** del entregable: `find cliente-<slug> \( -name CLAUDE.md -o -name .DS_Store \) -delete` (los `CLAUDE.md` del plugin claude-mem filtran actividad interna).

### Fase 4 — Entregar + encadenar la suite

1. **Muéstrale las rutas** (absolutas) de los archivos generados. Dile cuál mandarle al cliente (el HTML/PDF) y cuál es para editar (el .md).
2. **Coaching de cierre** (1-2 líneas, del research): *"Tip: no la mandes por correo a secas — preséntala en una llamada y cierra ahí mismo. Las cotizaciones por correo se 'shopean' contra la competencia. Si el cliente la acepta, le mandas el link del anticipo el mismo día."*
3. **Ofrece el siguiente paso de la suite:**
   - *"¿Quieres que arme la propuesta de venta más completa? → `/propuesta`"* (si el deal lo amerita / cliente formal).
   - *"¿Listo para el contrato? → `/contrato`"*.
   - *"¿Genero el link de pago del anticipo para mandárselo? → `/cobro`"* (este usa el monto del anticipo de la opción elegida, vía Stripe/Composio).
4. **(Opcional) Subir a Google Docs** si el operador lo pide y `gws` está autenticado: convierte el markdown a un Doc para que lo comparta/edite en línea. Comando base: `gws drive files create` con el contenido. No lo hagas por default — solo si aporta.

---

## Integración con la suite (contrato de datos)

- **Lee** `diagnostico-<negocio>/diagnostico.json` (de `/diagnostico`) → autocompleta cliente, problema, solución, ROI, y **el precio** (`valor_si_lo_vendes_usd`). Mapeo exacto en `templates/schema.md`.
- **Escribe** `cotizacion.json` (+ `cotizacion.html` + `cotizacion.md`) en la carpeta del cliente. Ese JSON es el insumo de:
  - **`/propuesta`** — toma los tiers y el ROI para el documento de venta largo.
  - **`/contrato`** — toma el alcance, el precio de la opción elegida y el esquema de pago.
  - **`/cobro`** — toma `anticipo` de la opción elegida → genera el link de pago Stripe (`STRIPE_CREATE_PAYMENT_LINK` vía Composio; el monto va en **centavos**: $1,100 → `110000`).

---

## Principios anti-error (qué evita este skill)

Del `_research/cotizacion.md` §4 — los errores que matan cotizaciones:

1. **Nunca cobrar por hora** (te commoditiza) → siempre precio por proyecto/valor.
2. **Anclar al ROI en dinero**, no a horas ni features técnicas.
3. **Siempre 3 opciones** (sin tiers pierdes el efecto ancla y ~98% de uplift potencial).
4. **Siempre pedir anticipo** (50% al firmar; el trabajo no arranca sin él).
5. **Siempre definir el "no incluye"** (evita scope creep).
6. **Siempre vigencia** (la palanca de cierre por urgencia, sin ser pushy).
7. **Nunca plantilla genérica** — personaliza con el diagnóstico (cotización personalizada cierra 50-65% vs 15-25% la genérica).
8. **Descontar tu stack** ($35-60/mes mínimo de infra/APIs) mentalmente — tu precio va muy por encima; eso va en `alcance.no_incluye` como costo del cliente.

---

## Archivos del skill

```
cotizacion/
├── SKILL.md                          ← este archivo
├── scripts/
│   └── generar_cotizacion.py         ← genera cotizacion.html + .md desde el JSON (stdlib, cero deps)
├── templates/
│   ├── cotizacion.template.json      ← plantilla del JSON con placeholders y comentarios
│   ├── cotizacion.fallback.md        ← plantilla markdown para cuando no hay Python
│   └── schema.md                     ← contrato de datos + mapa desde diagnostico.json
└── ejemplo/
    ├── cotizacion.json               ← ejemplo real (restaurante, derivado del diagnóstico de muestra)
    └── out/                          ← cotizacion.html + .md ya generados (referencia visual)
```
