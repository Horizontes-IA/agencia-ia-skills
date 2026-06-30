# Tu stack recomendado — {{negocio.nombre_negocio}}

> Plantilla del entregable `03-stack-recomendado.md`. Stack MÍNIMO viable, no exhaustivo.
> El público llega con poco (solo ChatGPT) → cada herramienta extra se justifica y se prioriza
> el plan gratis. Se rellena con las herramientas únicas de `automatizaciones[].herramientas[]`.

Lo mínimo viable para arrancar. No es exhaustivo: cada herramienta extra se justifica y se prioriza el plan gratis.

| Herramienta | Para qué | Costo |
|---|---|---|
| {{herramienta.nombre}} | {{herramienta.para_que}} ({{herramienta.costo_nota}}) | {{herramienta.costo_mes_usd}}/mes o Gratis |
| … (una fila por herramienta única en el top-3) | | |

**Costo total mensual estimado: {{roi_global.costo_total_mes_usd}}/mes.**

> Para construir esto paso a paso sin programar, usa el skill `/crear-agente`. *(solo si alguna automatización es agente en la nube)*

Notas:
- Nombres propios en inglés (Cloudflare, OpenAI, Claude, Twilio). Todo lo demás traducido.
- Una nota por herramienta solo si no es obvia.
- El costo total debe ser bajo: respeta el presupuesto declarado en D7.
