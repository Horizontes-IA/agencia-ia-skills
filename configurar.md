# Configurar tu agencia (onboarding — solo la primera vez)

> Este es el onboarding COMPARTIDO de todos los skills de agencia (`/cotizacion`,
> `/propuesta`, `/contrato`, `/cobro`, `/cerrar-cliente`). Se corre **una sola vez**:
> la primera vez que el usuario usa cualquiera de ellos, si no existe el perfil.
> Guarda el resultado en **`~/.config/agencia-ia/perfil.json`** y de ahí TODOS los
> skills salen personalizados (su marca, sus precios, su forma de cobrar, sus colores).

## Cuándo se dispara
- Cualquier skill de agencia, al inicio (Fase 0), revisa si existe `~/.config/agencia-ia/perfil.json`.
- **Si NO existe** → corre este onboarding (las preguntas de abajo), guarda el JSON, y continúa con lo que el usuario pidió.
- **Si SÍ existe** → lo carga y NO vuelve a preguntar. (Para reconfigurar: el usuario dice "configura mi agencia" / "actualiza mi perfil" → re-corre esto.)

## Cómo conducir el onboarding
Cálido, una pregunta a la vez (mismo estilo que el resto de skills de Horizontes IA), español neutro LATAM, sin tecnicismos. Ancla con ejemplos para que sea fácil responder. Abre así:

```
Antes de armarte tu primera [cotización/propuesta/etc.], déjame conocer tu
agencia — son 1-2 minutos y solo lo hago UNA vez. Después todo lo que generes
ya sale con TU marca, TUS precios y TU forma de cobrar. Empecemos:
```

Luego, una por una (si el usuario da varias de golpe, no re-preguntes):

1. **¿Cómo se llama tu agencia o tu marca?** (con la que te presentas a clientes) → `agencia.nombre_marca`
2. **Para los contratos, ¿cuál es tu nombre legal completo?** ¿Eres persona física o tienes empresa registrada? → `agencia.nombre_legal`, `agencia.tipo_legal` ("persona"|"empresa")
3. **¿Tu nombre y cómo te presentas?** (ej. "Santi, fundador") → `persona.nombre`, `persona.rol`
4. **¿A qué email y WhatsApp te escriben los clientes?** ¿Tienes web o portafolio? → `persona.email`, `persona.whatsapp`, `persona.web`
5. **¿Desde qué país operas y en qué moneda cobras?** (ej. México / USD) → `ubicacion.pais`, `ubicacion.moneda`
6. **¿Cuánto cobras normalmente por montar un sistema?** Muchos arrancan en **$1,500–$3,000 de setup** + **$200–$500 al mes** de mantenimiento. ¿Cómo lo manejas tú? → `precios.setup_min`, `precios.setup_max`, `precios.mensualidad` (0 si no cobras mensualidad)
7. **¿Cómo divides el pago?** Lo más común es **50% anticipo + 50% al entregar**. ¿Te sirve así o usas otra? → `precios.estructura_pago` (ej. "50/50")
8. **¿Con qué cobras?** (Stripe, PayPal, Mercado Pago, transferencia) y ¿tienes un link o datos de pago? → `cobro.proveedor`, `cobro.datos`
9. *(opcional)* **¿Color de acento de tu marca?** (hex, ej. #00E5FF) y ¿un logo (URL)? → `marca.color_acento`, `marca.logo_url`
10. *(opcional)* **¿Tono?** (cálido / formal / directo) → `tono`

Confirma en bloque lo que entendiste antes de guardar ("¿así está bien?").

## Guardar el perfil
Crea la carpeta y escribe el JSON (estructura en `perfil.ejemplo.json`):

```bash
mkdir -p ~/.config/agencia-ia
# escribe ~/.config/agencia-ia/perfil.json con la herramienta Write
```

Campos que faltaron → déjalos en `null` o un default razonable (márcalo). Defaults por país para moneda/costo-hora si no los dio.

## Cómo lo usan los skills
Cada generador/skill **lee `~/.config/agencia-ia/perfil.json`** y rellena con él: el nombre de la agencia en el encabezado, el nombre legal y datos en el contrato, los precios como punto de partida de la cotización, el proveedor/link en el cobro, el color de acento en los HTML, el tono en el copy. Así cada documento sale personalizado sin volver a preguntar.

> Regla: el perfil es el DEFAULT, no una jaula. Si para un cliente específico el precio o el alcance cambian, el skill lo ajusta para ESE trato sin tocar el perfil.
