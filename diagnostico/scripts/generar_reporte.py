#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_reporte.py — Generador del paquete de diagnóstico de Horizontes IA.

Consume un `diagnostico.json` (esquema canónico en _design/schema.md) y escribe,
en <output_dir>, el paquete completo:

    reporte.html              ← el artefacto WOW (self-contained, claro + acento, imprime a PDF)
    01-procesos-y-roi.md
    02-plan-90-dias.md
    03-stack-recomendado.md
    04-quick-win.md
    README.txt

Uso:
    python3 scripts/generar_reporte.py <diagnostico.json> <output_dir>

Reglas de diseño (cero dependencias):
- Python SOLO stdlib. Corre igual en Mac/Win/Linux.
- HTML con TODO el CSS inline en un <style>, fuentes vía @import con fallback
  a system-ui, logo SVG inline. Cero assets externos, cero JS.
- El generador NUNCA inventa datos: si un campo opcional falta, omite la sección
  o usa un fallback declarado. Recalcula los totales del lado del servidor
  (no confía en que la IA sume bien).
- Premium SIN pushy: nada de countdowns ni "oferta limitada".
"""

import sys
import os
import json
import html
import datetime


# ─────────────────────────────────────────────────────────────────────────────
# 0. UTILIDADES DE DATOS Y FORMATO
# ─────────────────────────────────────────────────────────────────────────────

def die(msg):
    """Imprime un error claro a stderr y sale con código 1."""
    sys.stderr.write("❌ " + msg + "\n")
    sys.exit(1)


def esc(s):
    """Escapa texto que viene del JSON (input de usuario/IA) antes de inyectarlo
    al HTML. OBLIGATORIO para todo string dinámico — el nombre del negocio o un
    quote del usuario pueden traer < > & " que rompan el documento."""
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


def get(d, path, default=None):
    """Acceso seguro a campos anidados con notación 'a.b.c'. Devuelve `default`
    si cualquier eslabón falta — la degradación con gracia del contrato."""
    cur = d
    for key in path.split("."):
        if isinstance(cur, dict) and key in cur and cur[key] is not None:
            cur = cur[key]
        else:
            return default
    return cur


def money(n):
    """Formatea un monto USD legible: 152 -> '$152', 3408 -> '$3,408'. None -> ''."""
    if n is None:
        return ""
    try:
        n = float(n)
    except (TypeError, ValueError):
        return ""
    # Sin decimales para montos enteros, con coma de miles.
    if abs(n - round(n)) < 0.01:
        return "${:,}".format(int(round(n)))
    return "${:,.2f}".format(n)


def hrs(n):
    """Formatea horas: 9.1 -> '9.1 h', 19.0 -> '19 h'. None -> ''."""
    if n is None:
        return ""
    try:
        n = float(n)
    except (TypeError, ValueError):
        return ""
    if abs(n - round(n)) < 0.05:
        return "{} h".format(int(round(n)))
    return "{:.1f} h".format(n)


def fecha_larga(iso):
    """'2026-06-23' -> '23 de junio de 2026'. Si no parsea, devuelve el string crudo."""
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    try:
        dt = datetime.date.fromisoformat(iso)
        return "{} de {} de {}".format(dt.day, meses[dt.month - 1], dt.year)
    except (ValueError, TypeError):
        return str(iso or "")


# Etiquetas de banda (score → veredicto visual). Coherentes con framework.md §2.
BANDA_INFO = {
    "automatiza_ya":  ("🟢", "Automatiza ya", "good"),
    "alto_potencial": ("🟡", "Alto potencial", "warn"),
    "mas_adelante":   ("🟠", "Más adelante", "orange"),
    "no_prioritario": ("⚪", "No prioritario", "dim"),
}


def banda_por_score(score):
    """Fallback: deriva la banda desde el score si el JSON no la trae."""
    if score >= 75:
        return "automatiza_ya"
    if score >= 55:
        return "alto_potencial"
    if score >= 35:
        return "mas_adelante"
    return "no_prioritario"


# Copys de encuadre por segmento (framework.md §6). El generador elige según `segment`.
SEGMENT_COPY = {
    "beginner": {
        "subtitulo": "Tu secuencia ordenada para dejar de saltar entre tutoriales — y dar el primer paso real hoy.",
        "resumen_cierre": "Deja de dar vueltas: esta es TU ruta, en orden, una cosa a la vez.",
    },
    "operator": {
        "subtitulo": "Un mapa para que tu negocio empiece a trabajar solo — como contratar a tu primer empleado digital.",
        "resumen_cierre": "Es hora de contratar procesos, no personas: tu primer empleado digital empieza por aquí.",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# 1. LOGO SVG INLINE (Horizontes IA) — mark geométrico cyan "horizonte + sol"
# ─────────────────────────────────────────────────────────────────────────────

def logo_svg(size=28):
    """Logo inline limpio: una línea de horizonte con un sol/arco cyan. Sin assets."""
    return (
        '<svg width="{s}" height="{s}" viewBox="0 0 48 48" fill="none" '
        'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<circle cx="24" cy="21" r="9" stroke="#00E5FF" stroke-width="2.5"/>'
        '<path d="M6 34 H42" stroke="#00E5FF" stroke-width="2.5" stroke-linecap="round"/>'
        '<path d="M13 40 H35" stroke="#22d3ee" stroke-width="2.5" stroke-linecap="round" opacity="0.6"/>'
        '</svg>'
    ).format(s=size)


# ─────────────────────────────────────────────────────────────────────────────
# 1b. MARCA DE LA AGENCIA (del perfil compartido) — el reporte sale con SU marca
# ─────────────────────────────────────────────────────────────────────────────

def cargar_marca():
    """Lee la marca de la agencia de ~/.config/agencia-ia/perfil.json (si existe).
    Devuelve nombre, color de acento, logo y contacto, con fallback a Horizontes IA."""
    base = {
        "nombre": "Horizontes IA",
        "color": None,
        "logo_url": None,
        "contacto": None,
        "tiene_perfil": False,
    }
    path = os.path.expanduser("~/.config/agencia-ia/perfil.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            p = json.load(f)
    except Exception:
        return base
    ag = p.get("agencia", {}) or {}
    marca = p.get("marca", {}) or {}
    persona = p.get("persona", {}) or {}
    color = (marca.get("color_acento") or "").strip() or None
    base.update({
        "nombre": ag.get("nombre_marca") or base["nombre"],
        "color": color if (color and len(color) == 7 and color[0] == "#") else None,
        "logo_url": (marca.get("logo_url") or "").strip() or None,
        "contacto": (persona.get("web") or persona.get("whatsapp") or persona.get("email") or "").strip() or None,
        "tiene_perfil": True,
    })
    return base


def logo_html(marca, size=28):
    """Logo de la agencia: su imagen si dio logo_url, si no el SVG inline."""
    url = (marca or {}).get("logo_url")
    if url:
        return ('<img src="{u}" alt="logo" height="{s}" '
                'style="height:{s}px;width:auto;display:block" />').format(u=html.escape(url, quote=True), s=size)
    return logo_svg(size)


def recolorear_html(s, hex_color):
    """Reemplaza el cyan de Horizontes por el color de acento de la agencia en TODO
    el HTML (variables CSS + literales rgba). Si no hay color válido, deja el cyan."""
    if not hex_color or len(hex_color) != 7 or hex_color[0] != "#":
        return s
    try:
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    except ValueError:
        return s
    rgb = "{},{},{}".format(r, g, b)
    # Texto sobre el acento: blanco si el acento es oscuro, tinta oscura si es claro.
    if (0.299 * r + 0.587 * g + 0.114 * b) < 150:
        s = s.replace("--on-accent:#15181e", "--on-accent:#ffffff")
    for lit in ("#00E5FF", "#00e5ff", "#22d3ee", "#22D3EE", "#00B8CC", "#00b8cc", "#0e7490", "#0E7490", "#06808f", "#06808F", "#0aa6bd", "#0AA6BD"):
        s = s.replace(lit, hex_color)
    s = s.replace("0,229,255", rgb).replace("0, 229, 255", rgb).replace("0,184,204", rgb).replace("0, 184, 204", rgb)
    return s


# ─────────────────────────────────────────────────────────────────────────────
# 2. CÁLCULOS SERVER-SIDE (no confiar en que la IA sume — recalcular)
# ─────────────────────────────────────────────────────────────────────────────

def derivar_totales(diag):
    """Recalcula los KPIs y la tabla de ROI sumando automatizaciones[].

    Las cifras DURAS (horas, ahorro, costo, neto, ROI) son AUTORITATIVAS desde las
    filas — NO se confía en `roi_global` para ellas. La IA puede modelar un total
    que no cuadre con la suma de las filas y eso es el peor error posible en un
    reporte cuya promesa es "conservador y defendible": el usuario hace la resta en
    2 segundos y pierde la confianza. Aquí el total SIEMPRE = suma de las filas.
    De `roi_global` solo tomamos lo narrativo (escenarios, headline, payback)."""
    autos = diag.get("automatizaciones", []) or []

    horas_total = 0.0
    valor_tiempo_total = 0
    ingreso_total = 0
    costo_tools_total = 0
    for a in autos:
        roi = a.get("roi", {}) or {}
        horas_total += roi.get("horas_ahorradas_mes") or 0
        valor_tiempo_total += roi.get("valor_tiempo_mes_usd") or 0
        ingreso_total += roi.get("ingreso_recuperado_mes_usd") or 0
        costo_tools_total += roi.get("costo_tools_mes_usd") or 0

    horas_total = round(horas_total, 1)
    ahorro_total = valor_tiempo_total + ingreso_total   # tiempo recuperado + ingreso recuperado
    neto = ahorro_total - costo_tools_total
    neto_anual = neto * 12
    costo_anual = costo_tools_total * 12

    rg = diag.get("roi_global", {}) or {}
    # ROI anual sobre el costo de herramientas; si el costo es ~0, no es divisible → usa roi_global.
    roi_x = round(neto_anual / costo_anual, 1) if costo_anual > 0 else rg.get("roi_anual_x")

    # Si roi_global contradice la suma de las filas, avisamos (no rompe) y ganan las filas.
    rg_neto = rg.get("neto_mes_usd")
    if rg_neto is not None and abs(rg_neto - neto) > 1:
        sys.stderr.write(
            "⚠️  roi_global.neto_mes_usd={} no cuadra con la suma de filas (${}). "
            "Uso la suma de filas (autoritativa).\n".format(rg_neto, neto))

    return {
        "horas_total": horas_total,
        "valor_tiempo_total": valor_tiempo_total,
        "ingreso_total": ingreso_total,
        "ahorro_total": ahorro_total,        # el número grande, real (tiempo + ingreso)
        "ahorro_base": valor_tiempo_total,   # solo tiempo (referencia interna)
        "costo_total": costo_tools_total,
        "neto_mes": neto,
        "neto_anual": neto_anual,
        "roi_anual_x": roi_x,
        "escenarios": rg.get("escenarios", {}),
        "headline": rg.get("headline"),
        "payback": rg.get("payback", {}),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 3. COMPONENTES HTML (helpers que devuelven fragmentos)
# ─────────────────────────────────────────────────────────────────────────────

def section_header(titulo, sub=None):
    s = '<header class="sec-head"><h2>{}</h2><span class="rule"></span>'.format(esc(titulo))
    if sub:
        s += '<p class="sec-sub">{}</p>'.format(esc(sub))
    s += '</header>'
    return s


def kpi_card(numero, label, contexto=None):
    ctx = '<p class="kpi-ctx">{}</p>'.format(esc(contexto)) if contexto else ""
    return (
        '<div class="kpi-card">'
        '<div class="kpi-num">{num}</div>'
        '<div class="kpi-label">{lab}</div>{ctx}'
        '</div>'
    ).format(num=esc(numero), lab=esc(label), ctx=ctx)


def verdict_badge(banda):
    icon, label, cls = BANDA_INFO.get(banda, BANDA_INFO["no_prioritario"])
    return '<span class="badge badge-{cls}">{icon} {label}</span>'.format(
        cls=cls, icon=icon, label=esc(label))


def score_bar(proc):
    """Fila de proceso: nombre + badge + barra de score + meta-línea con cita."""
    nombre = esc(proc.get("nombre", "Proceso"))
    score = int(proc.get("score", 0))
    banda = proc.get("banda") or banda_por_score(score)

    # Meta-línea: horas/sem · frecuencia textual · cita del dolor.
    freq_sem = proc.get("frecuencia_veces_semana")
    tiempo_vez = proc.get("tiempo_por_vez_min")
    horas_sem = None
    if freq_sem and tiempo_vez:
        horas_sem = round((freq_sem * tiempo_vez) / 60, 1)

    meta_bits = []
    if horas_sem:
        meta_bits.append('{}/sem'.format(hrs(horas_sem)))
    if freq_sem:
        meta_bits.append('{}× por semana'.format(int(freq_sem)))
    cita = proc.get("descripcion_usuario") or proc.get("score_rationale")
    meta_line = " · ".join(esc(b) for b in meta_bits)
    cita_html = '<span class="proc-quote">“{}”</span>'.format(esc(cita)) if cita else ""

    flagged = ('<span class="proc-flag" title="Tú nombraste esta tarea">'
               '★ la nombraste tú</span>') if proc.get("user_flagged") else ""

    return (
        '<div class="score-bar">'
        '<div class="score-bar-top">'
        '<h3 class="proc-name">{nombre}{flag}</h3>{badge}'
        '</div>'
        '<div class="track"><div class="fill" style="width:{score}%"></div>'
        '<span class="score-num">{score}<small>/100</small></span></div>'
        '<p class="proc-meta">{meta}{sep}{cita}</p>'
        '</div>'
    ).format(
        nombre=nombre, flag=flagged, badge=verdict_badge(banda),
        score=score, meta=meta_line,
        sep=' · ' if (meta_line and cita_html) else '',
        cita=cita_html,
    )


def arch_chain(pasos):
    """Cadena de arquitectura: pills conectados por flechas cyan (no diagrama técnico).
    Limpia el prefijo numérico '1. ' de cada paso para que el chip se vea limpio."""
    chips = []
    for p in pasos:
        txt = str(p).strip()
        # quitar '1. ', '2) ' etc del inicio
        for sep in [". ", ") ", "- ", "  "]:
            if len(txt) > 3 and txt[0].isdigit() and txt[1:3].startswith(sep[:2]):
                txt = txt.split(sep, 1)[-1].strip()
                break
        if txt and txt[0].isdigit() and ". " in txt[:4]:
            txt = txt.split(". ", 1)[-1].strip()
        chips.append('<span class="arch-step">{}</span>'.format(esc(txt)))
    return '<div class="arch-chain">' + '<span class="arch-arrow">→</span>'.join(chips) + '</div>'


def tool_chip(nombre):
    return '<span class="tool-chip">{}</span>'.format(esc(nombre))


def cost_badge(valor):
    """Badge de costo: 0 -> 'GRATIS' (verde), n -> '$n/mes' (muted)."""
    try:
        v = float(valor)
    except (TypeError, ValueError):
        return '<span class="cost-badge">{}</span>'.format(esc(valor))
    if v <= 0:
        return '<span class="cost-badge cost-free">GRATIS</span>'
    return '<span class="cost-badge">{}/mes</span>'.format(money(v))


# El diagnóstico es un ROUTER, no un funnel a Claude Code: cada automatización se
# construye con la herramienta que le TOCA — n8n/Make para flujos de conectar apps,
# Claude Code para sistemas/apps a la medida. Esto activa TODO el contenido de la
# comunidad (n8n, Make Y Claude Code) en vez de empujar todo a una sola herramienta.
COMUNIDAD_URL = "https://www.skool.com/horizontes-ia-9992"


def build_note_text(auto):
    """Línea de 'cómo construir esto' según `construir_con`
    ('n8n' | 'make' | 'n8n_o_make' | 'claude_code' | 'manual'), o `construir_con_nota`
    si el JSON trae una nota custom. Cae al booleano viejo `es_agente_nube`."""
    if auto.get("construir_con_nota"):
        return auto["construir_con_nota"]
    cc = (auto.get("construir_con") or ("claude_code" if auto.get("es_agente_nube") else "")).lower()
    if cc in ("n8n", "make", "n8n_o_make", "make_n8n"):
        tool = {"n8n": "n8n", "make": "Make"}.get(cc, "n8n o Make")
        return ("Esto es un flujo de conectar apps — se arma con {} (sin código). "
                "Lo ves paso a paso en los cursos de automatización de la comunidad.").format(tool)
    if cc in ("claude_code", "claude", "codigo"):
        return ("Esto es un sistema a la medida — se construye con Claude Code "
                "(skill /crear-agente), sin programar.")
    return ""


def build_categories(autos):
    """Qué tipos de construcción aparecen en el set: {'no_code', 'claude'}."""
    cats = set()
    for a in autos:
        cc = (a.get("construir_con") or ("claude_code" if a.get("es_agente_nube") else "")).lower()
        if cc in ("n8n", "make", "n8n_o_make", "make_n8n"):
            cats.add("no_code")
        elif cc in ("claude_code", "claude", "codigo"):
            cats.add("claude")
    return cats


def automation_card(auto, destacada):
    """Tarjeta de automatización. La #1 (destacada) lleva glow + badge EMPIEZA AQUÍ."""
    rank = auto.get("rank", 0)
    titulo = esc(auto.get("titulo", "Automatización"))
    que_hace = esc(auto.get("que_hace", ""))
    metafora = auto.get("metafora_empleado")
    roi = auto.get("roi", {}) or {}

    # Promesa en serif italic: metáfora de empleado si existe, si no, que_hace corto.
    promesa = metafora or que_hace

    # Cadena de arquitectura.
    arch = arch_chain(auto.get("arquitectura_simple", []) or [])

    # Chips de herramientas.
    tools = "".join(tool_chip(t.get("nombre", "")) for t in auto.get("herramientas", []) or [])

    # Stat row: costo · complejidad · ahorro.
    costo_tools = roi.get("costo_tools_mes_usd")
    costo_str = "GRATIS" if (costo_tools is not None and costo_tools <= 0) else money(costo_tools)
    complejidad = esc(auto.get("complejidad", "")).capitalize()
    horas_ah = roi.get("horas_ahorradas_mes")
    valor_t = roi.get("valor_tiempo_mes_usd")
    ahorro_str = ""
    if horas_ah is not None and valor_t is not None:
        ahorro_str = "{}/mes ≈ {}/mes".format(hrs(horas_ah), money(valor_t))
    elif horas_ah is not None:
        ahorro_str = "{}/mes".format(hrs(horas_ah))

    # Línea de ingreso recuperado (solo si existe).
    ing = roi.get("ingreso_recuperado_mes_usd")
    ing_line = ""
    if ing:
        sup = roi.get("ingreso_supuesto")
        ing_line = (
            '<p class="auto-ing">+ {} de ingreso recuperado al mes'
            '{}</p>'
        ).format(money(ing),
                 ' <span class="auto-ing-sup">— {}</span>'.format(esc(sup)) if sup else '')

    # Nota del haircut (la honestidad).
    fc_nota = roi.get("factor_captura_nota")
    fc_line = '<p class="auto-fc">{}</p>'.format(esc(fc_nota)) if fc_nota else ""

    # Cómo construir esto — con la herramienta que le TOCA (router, no funnel).
    agente_nota = ""
    _bn = build_note_text(auto)
    if _bn:
        agente_nota = '<p class="auto-agente">{}</p>'.format(
            esc(_bn).replace("/crear-agente", "<code>/crear-agente</code>"))

    badge = ('<span class="start-badge">★ EMPIEZA AQUÍ</span>' if destacada
             else '<span class="next-badge">Lo que sigue</span>')

    cls = "automation-card featured" if destacada else "automation-card"

    return (
        '<article class="{cls}">'
        '<div class="auto-head">'
        '<span class="auto-rank">#{rank}</span>'
        '<h3 class="auto-title">{titulo}</h3>'
        '{badge}'
        '</div>'
        '<p class="auto-promise">{promesa}</p>'
        '<div class="auto-block">'
        '<span class="micro-label">Cómo funciona</span>{arch}'
        '</div>'
        '<div class="auto-stats">'
        '<div class="stat"><span class="micro-label">Herramientas</span>'
        '<div class="chips">{tools}</div></div>'
        '<div class="stat-row">'
        '<div class="stat"><span class="micro-label">Costo</span><span class="stat-val">{costo}</span></div>'
        '<div class="stat"><span class="micro-label">Esfuerzo</span><span class="stat-val">{complejidad}</span></div>'
        '<div class="stat stat-save"><span class="micro-label">Ahorro</span>'
        '<span class="stat-val save">{ahorro}</span></div>'
        '</div>'
        '{ing}{fc}'
        '</div>'
        '{agente}'
        '</article>'
    ).format(
        cls=cls, rank=rank, titulo=titulo, badge=badge, promesa=esc(promesa),
        arch=arch, tools=tools, costo=esc(costo_str), complejidad=complejidad or "—",
        ahorro=esc(ahorro_str) or "—", ing=ing_line, fc=fc_line,
        agente=agente_nota,
    )


def roi_table(diag, totals):
    """Tabla de ROI con fila TOTAL destacada. Recalcula desde automatizaciones[]."""
    autos = diag.get("automatizaciones", []) or []
    rows = ""
    for a in autos:
        roi = a.get("roi", {}) or {}
        horas = roi.get("horas_ahorradas_mes")
        valor_t = roi.get("valor_tiempo_mes_usd")
        ing = roi.get("ingreso_recuperado_mes_usd")
        costo = roi.get("costo_tools_mes_usd")
        ahorro_mes = (valor_t or 0) + (ing or 0)
        neto = ahorro_mes - (costo or 0)
        titulo = esc(a.get("titulo", ""))
        rank = a.get("rank", "")
        costo_disp = "GRATIS" if (costo is not None and costo <= 0) else money(costo)
        rows += (
            '<tr>'
            '<td><strong>#{rank}</strong> {titulo}</td>'
            '<td>{horas}</td>'
            '<td class="col-save">{ahorro}</td>'
            '<td>{costo}</td>'
            '<td class="col-net">{neto}</td>'
            '</tr>'
        ).format(rank=rank, titulo=titulo, horas=hrs(horas),
                 ahorro=money(ahorro_mes), costo=esc(costo_disp), neto=money(neto))

    # Fila TOTAL (recalculada server-side).
    total_horas = totals["horas_total"]
    total_ahorro = totals["valor_tiempo_total"] + totals["ingreso_total"]
    total_costo = totals["costo_total"]
    total_neto = totals["neto_mes"]

    total_row = (
        '<tr class="total-row">'
        '<td><strong>TOTAL</strong></td>'
        '<td><strong>{h}</strong></td>'
        '<td class="col-save"><strong>{a}</strong></td>'
        '<td><strong>{c}/mes</strong></td>'
        '<td class="col-net"><strong>{n}/mes</strong></td>'
        '</tr>'
    ).format(h=hrs(total_horas), a=money(total_ahorro),
             c=money(total_costo), n=money(total_neto))

    costo_hora = get(diag, "negocio.costo_hora_usuario_usd", 8)
    nombre_neg = get(diag, "negocio.nombre_negocio") or get(diag, "negocio.tipo", "tu negocio")
    fuente = _costo_hora_fuente(diag)
    if fuente == "nomina_real":
        chf = "tu hora cuesta ≈{ch} (según tu nómina)".format(ch=money(costo_hora))
    elif fuente == "dato_usuario":
        chf = "tu hora la valoraste en ≈{ch}".format(ch=money(costo_hora))
    else:
        chf = "≈{ch}/h (estimado por tu país, editable)".format(ch=money(costo_hora))
    nota = ("Para {neg}: ahorro = horas recuperadas × {chf}. Es conservador: solo el "
            "tiempo recuperado (y el ingreso rescatado donde había datos).").format(neg=nombre_neg, chf=chf)

    return (
        '<div class="roi-table">'
        '<table>'
        '<thead><tr>'
        '<th>Automatización</th><th>Horas/mes</th><th>Ahorro/mes</th>'
        '<th>Costo/mes</th><th>Neto/mes</th>'
        '</tr></thead>'
        '<tbody>{rows}{total}</tbody>'
        '</table>'
        '<p class="roi-note">{nota}</p>'
        '</div>'
    ).format(rows=rows, total=total_row, nota=esc(nota))


def _costo_hora_fuente(diag):
    """Devuelve la fuente del costo-hora normalizada: nomina_real | dato_usuario | default_pais."""
    f = get(diag, "negocio.costo_hora_fuente")
    if f in ("nomina_real", "dato_usuario", "default_pais"):
        return f
    return "default_pais" if get(diag, "negocio.costo_hora_es_default") else "dato_usuario"


def numeros_negocio_section(diag):
    """Sección 'Los números de tu negocio' — muestra las cifras REALES que dio el
    usuario y de dónde sale el costo-hora. Es la base del ROI. Se OMITE por completo
    si no hay datos económicos (ej. un beginner que aún no factura)."""
    neg = diag.get("negocio", {}) or {}
    mi = neg.get("modelo_ingresos", {}) or {}
    eco = neg.get("economia", {}) or {}

    ingreso = mi.get("ingreso_mes_aprox_usd")
    ticket = mi.get("ticket_promedio_usd")
    margen = mi.get("margen_bruto_pct")
    nomina = eco.get("nomina_mes_usd")
    leads = eco.get("leads_mes")
    ventas = eco.get("ventas_mes")
    tasa = eco.get("tasa_cierre_pct")
    if tasa is None and leads and ventas:
        tasa = round(ventas / leads * 100)
    costo_hora = neg.get("costo_hora_usuario_usd")
    fuente = _costo_hora_fuente(diag)
    kpis = eco.get("kpis", []) or []

    tiene = any(v is not None for v in [ingreso, nomina, ticket, leads, ventas, margen]) or bool(kpis)
    if not tiene:
        return ""

    cards = []
    if ingreso is not None:
        cards.append(kpi_card(money(ingreso), "Ingresos / mes", "Lo que factura el negocio, aprox."))
    if nomina is not None:
        cards.append(kpi_card(money(nomina), "Nómina / mes", "El costo de tu equipo al mes."))
    if costo_hora is not None:
        ch_ctx = {
            "nomina_real": "Tu costo REAL por hora (nómina ÷ horas). El ROI usa esto, no un promedio de industria.",
            "dato_usuario": "El valor que le diste a tu hora.",
            "default_pais": "Estimado por tu país — ajústalo si tu hora vale más.",
        }.get(fuente, "El valor de tu hora.")
        cards.append(kpi_card(money(costo_hora) + "/h", "Cuánto vale tu hora", ch_ctx))
    if ticket is not None:
        cards.append(kpi_card(money(ticket), "Ticket promedio", "Lo que deja una venta."))
    if leads is not None:
        cards.append(kpi_card(str(leads), "Leads / mes", "Interesados que te llegan al mes."))
    if tasa is not None:
        cards.append(kpi_card("{}%".format(tasa), "Tasa de cierre", "De cada interesado, cuántos compran."))
    if margen is not None:
        cards.append(kpi_card("{}%".format(margen), "Margen bruto", "Lo que te queda de cada venta."))
    for k in kpis:
        val = str(k.get("valor", ""))
        cards.append(kpi_card(val, esc(k.get("nombre", "")), esc(k.get("unidad", "")) or None))

    real = fuente == "nomina_real"
    nota = ("Estos son <strong>tus</strong> números — el ahorro y el ROI de este reporte se calculan "
            "con ellos, no con promedios de industria." if real else
            "Con estos números afinamos el ROI a tu negocio; lo que falte lo estimamos y lo marcamos como supuesto.")

    return (
        '<section><div class="wrap">'
        + section_header("Los números de tu negocio",
                         "La base real del diagnóstico. Todo el ROI de abajo sale de aquí.")
        + '<div class="kpi-grid">' + "".join(cards) + '</div>'
        + '<p class="roi-note">{}</p>'.format(nota)
        + '</div></section>'
    )


def code_block(texto, label="Copia esto:"):
    """Bloque <pre> monospace con variables [ASÍ] resaltadas en cyan."""
    safe = esc(texto)
    # Resaltar [VARIABLES] — se hace tras escapar para no romper el HTML.
    import re
    safe = re.sub(r'(\[[^\[\]]+\])', r'<span class="var">\1</span>', safe)
    return (
        '<div class="code-wrap">'
        '<span class="code-label">{label}</span>'
        '<pre class="code-block">{txt}</pre>'
        '</div>'
    ).format(label=esc(label), txt=safe)


def timeline_month(fase):
    """Bloque de fase del roadmap como item de timeline con punto cyan."""
    titulo = esc(fase.get("titulo", ""))
    rango = esc(fase.get("rango", ""))
    objetivo = esc(fase.get("objetivo", ""))
    hito = fase.get("hito", "")
    es_meta = fase.get("fase") == 3  # la fase 3 aterriza en la meta a 90 días

    acciones = ""
    for ac in fase.get("acciones", []) or []:
        acciones += '<li>{}</li>'.format(esc(ac))

    hito_cls = "hito hito-meta" if es_meta else "hito"
    hito_icon = "✦ " if es_meta else "→ "
    hito_html = ('<p class="{cls}">{icon}<strong>Meta de la fase:</strong> {hito}</p>'
                 ).format(cls=hito_cls, icon=hito_icon, hito=esc(hito)) if hito else ""

    return (
        '<div class="timeline-month">'
        '<div class="tl-dot"></div>'
        '<div class="tl-body">'
        '<span class="tl-range">{rango}</span>'
        '<h3 class="tl-title">{titulo}</h3>'
        '<p class="tl-obj">{objetivo}</p>'
        '<ul class="tl-actions">{acciones}</ul>'
        '{hito}'
        '</div>'
        '</div>'
    ).format(rango=rango, titulo=titulo, objetivo=objetivo,
             acciones=acciones, hito=hito_html)


# ─────────────────────────────────────────────────────────────────────────────
# 4. EL CSS (todo inline, claro + acento, con print)
# ─────────────────────────────────────────────────────────────────────────────

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap');

:root{
  --bg:#ffffff; --surface:#f7f9fc; --surface-2:#eef2f7;
  --border:rgba(17,24,39,.12);
  --text:#15181e; --muted:#5b6573;
  --cyan:#00E5FF; --cyan-2:#22d3ee; --cyan-soft:rgba(0,229,255,.10);
  --on-accent:#15181e;
  --good:#34d399; --warn:#fbbf24; --orange:#fb923c; --dim:#8a94a3;
  --radius:16px; --radius-sm:10px;
  --shadow:0 8px 30px -12px rgba(17,24,39,.12);
  --glow:none;
}

*{box-sizing:border-box;}
html{-webkit-text-size-adjust:100%;}
body{
  margin:0; background:var(--bg); color:var(--text);
  font-family:'Space Grotesk',system-ui,-apple-system,sans-serif;
  font-size:16px; line-height:1.65;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:820px; margin:0 auto; padding:0 28px;}
.accent{font-family:'Instrument Serif',Georgia,serif; font-style:italic; color:var(--cyan-2); font-weight:400;}
a{color:var(--cyan); text-decoration:none;}
code{font-family:ui-monospace,'SF Mono',Menlo,monospace; background:var(--surface-2);
  padding:1px 6px; border-radius:6px; font-size:.88em; color:var(--cyan-2);}
.micro-label{display:block; font-size:11px; letter-spacing:.14em; text-transform:uppercase;
  color:var(--muted); margin-bottom:8px; font-weight:600;}

section{padding:56px 0; border-top:1px solid var(--border);}
section:first-of-type{border-top:none;}
.sec-head{margin-bottom:32px;}
.sec-head h2{font-size:30px; font-weight:700; margin:0; letter-spacing:-.02em;}
.sec-head .rule{display:block; width:54px; height:2px; background:var(--cyan); margin:14px 0 0;}
.sec-sub{color:var(--muted); margin:14px 0 0; font-size:15.5px;}

/* ── PORTADA ── */
.cover{
  min-height:100vh; display:flex; flex-direction:column; justify-content:center;
  padding:64px 0; border-top:none; position:relative; overflow:hidden;
}
.cover::before{
  content:""; position:absolute; inset:0;
  background:radial-gradient(ellipse 60% 50% at 18% 12%, rgba(0,229,255,.14), transparent 60%);
  pointer-events:none;
}
.cover .wrap{position:relative; z-index:1;}
.lockup{display:flex; align-items:center; justify-content:space-between; margin-bottom:64px;}
.lockup-left{display:flex; align-items:center; gap:11px;}
.wordmark{font-size:12px; letter-spacing:.20em; text-transform:uppercase; color:var(--cyan); font-weight:600;}
.lockup-date{font-size:13px; color:var(--muted);}
.eyebrow{font-size:12px; letter-spacing:.20em; text-transform:uppercase; color:var(--cyan); font-weight:600; margin-bottom:20px;}
.cover h1{font-size:52px; font-weight:700; line-height:1.05; margin:0 0 18px; letter-spacing:-.03em;}
.cover-sub{font-size:25px; line-height:1.4; color:var(--text); max-width:660px; margin:0 0 28px;}
.cover-meta{font-size:14.5px; color:var(--muted); margin:0 0 56px;}
.cover-meta .sep{color:var(--cyan); margin:0 9px;}
.kpi-teaser{display:flex; flex-wrap:wrap; gap:20px;}
.kpi-teaser .kt{flex:1; min-width:160px;}
.kpi-teaser .kt-num{font-family:'Instrument Serif',Georgia,serif; font-style:italic; font-size:40px; color:var(--cyan); line-height:1;}
.kpi-teaser .kt-label{font-size:12px; letter-spacing:.10em; text-transform:uppercase; color:var(--muted); margin-top:8px;}

/* ── KPI cards (resumen) ── */
.kpi-grid{display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin:28px 0;}
.kpi-card{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:24px;}
.kpi-num{font-family:'Instrument Serif',Georgia,serif; font-style:italic; font-size:40px; color:var(--cyan); line-height:1;}
.kpi-label{font-size:12px; letter-spacing:.10em; text-transform:uppercase; color:var(--text); margin-top:10px; font-weight:600;}
.kpi-ctx{font-size:13.5px; color:var(--muted); margin:8px 0 0; line-height:1.45;}

.tesis{font-size:18px; line-height:1.7; color:var(--text); margin:0 0 8px;}
.callout{
  background:var(--surface); border:1px solid var(--border); border-left:3px solid var(--cyan);
  border-radius:var(--radius-sm); padding:20px 24px; margin-top:26px;
}
.callout .micro-label{color:var(--cyan);}
.callout p{margin:0; font-size:15.5px;}

/* recognition quote */
.recognition{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
  padding:30px 32px; margin-bottom:8px;}
.recognition .q{font-family:'Instrument Serif',Georgia,serif; font-style:italic; font-size:24px; line-height:1.45; color:var(--text); margin:0;}
.recognition .q::before{content:"“"; color:var(--cyan);}
.recognition .q::after{content:"”"; color:var(--cyan);}
.recognition .attr{font-size:13.5px; color:var(--muted); margin:14px 0 0;}

/* ── score bars ── */
.score-bar{padding:20px 0; border-bottom:1px solid var(--border);}
.score-bar:last-child{border-bottom:none;}
.score-bar-top{display:flex; align-items:center; justify-content:space-between; gap:14px; margin-bottom:11px;}
.proc-name{font-size:18px; font-weight:600; margin:0;}
.proc-flag{font-size:11px; color:var(--cyan); margin-left:9px; font-weight:600; letter-spacing:.04em;}
.track{position:relative; height:10px; background:var(--surface-2); border-radius:99px; overflow:hidden; margin-bottom:11px;}
.fill{position:absolute; left:0; top:0; bottom:0; border-radius:99px;
  background:linear-gradient(90deg,var(--cyan-2),var(--cyan));
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.score-num{position:absolute; right:0; top:-26px; font-size:13px; font-weight:600; color:var(--muted);}
.score-num small{color:var(--dim);}
.proc-meta{font-size:13.5px; color:var(--muted); margin:0;}
.proc-quote{font-style:italic; color:var(--text);}

.badge{display:inline-flex; align-items:center; gap:5px; font-size:12px; font-weight:600;
  padding:5px 12px; border-radius:99px; white-space:nowrap;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.badge-good{background:rgba(52,211,153,.12); color:var(--good); border:1px solid rgba(52,211,153,.3);}
.badge-warn{background:rgba(251,191,36,.12); color:var(--warn); border:1px solid rgba(251,191,36,.3);}
.badge-orange{background:rgba(251,146,60,.12); color:var(--orange); border:1px solid rgba(251,146,60,.3);}
.badge-dim{background:rgba(100,116,139,.12); color:var(--dim); border:1px solid rgba(100,116,139,.3);}

/* ── automation cards ── */
.automation-card{background:var(--surface); border:1px solid var(--border);
  border-radius:var(--radius); padding:32px; margin-bottom:24px; opacity:.94;}
.automation-card.featured{border:1px solid var(--cyan); box-shadow:var(--glow); opacity:1;}
.auto-head{display:flex; align-items:center; gap:14px; flex-wrap:wrap; margin-bottom:14px;}
.auto-rank{font-size:14px; font-weight:700; color:var(--cyan); background:var(--cyan-soft);
  border:1px solid rgba(0,229,255,.3); border-radius:99px; padding:4px 13px;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.auto-title{font-size:21px; font-weight:700; margin:0; flex:1; letter-spacing:-.01em;}
.start-badge{font-size:11px; font-weight:700; letter-spacing:.08em; color:var(--on-accent);
  background:var(--cyan); border-radius:99px; padding:5px 13px;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.next-badge{font-size:11px; font-weight:600; letter-spacing:.06em; color:var(--muted);
  border:1px solid var(--border); border-radius:99px; padding:5px 13px;}
.auto-promise{font-family:'Instrument Serif',Georgia,serif; font-style:italic; font-size:19px;
  line-height:1.45; color:var(--text); margin:0 0 24px;}
.auto-block{background:var(--bg); border:1px solid var(--border); border-radius:var(--radius-sm);
  padding:18px 20px; margin-bottom:20px;}
.arch-chain{display:flex; flex-wrap:wrap; align-items:center; gap:9px;}
.arch-step{background:var(--surface-2); border:1px solid var(--border); border-radius:8px;
  padding:7px 12px; font-size:13px; color:var(--text);}
.arch-arrow{color:var(--cyan); font-weight:700; font-size:15px;}
.chips{display:flex; flex-wrap:wrap; gap:8px;}
.tool-chip{background:var(--cyan-soft); border:1px solid rgba(0,229,255,.25); color:var(--cyan-2);
  border-radius:99px; padding:5px 13px; font-size:13px; font-weight:600;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.auto-stats .stat{margin-bottom:18px;}
.stat-row{display:flex; flex-wrap:wrap; gap:28px; margin-bottom:4px;}
.stat-row .stat{margin-bottom:0;}
.stat-val{font-size:17px; font-weight:600;}
.stat-val.save{color:var(--good);}
.auto-ing{font-size:14px; color:var(--good); margin:14px 0 0;}
.auto-ing-sup{color:var(--muted); font-weight:400;}
.auto-fc{font-size:13px; color:var(--muted); margin:14px 0 0; line-height:1.5; font-style:italic;}
.auto-agente{font-size:13px; color:var(--muted); margin:12px 0 0;}

/* ── ROI table ── */
.roi-table table{width:100%; border-collapse:collapse; font-size:14.5px;
  background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); overflow:hidden;}
.roi-table th{background:var(--cyan-soft); color:var(--cyan-2); text-align:left;
  padding:14px 16px; font-size:12px; letter-spacing:.06em; text-transform:uppercase; font-weight:600;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.roi-table td{padding:14px 16px; border-top:1px solid var(--border);}
.roi-table tbody tr:nth-child(even){background:rgba(17,24,39,.025);}
.roi-table .col-save{color:var(--good);}
.roi-table .col-net{color:var(--cyan-2); font-weight:600;}
.roi-table .total-row{background:var(--cyan-soft) !important;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.roi-table .total-row td{color:var(--cyan); border-top:2px solid rgba(0,229,255,.3);}
.roi-note{font-size:13px; color:var(--muted); margin:16px 0 0; line-height:1.55;}

/* ── quick win ── */
.quickwin{background:var(--cyan-soft); border:1px solid var(--cyan); border-radius:var(--radius);
  box-shadow:var(--glow); padding:40px; -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.qw-eyebrow{font-size:12px; letter-spacing:.16em; text-transform:uppercase; color:var(--cyan); font-weight:700; margin-bottom:14px;}
.qw-title{font-size:27px; font-weight:700; margin:0 0 12px; letter-spacing:-.02em;}
.qw-promise{font-size:16.5px; color:var(--text); margin:0 0 24px;}
.code-wrap{margin:8px 0 24px;}
.code-label{font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); font-weight:600;}
.code-block{background:var(--bg); border:1px solid var(--border); border-radius:var(--radius-sm);
  padding:20px; margin:8px 0 0; overflow-x:auto; font-family:ui-monospace,'SF Mono',Menlo,monospace;
  font-size:13.5px; line-height:1.7; color:var(--text); white-space:pre-wrap; word-break:break-word;}
.code-block .var{color:var(--cyan); font-weight:600;}
.qw-steps{margin:0 0 18px; padding-left:0; list-style:none; counter-reset:qw;}
.qw-steps li{counter-increment:qw; position:relative; padding:6px 0 6px 34px; font-size:15px;}
.qw-steps li::before{content:counter(qw); position:absolute; left:0; top:6px;
  width:23px; height:23px; background:var(--cyan); color:var(--on-accent); border-radius:50%;
  font-size:12px; font-weight:700; display:flex; align-items:center; justify-content:center;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.qw-cont{font-size:13.5px; color:var(--muted); margin:0;}
.qw-result{font-size:15px; color:var(--good); margin:18px 0 0; font-weight:500;}

/* ── timeline ── */
.timeline{position:relative; padding-left:8px;}
.timeline-month{position:relative; padding:0 0 36px 32px;}
.timeline-month::before{content:""; position:absolute; left:5px; top:18px; bottom:-18px;
  width:2px; background:var(--border);}
.timeline-month:last-child::before{display:none;}
.tl-dot{position:absolute; left:0; top:6px; width:12px; height:12px; border-radius:50%;
  background:var(--cyan); box-shadow:0 0 0 4px var(--cyan-soft);
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.tl-range{font-size:12px; letter-spacing:.1em; text-transform:uppercase; color:var(--cyan); font-weight:600;}
.tl-title{font-size:19px; font-weight:700; margin:6px 0 4px;}
.tl-obj{font-size:14.5px; color:var(--muted); margin:0 0 12px;}
.tl-actions{margin:0; padding-left:18px; font-size:14.5px;}
.tl-actions li{margin-bottom:6px;}
.hito{font-size:14px; color:var(--text); margin:14px 0 0; padding:12px 16px;
  background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-sm);}
.hito-meta{border:1px solid rgba(52,211,153,.4); background:rgba(52,211,153,.08); color:var(--good);
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.hito-meta strong{color:var(--good);}

/* ── stack ── */
.stack-grid{display:grid; grid-template-columns:repeat(2,1fr); gap:14px; margin-bottom:28px;}
.stack-card{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-sm); padding:18px 20px;}
.stack-name{font-size:16px; font-weight:600; margin:0 0 4px;}
.stack-for{font-size:13.5px; color:var(--muted); margin:0 0 12px; line-height:1.45;}
.cost-badge{display:inline-block; font-size:12px; font-weight:600; padding:4px 11px; border-radius:99px;
  background:var(--surface-2); color:var(--muted); border:1px solid var(--border);}
.cost-free{background:rgba(52,211,153,.12); color:var(--good); border-color:rgba(52,211,153,.3);
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.stack-total{font-family:'Instrument Serif',Georgia,serif; font-style:italic; font-size:26px; color:var(--cyan); margin:0;}
.stack-total small{font-family:'Space Grotesk',sans-serif; font-style:normal; font-size:14px;
  color:var(--muted); display:block; letter-spacing:.06em; text-transform:uppercase; margin-bottom:6px; font-weight:600;}
.stack-agente{font-size:14px; color:var(--cyan-2); margin:20px 0 0; padding:14px 18px;
  background:var(--cyan-soft); border:1px solid rgba(0,229,255,.25); border-radius:var(--radius-sm);
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}

/* ── supuestos ── */
.supuestos{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:26px 30px;}
.supuestos ul{margin:0; padding-left:20px;}
.supuestos li{font-size:14px; color:var(--muted); margin-bottom:9px; line-height:1.55;}

/* ── closing ── */
.closing{text-align:center;}
.closing-card{background:var(--surface); border:1px solid rgba(0,229,255,.25); border-radius:var(--radius);
  padding:48px 40px; max-width:640px; margin:0 auto;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.closing-title{font-family:'Instrument Serif',Georgia,serif; font-style:italic; font-size:30px; color:var(--text); margin:0 0 18px; line-height:1.3;}
.closing-text{font-size:16px; color:var(--muted); margin:0 0 30px; line-height:1.65;}
.cta-primary{display:inline-block; background:var(--cyan); color:var(--on-accent); font-weight:700; font-size:16px;
  padding:14px 30px; border-radius:99px; box-shadow:var(--glow); margin-bottom:18px;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.cta-secondary{display:block; font-size:14.5px; color:var(--muted); margin-top:6px;}
.cta-secondary a{color:var(--cyan-2);}
.doc-footer{text-align:center; padding:40px 0 64px; color:var(--muted); font-size:12.5px;}
.doc-footer .lf{display:inline-flex; align-items:center; gap:8px; margin-bottom:10px;}

@media (max-width:640px){
  .wrap{padding:0 20px;}
  .cover h1{font-size:38px;} .cover-sub{font-size:21px;}
  .kpi-grid{grid-template-columns:1fr;} .stack-grid{grid-template-columns:1fr;}
  .sec-head h2{font-size:25px;} .automation-card,.quickwin{padding:24px;}
}

/* ── PRINT ── */
@media print{
  p,li{orphans:3; widows:3;}  /* sin líneas sueltas al pie/inicio de página */
  *{-webkit-print-color-adjust:exact !important; print-color-adjust:exact !important;}
  @page{size:A4; margin:14mm;}
  body{background:var(--bg) !important; font-size:12pt;}
  .wrap{max-width:100%; padding:0;}
  section{padding:22px 0;}
  /* La portada NO fuerza salto: deja que el resumen fluya en la misma hoja para
     no desperdiciar media página en blanco. Solo evitamos cortar bloques atómicos. */
  .cover{min-height:auto; padding:24px 0 18px;}
  .cover h1{font-size:40px;}
  .automation-card{break-inside:avoid;}
  .timeline-month{break-inside:avoid;}
  .score-bar{break-inside:avoid;}
  .kpi-card,.stack-card{break-inside:avoid;}
  .quickwin,.recognition,.callout,.closing-card,.supuestos{break-inside:avoid;}
  /* Encabezado de sección: nunca se parte por dentro (título + regla + subtítulo
     juntos) NI se queda huérfano al final de una página (va con su contenido). */
  .sec-head{break-inside:avoid; break-after:avoid; page-break-inside:avoid; page-break-after:avoid;}
  h2,h3{break-after:avoid; page-break-after:avoid;}
  /* La tabla de ROI puede ser alta: que fluya entre páginas por FILAS (no se parte
     una fila), en vez de saltar entera y orfanar el encabezado. */
  .roi-table tr, .roi-table thead{break-inside:avoid;}
}
"""


# ─────────────────────────────────────────────────────────────────────────────
# 5. ENSAMBLADO DEL HTML
# ─────────────────────────────────────────────────────────────────────────────

def build_html(diag, marca=None):
    marca = marca or cargar_marca()
    totals = derivar_totales(diag)
    neg = diag.get("negocio", {}) or {}
    nombre_negocio = neg.get("nombre_negocio") or neg.get("tipo") or "Tu negocio"
    nombre_persona = neg.get("nombre_persona") or ""
    segment = diag.get("segment", "operator")
    seg_copy = SEGMENT_COPY.get(segment, SEGMENT_COPY["operator"])
    fecha = get(diag, "meta.fecha", "")

    autos = diag.get("automatizaciones", []) or []
    auto1 = autos[0] if autos else None

    # KPI numbers (recalculados). El ahorro mostrado es el TOTAL (tiempo + ingreso
    # recuperado) = el mismo número que el TOTAL de la tabla de ROI. Nunca el
    # tiempo-solo, para que la portada no subvenda y no se contradiga con el cuerpo.
    kpi_horas = hrs(totals["horas_total"]) if totals["horas_total"] else "—"
    kpi_dinero = money(totals["ahorro_total"]) if totals["ahorro_total"] else "—"
    roi_x = totals.get("roi_anual_x")
    kpi_roi = "{}×".format(roi_x) if roi_x else "—"

    out = []
    out.append('<!DOCTYPE html><html lang="es"><head>')
    out.append('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">')
    out.append('<title>Diagnóstico — {}</title>'.format(esc(nombre_negocio)))
    out.append('<style>{}</style>'.format(CSS))
    out.append('</head><body>')

    # ── A. PORTADA ──
    meta_bits = []
    if nombre_persona:
        meta_bits.append('Preparado para {}'.format(esc(nombre_persona)))
    if neg.get("tipo"):
        meta_bits.append('Sector: {}'.format(esc(neg.get("tipo"))))
    ubic = neg.get("ciudad") or neg.get("pais")
    if ubic:
        meta_bits.append(esc(ubic))
    cover_meta = '<span class="sep">·</span>'.join(meta_bits)

    subtitulo = seg_copy["subtitulo"]

    out.append('<section class="cover"><div class="wrap">')
    out.append('<div class="lockup">'
               '<div class="lockup-left">{logo}<span class="wordmark">{marca}</span></div>'
               '<span class="lockup-date">{fecha}</span></div>'.format(
                   logo=logo_html(marca, 28), marca=esc(marca["nombre"]), fecha=esc(fecha_larga(fecha))))
    out.append('<div class="eyebrow">Diagnóstico de automatización</div>')
    out.append('<h1>{}</h1>'.format(esc(nombre_negocio)))
    out.append('<p class="cover-sub accent">{}</p>'.format(esc(subtitulo)))
    if cover_meta:
        out.append('<p class="cover-meta">{}</p>'.format(cover_meta))
    out.append('<div class="kpi-teaser">'
               '<div class="kt"><div class="kt-num">{h}</div><div class="kt-label">recuperables al mes</div></div>'
               '<div class="kt"><div class="kt-num">{d}</div><div class="kt-label">de ahorro estimado/mes</div></div>'
               '<div class="kt"><div class="kt-num">{r}</div><div class="kt-label">retorno anual estimado</div></div>'
               '</div>'.format(h=kpi_horas, d=kpi_dinero, r=kpi_roi))
    out.append('</div></section>')

    # ── B. RESUMEN EJECUTIVO ──
    out.append('<section><div class="wrap">')
    out.append(section_header("Resumen ejecutivo"))
    # Tesis derivada de la data.
    proc_dolor = ""
    sd = diag.get("sangrado_declarado", {}) or {}
    if sd.get("proceso_id_match"):
        for p in diag.get("procesos", []):
            if p.get("id") == sd["proceso_id_match"]:
                proc_dolor = p.get("nombre", "")
                break
    auto1_titulo = auto1.get("titulo") if auto1 else "tu primera automatización"
    tesis = (
        "{neg} {desc} Hoy se te van ~{horas} en tareas repetitivas que se "
        "pueden automatizar. Las {n} automatizaciones de este reporte recuperan ese "
        "tiempo y te acercan a tu meta. Empieza por <strong>{q}</strong>."
    ).format(
        neg='<strong>' + esc(nombre_negocio) + '</strong>',
        desc=("es " + esc(neg.get("descripcion") or neg.get("tipo")) + ".") if (neg.get("descripcion") or neg.get("tipo")) else "tiene procesos que hoy te roban tiempo.",
        horas=hrs(round((totals["horas_total"] / 4.33), 1)) + "/semana" if totals["horas_total"] else "varias horas/semana",
        n=len(autos), q=esc(auto1_titulo),
    )
    out.append('<p class="tesis">{}</p>'.format(tesis))

    out.append('<div class="kpi-grid">')
    out.append(kpi_card(kpi_horas, "Horas recuperables/mes",
                        "Sumando las {} automatizaciones recomendadas.".format(len(autos))))
    out.append(kpi_card(kpi_dinero, "Ahorro mensual estimado",
                        "Tu tiempo recuperado más los ingresos que hoy dejas de perder."))
    payback_nota = get(diag, "roi_global.payback.nota")
    out.append(kpi_card(kpi_roi, "Retorno anual estimado",
                        esc(payback_nota) if payback_nota else "Sobre el costo de herramientas."))
    out.append('</div>')

    # Callout: tu mayor oportunidad.
    if auto1:
        por_que = get(diag, "quick_win.por_que_esta", "")
        out.append('<div class="callout"><span class="micro-label">Tu mayor oportunidad ahora mismo</span>'
                   '<p><strong>{t}</strong> — {pq} La marcamos como tu quick-win más abajo.</p></div>'.format(
                       t=esc(auto1.get("titulo", "")), pq=esc(por_que)))
    out.append('</div></section>')

    # ── B.5 LOS NÚMEROS DE TU NEGOCIO (la base real del ROI; se omite si no hay data) ──
    out.append(numeros_negocio_section(diag))

    # ── Reconocimiento (quote del usuario) ──
    if sd.get("frase_textual"):
        out.append('<section><div class="wrap"><div class="recognition">')
        out.append('<p class="q">{}</p>'.format(esc(sd["frase_textual"])))
        attr = "Eso es exactamente el cuello de botella que vamos a cortar."
        out.append('<p class="attr">— Lo que me dijiste. {}</p>'.format(esc(attr)))
        out.append('</div></div></section>')

    # ── C. MAPA DE PROCESOS ──
    procesos = sorted(diag.get("procesos", []) or [],
                      key=lambda p: p.get("score", 0), reverse=True)
    if procesos:
        out.append('<section><div class="wrap">')
        out.append(section_header(
            "Mapa de tus procesos",
            "Cada proceso, calificado por qué tan automatizable es y cuánto tiempo te devuelve."))
        for p in procesos:
            out.append(score_bar(p))
        out.append('</div></section>')

    # ── D. LAS AUTOMATIZACIONES ──
    if autos:
        out.append('<section><div class="wrap">')
        out.append(section_header(
            "Las {} automatizaciones que te recomiendo".format(len(autos)),
            "En orden. No intentes las tres a la vez — domina la primera."))
        for i, a in enumerate(autos):
            out.append(automation_card(a, destacada=(i == 0)))
        out.append('</div></section>')

    # ── E. TABLA DE ROI ──
    if autos:
        out.append('<section><div class="wrap">')
        out.append(section_header(
            "El retorno de tu inversión",
            "Tiempo y dinero, en frío. Estimaciones conservadoras."))
        out.append(roi_table(diag, totals))
        # Escenarios (3 números, framework §3.6).
        esc_data = totals.get("escenarios", {}) or {}
        if esc_data:
            out.append('<div class="kpi-grid" style="margin-top:24px">')
            out.append(kpi_card(money(esc_data.get("conservador_usd")), "Conservador",
                                "Aun en el peor caso, recuperas esto."))
            out.append(kpi_card(money(esc_data.get("base_usd")), "Base",
                                "Lo más probable."))
            out.append(kpi_card(money(esc_data.get("optimista_usd")), "Optimista",
                                "Si lo aprovechas bien."))
            out.append('</div>')
        out.append('</div></section>')

    # ── F. QUICK WIN ──
    qw = diag.get("quick_win", {}) or {}
    if qw and auto1:
        # Encontrar la automatización referida.
        qw_auto = None
        for a in autos:
            if a.get("id") == qw.get("automatizacion_id"):
                qw_auto = a
                break
        qw_auto = qw_auto or auto1
        out.append('<section><div class="wrap"><div class="quickwin">')
        out.append('<div class="qw-eyebrow">★ Tu quick win — úsalo hoy, en 5 minutos</div>')
        out.append('<h2 class="qw-title">{}</h2>'.format(esc(qw_auto.get("titulo", ""))))
        promesa = qw.get("accion_hoy") or (
            "En 5 minutos, sin instalar nada, das el primer paso real para {}.".format(nombre_negocio))
        out.append('<p class="qw-promise">{}</p>'.format(esc(promesa)))

        # El recurso EJECUTABLE HOY: el prompt copy-paste real. Si no hay prompt,
        # caemos al primer_paso de la automatización (degradación con gracia).
        prompt = qw.get("prompt")
        if prompt:
            out.append(code_block(prompt, label="Pega esto en ChatGPT o Claude:"))
        else:
            contenido = qw_auto.get("primer_paso", "")
            if contenido:
                out.append(code_block(contenido, label="Empieza juntando esto:"))

        pasos = qw.get("pasos_hoy", []) or []
        if pasos:
            out.append('<ol class="qw-steps">')
            for paso in pasos:
                txt = str(paso).strip()
                # quitar prefijo numérico para no duplicar con el contador CSS
                if txt[:2].rstrip(".").isdigit() and ". " in txt[:4]:
                    txt = txt.split(". ", 1)[-1].strip()
                out.append('<li>{}</li>'.format(esc(txt)))
            out.append('</ol>')

        resultado = qw.get("resultado_esperado")
        if resultado:
            out.append('<p class="qw-result">→ {}</p>'.format(esc(resultado)))
        out.append('<p class="qw-cont">El archivo <code>04-quick-win.md</code> tiene esto '
                   'mismo para copiar fácil. Cuando funcione, automatízalo del todo (ver el roadmap).</p>')
        out.append('</div></div></section>')

    # ── G. ROADMAP ──
    roadmap = diag.get("roadmap_90_dias", []) or []
    if roadmap:
        out.append('<section><div class="wrap">')
        out.append(section_header("Tu ruta a 90 días", "El orden exacto. Una cosa a la vez."))
        out.append('<div class="timeline">')
        for fase in sorted(roadmap, key=lambda f: f.get("fase", 0)):
            out.append(timeline_month(fase))
        out.append('</div></div></section>')

    # ── H. STACK ──
    stack_cats = build_categories(autos)
    # Construir el stack desde las herramientas únicas de las automatizaciones.
    stack_seen = {}
    for a in autos:
        for t in a.get("herramientas", []) or []:
            nm = t.get("nombre", "")
            if nm and nm not in stack_seen:
                stack_seen[nm] = t
    if stack_seen:
        out.append('<section><div class="wrap">')
        out.append(section_header("Tu stack",
                                  "Lo mínimo para arrancar. Casi todo tiene plan gratis."))
        out.append('<div class="stack-grid">')
        for nm, t in stack_seen.items():
            out.append('<div class="stack-card">'
                       '<p class="stack-name">{nm}</p>'
                       '<p class="stack-for">{para}</p>{badge}</div>'.format(
                           nm=esc(nm), para=esc(t.get("para_que", "")),
                           badge=cost_badge(t.get("costo_mes_usd", 0))))
        out.append('</div>')
        out.append('<p class="stack-total"><small>Costo total para empezar</small>{}/mes</p>'.format(
            money(totals["costo_total"])))
        if "no_code" in stack_cats:
            out.append('<p class="stack-agente">Los flujos de conectar apps los armas con '
                       '<strong>n8n</strong> o <strong>Make</strong> — los tienes paso a paso en '
                       'los cursos de automatización de la comunidad.</p>')
        if "claude" in stack_cats:
            out.append('<p class="stack-agente">Para construir un sistema a la medida, el skill '
                       '<code>/crear-agente</code> te guía paso a paso, sin programar.</p>')
        out.append('</div></section>')

    # ── Supuestos ──
    supuestos = diag.get("supuestos_globales", []) or []
    if supuestos:
        out.append('<section><div class="wrap">')
        out.append(section_header("Nuestros supuestos", "La letra clara que da confianza."))
        out.append('<div class="supuestos"><ul>')
        for s in supuestos:
            out.append('<li>{}</li>'.format(esc(s)))
        out.append('</ul></div></div></section>')

    # ── I. CIERRE ──
    cierre = diag.get("cierre", {}) or {}
    out.append('<section class="closing"><div class="wrap"><div class="closing-card">')
    out.append('<h2 class="closing-title">Ya tienes el mapa de {}. El siguiente paso es construir.</h2>'.format(
        esc(nombre_negocio)))
    mensaje_cierre = cierre.get("mensaje_segment") or seg_copy["resumen_cierre"]
    siguiente = cierre.get("siguiente_paso", "")
    cta_com = cierre.get("cta_comunidad", "")
    out.append('<p class="closing-text">{m} {s}</p>'.format(
        m=esc(mensaje_cierre), s=esc(siguiente)))
    out.append('<p class="closing-text" style="margin-bottom:24px">{}</p>'.format(esc(cta_com)))
    out.append('<span class="cta-primary">Empieza tu quick-win hoy →</span>')
    if marca["tiene_perfil"]:
        c = marca["contacto"]
        if c and c.startswith("http"):
            out.append('<span class="cta-secondary">¿Lo construimos juntos? '
                       '<a href="{url}">{nombre} →</a></span>'.format(url=esc(c), nombre=esc(marca["nombre"])))
        elif c:
            out.append('<span class="cta-secondary">¿Lo construimos juntos? Escríbele a '
                       '{nombre}: {c}</span>'.format(nombre=esc(marca["nombre"]), c=esc(c)))
        else:
            out.append('<span class="cta-secondary">{} puede construir tu automatización #1.</span>'.format(
                esc(marca["nombre"])))
    else:
        cta_url = cierre.get("cta_url", "https://www.skool.com/horizontes-ia-9992")
        out.append('<span class="cta-secondary">Conoce la comunidad de '
                   '<a href="{url}">Horizontes IA →</a></span>'.format(url=esc(cta_url)))
    out.append('</div></div></section>')

    # ── Footer ──
    out.append('<div class="doc-footer"><div class="lf">{logo}'
               '<span class="wordmark">{marca}</span></div><br>'
               'Diagnóstico generado por {marca} · {fecha} · Hecho para {neg}'
               '</div>'.format(logo=logo_html(marca, 20), marca=esc(marca["nombre"]),
                               fecha=esc(fecha_larga(fecha)), neg=esc(nombre_negocio)))

    out.append('</body></html>')
    return "".join(out)


# ─────────────────────────────────────────────────────────────────────────────
# 6. ENTREGABLES MARKDOWN
# ─────────────────────────────────────────────────────────────────────────────

def md_procesos_y_roi(diag, totals):
    neg = diag.get("negocio", {}) or {}
    nombre = neg.get("nombre_negocio") or neg.get("tipo") or "tu negocio"
    autos = diag.get("automatizaciones", []) or []
    procesos = sorted(diag.get("procesos", []) or [], key=lambda p: p.get("score", 0), reverse=True)

    L = []
    L.append("# Diagnóstico de automatización — {}".format(nombre))
    L.append("")
    desc = neg.get("descripcion") or neg.get("tipo") or ""
    horas_sem = round(totals["horas_total"] / 4.33, 1) if totals["horas_total"] else 0
    L.append("{desc} Hay {n} procesos que hoy te roban ~{h}h/semana. "
             "Automatizarlos en este orden te acerca a tu meta a 90 días.".format(
                 desc=desc, n=len(autos), h=horas_sem))
    L.append("")
    L.append("## Tus procesos, calificados")
    L.append("")
    L.append("| Proceso | Veces/sem | Horas/sem | Score | Veredicto |")
    L.append("|---|---|---|---|---|")
    for p in procesos:
        freq = p.get("frecuencia_veces_semana", "")
        tv = p.get("tiempo_por_vez_min")
        hsem = round((freq * tv) / 60, 1) if (freq and tv) else ""
        banda = p.get("banda") or banda_por_score(p.get("score", 0))
        icon, label, _ = BANDA_INFO.get(banda, BANDA_INFO["no_prioritario"])
        L.append("| {n} | {f} | {h} | {s}/100 | {i} {l} |".format(
            n=p.get("nombre", ""), f=freq, h=hsem, s=p.get("score", 0), i=icon, l=label))
    L.append("")
    L.append("## Las automatizaciones recomendadas")
    L.append("")
    for a in autos:
        roi = a.get("roi", {}) or {}
        L.append("### #{r} — {t}".format(r=a.get("rank", ""), t=a.get("titulo", "")))
        L.append("")
        L.append(a.get("que_hace", ""))
        if a.get("metafora_empleado"):
            L.append("")
            L.append("> {}".format(a["metafora_empleado"]))
        L.append("")
        horas = roi.get("horas_ahorradas_mes")
        valor = roi.get("valor_tiempo_mes_usd")
        L.append("- **Ahorro:** {h}/mes ≈ {v}/mes".format(h=hrs(horas), v=money(valor)))
        ing = roi.get("ingreso_recuperado_mes_usd")
        if ing:
            L.append("- **Ingreso recuperado:** +{}/mes (estimación conservadora)".format(money(ing)))
        tools = ", ".join(t.get("nombre", "") for t in a.get("herramientas", []) or [])
        L.append("- **Herramientas:** {}".format(tools))
        L.append("- **Complejidad:** {}".format((a.get("complejidad") or "").capitalize()))
        _bn = build_note_text(a)
        if _bn:
            L.append("- **Cómo construirlo:** {}".format(_bn))
        L.append("")
    # Tabla ROI consolidada.
    L.append("## ROI consolidado")
    L.append("")
    L.append("| Automatización | Horas/mes | Ahorro/mes | Costo/mes | Neto/mes |")
    L.append("|---|---|---|---|---|")
    for a in autos:
        roi = a.get("roi", {}) or {}
        ahorro = (roi.get("valor_tiempo_mes_usd") or 0) + (roi.get("ingreso_recuperado_mes_usd") or 0)
        costo = roi.get("costo_tools_mes_usd") or 0
        L.append("| #{r} {t} | {h} | {a} | {c} | {n} |".format(
            r=a.get("rank", ""), t=a.get("titulo", ""), h=hrs(roi.get("horas_ahorradas_mes")),
            a=money(ahorro), c=("GRATIS" if costo <= 0 else money(costo)), n=money(ahorro - costo)))
    L.append("| **TOTAL** | **{h}** | **{a}** | **{c}/mes** | **{n}/mes** |".format(
        h=hrs(totals["horas_total"]),
        a=money(totals["valor_tiempo_total"] + totals["ingreso_total"]),
        c=money(totals["costo_total"]), n=money(totals["neto_mes"])))
    L.append("")
    qw_titulo = ""
    if autos:
        for a in autos:
            if a.get("id") == get(diag, "quick_win.automatizacion_id"):
                qw_titulo = a.get("titulo", "")
                break
        qw_titulo = qw_titulo or autos[0].get("titulo", "")
    L.append("La #1 es **{}** — empieza por ahí. El archivo `04-quick-win.md` ya tiene "
             "lo que necesitas para arrancar hoy.".format(qw_titulo))
    L.append("")
    return "\n".join(L)


def md_plan_90_dias(diag):
    roadmap = sorted(diag.get("roadmap_90_dias", []) or [], key=lambda f: f.get("fase", 0))
    neg = diag.get("negocio", {}) or {}
    nombre = neg.get("nombre_negocio") or neg.get("tipo") or "tu negocio"
    L = []
    L.append("# Tu ruta a 90 días — {}".format(nombre))
    L.append("")
    L.append("El orden exacto, semana a semana. No es una lista de temas; es una secuencia "
             "de acciones con resultado. Una cosa a la vez.")
    L.append("")
    nombres_mes = {1: "Mes 1", 2: "Mes 2", 3: "Mes 3"}
    for fase in roadmap:
        mes = nombres_mes.get(fase.get("fase"), fase.get("rango", ""))
        L.append("## {mes} — {t}".format(mes=mes, t=fase.get("titulo", "")))
        L.append("")
        L.append("*{}*".format(fase.get("objetivo", "")))
        L.append("")
        for ac in fase.get("acciones", []) or []:
            L.append("- [ ] {}".format(ac))
        if fase.get("hito"):
            L.append("")
            L.append("**Hito de la fase:** {}".format(fase["hito"]))
        L.append("")
    L.append("---")
    L.append("")
    L.append("El Mes 3 aterriza en tu meta a 90 días a propósito: cada fase deja un hito "
             "medible, para que veas el avance del negocio mes a mes — no una promesa, "
             "sino procesos funcionando.")
    L.append("")
    return "\n".join(L)


def md_stack(diag, totals):
    autos = diag.get("automatizaciones", []) or []
    neg = diag.get("negocio", {}) or {}
    nombre = neg.get("nombre_negocio") or neg.get("tipo") or "tu negocio"
    # herramientas únicas
    seen = {}
    for a in autos:
        for t in a.get("herramientas", []) or []:
            nm = t.get("nombre", "")
            if nm and nm not in seen:
                seen[nm] = t
    L = []
    L.append("# Tu stack recomendado — {}".format(nombre))
    L.append("")
    L.append("Lo mínimo viable para arrancar. No es exhaustivo: cada herramienta extra se "
             "justifica y se prioriza el plan gratis.")
    L.append("")
    L.append("| Herramienta | Para qué | Costo |")
    L.append("|---|---|---|")
    for nm, t in seen.items():
        costo = t.get("costo_mes_usd", 0)
        costo_str = "Gratis" if (costo is not None and costo <= 0) else "{}/mes".format(money(costo))
        nota = t.get("costo_nota")
        para = t.get("para_que", "")
        if nota:
            para = "{} ({})".format(para, nota)
        L.append("| {nm} | {para} | {c} |".format(nm=nm, para=para, c=costo_str))
    L.append("")
    L.append("**Costo total mensual estimado: {}/mes.**".format(money(totals["costo_total"])))
    L.append("")
    _cats = build_categories(autos)
    if "no_code" in _cats:
        L.append("> Los flujos de conectar apps los armas con **n8n** o **Make** — en los cursos de automatización de la comunidad.")
        L.append("")
    if "claude" in _cats:
        L.append("> Para construir un sistema a la medida sin programar, usa el skill `/crear-agente`.")
        L.append("")
    return "\n".join(L)


def md_quick_win(diag):
    qw = diag.get("quick_win", {}) or {}
    autos = diag.get("automatizaciones", []) or []
    neg = diag.get("negocio", {}) or {}
    nombre = neg.get("nombre_negocio") or neg.get("tipo") or "tu negocio"
    qw_auto = None
    for a in autos:
        if a.get("id") == qw.get("automatizacion_id"):
            qw_auto = a
            break
    qw_auto = qw_auto or (autos[0] if autos else {})

    L = []
    L.append("# Tu quick-win — úsalo hoy, en 5 minutos")
    L.append("")
    L.append("## {}".format(qw_auto.get("titulo", "")))
    L.append("")
    if qw.get("por_que_esta"):
        L.append("*{}*".format(qw["por_que_esta"]))
        L.append("")
    if qw.get("accion_hoy"):
        L.append(qw["accion_hoy"])
        L.append("")
    # El recurso ejecutable HOY: el prompt copy-paste real (cae al primer_paso si falta).
    prompt = qw.get("prompt")
    if prompt:
        L.append("**Pega esto en ChatGPT o Claude (reemplaza lo que está [entre corchetes]):**")
        L.append("")
        L.append("```")
        L.append(prompt)
        L.append("```")
        L.append("")
    elif qw_auto.get("primer_paso"):
        L.append("Empieza juntando esto:")
        L.append("")
        L.append("```")
        L.append(qw_auto["primer_paso"])
        L.append("```")
        L.append("")
    L.append("### Pasos para hoy")
    L.append("")
    for paso in qw.get("pasos_hoy", []) or []:
        txt = str(paso).strip()
        if txt[:2].rstrip(".").isdigit() and ". " in txt[:4]:
            txt = txt.split(". ", 1)[-1].strip()
        L.append("1. {}".format(txt))
    L.append("")
    if qw.get("tiempo_estimado"):
        L.append("**Tiempo estimado:** {}".format(qw["tiempo_estimado"]))
        L.append("")
    if qw.get("resultado_esperado"):
        L.append("**Resultado esperado:** {}".format(qw["resultado_esperado"]))
        L.append("")
    L.append("---")
    L.append("")
    L.append("Cuando esto te funcione, el siguiente paso es automatizarlo del todo "
             "(ver `02-plan-90-dias.md`): con **n8n** o **Make** si es un flujo entre apps, "
             "o con **Claude Code** (`/crear-agente`) si es un sistema a la medida.")
    L.append("")
    return "\n".join(L)


def txt_readme(diag, marca=None):
    marca = marca or cargar_marca()
    neg = diag.get("negocio", {}) or {}
    nombre = neg.get("nombre_negocio") or neg.get("tipo") or "tu negocio"
    fecha = fecha_larga(get(diag, "meta.fecha", ""))
    return (
        "DIAGNÓSTICO DE AUTOMATIZACIÓN — {nombre}\n"
        "Generado por " + marca["nombre"] + " · {fecha}\n"
        "\n"
        "Empieza aquí:\n"
        "1. Abre reporte.html (doble clic) — tu diagnóstico completo. "
        "Para PDF: Cmd/Ctrl+P → Guardar como PDF.\n"
        "2. Abre 04-quick-win.md — algo que puedes usar HOY mismo, en 5 minutos.\n"
        "3. El resto: tu plan a 90 días (02), los procesos con ROI (01) y el stack (03).\n"
    ).format(nombre=nombre, fecha=fecha)


# ─────────────────────────────────────────────────────────────────────────────
# 7. MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) != 3:
        die("Uso: python3 generar_reporte.py <diagnostico.json> <output_dir>")

    json_path, out_dir = sys.argv[1], sys.argv[2]

    if not os.path.isfile(json_path):
        die("No encontré el archivo de diagnóstico: {}".format(json_path))

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            diag = json.load(f)
    except json.JSONDecodeError as e:
        die("El JSON no es válido ({}). Revisa que esté bien formado.".format(e))
    except Exception as e:
        die("No pude leer el diagnóstico: {}".format(e))

    # Validación mínima del contrato.
    if not isinstance(diag, dict):
        die("El diagnóstico debe ser un objeto JSON, no {}.".format(type(diag).__name__))
    if "negocio" not in diag:
        die("Falta el bloque 'negocio' en el diagnóstico (req por el esquema).")
    if not diag.get("automatizaciones"):
        die("El diagnóstico no trae automatizaciones — no hay nada que reportar.")

    # Crear el directorio de salida.
    try:
        os.makedirs(out_dir, exist_ok=True)
    except Exception as e:
        die("No pude crear la carpeta de salida {}: {}".format(out_dir, e))

    totals = derivar_totales(diag)
    marca = cargar_marca()  # marca de la agencia (perfil compartido), con fallback a Horizontes IA

    # Generar y escribir todos los archivos. El reporte se recolorea con el acento de la agencia.
    archivos = {
        "reporte.html": recolorear_html(build_html(diag, marca), marca["color"]),
        "01-procesos-y-roi.md": md_procesos_y_roi(diag, totals),
        "02-plan-90-dias.md": md_plan_90_dias(diag),
        "03-stack-recomendado.md": md_stack(diag, totals),
        "04-quick-win.md": md_quick_win(diag),
        "README.txt": txt_readme(diag, marca),
    }

    for nombre, contenido in archivos.items():
        ruta = os.path.join(out_dir, nombre)
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)
        except Exception as e:
            die("No pude escribir {}: {}".format(ruta, e))

    # Salida clara (sin abrir el browser solo — cross-platform).
    reporte = os.path.join(out_dir, "reporte.html")
    print("✅ Reporte generado: {}".format(os.path.abspath(reporte)))
    print("   Paquete completo en: {}".format(os.path.abspath(out_dir)))
    print("   Para PDF: abre reporte.html y haz Cmd/Ctrl+P → Guardar como PDF.")


if __name__ == "__main__":
    main()
