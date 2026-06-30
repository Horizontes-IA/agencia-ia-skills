# Diagnóstico de automatización — {{negocio.nombre_negocio}}

> Plantilla del entregable `01-procesos-y-roi.md`. El generador (`scripts/generar_reporte.py`)
> la rellena desde `diagnostico.json`. Los marcadores `{{...}}` mapean a campos del esquema
> canónico (`_design/schema.md`). Tono: consultor, segunda persona, ~1.5 páginas.

{{negocio.descripcion}} Hay {{n_automatizaciones}} procesos que hoy te roban ~{{horas_total_semana}}h/semana. Automatizarlos en este orden te acerca a tu meta y te devuelve esas horas.

## Tus procesos, calificados

| Proceso | Veces/sem | Horas/sem | Score | Veredicto |
|---|---|---|---|---|
| {{proceso.nombre}} | {{proceso.frecuencia_veces_semana}} | {{proceso.horas_semana}} | {{proceso.score}}/100 | {{proceso.banda_icon}} {{proceso.banda_label}} |
| … (una fila por cada proceso, ordenadas por score descendente) | | | | |

> Veredictos: 🟢 Automatiza ya (≥75) · 🟡 Alto potencial (55-74) · 🟠 Más adelante (35-54) · ⚪ No prioritario (<35).

## Las automatizaciones recomendadas

### #{{automatizacion.rank}} — {{automatizacion.titulo}}

{{automatizacion.que_hace}}

> {{automatizacion.metafora_empleado}}

- **Ahorro:** {{automatizacion.roi.horas_ahorradas_mes}}h/mes ≈ {{automatizacion.roi.valor_tiempo_mes_usd}}/mes
- **Ingreso recuperado:** +{{automatizacion.roi.ingreso_recuperado_mes_usd}}/mes (estimación conservadora) — *solo si existe*
- **Herramientas:** {{automatizacion.herramientas[].nombre}}
- **Complejidad:** {{automatizacion.complejidad}}
- **Cómo construirlo:** con el skill `/crear-agente`, paso a paso, sin programar. *(solo si `es_agente_nube`)*

*(repetir por cada automatización del top-3)*

## ROI consolidado

| Automatización | Horas/mes | Ahorro/mes | Costo/mes | Neto/mes |
|---|---|---|---|---|
| #{{rank}} {{titulo}} | {{horas}} | {{ahorro_mes}} | {{costo_mes}} | {{neto_mes}} |
| **TOTAL** | **{{horas_total}}** | **{{ahorro_total}}** | **{{costo_total}}/mes** | **{{neto_total}}/mes** |

> El ahorro se recalcula del lado del generador (suma de `automatizaciones[].roi`), nunca se copia de la IA.

La #1 es **{{quick_win.titulo}}** — empieza por ahí. El archivo `04-quick-win.md` ya tiene lo que necesitas para arrancar hoy.
