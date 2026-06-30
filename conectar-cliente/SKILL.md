---
name: conectar-cliente
description: Genera links para que tus clientes conecten SUS cuentas (Gmail, Calendar, WhatsApp, Sheets, Drive, Notion, Slack, etc.) a TU Composio — sin que el cliente cree cuenta ni te dé contraseñas, solo autoriza con un clic. Úsalo cuando digas "genera un enlace para [cliente] para [app]", "conéctale el [app] a [cliente]", "¿qué tiene conectado [cliente]?", "¿[cliente] ya conectó su [app]?", "desconecta el [app] de [cliente]". Es la pieza de onboarding/offboarding técnico del cliente: va DESPUÉS de cobrar el anticipo y antes del kickoff, para tener listas las cuentas que tu automatización va a usar. Necesita una llave gratis de Composio (se pide la primera vez que lo usas).
---

# Conectar Cliente (Composio)

Onboarding de las cuentas del cliente con **una sola cuenta de Composio tuya**. Cada cliente es un `userId`; el cliente NO necesita cuenta de Composio — solo da clic y autoriza con su cuenta real. Tú nunca tocas sus contraseñas.

> **Dónde encaja en el flujo de la agencia:** `…/cobro (anticipo) → /conectar-cliente → kickoff`. Una vez cobrado el anticipo, conectas las apps que la automatización del cliente va a necesitar (su Gmail, su WhatsApp, su Calendar…) para arrancar la construcción/entrega.

## Configuración (la PRIMERA vez que se usa)

Antes de correr el script, asegúrate de dos cosas (hazlo solo si faltan):

1. **Llave de Composio.** Si no existe `.env` junto a `connect.mjs` con un `COMPOSIO_API_KEY`, **pídesela al usuario**: dile que entre a **https://app.composio.dev** (cuenta gratis) → *Settings → API Keys* → copie su API key. Luego escríbela en `~/.claude/skills/conectar-cliente/.env` así:
   ```
   COMPOSIO_API_KEY=la_llave_que_te_dio
   ```
   Nunca muestres ni repitas la llave en el chat después de guardarla.
2. **Dependencias.** Si no existe la carpeta `node_modules/` en el skill, instálalas una vez:
   ```bash
   cd ~/.claude/skills/conectar-cliente && npm install
   ```
   (El instalador del paquete ya las deja listas; esto es solo el plan B.)

## Cómo ejecutarlo

Corre el script y muéstrale al usuario el resultado tal cual (el link + el mensaje listo para mandar al cliente):

```bash
node ~/.claude/skills/conectar-cliente/connect.mjs <accion> <cliente> [app]
```

Acciones:
| Acción | Uso | Qué hace |
|---|---|---|
| `link` | `link juan gmail` · `link juan gmail,calendario` | Genera el/los link(s) + mensaje listo para mandar |
| `estado` | `estado juan gmail` | ¿Ese cliente ya conectó esa app? |
| `apps` | `apps juan` | Qué cuentas tiene conectadas ese cliente |
| `revoke` | `revoke juan gmail` | Desconecta (offboarding cuando el cliente cancela) |

**Default**: si solo te dicen "genera un enlace para X para Y" → usa `link`.

## Reglas

1. **Normaliza el nombre del cliente a un `userId` estable y sin espacios** (ej: "Barbería Hugo" → `barberia-hugo`). Usa SIEMPRE el mismo userId para el mismo cliente — es la llave de todas sus conexiones. Si ya usaste uno antes para ese cliente, reúsalo.
2. **Apps por nombre común**: el script ya entiende `correo/gmail`, `calendario`, `whatsapp`, `hojas/sheets`, `drive`, `notion`, `slack`, `hubspot`, `instagram`, `github`, `outlook`, `trello`. Si piden otra, pásala tal cual (slug de Composio).
3. **Muéstrale el link y el mensaje listo para mandar.** No expongas la API key ni IDs internos.
4. Si el script falla por falta de key, revisa que `~/.claude/skills/conectar-cliente/.env` tenga el `COMPOSIO_API_KEY` (ver §Configuración).

## Ejemplo

Usuario: *"genera un enlace para juan para gmail"*
→ `node ~/.claude/skills/conectar-cliente/connect.mjs link juan gmail`
→ devuelve el `https://connect.composio.dev/link/...` + el mensaje listo para mandarle a Juan.
