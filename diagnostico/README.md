# 🩺 Diagnóstico — Skill para Claude Code

> Un consultor de IA que entrevista un negocio en unos minutos y entrega un paquete de consultoría premium: qué automatizar primero, cuánto tiempo y dinero recupera, y un plan a 90 días — con el nombre del negocio, listo para descargar.

Forma parte de **[agencia-ia-skills](../README.md)**. Es la pieza de **diagnóstico**: arranca el flujo entendiendo el negocio y detectando qué conviene automatizar adentro. (El papeleo de vender — cotizar, proponer, contratar, cobrar — lo cubren los otros skills del repo: `/cotizacion`, `/propuesta`, `/contrato`, `/cobro`, `/cerrar-cliente`.)

---

## ¿Qué hace este skill?

Escribes `/diagnostico` y Claude entrevista el negocio como lo haría un consultor que cobra un par de miles de dólares — una pregunta a la vez, en español, sin tecnicismos. Con las respuestas encuentra **qué es lo que más tiempo o dinero está costando**, qué automatizar primero y cómo, y cuánto tiempo/dinero regresa eso. Al final arma un **reporte premium con el nombre del negocio** que se descarga, imprime a PDF y se guarda — y si se quiere, **construye la automatización #1 ahí mismo**. No es un texto genérico de IA: es reconocerse ("esto es MI negocio, no un ejemplo") y ver el número ("recupero ~18 horas al mes ≈ $312 USD"). Eso es el wow.

**Alcance:** este skill diagnostica el negocio (qué automatizar adentro y cuánto ahorra/recupera). **No** cubre cómo vender automatizaciones a terceros, montar una agencia ni conseguir clientes — para eso están los otros skills del repo.

**Para quién:** dueños de negocios y gente que está arrancando su propio negocio o emprendimiento y siente que tiene "un desorden de mil tutoriales y no avanza". Si no sabe por dónde empezar, este skill es justo el orden que falta. **No hace falta saber programar** ni tener nada montado todavía.

---

## 📦 ¿Qué genera? (el paquete de consultoría)

Al terminar la entrevista, el skill genera el expediente `cliente-<negocio>/1-diagnostico/` con:

| Archivo | Qué es |
|---|---|
| **`reporte.html`** ⭐ | El diagnóstico completo, visual y premium. Se abre con doble clic. Para PDF: `Cmd/Ctrl + P → Guardar como PDF`. |
| `04-quick-win.md` ⭐ | Algo que se puede **usar HOY mismo, en 5 minutos**, sin instalar nada. La acción chica y ganable contra "no sé por dónde empezar". |
| `01-procesos-y-roi.md` | Los 3 procesos a automatizar, rankeados, con números: cuánto tiempo roban y cuánto se recupera. |
| `02-plan-90-dias.md` | La ruta mes a mes hacia la meta a 90 días, con un hito medible por fase. |
| `03-stack-recomendado.md` | Las herramientas exactas, con costo real (muchas gratis). Pensado para arrancar con poco. |
| `README.txt` | 3 líneas que dicen por dónde empezar. |

Dentro del reporte: el negocio en portada, la tabla de procesos priorizados (🟢 automatiza ya / 🟡 después / ⚪ no urgente), las **3 automatizaciones que más mueven la aguja** (qué hacen, herramientas, costo, cuánto ahorran), el **quick-win marcado como "EMPIEZA POR AQUÍ"**, el ROI con 3 escenarios, y el plan a 90 días. Todo en dark mode con acento cyan, todos los números con sus supuestos a la vista — un diagnóstico que se puede defender.

---

## 🚀 Instalación

Se instala junto con el resto del repo (ver el [README principal](../README.md)):

```bash
curl -fsSL https://raw.githubusercontent.com/Horizontes-IA/agencia-ia-skills/main/instalar.sh | bash
```

> ¿A mano? Copia esta carpeta `diagnostico/` a `~/.claude/skills/diagnostico/`.

Necesitas **Claude Code** (https://claude.com/code) y **Python 3** (Mac y Linux ya lo traen; en Windows desde https://python.org — y aunque no lo tengas, el skill genera el reporte igual con su fallback).

---

## 📖 Cómo usar

```
1. Abre Claude Code (cualquier proyecto) y escribe:  /diagnostico
2. Contesta las preguntas — una por una, sin prisa.
3. Cuando tenga lo suficiente, te confirma lo que entendió y arranca.
4. Recibes el paquete: abre reporte.html y empieza por 04-quick-win.md hoy mismo.
```

También se activa en lenguaje natural:

> *"diagnostica mi negocio"* · *"diagnostica este negocio"* · *"qué puedo automatizar"* · *"¿por dónde empiezo con la IA en mi negocio?"*

---

## 🤝 Y si se quiere construir la automatización #1…

El reporte no se queda en el papel. Si la automatización más importante es un asistente que corre solo en la nube (ej. "el que responde las cotizaciones 24/7, como un empleado que no duerme"), el skill ofrece **construirlo en el momento** — y le pasa la batuta al skill `/crear-agente`, que ya recibe todo el contexto del negocio para no volver a entrevistar. Se pasa de "me diagnosticaron" a "ya tengo algo funcionando".

---

## 🧠 ¿De dónde sale tan buen diagnóstico?

El skill no improvisa: entrevista como consultor senior (una pregunta a la vez, reflejando lo que se dice), rankea los procesos con una fórmula real de impacto vs. esfuerzo, investiga precios y benchmarks de la industria en internet, y calcula el ROI de forma **conservadora y defendible** — cada número viaja con su supuesto a la vista. Nada inflado.

---

*Hecho por [Horizontes IA](https://www.skool.com/horizontes-ia-9992) — academia de IA y automatización en español para LATAM.*
