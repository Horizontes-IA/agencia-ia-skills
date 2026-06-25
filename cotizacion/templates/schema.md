# Esquema de `cotizacion.json`

Contrato de datos que consume `scripts/generar_cotizacion.py`. Todo opcional **se omite con gracia** si falta. El generador **recalcula** los montos (anticipo, totales) — no confíes en que el modelo sume.

## Mapa desde `diagnostico.json` (si existe)

Cuando hay una carpeta `diagnostico-<negocio>/diagnostico.json`, NO vuelvas a entrevistar. Mapea así:

| Campo de `cotizacion.json` | Viene de `diagnostico.json` |
|---|---|
| `cliente.nombre_negocio` | `negocio.nombre_negocio` |
| `cliente.contacto` | `negocio.nombre_persona` + `negocio.ciudad` |
| `cliente.pais` | `negocio.pais` |
| `comercial.moneda` | `meta.moneda_display` |
| `problema.frase_cliente` | `sangrado_declarado.frase_textual` |
| `problema.texto` | proceso #1 (`procesos[0]`): frecuencia + tiempo_por_vez + cómo_hoy |
| `solucion.texto` | `automatizaciones[0].que_hace` |
| `solucion.entregables` | `automatizaciones[0].arquitectura_simple` (resumido a entregables) |
| `roi.cards` | `roi_global` (horas + neto) + `automatizaciones[0].roi.ingreso_recuperado_mes_usd` + `costo_tools_mes_usd` |
| `alcance.no_incluye` | `perfil_tecnico.no_automatizar` (lo que el cliente quiere personal) + costos de APIs |
| **precio de las opciones** | `automatizaciones[].valor_si_lo_vendes_usd` = `[min, max]`. El **min** ancla el tier bajo, el **max** el alto, el medio entre ambos. Si hay 2-3 automatizaciones, el tier alto puede sumar varias. |
| `retainer.precio_mes` | regla de mercado: 50%-100% del setup ÷ 12, o $400-$1,500 según alcance |

## Campos

### `agencia` (obj)
- `nombre` (str) — tu marca.
- `contacto` (str) — correo/WhatsApp.

### `cliente` (obj) — **requerido** `nombre_negocio`
- `nombre_negocio` (str, req)
- `contacto` (str, opc) · `pais` (str, opc)

### `comercial` (obj)
- `folio` (str) · `fecha` (str, YYYY-MM-DD) · `moneda` (str, default "USD")
- `titulo` (str, **req**) — orientado a resultado.
- `subtitulo` (str) · `resumen_ejecutivo` (str)
- `anticipo_pct` (num, default 50) — % de anticipo. El generador calcula el monto de cada opción.
- `forma_pago` (str) · `forma_pago_nota` (str)
- `tiempo_entrega` (str) · `tiempo_entrega_nota` (str)
- `garantia` (str) · `garantia_nota` (str)
- `vigencia_fecha` (str, legible) — por default hoy + 14 días. Es la **única** palanca de urgencia permitida.

### `problema` (obj)
- `frase_cliente` (str) — cita textual. `frase_attr` (str).
- `texto` (str) — el cuello de botella con sus números.

### `solucion` (obj)
- `texto` (str) — orientado a resultado.
- `entregables` (array de str).

### `roi` (obj)
- `subtitulo` (str) · `nota` (str)
- `cards` (array, máx 3): `{ num, label, ctx }` — **siempre en dinero**, no en tiempo abstracto.

### `alcance` (obj)
- `incluye` (array de str) · `no_incluye` (array de str) — el `no_incluye` previene scope creep.

### `proceso` (array)
- cada fase: `{ titulo, duracion, descripcion }`.

### `opciones` (array, **req** ≥1, ideal 3) — los tiers good/better/best
- `nombre` (str, req) · `precio_total` (num) — o deja que se sume de `incluye[].precio`.
- `recomendada` (bool) — pone glow + flag al tier medio (el que quieres que elijan).
- `flag` (str, default "Recomendada") · `tagline` (str)
- `anticipo_pct` (num) — override del global por tier (opcional).
- `esquema_pago` (str) — texto del esquema (default "X% anticipo / Y% al entregar").
- `incluye` (array): str **o** `{ texto, muted }`. `muted:true` = item tachado/dim (decoy: muestra lo que ese tier NO trae).

### `retainer` (obj, opcional pero **ofrécelo siempre**)
- `titulo` (str) · `descripcion` (str) · `precio_mes` (num, req para mostrarlo).

### `cierre` (obj)
- `titulo` (str) · `texto` (str) · `cta_label` (str) · `cta_url` (str).

### `supuestos` (array de str) — notas al pie honestas (costo/hora, precios verificados, vigencia).

## Reglas duras del generador
- Si falta `opciones`, NO hay cotización válida → el modelo debe pedir el alcance/precio.
- Montos en `precio_total` y `precio_mes` son números enteros en la moneda (1500 = $1,500), **no centavos** (a diferencia de Stripe).
- El anticipo se calcula server-side: `precio_total × anticipo_pct / 100`.
