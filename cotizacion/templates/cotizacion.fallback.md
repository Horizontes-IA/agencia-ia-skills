# {{TITULO}}

**Preparada para:** {{CLIENTE_NEGOCIO}}
**Contacto:** {{CLIENTE_CONTACTO}}
**Preparada por:** {{AGENCIA}}
**Fecha:** {{FECHA}}  ·  **Folio:** {{FOLIO}}  ·  **Moneda:** {{MONEDA}}
**Válida hasta:** {{VIGENCIA}}

---

## Resumen

{{RESUMEN_EJECUTIVO}}

## El problema que vamos a resolver

> *"{{FRASE_CLIENTE}}"*

{{PROBLEMA_TEXTO}}

## La solución

{{SOLUCION_TEXTO}}

**Lo que vas a tener funcionando:**

- {{ENTREGABLE_1}}
- {{ENTREGABLE_2}}
- {{ENTREGABLE_3}}

## Lo que esto te regresa

- **{{ROI_1_NUM}}** — {{ROI_1_LABEL}}: {{ROI_1_CTX}}
- **{{ROI_2_NUM}}** — {{ROI_2_LABEL}}: {{ROI_2_CTX}}
- **{{ROI_3_NUM}}** — {{ROI_3_LABEL}}: {{ROI_3_CTX}}

_{{ROI_NOTA}}_

## Alcance

**Incluye:**

- {{INCLUYE_1}}
- {{INCLUYE_2}}

**No incluye (este proyecto):**

- {{NO_INCLUYE_1}}
- {{NO_INCLUYE_2}}

## Cómo vamos a trabajar

1. **{{FASE_1_TITULO}}** ({{FASE_1_DUR}}) — {{FASE_1_DESC}}
2. **{{FASE_2_TITULO}}** ({{FASE_2_DUR}}) — {{FASE_2_DESC}}
3. **{{FASE_3_TITULO}}** ({{FASE_3_DUR}}) — {{FASE_3_DESC}}

## Tu inversión

| Opción | Precio | Anticipo ({{ANTICIPO_PCT}}%) | Incluye |
|---|---|---|---|
| **{{OP1_NOMBRE}}** | {{OP1_PRECIO}} {{MONEDA}} | {{OP1_ANTICIPO}} | {{OP1_INCLUYE}} |
| **{{OP2_NOMBRE}}** ⭐ (recomendada) | {{OP2_PRECIO}} {{MONEDA}} | {{OP2_ANTICIPO}} | {{OP2_INCLUYE}} |
| **{{OP3_NOMBRE}}** | {{OP3_PRECIO}} {{MONEDA}} | {{OP3_ANTICIPO}} | {{OP3_INCLUYE}} |

**Mantenimiento mensual (opcional):** {{RETAINER_PRECIO}} /mes — {{RETAINER_DESC}}

## Términos

- **Anticipo:** {{ANTICIPO_PCT}}% al firmar. El trabajo arranca cuando entra el anticipo.
- **Forma de pago:** {{FORMA_PAGO}}
- **Tiempo de entrega:** {{TIEMPO_ENTREGA}}
- **Soporte incluido:** {{GARANTIA}}
- **Vigencia:** esta cotización es válida hasta el {{VIGENCIA}}. Después puede ajustarse.

## {{CIERRE_TITULO}}

{{CIERRE_TEXTO}}

---

**Notas y supuestos:**

- {{SUPUESTO_1}}
- {{SUPUESTO_2}}

---

_Cotización generada por {{AGENCIA}} · Documento confidencial._

<!--
NOTA: Esta es la plantilla de FALLBACK en markdown puro, para cuando NO hay Python disponible.
El camino preferido SIEMPRE es generar con `scripts/generar_cotizacion.py` (produce el HTML
profesional cliente-facing + el markdown). Esta plantilla es el plan B: rellena los {{PLACEHOLDERS}}
a mano con los datos del cotizacion.json y entrega el markdown. El anticipo se calcula
multiplicando el precio por el porcentaje (ej. $2,200 x 50% = $1,100).
-->
