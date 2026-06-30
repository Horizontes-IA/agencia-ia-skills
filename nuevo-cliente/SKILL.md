---
name: nuevo-cliente
description: La PUERTA DE ENTRADA del kit de agencia con IA — un solo skill que arma todo para un cliente sin que tengas que recordar los demás. Dile "nuevo cliente", dale la info que tengas del cliente (toda, la básica, o nada) y qué necesitas (el kit completo, solo el paquete de venta, solo el cierre, o una sola pieza), y este skill te hace las preguntas que falten y encadena los skills correctos en orden: /diagnostico → /cotizacion → /propuesta → /contrato → /cobro → /conectar-cliente. Es inteligente con los candados: NO le genera contrato ni cobro a un prospecto que todavía no ha cerrado. Úsalo cuando alguien escriba "/nuevo-cliente", "nuevo cliente", "arma el kit de [cliente]", "quiero generar el kit", "genérame todo para [cliente]", "tengo un cliente nuevo", "empecemos con [cliente]", "arma todo para [negocio]", o incluso pidiendo una sola pieza ("solo la cotización de [cliente]", "hazme el diagnóstico de [negocio]"). Acepta info incompleta: con lo que tengas, pregunta lo mínimo y genera lo que se pueda. Todo sale con la marca del usuario (de su perfil) y en PDF, junto en una carpeta `cliente-<negocio>/`. Español neutro LATAM, friendly para cualquier nivel. Reusa los skills existentes, no los reimplementa.
---

# Nuevo Cliente — Skill `/nuevo-cliente`

**El punto de entrada del kit.** En vez de que el usuario recuerde 7 skills, dice *"nuevo cliente, arma el kit de Sabores de Casa"* y este skill se encarga: junta lo que ya tenga, pregunta lo que falte (poquito y una a una), y **encadena los skills correctos en el orden correcto** — entregando todo con su marca, en PDF, en una sola carpeta.

> **No reimplementa nada.** Orquesta los skills que ya existen (`/diagnostico`, `/cotizacion`, `/propuesta`, `/contrato`, `/cobro`, `/conectar-cliente`) leyendo su `SKILL.md` y siguiendo su pipeline. Para el **cierre completo** (cotización→cobro→accesos→kickoff) **delega en `/cerrar-cliente`**, que ya orquesta esa cadena. Este skill agrega lo de "antes de cerrar" (diagnóstico + venta) y la inteligencia de **cuánto generar según el punto del trato y la info que haya**.

## ⚙️ Fase 0 — Perfil de tu agencia (auto-config, una sola vez)

- Si **NO existe** `~/.config/agencia-ia/perfil.json` → lee `~/.config/agencia-ia/configurar.md` y corre el onboarding (unas preguntas amigables, guarda el perfil). **Solo la primera vez.**
- Si **SÍ existe** → cárgalo y NO vuelvas a preguntar. Todos los sub-skills lo reusan → todo sale con la marca, color, precios y forma de cobrar del usuario.
- Para reconfigurar: "configura mi agencia" → re-corre `configurar.md`.

---

## Cuándo invocar / cuándo NO

**SÍ:** *"/nuevo-cliente"*, *"nuevo cliente"*, *"arma el kit de [cliente]"*, *"quiero generar el kit"*, *"genérame todo para [negocio]"*, *"tengo un cliente nuevo"*, *"empecemos con [cliente]"*, y también pedidos de UNA pieza (*"solo la cotización de [cliente]"*, *"hazme el diagnóstico de [negocio]"*) — en ese caso solo corres esa pieza.

**NO (o redirige):** si ya pasó el cierre y quiere **construir/entregar/mantener** → `/crear-agente` → `/docs-entrega` → `/mantenimiento`. Si quiere **reconfigurar su agencia** → "configura mi agencia".

---

## Fase 1 — Entender qué necesitas (lo MÍNIMO, adaptativo)

Abre cálido y pregunta solo lo que no esté claro de lo que el usuario ya dijo. **Si ya te dio algo, no lo vuelvas a preguntar.** Necesitas resolver 3 cosas (en lenguaje normal, una a una):

**1. ¿Qué cliente y en qué punto estás con él?** → define cuánto generar:
- **Apenas lo conociste / es un prospecto** → arrancas por el **diagnóstico** (para engancharlo) y el **paquete de venta**.
- **Ya lo quiere, falta cerrar** → **cotización + propuesta** (lo que cierra).
- **Ya te dijo que sí / ya cerró** → el **cierre completo** (contrato, cobro, accesos) — eso lo corre `/cerrar-cliente`.

**2. ¿Qué quieres que arme?**
- **"Todo el kit"** → la cadena completa que aplique según el punto del trato (ver §El mapa).
- **Solo una pieza** ("solo la cotización", "solo el contrato") → corres ese skill directo.

**3. ¿Qué info tienes del cliente?** Acepta lo que sea:
- **Toda / un brief** → úsala para no preguntar de más.
- **Lo básico** (nombre del negocio, a qué se dedica, su dolor) → suficiente para arrancar.
- **Nada** → no pasa nada: el **diagnóstico entrevista** y de ahí sale todo. Solo dile *"cuéntame del cliente como si me lo platicaras"*.

> **Regla de oro: la cantidad de preguntas depende de la info.** Con un brief completo, casi no preguntas. Con nada, la entrevista del diagnóstico hace el trabajo. **Nunca pidas más de lo necesario para el siguiente paso**, y nunca te trabes por un dato menor (márcalo `[revisar]` y sigue).

Cuando tengas claras las 3, **confirma en una línea** lo que vas a hacer y arranca:
> *"Va: [cliente] es un prospecto nuevo y quieres el kit completo. Empiezo por el diagnóstico (te hago unas preguntas del negocio), y con eso armo la cotización y la propuesta para que se lo mandes y cierre. El contrato y el cobro los dejo para cuando te diga que sí. ¿Le entro?"*

---

## El mapa de decisión (qué generar según el punto del trato)

| Punto del trato | Qué genera el kit | Cómo |
|---|---|---|
| **Prospecto nuevo** (apenas, o sin info) | **Diagnóstico** → (con su OK) **Cotización** → **Propuesta** | el paquete para enganchar y cerrar |
| **Ya lo quiere, falta cerrar** | **Cotización** → **Propuesta** (+ diagnóstico si no hay, para fundamentar) | lo que gana la decisión |
| **Ya cerró** ("me dijo que sí") | **Contrato** → **Cobro (anticipo)** → **Conectar cuentas** → **Kickoff** | delega en **`/cerrar-cliente`** |
| **Una sola pieza** | solo esa | corre ese skill directo |

**"Todo el kit" para un prospecto nuevo = el paquete de PRE-VENTA** (diagnóstico + cotización + propuesta). El **contrato y el cobro NO se generan todavía** (candado, ver abajo) — quedan a un comando de distancia para cuando cierre.

---

## Los candados (para no sacar documentos de aire)

1. **No contratas ni cobras a quien no ha cerrado.** Contrato y cobro solo cuando el usuario confirme que el cliente **dijo que sí**. Si está en venta, paras en la propuesta y le dices: *"cuando te diga que sí, vuelve y con un 'ya cerré a [cliente]' corro el contrato, el cobro y los accesos."*
2. **El diagnóstico va antes de poner precio.** Si no hay diagnóstico ni info, no inventes el alcance ni el precio: corre el diagnóstico (entrevista) primero.
3. **El anticipo va antes de construir/conectar** (lo respeta `/cerrar-cliente`).
4. **Checkpoint antes de la cadena larga.** Si vas a generar varias piezas, resume el plan y pide un OK una sola vez (no interrumpas en cada documento).

---

## Cómo lo ejecuta (orquestación)

Igual que `/cerrar-cliente`: **lee el `SKILL.md` del sub-skill y sigue su pipeline**, reusando el contexto para no re-preguntar, y manda toda la salida a la **carpeta del cliente** `cliente-<slug>/`. Los skills viven en `/Users/santiagomunoz/Documents/agencia-ia-skills/<skill>/SKILL.md` (y `/conectar-cliente` en `~/.claude/skills/conectar-cliente/`).

- **Diagnóstico:** `Read .../diagnostico/SKILL.md` y sigue su pipeline. Si el usuario dio info, pre-llénala; lo que falte, la entrevista lo saca. Salida → `cliente-<slug>/` (renombra `diagnostico-*/` a la carpeta del cliente).
- **Venta (cotización + propuesta):** corre `/cotizacion` y luego `/propuesta` (la propuesta reusa la cotización). Heredan el diagnóstico → no re-preguntan.
- **Cierre completo (ya cerró):** **delega en `/cerrar-cliente`** — `Read .../cerrar-cliente/SKILL.md` y sigue su flujo (él ya encadena cotización→propuesta→contrato→cobro→conectar→kickoff y consolida la carpeta). No dupliques su lógica.
- **Una pieza:** corre solo ese `SKILL.md`.
- **PDF automático:** cada sub-skill ya genera su PDF con `~/.config/agencia-ia/html2pdf.py`. No tienes que hacer nada extra.

---

## Fase final — Entregar + decir qué sigue

Entrega la carpeta con los **datos reales** (no genéricos) y un mini-plan de **qué mandar y cuándo**. Ejemplo (prospecto nuevo, paquete de venta):

```
Listo. Armé el kit de venta de [cliente] en `cliente-[slug]/`:
  • reporte-diagnostico.html  ← mándaselo PRIMERO (lo engancha: ve su problema y el ahorro)
  • cotizacion.html           ← las 3 opciones de precio
  • propuesta.html            ← el documento que cierra

Cómo usarlo:
  1. Manda el diagnóstico (o preséntaselo). Es lo que hace que te tome en serio.
  2. Si muestra interés → manda la propuesta con las 3 opciones.
  3. En cuanto te diga que sí → vuelve y dime "ya cerré a [cliente]":
     corro el contrato, el cobro del anticipo y los links para conectar sus cuentas.

(Todo salió con tu marca y en PDF — solo abre, revisa y manda.)
```

Si ya cerró, el resumen lo da `/cerrar-cliente` (el expediente completo). Indica SIEMPRE rutas absolutas y cómo abrir el PDF según el OS.

---

## Reglas duras (las 8)

1. **Una puerta, cero comandos que memorizar.** El usuario habla normal; tú ruteas al skill correcto.
2. **Adaptativo a la info.** Con brief completo casi no preguntas; con nada, la entrevista del diagnóstico trabaja. Pide solo lo del siguiente paso.
3. **Orquesta, no reimplementes.** Corre el `SKILL.md` de cada sub-skill; para el cierre, delega en `/cerrar-cliente`.
4. **Respeta los candados.** Nada de contrato/cobro sin cierre; nada de precio sin diagnóstico/info.
5. **Una sola vez.** Datos de la agencia (perfil) y del cliente (diagnóstico) se reusan en todo. No re-preguntes.
6. **Todo junto en `cliente-<slug>/`**, con marca y PDF.
7. **NUNCA pushy.** Sin countdowns ni "cupos". La única urgencia válida es la vigencia de la cotización.
8. **No te trabes.** Falta un dato → márcalo `[revisar]` y sigue. Falta Python/Node → el sub-skill tiene su fallback. El usuario nunca se queda sin entregable.

---

## Integración con la suite

`/nuevo-cliente` (puerta de entrada) → orquesta **`/diagnostico`**, **`/cotizacion`**, **`/propuesta`**, y delega el cierre en **`/cerrar-cliente`** (que a su vez corre `/contrato`, `/cobro`, `/conectar-cliente` + kickoff). Después del cierre, el hand-off downstream es `/crear-agente` → `/docs-entrega` → `/mantenimiento`. Todo se autoconfigura con `~/.config/agencia-ia/perfil.json`.
