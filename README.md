# Sistema de Agencia IA — Skills para Claude Code

Diez skills de [Claude Code](https://claude.com/claude-code) que cubren el ciclo completo de una agencia de automatización con IA: **del diagnóstico al mantenimiento mensual**. Pensados para operadores de LATAM que están arrancando — premium, sin tecnicismos, y **se auto-configuran con TU marca una sola vez**.

Hecho por [Horizontes IA](https://www.skool.com/horizontes-ia-9992).

---

## Empieza por aquí: `/nuevo-cliente`

No necesitas recordar los 10 skills. Di **`/nuevo-cliente`** (o *"arma el kit de [cliente]"*), dale la info que tengas del cliente —toda, la básica o nada— y este skill te pregunta lo que falte y **encadena los demás en orden**, generando todo con tu marca y en PDF, junto en una carpeta. Es inteligente: a un prospecto que aún no cierra le arma el **paquete de venta** (diagnóstico + cotización + propuesta) y deja el contrato y el cobro para cuando diga que sí.

## Qué incluye

| Skill | Para qué sirve |
|---|---|
| `/nuevo-cliente` ⭐ | **La puerta de entrada.** Orquesta todo el kit a partir de la info que tengas; pregunta lo que falte y genera el kit completo o la pieza que pidas. |
| `/diagnostico` | Entrevista el negocio del prospecto, rankea qué automatizar y arma el reporte premium con ROI y plan a 90 días — va ANTES de cotizar. |
| `/cotizacion` | La cotización que el cliente ve y firma — 3 opciones con efecto ancla, anticipo y vigencia. |
| `/propuesta` | El documento de venta que **gana la decisión** antes del "sí" (narrativa de cierre). |
| `/contrato` | El contrato de prestación de servicios que te protege (alcance, IP atada al pago, datos, terminación). |
| `/cobro` | La factura + el **link de pago real** + la cadena de recordatorios. |
| `/conectar-cliente` | Genera links para que el cliente conecte SUS cuentas (Gmail, Calendar, WhatsApp…) sin darte contraseñas, vía Composio — el onboarding técnico, va DESPUÉS de cobrar. *(Llave gratis de Composio, se pide al usarlo.)* |
| `/cerrar-cliente` | El orquestador: del apretón de manos al kickoff corre todos los anteriores en orden, sin re-preguntar. |
| `/docs-entrega` | Los documentos de entrega del proyecto (manual, accesos, docs técnicas) en Word — para el handoff que te hace ver pro. |
| `/mantenimiento` | El reporte mensual de salud del sistema en Word, para mandárselo al cliente cada mes — eso justifica la mensualidad. |

Cada skill entrega **markdown editable + un HTML premium que imprime a PDF** (listo para mandárselo a un cliente real).

---

## Instalación (1 comando)

```bash
curl -fsSL https://raw.githubusercontent.com/Horizontes-IA/agencia-ia-skills/main/instalar.sh | bash
```

Esto copia los 10 skills a `~/.claude/skills/`, deja listas las dependencias de `/conectar-cliente` (Node), el conversor a PDF y el onboarding compartido a `~/.config/agencia-ia/`. (`/docs-entrega` y `/mantenimiento` generan Word con `python-docx`, que el propio skill instala en su primera corrida.)

> ¿Prefieres a mano? Clona el repo y copia cada carpeta de skill a `~/.claude/skills/`, y `configurar.md` + `perfil.ejemplo.json` a `~/.config/agencia-ia/`.

---

## Se configura UNA sola vez

La **primera** vez que uses cualquier skill (por ejemplo `/cotizacion`), te hará unas preguntas rápidas sobre tu agencia (nombre, precios, cómo cobras, color de marca…) y guardará tu perfil en:

```
~/.config/agencia-ia/perfil.json
```

A partir de ahí **TODO** lo que generes sale con tu marca, tus precios y tu forma de cobrar — sin volver a preguntar. Para reconfigurar: dile a Claude **"configura mi agencia"**.

El perfil es el DEFAULT, no una jaula: si para un cliente el precio o el alcance cambian, el skill lo ajusta para ESE trato sin tocar tu perfil.

---

## Cómo se usa (el flujo de una agencia real)

```
            ┌──────────────── /nuevo-cliente lo orquesta según el punto del trato ────────────────┐
Prospecto → /diagnostico → /cotizacion → /propuesta → (sí) → /contrato → /cobro → /conectar-cliente → kickoff
                                       └──── /cerrar-cliente corre de /cotizacion a /cobro ────┘
   … construyes … → /docs-entrega (entregas) → /mantenimiento (cada mes → cobras el retainer)
```

La forma fácil: **`/nuevo-cliente`** y deja que él rutee. La forma manual (skill por skill):

0. **`/diagnostico`** — "diagnostica el negocio de [prospecto]" → reporte con qué automatizar, ROI y plan (la base de la cotización).
1. **`/cotizacion`** — "cotiza a este cliente" → 3 opciones de precio.
2. **`/propuesta`** — "arma la propuesta para [negocio]" → documento de venta.
3. **`/contrato`** — "el cliente ya dijo que sí, hazme el contrato".
4. **`/cobro`** — "cobra el anticipo" → factura + link de pago.
5. **`/conectar-cliente`** — "conecta el Gmail/WhatsApp de [cliente]" → links de autorización para tener listas sus cuentas antes del kickoff.
6. **`/cerrar-cliente`** — "acabo de cerrar a [cliente]" → corre `/cotizacion`→`/cobro` en orden y arma el expediente `cliente-<nombre>/`.
7. *(construyes la automatización — con `/crear-agente`, n8n o Make)*
8. **`/docs-entrega`** — "documenta la entrega de [cliente]" → manual, accesos y docs técnicas en Word para el handoff.
9. **`/mantenimiento`** — "genera el reporte mensual de [cliente]" → health check en Word que le mandas cada mes (y cobras el retainer con `/cobro`).

---

## Compañeros (otros skills de Horizontes IA)

Estos no vienen en este paquete pero completan el ciclo:

- **`/crear-agente`** — construye la automatización que vendiste (el paso entre el cierre y la entrega). Es el "construir", no el papeleo.

---

## Requisitos

- [Claude Code](https://claude.com/claude-code) instalado.
- Python 3 (para los generadores de HTML/PDF). Si no lo tienes, los skills pueden escribir el HTML a mano — el script es la vía cómoda, no la única.
- Node.js + npm (solo para `/conectar-cliente`, que usa la SDK de Composio). El instalador deja sus dependencias listas; la **llave gratis de Composio** te la pide el skill la primera vez que lo usas.

---

## Aviso

Los contratos y documentos son **modelos de trabajo**, no asesoría legal. Las leyes varían por país; para tratos de monto alto, haz que un abogado de tu país los revise antes de firmar.

---

*Comunidad: [Horizontes IA en Skool](https://www.skool.com/horizontes-ia-9992) · [horizontesia.com](https://horizontesia.com)*
