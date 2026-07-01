---
name: conectar-cliente
description: Conecta las cuentas del cliente (Gmail, Calendar, WhatsApp, Sheets, Drive, Notion, Slack, APIs, etc.) que tu automatización va a usar — en DOS modos que el skill te deja elegir. Modo Composio - le mandas al cliente un link, da 1 clic y autoriza, sin contraseñas ni cuenta de Composio (revocable). Modo Manual "a la antigua" - tú creas las cuentas o le pides sus API keys, y el skill te genera un DOCUMENTO DE ACCESOS con tu marca para guardarlos ordenados. El skill te pregunta qué método quieres y qué cuentas vas a conectar. Úsalo cuando digas "conéctale las cuentas a [cliente]", "genera un enlace para [cliente] para [app]", "conéctale el [app] a [cliente]", "arma el documento de accesos de [cliente]", "¿qué tiene conectado [cliente]?", "desconecta el [app] de [cliente]". Es la pieza de onboarding técnico del cliente: va DESPUÉS de cobrar el anticipo y antes del kickoff. El modo Composio necesita una llave gratis de Composio (se pide la primera vez).
---

# Conectar Cliente — dos modos

Conecta las cuentas que la automatización del cliente va a necesitar (su Gmail, su WhatsApp, su Calendar, una API…). Hay **dos formas** de hacerlo, y este skill te deja elegir:

- **Modo Composio (recomendado):** le mandas al cliente un link, da **1 clic** y autoriza con su cuenta real. **Sin contraseñas, sin que él cree cuenta de Composio, y revocable** cuando el trato termine.
- **Modo Manual ("a la antigua"):** tú creas las cuentas o le pides sus **API keys**, y el skill te genera un **documento de accesos con tu marca** para guardarlos ordenados.

> **Dónde encaja en el flujo:** `…/cobro (anticipo) → /conectar-cliente → kickoff`. Una vez cobrado el anticipo, dejas listas las cuentas para arrancar la construcción.

## ⚙️ Fase 0 — Perfil de tu agencia (auto-config, una sola vez)

Este skill es parte del kit **agencia-ia-skills**. Revisa si existe `~/.config/agencia-ia/perfil.json`:
- Si **NO existe** → lee `~/.config/agencia-ia/configurar.md`, corre el onboarding (una vez) y guárdalo.
- Si **SÍ existe** → cárgalo. Solo importa para el **Modo Manual**: el documento de accesos sale con `agencia.nombre_marca`, `persona.*` (contacto) y `marca.color_acento`. El Modo Composio no necesita marca.

## Fase 1 — Elige el modo y las cuentas (pregúntalo)

Antes de nada, pregunta **dos cosas** (a menos que el usuario ya lo haya dicho):

```
¿Cómo quieres conectar las cuentas de [cliente]?

  A) Composio (recomendado) — le mandas un link, da 1 clic y autoriza.
     Sin contraseñas, sin que cree cuenta, y lo puedes revocar. ✅

  B) A la antigua — tú creas las cuentas o le pides sus API keys,
     y te armo un documento de accesos con tu marca para guardarlos.

¿Y qué cuentas vas a conectar? (Gmail, WhatsApp, Calendar, Sheets,
Notion, la API de OpenAI, etc.)
```

Con la respuesta, ve al **Modo A** o al **Modo B**.

---

## Modo A — Composio (links de 1 clic)

Onboarding con **una sola cuenta de Composio tuya**. Cada cliente es un `userId`; el cliente solo da clic y autoriza. Tú nunca tocas sus contraseñas.

**Configuración (la PRIMERA vez):**
1. **Llave de Composio.** Si no existe `.env` junto a `connect.mjs` con `COMPOSIO_API_KEY`, pídesela al usuario: entra a **https://app.composio.dev** (gratis) → *Settings → API Keys* → copia la key, y escríbela en `~/.claude/skills/conectar-cliente/.env`:
   ```
   COMPOSIO_API_KEY=la_llave_que_te_dio
   ```
   Nunca muestres ni repitas la llave en el chat.
2. **Dependencias.** Si falta `node_modules/`, corre una vez: `cd ~/.claude/skills/conectar-cliente && npm install` (el instalador del kit ya las deja listas).

**Ejecutarlo:** corre el script y muéstrale al usuario el resultado tal cual (el link + el mensaje listo para mandar):
```bash
node ~/.claude/skills/conectar-cliente/connect.mjs <accion> <cliente> [app]
```

| Acción | Uso | Qué hace |
|---|---|---|
| `link` | `link juan gmail` · `link juan gmail,calendario` | Genera el/los link(s) + mensaje listo para mandar |
| `estado` | `estado juan gmail` | ¿Ese cliente ya conectó esa app? |
| `apps` | `apps juan` | Qué cuentas tiene conectadas ese cliente |
| `revoke` | `revoke juan gmail` | Desconecta (offboarding cuando el cliente cancela) |

**Reglas:**
1. Normaliza el nombre del cliente a un `userId` estable sin espacios (ej. "Barbería Hugo" → `barberia-hugo`). Usa SIEMPRE el mismo para ese cliente. Si ya usaste uno antes, reúsalo.
2. Apps por nombre común que el script entiende: `correo/gmail`, `calendario`, `whatsapp`, `hojas/sheets`, `drive`, `notion`, `slack`, `hubspot`, `instagram`, `github`, `outlook`, `trello`. Otras → pásalas como su slug de Composio.
3. Muéstrale el link y el mensaje listo para mandar. **No expongas la API key ni IDs internos.**

---

## Modo B — Manual ("a la antigua")

Para quien prefiere crear las cuentas él mismo o pedirle al cliente sus API keys. El skill **no toca contraseñas** ni las guarda: arma un **documento de accesos ordenado** (con tu marca) donde queda registrado, por cada cuenta, **de dónde sale el acceso** y **dónde vive la credencial** — con espacios `[así]` para que TÚ pegues las claves en un lugar seguro, nunca en el chat ni en el repo.

### Paso 1 — Junta, por cada cuenta, cómo se accede

Para cada app que el usuario nombró, pregúntale (rápido, en una tanda) cuál de estos aplica:
- **La agencia crea una cuenta nueva** (ej. le abres un número de WhatsApp Business, una cuenta de OpenAI para el proyecto).
- **El cliente da su API key** (ej. su key de OpenAI, su token de una herramienta que ya usa).
- **Login compartido del cliente** (te da acceso a su cuenta existente).

Y para cada una: quién es el **usuario/email**, y **dónde vas a guardar la credencial** (gestor de contraseñas, .env del proyecto, etc.).

### Paso 2 — Escribe el `accesos.json`

Guárdalo en el expediente del cliente (`cliente-<slug>/` si existe, o `accesos-<slug>/`):
```json
{
  "cliente": "Sabores de Casa",
  "fecha": "30 de junio de 2026",
  "accesos": [
    { "app": "WhatsApp Business API", "metodo": "La agencia crea la cuenta", "usuario": "número nuevo del proyecto", "ubicacion": "[gestor de contraseñas del proyecto]", "notas": "el número lo administra la agencia" },
    { "app": "OpenAI API", "metodo": "API key del cliente", "usuario": "cuenta del cliente", "ubicacion": "[pega la key en el gestor]", "notas": "el consumo lo paga el cliente" },
    { "app": "Google Calendar", "metodo": "Login compartido del cliente", "usuario": "agenda@saboresdecasa.com", "ubicacion": "[acceso vía el gestor]", "notas": "solo lectura/escritura de eventos" }
  ],
  "nota_seguridad": "Este documento NO contiene las claves. Guárdalas en un gestor de contraseñas; nunca por correo o WhatsApp."
}
```
> **Regla dura de seguridad:** en `ubicacion` va SIEMPRE un placeholder `[...]`, **nunca la clave real**. No pegues claves/API keys en el chat, en el JSON ni en el HTML. El documento es un índice de accesos, no un almacén de secretos.

### Paso 3 — Genera el documento (con tu marca)

```bash
python3 ~/.claude/skills/conectar-cliente/generar-accesos.py <ruta>/accesos.json <ruta>/
```
Escribe `accesos.html` (imprime a PDF, con tu color y marca del perfil) + `accesos.md` (editable). Luego, para el PDF:
```bash
python3 ~/.config/agencia-ia/html2pdf.py <ruta>/accesos.html
```
Si no hay Python, escribe tú el `accesos.html`/`.md` con la misma tabla (App · Método · Usuario · Dónde vive la credencial · Notas) y la nota de seguridad.

---

## Reglas del skill

1. **Siempre pregunta el modo y las cuentas primero** (Fase 1). No asumas Composio si el usuario prefiere hacerlo a mano.
2. **Nunca expongas secretos:** ni la API key de Composio, ni las claves del cliente. En el Modo B, las credenciales van con placeholder `[...]`.
3. Modo Composio = 1 cuenta tuya + 1 `userId` por cliente, revocable. Modo Manual = documento de accesos con tu marca, sin guardar secretos.
4. Ambos modos van DESPUÉS de cobrar el anticipo y antes del kickoff.
