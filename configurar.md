# Configurar tu agencia (onboarding — solo la primera vez)

> Este es el onboarding COMPARTIDO de todos los skills de agencia (`/diagnostico`,
> `/cotizacion`, `/propuesta`, `/contrato`, `/cobro`, `/cerrar-cliente`). Se corre
> **una sola vez**: la primera vez que el usuario usa cualquiera de ellos, si no
> existe el perfil. Guarda el resultado en **`~/.config/agencia-ia/perfil.json`** y
> de ahí TODOS los skills salen personalizados: su marca, sus colores, su nicho, su
> metodología, sus precios y su forma de cobrar.
>
> (`/conectar-cliente` no usa este perfil — tiene su propia llave de Composio.)

## Cuándo se dispara
- Cualquier skill de agencia, al inicio (Fase 0), revisa si existe `~/.config/agencia-ia/perfil.json`.
- **Si NO existe** → corre este onboarding (las preguntas de abajo), guarda el JSON, y continúa con lo que el usuario pidió.
- **Si SÍ existe** → lo carga y NO vuelve a preguntar. (Para reconfigurar: el usuario dice "configura mi agencia" / "actualiza mi perfil" → re-corre esto.)

## Cómo conducir el onboarding
Cálido, **una pregunta a la vez**, español neutro LATAM, **sin tecnicismos** — pensado para que cualquiera lo conteste, joven o adulto, sepa o no de tecnología. Ancla cada pregunta con un ejemplo para que sea fácil responder. Si el usuario contesta varias de golpe, **no re-preguntes** — extrae todo y sigue. Las preguntas marcadas *(opcional)* se pueden saltar con un "no sé / luego". Abre así:

```
Antes de armarte tu primer documento, déjame conocer tu agencia — son
1-2 minutos y solo lo hago UNA vez. Después TODO lo que generes ya sale
con tu marca, tu forma de trabajar y tus precios. Te pregunto de a una,
tranquilo. Si no sabes algo, me dices "no sé" y seguimos.
```

Luego, una por una:

### Sobre tu agencia (lo que te hace TÚ)
1. **¿Cómo se llama tu agencia o tu marca?** (con la que te presentas a clientes) → `agencia.nombre_marca`
2. **¿A qué se dedica tu agencia y a qué tipo de negocios ayudas?** (ej. *"pongo asistentes de WhatsApp y agendas automáticas para clínicas y spas"*) → `agencia.que_hace`, `agencia.nicho` (si atiende a todos, pon `nicho: "general"`)
3. **En pocas palabras, ¿cómo trabajas con un cliente, de principio a fin?** Tu forma de trabajar. Ancla suave: *"muchos lo hacen así: 1) reviso qué se puede automatizar, 2) lo construyo, 3) te lo entrego y te doy soporte — ¿el tuyo cómo es?"* → `agencia.metodologia`
4. *(opcional)* **¿Qué te hace diferente — por qué te eligen a ti?** (ej. *"voy rápido y explico sin tecnicismos"*) → `agencia.propuesta_valor`
5. *(opcional)* **¿Con qué herramientas armas tus automatizaciones?** (ej. *n8n, Make, Claude Code, WhatsApp API*) → `agencia.construye_con` (lista)

### Datos para los documentos
6. **Para los contratos, ¿cuál es tu nombre legal completo?** ¿Eres persona física o tienes empresa registrada? → `agencia.nombre_legal`, `agencia.tipo_legal` ("persona"|"empresa")
7. **¿Tu nombre y cómo te presentas?** (ej. "Santi, fundador") → `persona.nombre`, `persona.rol`
8. **¿A qué email y WhatsApp te escriben los clientes?** ¿Tienes web o portafolio? → `persona.email`, `persona.whatsapp`, `persona.web`
9. **¿Desde qué país operas y en qué moneda cobras?** (ej. México / USD) → `ubicacion.pais`, `ubicacion.moneda`
10. **¿Cuánto cobras normalmente por montar un sistema?** Muchos arrancan en **$1,500–$3,000 de setup** + **$200–$500 al mes** de mantenimiento. ¿Cómo lo manejas tú? → `precios.setup_min`, `precios.setup_max`, `precios.mensualidad` (0 si no cobras mensualidad)
11. **¿Cómo divides el pago?** Lo más común es **50% anticipo + 50% al entregar**. ¿Te sirve así o usas otra? → `precios.estructura_pago` (ej. "50/50")
12. **¿Con qué cobras?** (Stripe, PayPal, Mercado Pago, transferencia) y ¿tienes un link o datos de pago? → `cobro.proveedor`, `cobro.datos`

### Tu marca (cómo se VEN tus documentos)
13. *(opcional)* **¿Color de tu marca?** (un código hex, ej. #7C3AED; si no sabes, lo dejamos en el cyan por defecto) y ¿un logo (URL de imagen)? → `marca.color_acento`, `marca.logo_url`
14. *(opcional)* **¿Qué tono prefieres?** (cálido / formal / directo) → `tono`

Confirma en bloque lo que entendiste antes de guardar ("¿así está bien?").

## Guardar el perfil
Crea la carpeta y escribe el JSON (estructura completa en `perfil.ejemplo.json`):

```bash
mkdir -p ~/.config/agencia-ia
# escribe ~/.config/agencia-ia/perfil.json con la herramienta Write
```

Campos que faltaron → déjalos en `null` (o `[]` para listas) y márcalo. Defaults por país para moneda/costo-hora si no los dio. Para `marca.color_acento`, si no lo dio, déjalo en `null` (los HTML usan el cyan por defecto de Horizontes).

## Cómo lo usan los skills
Cada skill **lee `~/.config/agencia-ia/perfil.json`** y se personaliza con él:
- **Marca visual (todos los HTML):** `agencia.nombre_marca` en el encabezado/pie, `marca.color_acento` como color de acento de TODO el documento (con fallback al cyan), `marca.logo_url` como logo si lo dio.
- **Contenido:** `agencia.que_hace` / `nicho` / `propuesta_valor` encuadran la propuesta y la cotización; `agencia.metodologia` arma la sección de "cómo trabajamos" (propuesta, contrato, plan del diagnóstico); `agencia.construye_con` sesga las herramientas que recomienda el diagnóstico; `tono` ajusta el copy.
- **Datos:** nombre legal y datos en el contrato; precios como punto de partida de la cotización; proveedor/link en el cobro.

> Regla: el perfil es el DEFAULT, no una jaula. Si para un cliente específico el precio, el alcance o el tono cambian, el skill lo ajusta para ESE trato sin tocar el perfil.
