# `diagnostico.json` — Esquema canónico (el contrato)

> Este archivo define EXACTAMENTE qué produce la entrevista (`SKILL.md`) y qué consume el generador (`scripts/generar_reporte.py`). Es el contrato entre ambos. El generador debe poder renderizar un reporte premium a partir de SOLO este JSON, sin más contexto. Todos los campos marcados **(req)** son obligatorios; los **(opt)** pueden faltar y el generador degrada con gracia (omite la sección o usa un fallback declarado).
>
> Reglas del contrato:
> - Moneda: todos los montos en **USD**, número (no string), sin símbolo. El campo `moneda_display` define cómo se muestra.
> - Todo número de ROI viaja con su supuesto en un campo `*_supuesto` o dentro de `supuestos[]`.
> - Listas vacías `[]` son válidas (mejor que `null`) salvo donde se indique req.
> - El generador NUNCA inventa datos faltantes: si falta, omite la sección o muestra el fallback.
> - `schema_version` permite evolucionar sin romper el generador.

---

## Estructura de alto nivel

```jsonc
{
  "schema_version": "1.0",
  "meta": { ... },              // datos de la corrida
  "negocio": { ... },           // D1 + D2 — identidad y modelo de ingresos
  "segment": "operator",        // beginner | operator  (calibra el encuadre)
  "procesos": [ ... ],          // D3 — inventario completo, RANKEADO con scores
  "sangrado_declarado": { ... },// D4 — el voto emocional del usuario
  "stack_actual": { ... },      // D5
  "perfil_tecnico": { ... },    // D6 + D7
  "meta_90_dias": { ... },      // D8
  "research": [ ... ],          // §4 framework — hallazgos web con fuente
  "automatizaciones": [ ... ],  // top-3 diseñadas (arquitectura + tools + costo + ROI)
  "quick_win": { ... },         // la construible HOY
  "roi_global": { ... },        // número headline + escenarios + payback
  "roadmap_90_dias": [ ... ],   // 3 fases hacia meta_90_dias
  "hand_off": { ... },          // sinergia con /crear-agente
  "supuestos_globales": [ ... ],// todos los supuestos visibles del reporte
  "cierre": { ... }             // mensaje final + CTA suave
}
```

---

## 1. `meta` (req)

```jsonc
"meta": {
  "fecha": "2026-06-23",                       // req — ISO date
  "generado_por": "/diagnostico v1.0",         // req
  "id": "diag-2026-06-23-marisol",             // req — slug único (fecha + nombre)
  "duracion_entrevista_min": 8,                // opt — informativo
  "moneda_display": "USD",                     // req — "USD" | "MXN" | "COP" | ...
  "tasa_cambio_a_local": null                  // opt — si se quiere mostrar también en moneda local; null = solo USD
}
```

---

## 2. `negocio` (req) — D1 + D2

```jsonc
"negocio": {
  "nombre_persona": "Marisol",                 // req — nombre de pila (personaliza el reporte)
  "nombre_negocio": "Sabores de Casa",         // opt — si tiene marca; si no, null
  "tipo": "Restaurante / comida casera",       // req — descripción corta del giro
  "descripcion": "Restaurante de comida casera con servicio a domicilio en CDMX; recibe pedidos por WhatsApp e Instagram.",  // req — 1-2 frases en palabras del usuario
  "pais": "México",                            // req — afecta moneda y costo-hora default
  "ciudad": "CDMX",                            // opt
  "tamano": "con_equipo",                      // req — "solo" | "con_equipo" | "freelancer"
  "empleados_aprox": 3,                        // opt — número o null
  "vende_a": "B2C local",                      // req — "B2C" | "B2B" | "B2C local" | "online" | mixto
  "modelo_ingresos": {                         // req (campos internos opt)
    "que_vende": "Comidas a domicilio y para llevar",   // req
    "ticket_promedio_usd": 12,                 // opt — null si no lo dio
    "volumen_mes": "≈400 pedidos/mes",         // opt — string libre o null
    "como_cobra": "por pedido",                // opt — "por proyecto" | "recurrente" | "por hora" | "por pedido"
    "ingreso_mes_aprox_usd": 4800,             // opt — null si no lo dio (NO inventar)
    "margen_bruto_pct": 45                     // opt — margen grueso si lo sabe, null si no
  },

  // --- Los números duros del negocio (D-Números). Para OPERATORS es data CRÍTICA: es lo que hace
  // --- el ROI 100% real (no estimado). Para beginners suele ir vacío (aún no factura). NUNCA inventar.
  "economia": {                                // opt (pero la entrevista la EXIGE a operators)
    "nomina_mes_usd": 2400,                    // opt — costo del equipo al mes (nómina; incluye al dueño si se paga sueldo)
    "horas_trabajadas_mes": 300,               // opt — horas totales del equipo/persona al mes (para derivar el costo-hora REAL)
    "leads_mes": 80,                           // opt — # de interesados/prospectos al mes
    "ventas_mes": 40,                          // opt — # de operaciones/ventas cerradas al mes
    "tasa_cierre_pct": null,                   // opt — % de leads que cierran (o se deriva de ventas_mes/leads_mes)
    "kpis": [                                  // opt — KPIs libres que dio el usuario (se muestran en "Los números de tu negocio")
      { "nombre": "Pedidos grandes que se enfrían", "valor": 27, "unidad": "al mes" }
    ]
  },

  "costo_hora_usuario_usd": 8,                 // req — costo REAL de una hora. Prioridad (§3.2 framework):
                                               //   1) economia.nomina_mes_usd / economia.horas_trabajadas_mes  (REAL, preferido)
                                               //   2) el número que el usuario dé directo
                                               //   3) default_por_pais (último recurso, se marca editable)
  "costo_hora_fuente": "nomina_real",          // req — "nomina_real" | "dato_usuario" | "default_pais"
  "costo_hora_es_default": false               // req — true SOLO si costo_hora_fuente == "default_pais"
}
```

---

## 3. `segment` (req)

```jsonc
"segment": "operator"   // "beginner" | "operator"
```
Detectado por Claude (D1+D2+D6). Controla el encuadre del reporte (§6 framework). El generador elige copys según este valor.

---

## 4. `procesos` (req) — D3, el inventario RANKEADO

Array de TODOS los procesos detectados (no solo el top-3), **ordenado por `score` descendente**. Cada uno:

```jsonc
{
  "id": "p1",                                  // req — slug estable
  "nombre": "Responder cotizaciones de pedidos grandes",  // req — en palabras del usuario
  "descripcion_usuario": "Cada que alguien quiere pedido para evento le tengo que escribir precios, opciones, tiempos... casi siempre lo mismo.",  // req — quote/parafraseo del usuario (esto da el reconocimiento)
  "area": "preventa",                          // req — "adquisicion" | "preventa" | "atencion" | "entrega" | "cobro" | "marketing" | "datos" | "admin"

  // --- inputs crudos de la entrevista ---
  "frecuencia_veces_semana": 15,               // req — número (veces/semana)
  "tiempo_por_vez_min": 12,                    // req — minutos por ocurrencia
  "quien_lo_hace": "Marisol",                  // req — "usuario" | nombre | "empleado" | "nadie"
  "como_hoy": "manual por WhatsApp, escribe cada respuesta",  // req

  // --- los 5 factores 0-5 (§2 framework) ---
  "factores": {
    "bleed": 4,                                // req — 0-5
    "frequency": 5,                            // req
    "automatability": 5,                       // req
    "revenue_impact": 4,                       // req — toca ventas (pedidos que se enfrían)
    "speed_to_value": 4                        // req
  },

  // --- salida del scoring (§2) ---
  "score": 86,                                 // req — 0-100, calculado con la fórmula
  "banda": "automatiza_ya",                    // req — "automatiza_ya" | "alto_potencial" | "mas_adelante" | "no_prioritario"
  "score_rationale": "Lo haces ~15 veces/semana, 12 min cada una, casi siempre la misma respuesta, y son pedidos grandes que se te enfrían si tardas. Máximo retorno.",  // req — 1 línea que explica el puntaje

  // --- flags ---
  "user_flagged": true,                        // req — true si el usuario lo nombró en D4 (sangrado declarado)
  "horas_brutas_mes": 13.0,                    // req — (12×15×4.33)/60, redondeado
  "factor_captura": 0.70,                      // req — del haircut §3.1
  "horas_ahorradas_mes": 9.1                   // req — horas_brutas × factor_captura
}
```

> El generador usa el array completo para la **tabla de priorización** (todos los procesos con su score y banda, color-coded) y toma los `automatizable=true` top-3 para diseñar automatizaciones. Procesos con banda `no_prioritario` se muestran en la tabla pero NO generan automatización.

---

## 5. `sangrado_declarado` (req) — D4, el voto emocional

```jsonc
"sangrado_declarado": {
  "tarea_que_quitaria": "Responder cotizaciones de eventos",  // req — respuesta literal a "qué te quitarías de encima"
  "proceso_id_match": "p1",                    // req — id del proceso que matchea, o null
  "que_pierde_dinero": "Pierdo pedidos grandes porque tardo en contestar y se van con otro", // opt
  "frase_textual": "Se me va la tarde contestando lo mismo y aún así se me escapan los pedidos buenos."  // opt — quote textual para citar en el reporte (oro para el reconocimiento)
}
```

---

## 6. `stack_actual` (req) — D5

```jsonc
"stack_actual": {
  "herramientas": ["WhatsApp", "Instagram", "Excel", "ChatGPT"],  // req — normalizado (n8n/N8N→"n8n", Make.com→"Make")
  "sabe_usar": ["WhatsApp", "Excel"],          // opt
  "gasto_desperdiciado": null,                 // opt — suscripción zombi detectada, o null
  "nota": "Llega con poco stack: solo apps de mensajería + ChatGPT esporádico."  // opt — 1 línea
}
```

---

## 7. `perfil_tecnico` (req) — D6 + D7

```jsonc
"perfil_tecnico": {
  "sabe_programar": false,                     // req
  "prefiere": "construirlo_el_mismo",          // req — "construirlo_el_mismo" | "que_se_lo_hagan"
  "horas_semana_para_implementar": 4,          // opt — número o null
  "presupuesto_tools_mes_usd": 30,             // req — tope mensual para herramientas (D7); usado por el QA de costo
  "no_automatizar": "El trato con clientes de eventos VIP lo quiero personal", // opt
  "sensibilidad_bot": "alta"                   // opt — "alta" | "media" | "baja" — qué tanto le importa que no suene a bot
}
```

---

## 8. `meta_90_dias` (req) — D8

```jsonc
"meta_90_dias": {
  "objetivo": "Dejar de perder pedidos grandes y recuperar mis tardes",  // req — en palabras del usuario
  "tipo": "recuperar_tiempo",                  // req — "recuperar_tiempo" | "dejar_de_perder_leads" | "crecer_el_negocio"
  "metrica_exito": "Responder toda cotización en <2 min y recuperar ~9 h/semana"  // opt — cómo sabrá que lo logró
}
```

---

## 9. `research` (req) — §4 framework, hallazgos web

Array de hallazgos de la investigación. Mínimo 2 con fuente citable.

```jsonc
{
  "tipo": "benchmark_industria",               // req — "benchmark_industria" | "ejemplo_competidor" | "precio_herramienta"
  "hallazgo": "Restaurantes con pedidos por WhatsApp reportan 8-12 h/semana en responder cotizaciones y pedidos repetidos.",  // req — la afirmación
  "valor": null,                               // opt — número estructurado si aplica (ej. precio)
  "fuente": "https://...",                     // req — URL citable, o "estimación propia" si no se halló
  "es_estimacion": false,                      // req — true si fuente == "estimación propia" (el reporte lo marca con menos peso)
  "usado_en": ["automatizacion:a1", "roi"]     // opt — dónde se cita en el reporte
}
```

---

## 10. `automatizaciones` (req) — el top-3 diseñado

Array de exactamente las automatizaciones recomendadas (1-3), ordenadas por prioridad. **La sección estrella del reporte.**

```jsonc
{
  "id": "a1",                                  // req
  "rank": 1,                                   // req — 1 = la #1
  "proceso_id": "p1",                          // req — el proceso que resuelve
  "titulo": "Tu cotizador automático de WhatsApp",  // req — nombre vendible, en lenguaje de empleado/resultado
  "que_hace": "Un asistente que recibe el mensaje de quien quiere cotizar, le pregunta lo necesario (personas, fecha, tipo), y le manda la cotización lista en segundos, 24/7.",  // req — 1-2 frases, beneficio primero
  "metafora_empleado": "Como tener una recepcionista que cotiza sola, que nunca duerme y nunca se equivoca de precio.",  // opt — la metáfora "empleado" (resuena con el dataset)

  "arquitectura_simple": [                     // req — pasos en lenguaje NO técnico (3-6 pasos)
    "1. Llega un mensaje a tu WhatsApp pidiendo cotización",
    "2. El asistente lee qué necesita y pregunta lo que falte",
    "3. Calcula el precio con tu lista y arma la respuesta",
    "4. Se la manda al cliente al instante",
    "5. Te avisa a ti que entró un pedido grande"
  ],

  "herramientas": [                            // req — stack recomendado
    {
      "nombre": "WhatsApp API (Twilio)",       // req
      "para_que": "conectar tu WhatsApp",      // req
      "costo_mes_usd": 5,                      // req — número (0 si gratis)
      "costo_nota": "número + por conversación; servicio iniciado por el cliente es gratis",  // opt
      "fuente_precio": "https://chatarmin.com/en/blog/twilio-whats-app-api"  // opt — de research[]
    },
    { "nombre": "Cloudflare Workers", "para_que": "donde vive el asistente", "costo_mes_usd": 5, "costo_nota": "el patrón barato", "fuente_precio": "estimación propia" },
    { "nombre": "Claude/OpenAI API", "para_que": "el cerebro que redacta", "costo_mes_usd": 4, "costo_nota": "a tu volumen, <$5/mes", "fuente_precio": "https://openai.com/api/pricing/" }
  ],

  "encaja_con_stack": true,                    // req — true si reusa algo que ya tiene (D5)
  "complejidad": "media",                      // req — "baja" | "media" | "alta"
  "construible_por_usuario": true,             // req — ¿lo puede hacer él con Claude Code?

  "roi": {                                     // req — modelo §3 aplicado a ESTA automatización
    "horas_ahorradas_mes": 9.1,                // req
    "costo_hora_usd": 8,                        // req
    "valor_tiempo_mes_usd": 73,                // req — horas × costo_hora
    "ingreso_recuperado_mes_usd": 180,         // opt — null si no hay datos (NO inventar)
    "ingreso_supuesto": "Asumiendo que recuperas 1 de cada 5 pedidos grandes que hoy se enfrían (≈3/mes × $60).",  // opt — req si ingreso_recuperado != null
    "costo_tools_mes_usd": 14,                 // req — suma de herramientas[].costo_mes_usd
    "neto_mes_usd": 239,                       // req — (valor_tiempo + ingreso_recuperado) − costo_tools
    "factor_captura": 0.70,                    // req
    "factor_captura_nota": "De las ~13 h/mes que esto te come, recuperas ~9 reales; el resto sigue siendo revisar casos especiales."  // req — la honestidad del haircut
  },

  "es_agente_nube": true,                      // opt (legacy) — fallback de construir_con; true → claude_code
  "construir_con": "claude_code",              // req — ROUTER de herramienta: "n8n" | "make" | "n8n_o_make" (flujo de conectar apps)
                                               //       | "claude_code" (sistema/app/agente a la medida → /crear-agente) | "manual".
                                               //       Elige por FIT del trabajo, NO siempre Claude Code. Una mezcla es lo ideal.
  "construir_con_nota": null,                  // opt — override de la línea "cómo construir esto"; si null, se genera del construir_con
  "primer_paso": "Junta tu lista de precios y las 5 preguntas que siempre haces para cotizar."  // req — el primer paso concreto
}
```

---

## 11. `quick_win` (req) — la construible HOY

```jsonc
"quick_win": {
  "automatizacion_id": "a1",                   // req — apunta a una de automatizaciones[]
  "por_que_esta": "Es la que más sangras (la nombraste tú) y se puede tener funcionando hoy mismo.",  // req — justifica la elección (regla D4 / speed_to_value)
  "accion_hoy": "Pega este prompt en ChatGPT (o Claude) junto con tu lista de precios y desde hoy respondes cualquier cotización en segundos, sin instalar nada.",  // req — la promesa de UNA línea del quick-win: qué logra HOY
  "prompt": "Eres mi asistente de cotizaciones para [negocio]...\n\nMis precios y reglas:\n[PEGA AQUÍ TU LISTA]\n\nCuando te pase los datos, respóndeme con una cotización lista para copiar a WhatsApp...",  // req — EL ENTREGABLE ESTRELLA: el recurso copy-paste ejecutable HOY (un prompt listo, con [placeholders] que el usuario rellena). Es scope-neutral: automatiza SU negocio. El generador lo renderiza en un bloque de código copiable; sin él, el quick-win queda débil.
  "pasos_hoy": [                               // req — 3-5 pasos accionables para HOY (complementan al prompt: cómo usarlo/probarlo)
    "1. Junta tu lista de precios y las preguntas que siempre haces para cotizar",
    "2. Pega el prompt de arriba en ChatGPT y reemplaza [lo de corchetes] con tus datos reales",
    "3. Mándale una solicitud real y copia su respuesta a WhatsApp",
    "4. Cuando veas que cotiza bien, ese guion es la base para automatizarlo del todo (Fase 1 del plan)"
  ],
  "tiempo_estimado": "≈5 minutos",             // req
  "resultado_esperado": "Hoy mismo respondes cotizaciones en segundos copiando y pegando."  // req
}
```

---

## 12. `roi_global` (req) — el número headline + escenarios

```jsonc
"roi_global": {
  "horas_ahorradas_mes_total": 18.4,           // req — suma del top-3
  "ahorro_base_mes_usd": 312,                  // req — escenario base (§3.5)
  "escenarios": {                              // req — los 3 (§3.6)
    "conservador_usd": 198,                    // req
    "base_usd": 312,                           // req
    "optimista_usd": 470                       // req
  },
  "costo_total_mes_usd": 28,                    // req — suma herramientas top-3 + API
  "neto_mes_usd": 284,                          // req — base − costo
  "neto_anual_usd": 3408,                       // req — neto_mes × 12
  "roi_anual_x": 10.1,                          // req — (neto×12)/(costo×12)
  "payback": {                                  // opt — relevante si lo CONTRATA; ≈0 si lo construye él
    "dias": 0,                                  // opt
    "nota": "Si lo construyes tú con Claude Code, no hay costo de setup: recuperas desde el día 1."  // req si payback presente
  },
  "headline": "Recuperas ~18 h/mes ≈ $312 USD, por ~$28 de herramientas. Neto: ~$284/mes."  // req — la frase de portada
}
```

---

## 13. `roadmap_90_dias` (req) — 3 fases hacia la meta

Array de exactamente 3 fases (back-casting desde `meta_90_dias`).

```jsonc
{
  "fase": 1,                                    // req — 1 | 2 | 3
  "rango": "Días 1-30",                         // req
  "titulo": "Tu primer empleado digital",       // req
  "objetivo": "Montar el cotizador automático y dejar de perder tardes",  // req
  "acciones": [                                 // req — 2-4 acciones concretas
    "Construir el cotizador de WhatsApp (quick-win)",
    "Probarlo 1 semana y ajustar las respuestas",
    "Medir cuántas horas recuperaste"
  ],
  "automatizaciones_ref": ["a1"],               // opt — qué automatizaciones se montan en esta fase
  "hito": "Cotización respondida en <2 min, automático"  // req — el hito medible de la fase
}
```

---

## 14. `hand_off` (req) — sinergia con `/crear-agente`

```jsonc
"hand_off": {
  "ofrecer_construir": true,                    // req — true si la #1 es agente nube construible
  "automatizacion_id": "a1",                    // req — cuál se ofrece construir
  "skill_destino": "/crear-agente",             // req — "/crear-agente" | null
  "mensaje": "Tu automatización #1 es un agente que corre solo en la nube. ¿Quieres que lo construyamos ahora mismo? Te llevo paso a paso con /crear-agente — ya tengo todo el contexto de tu negocio.",  // req
  "contexto_precargado": {                      // opt — para que /crear-agente NO re-entreviste
    "que_automatizar": "asistente de WhatsApp que cotiza pedidos de eventos",
    "fuentes_datos": ["WhatsApp", "lista de precios"],
    "frecuencia": "evento (cada mensaje entrante)",
    "destino": "respuesta en WhatsApp + aviso a Marisol",
    "notificacion": "Pushover o WhatsApp"
  }
}
```

---

## 15. `supuestos_globales` (req)

Todos los supuestos que el reporte muestra explícitamente (la honestidad que da confianza).

```jsonc
"supuestos_globales": [
  "Tu hora la valoramos en ~$8 USD (default México). Si vale más, multiplica el ahorro.",
  "Aplicamos un factor de captura de 70% — la automatización no elimina el 100%, sigues revisando casos.",
  "Los ahorros de tiempo son lo más sólido; los ingresos recuperados son una estimación conservadora.",
  "Precios de herramientas verificados en junio 2026; pueden cambiar."
]
```

---

## 16. `cierre` (req) — mensaje final + CTA suave

```jsonc
"cierre": {
  "mensaje_segment": "Ya no estás dando vueltas entre tutoriales: esta es TU secuencia, en orden.",  // req — copy según segment
  "siguiente_paso": "Empieza por el quick-win hoy. Cuando lo tengas, vuelve y montamos la #2.",  // req
  "cta_comunidad": "Si quieres que te acompañe a construir las 3 — con gente que va en tu mismo camino — eso es justo lo que hacemos en Horizontes IA.",  // req — SUAVE, sin presión, sin countdown
  "cta_url": "https://www.skool.com/horizontes-ia-9992"  // req
}
```

---

## Notas finales para el generador

- **Orden de render**: portada (negocio + headline ROI) → reconocimiento (sangrado_declarado quote) → tabla de priorización (procesos) → las 3 automatizaciones (cards) → quick-win destacado → ROI global con 3 escenarios → roadmap 90 días (timeline) → hand-off (CTA construir) → supuestos (footer) → cierre.
- **Degradación con gracia**: si `automatizaciones` tiene 1-2 en vez de 3, render igual. Si `ingreso_recuperado_mes_usd == null`, omite esa línea y muestra solo el ahorro de tiempo. Si `research` solo trae estimaciones, no muestra el badge de "investigado".
- **Color/marca**: dark mode, acento cyan `#00E5FF`, bandas con sus colores (🟢🟡🟠⚪). Self-contained con CSS inline, imprimible a PDF (página A4/Letter, márgenes seguros, `@media print`).
- **El ejemplo completo lleno** vive en `ejemplo/diagnostico.json` (caso "Marisol / restaurante" usado aquí como referencia inline). Ese archivo es el que testea el generador.
