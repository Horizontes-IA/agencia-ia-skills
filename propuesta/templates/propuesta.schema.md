# `propuesta.json` — Contrato del documento (el que consume el generador)

> Este archivo define EXACTAMENTE qué necesita `scripts/generar_propuesta.mjs` para
> renderizar el HTML cliente-facing. Es el contrato. El generador renderiza SOLO lo que
> viene aquí — **no inventa nada** — y degrada con gracia: si una sección falta, la omite.
>
> Reglas:
> - Montos en **USD**, número (sin símbolo). `meta.moneda_display` controla cómo se muestra.
> - Listas vacías `[]` son válidas (se omite la sección).
> - Texto admite **markdown-lite**: `**negrita**` y saltos de línea `\n`.
> - NUNCA pongas un dato que no salió del diagnóstico o de la cotización o que el usuario no confirmó.

---

## Estructura completa

```jsonc
{
  "schema_version": "1.0",
  "meta": {
    "fecha": "2026-06-25",            // req — ISO
    "validez_dias": 14,               // req — vigencia (default 14, de la investigación)
    "moneda_display": "USD",          // req — "USD" | "MXN" | ...
    "generado_por": "/propuesta v1.0",
    "id": "prop-2026-06-25-<slug>"
  },

  "agencia": {                        // req — quién la manda (la agencia del usuario del skill)
    "nombre": "Nodo Automatización",  // req
    "tagline": "...",                 // opt — bajada de marca
    "contacto": "Nombre · email · wa.me/..."  // req — cómo lo contactan
  },

  "cliente": {                        // req — a quién va dirigida
    "nombre": "Marisol",              // req — persona
    "nombre_negocio": "Sabores de Casa",  // opt
    "contacto": "Marisol (dueña)"     // opt
  },

  "titulo": "Un asistente que cotiza tus eventos por ti, 24/7",  // req — promesa, no "Propuesta de servicios"
  "subtitulo": "Para que dejes de perder las tardes...",          // opt — en sus palabras

  // ── SECCIÓN 1: Resumen ejecutivo (el gancho de 30s — cierra solo) ──
  "resumen_ejecutivo": {              // req
    "parrafo": "Hoy **<negocio>** pierde ~X h/mes... Te proponemos...",  // req — dolor + costo + solución + entrega
    "kpis": [                         // opt — 2-3 números de portada (recupera del diagnóstico)
      { "valor": "~13 h", "etiqueta": "que recuperas al mes" }
    ],
    "costo_del_problema": "cada pedido que se enfría vale ~$60..."  // opt — el costo de NO actuar
  },

  // ── SECCIÓN 2: El problema EN SUS PALABRAS (lo que te separa) ──
  "problema": {                       // req
    "titulo": "El reto que estás viviendo hoy",
    "intro": "En el diagnóstico nos quedó claro dónde está el sangrado:",  // opt
    "cita_cliente": "Se me va la tarde contestando lo mismo...",  // opt — quote LITERAL (oro: de sangrado_declarado.frase_textual)
    "cita_fuente": "Marisol, en tu diagnóstico",                  // opt
    "puntos": [                       // opt — 2-4 puntos de dolor cuantificados
      { "titulo": "15 cotizaciones/semana, a mano", "detalle": "~12 min cada una..." }
    ]
  },

  // ── SECCIÓN 3: La solución como TRANSFORMACIÓN (3 fases) ──
  "solucion": {                       // req
    "titulo": "Cómo lo vamos a resolver",
    "intro": "No te entregamos una herramienta suelta: **un sistema que trabaja por ti**...",  // opt
    "fases": [                        // req — exactamente 3 (Descubrimiento → Construcción → Handoff)
      { "numero": 1, "nombre": "Descubrimiento y setup", "descripcion": "..." },
      { "numero": 2, "nombre": "Construcción y pruebas", "descripcion": "..." },
      { "numero": 3, "nombre": "Entrega y capacitación", "descripcion": "..." }
    ],
    "nota_confianza_ia": "**La IA aquí es una herramienta que controlamos, no una caja negra.** ..."  // req — ataca el trust gap de IA (privacidad + control humano)
  },

  // ── SECCIÓN 4: Entregables (formatos y cantidades específicas) ──
  "entregables": {                    // req
    "items": [                        // req — lista concreta (elimina ambigüedad)
      { "titulo": "Asistente de cotización en WhatsApp", "detalle": "..." }
    ],
    "revisiones": "1 ronda",          // opt — rondas incluidas (típico: 1)
    "fuera_de_alcance": [             // opt — qué NO incluye (previene scope creep)
      "Integración con facturación (se cotiza aparte)."
    ]
  },

  // ── SECCIÓN 5: Timeline semana por semana ──
  "timeline": {                       // req
    "intro": "De la firma a tu asistente funcionando, en 3 semanas:",  // opt
    "hitos": [                        // req — hitos con "cuando" + "titulo" + "detalle"
      { "cuando": "Semana 1", "titulo": "Setup y conexión", "detalle": "..." }
    ],
    "nota_pausa": "El reloj se pausa si no recibimos a tiempo X de tu lado..."  // opt — lenguaje protector anti-retraso
  },

  // ── SECCIÓN 6: Inversión (3 opciones — anclaje) ──
  "inversion": {                      // req — el envoltorio de la sección de precio
    "intro": "Tres formas de arrancar... La mayoría elige **Recomendado**.",  // opt
    "ancla_valor": "Si recuperas 3 pedidos/mes (~$180), se paga solo...",     // opt — ata el precio al costo del problema
    "nota_anticipo": "50% al firmar, 50% al entregar. Empezamos en 3 días hábiles."  // opt
  },
  "opciones": [                       // req — 3 tiers (Esencial / Recomendado / Completo)
    {
      "nombre": "Esencial",
      "para_quien": "Quiero solo X, rápido.",   // opt — para quién es
      "precio_usd": 1500,                        // req — número
      "precio_nota": "USD único",                // opt — sufijo del precio
      "incluye": ["...", "..."],                 // req — qué trae
      "pago": "50% al firmar / 50% al entregar", // opt
      "recomendada": false,                      // opt — true SOLO en el del medio (el target)
      "retainer_mes_usd": null                   // opt — mensualidad de soporte si aplica
    },
    { "nombre": "Recomendado", "recomendada": true, "precio_usd": 2500, "retainer_mes_usd": 150, "incluye": ["..."] },
    { "nombre": "Completo", "precio_usd": 4500, "retainer_mes_usd": 250, "incluye": ["..."] }
  ],

  // ── SECCIÓN 7: Prueba social (credibilidad) ──
  "prueba_social": {                  // opt — si no hay casos reales, omitir TODO (no inventar)
    "titulo": "Por qué confiar en nosotros",
    "intro": "...",                   // opt
    "casos": [                        // opt — casos con métrica concreta
      { "metrica": "60% menos tiempo", "texto": "...", "fuente": "Cliente repostería, CDMX" }
    ],
    "logos": ["WhatsApp Business", "Cloudflare", "OpenAI"]  // opt — tech/marcas de confianza
  },

  // ── SECCIÓN 8: Sobre la agencia (al FINAL a propósito) ──
  "sobre_agencia": {                  // req
    "parrafo": "Somos una agencia enfocada en... entregamos sistemas que funcionan...",  // req
    "herramientas": ["Claude", "OpenAI", "WhatsApp API", "Cloudflare", "n8n"]  // opt
  },

  // ── Términos clave (resumen; el contrato completo es otro skill) ──
  "terminos": {                       // opt
    "items": [
      { "titulo": "Propiedad", "detalle": "al pagar el total, el sistema es 100% tuyo." }
    ]
  },

  // ── CTA: siguiente paso (máx 3 pasos + urgencia suave) ──
  "cta": {                            // req
    "titulo": "Para empezar",
    "pasos": [                        // req — MÁX 3 pasos numerados
      "Confirma qué opción prefieres.",
      "Te mando el acuerdo de alcance y el link de pago del anticipo.",
      "Con el anticipo, arrancamos en <3 días hábiles."
    ],
    "boton_label": "Agendar 15 min para revisarla",  // opt — re-enganche de baja fricción
    "boton_url": "https://cal.com/...",               // opt — link de calendario
    "urgencia": "Precios válidos por 14 días...",     // opt — urgencia SUAVE (validez), nunca falsa
    "contacto": "¿Dudas? Escríbeme: **email** o **wa.me/...**"  // opt
  }
}
```

---

## De dónde sale cada campo (mapeo desde `diagnostico.json`)

| Campo de propuesta.json | Fuente en diagnostico.json |
|---|---|
| `cliente.nombre`, `cliente.nombre_negocio` | `negocio.nombre_persona`, `negocio.nombre_negocio` |
| `titulo`, `subtitulo` | `automatizaciones[0].titulo` + `meta_90_dias.objetivo` |
| `resumen_ejecutivo.kpis` | `roi_global.horas_ahorradas_mes_total`, `automatizaciones[0].roi` |
| `resumen_ejecutivo.costo_del_problema` | `sangrado_declarado.que_pierde_dinero` + ROI |
| `problema.cita_cliente` | `sangrado_declarado.frase_textual` (LITERAL — el oro del reconocimiento) |
| `problema.puntos` | `procesos[]` top + `score_rationale` |
| `solucion.fases` | metodología estándar (Descubrimiento → Construcción → Handoff) |
| `entregables.items` | `automatizaciones[].arquitectura_simple` + `que_hace` |
| `opciones[].precio_usd` | `automatizaciones[].valor_si_lo_vendes_usd` (ancla los 3 tiers a ese rango) |
| `inversion.ancla_valor` | `roi_global` / `automatizaciones[].roi.ingreso_recuperado_mes_usd` |
| `sobre_agencia.herramientas` | `automatizaciones[].herramientas[].nombre` |

> Si NO existe `diagnostico.json`, el skill levanta estos datos con un mini-cuestionario (ver SKILL.md, Fase 1B). Nunca inventa cifras de ROI ni precios.
