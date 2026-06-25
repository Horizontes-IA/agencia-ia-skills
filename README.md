# Sistema de Agencia IA — Skills para Claude Code

Cinco skills de [Claude Code](https://claude.com/claude-code) que cubren **todo el papeleo de una agencia de automatización con IA**: del precio al cobro. Pensados para operadores de LATAM que están arrancando — premium, sin tecnicismos, y **se auto-configuran con TU marca una sola vez**.

Hecho por [Horizontes IA](https://www.skool.com/horizontes-ia-9992).

---

## Qué incluye

| Skill | Para qué sirve |
|---|---|
| `/cotizacion` | La cotización que el cliente ve y firma — 3 opciones con efecto ancla, anticipo y vigencia. |
| `/propuesta` | El documento de venta que **gana la decisión** antes del "sí" (narrativa de cierre). |
| `/contrato` | El contrato de prestación de servicios que te protege (alcance, IP atada al pago, datos, terminación). |
| `/cobro` | La factura + el **link de pago real** + la cadena de recordatorios. |
| `/cerrar-cliente` | El orquestador: del apretón de manos al kickoff corre todos los anteriores en orden, sin re-preguntar. |

Cada skill entrega **markdown editable + un HTML premium que imprime a PDF** (listo para mandárselo a un cliente real).

---

## Instalación (1 comando)

```bash
curl -fsSL https://raw.githubusercontent.com/Horizontes-IA/agencia-ia-skills/main/instalar.sh | bash
```

Esto copia los 5 skills a `~/.claude/skills/` y el onboarding compartido a `~/.config/agencia-ia/`.

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
Prospecto → /cotizacion → /propuesta → (sí) → /contrato → /cobro (anticipo) → conectar apps → kickoff
                                    └────────────── /cerrar-cliente corre todo esto de un jalón ──────────────┘
```

1. **`/cotizacion`** — "cotiza a este cliente" → 3 opciones de precio.
2. **`/propuesta`** — "arma la propuesta para [negocio]" → documento de venta.
3. **`/contrato`** — "el cliente ya dijo que sí, hazme el contrato".
4. **`/cobro`** — "cobra el anticipo" → factura + link de pago.
5. **`/cerrar-cliente`** — "acabo de cerrar a [cliente]" → corre los 4 anteriores en orden y arma el expediente `cliente-<nombre>/`.

---

## Compañeros (otros skills de Horizontes IA)

Estos no vienen en este paquete pero completan el ciclo de la agencia:

- **`/diagnostico`** — entrevista al prospecto y arma el plan técnico (va ANTES de cotizar).
- **`/conectar-cliente`** — genera links para que el cliente conecte sus apps (Gmail, Calendar, WhatsApp…) sin darte contraseñas, vía Composio. → [Horizontes-IA/conectar-cliente-skill](https://github.com/Horizontes-IA/conectar-cliente-skill)
- **`/docs-entrega`** — los documentos de entrega del proyecto. → [santmun/docs-entrega-skill](https://github.com/santmun/docs-entrega-skill)
- **`/mantenimiento`** — el reporte mensual de salud del sistema. → [santmun/mantenimiento-skill](https://github.com/santmun/mantenimiento-skill)

---

## Requisitos

- [Claude Code](https://claude.com/claude-code) instalado.
- Python 3 (para los generadores de HTML/PDF). Si no lo tienes, los skills pueden escribir el HTML a mano — el script es la vía cómoda, no la única.

---

## Aviso

Los contratos y documentos son **modelos de trabajo**, no asesoría legal. Las leyes varían por país; para tratos de monto alto, haz que un abogado de tu país los revise antes de firmar.

---

*Comunidad: [Horizontes IA en Skool](https://www.skool.com/horizontes-ia-9992) · [horizontesia.com](https://horizontesia.com)*
