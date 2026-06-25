# ANEXO A — ALCANCE DEL TRABAJO

> Parte integral del Contrato de Prestación de Servicios con folio **{{FOLIO}}**, fecha **{{FECHA}}**.
> Define con precisión qué se construye, qué se entrega, cuántas revisiones, y — tan importante como lo anterior — **qué NO incluye**.

<!--
LLENADO: este Anexo se autollena del diagnostico.json si existe.
- Cada automatización del array `automatizaciones[]` → una entrada en "Automatizaciones incluidas".
  · titulo → título de la entrada
  · que_hace → "Qué hace"
  · arquitectura_simple[] → "Cómo funciona (pasos)"
  · herramientas[].nombre → "Herramientas / servicios" (recuerda: las paga el Cliente, cláusula 7)
  · construible_por_usuario / construir_con → contexto técnico interno (no obligatorio mostrarlo al cliente)
- Si NO hay diagnostico.json, llena a mano con lo acordado en la propuesta/cotización.
-->

## 1. Resumen del proyecto

**Cliente:** {{NOMBRE_NEGOCIO_CLIENTE}}
**Giro:** {{TIPO_NEGOCIO}}
**Objetivo del proyecto:** {{OBJETIVO_PROYECTO}}

{{DESCRIPCION_PROYECTO}}

## 2. Automatizaciones incluidas

### 2.1 {{AUTOMATIZACION_1_TITULO}}

- **Qué hace:** {{AUTOMATIZACION_1_QUE_HACE}}
- **Cómo funciona (pasos):**
  {{AUTOMATIZACION_1_PASOS}}
- **Herramientas / servicios que usa** (contratados a nombre del Cliente, cláusula 7): {{AUTOMATIZACION_1_HERRAMIENTAS}}

[[OPCIONAL: repetir el bloque 2.x por cada automatización del diagnostico.json. Borra los bloques sobrantes.]]

### 2.2 {{AUTOMATIZACION_2_TITULO}}

- **Qué hace:** {{AUTOMATIZACION_2_QUE_HACE}}
- **Cómo funciona (pasos):**
  {{AUTOMATIZACION_2_PASOS}}
- **Herramientas / servicios que usa:** {{AUTOMATIZACION_2_HERRAMIENTAS}}

### 2.3 {{AUTOMATIZACION_3_TITULO}}

- **Qué hace:** {{AUTOMATIZACION_3_QUE_HACE}}
- **Cómo funciona (pasos):**
  {{AUTOMATIZACION_3_PASOS}}
- **Herramientas / servicios que usa:** {{AUTOMATIZACION_3_HERRAMIENTAS}}

## 3. Entregables

Al cierre del proyecto, el Proveedor entregará:

- {{ENTREGABLE_1}}
- {{ENTREGABLE_2}}
- Documentación de uso y puesta en marcha (handoff).
- {{ENTREGABLE_EXTRA}}

## 4. Revisiones incluidas

Se incluyen **{{NUM_REVISIONES}}** ronda(s) de revisión por entregable. Ajustes solicitados más allá de esto se tratan como **Orden de Cambio** (cláusula 6 del Contrato).

## 5. Lo que NO incluye este alcance

> Esta lista evita malentendidos. Todo lo de abajo es **fuera de alcance** y requiere Orden de Cambio con precio aparte.

- Automatizaciones o integraciones no listadas en la sección 2.
- {{FUERA_ALCANCE_1}}
- {{FUERA_ALCANCE_2}}
- Costos de las APIs, suscripciones y servicios de terceros (los paga el Cliente — cláusula 7).
- Soporte o mantenimiento más allá del periodo de garantía [[OPCIONAL: o del retainer contratado]].
- Capacitación extensa al equipo del Cliente más allá del handoff básico.
- Creación de contenido, datos o catálogos que el Cliente debe proveer.

## 6. Responsabilidades del Cliente

Para cumplir los plazos, el Cliente se compromete a entregar de forma oportuna:

- Accesos a sus sistemas (vía la autorización segura de la cláusula 10 — un clic, sin contraseñas).
- {{INSUMO_CLIENTE_1}} (por ejemplo: lista de precios, catálogo, preguntas frecuentes).
- Aprobaciones y retroalimentación en las rondas de revisión.

> El reloj de los plazos **se pausa** mientras el Proveedor espere insumos o aprobaciones del Cliente.

## 7. Métricas de éxito y puesta en marcha

- **Criterio de aceptación:** {{CRITERIO_ACEPTACION}} (qué tiene que hacer la automatización para considerarse entregada).
- **Periodo de garantía post go-live:** {{GARANTIA}} (por ejemplo, 2 semanas de corrección de errores sin costo).
