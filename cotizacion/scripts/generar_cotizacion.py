#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_cotizacion.py — Generador de la COTIZACIÓN cliente-facing de la suite agencia-ia-skills.

Consume un `cotizacion.json` (esquema en _design/schema.md) y escribe, en <output_dir>:

    cotizacion.html   ← el documento que VE EL CLIENTE (self-contained, dark + cyan, imprime a PDF)
    cotizacion.md     ← versión markdown editable / archivable

Uso:
    python3 scripts/generar_cotizacion.py <cotizacion.json> <output_dir>

Reglas de diseño (idénticas a /diagnostico, para que la suite se vea coherente):
- Python SOLO stdlib. Corre igual en Mac/Win/Linux. Cero pip install.
- HTML con TODO el CSS inline en un <style>, fuentes vía @import con fallback a
  system-ui, logo SVG inline. Cero assets externos, cero JS. Imprime limpio a PDF.
- El generador NUNCA inventa datos: si un campo opcional falta, omite la sección
  o usa un fallback declarado. RECALCULA los totales del lado del servidor
  (no confía en que la IA sume bien): subtotal de cada opción, anticipo, etc.
- Premium SIN pushy: nada de countdowns ni "oferta limitada". La urgencia única y
  permitida es la VIGENCIA de la cotización (palanca de cierre estándar B2B).

Fuentes de la estructura (ver _research/cotizacion.md):
- 3 tiers good/better/best + efecto ancla (freshproposals, HVAC Know It All)
- ROI monetario atado al diagnóstico (optimizesmart)
- Anticipo 50/50, vigencia 14 días (digitalapplied, dealhub)
- Fuera de alcance explícito para evitar scope creep (Arsum)
"""

import sys
import os
import json
import html
import datetime


def _color_marca():
    """Color de acento de la agencia desde el perfil compartido (o None)."""
    path = os.path.expanduser("~/.config/agencia-ia/perfil.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            p = json.load(f)
        c = ((p.get("marca") or {}).get("color_acento") or "").strip()
        return c if (len(c) == 7 and c[0] == "#") else None
    except Exception:
        return None


def _recolorear(s, hex_color):
    """Reemplaza el cyan de Horizontes por el acento de la agencia en TODO el HTML."""
    if not hex_color or len(hex_color) != 7 or hex_color[0] != "#":
        return s
    try:
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    except ValueError:
        return s
    rgb = "{},{},{}".format(r, g, b)
    for lit in ("#00E5FF", "#00e5ff", "#22d3ee", "#22D3EE", "#00B8CC", "#00b8cc", "#0e7490", "#0E7490", "#06808f", "#06808F", "#0aa6bd", "#0AA6BD"):
        s = s.replace(lit, hex_color)
    return s.replace("0,229,255", rgb).replace("0, 229, 255", rgb).replace("0,184,204", rgb).replace("0, 184, 204", rgb)


# ─────────────────────────────────────────────────────────────────────────────
# 0. UTILIDADES
# ─────────────────────────────────────────────────────────────────────────────

def die(msg):
    sys.stderr.write("❌ " + msg + "\n")
    sys.exit(1)


def esc(s):
    """Escapa texto dinámico (nombre del cliente, descripciones) antes de inyectarlo
    al HTML. Obligatorio: un nombre puede traer < > & " que rompan el documento."""
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


def get(d, path, default=None):
    """Acceso seguro a campos anidados 'a.b.c'. Devuelve default si falta un eslabón."""
    cur = d
    for key in path.split("."):
        if isinstance(cur, dict) and key in cur and cur[key] is not None:
            cur = cur[key]
        else:
            return default
    return cur


def money(n, simbolo="$"):
    """152 -> '$152', 3408 -> '$3,408'. None/'' -> ''."""
    if n is None or n == "":
        return ""
    try:
        n = float(n)
    except (TypeError, ValueError):
        return ""
    if abs(n - round(n)) < 0.01:
        return "{}{:,}".format(simbolo, int(round(n)))
    return "{}{:,.2f}".format(simbolo, n)


# ─────────────────────────────────────────────────────────────────────────────
# 1. RECÁLCULO SERVER-SIDE (no confiar en que la IA sume)
# ─────────────────────────────────────────────────────────────────────────────

def derivar(coti):
    """Recalcula los totales de cada opción y del anticipo desde sus partidas.
    Si una opción ya trae `precio_total`, lo respeta como verdad SOLO si no hay
    line items; si hay line items, suma esos (la suma manda)."""
    moneda = get(coti, "comercial.moneda", "USD")
    simbolo = "$"  # USD/MXN/etc todos usan $; la moneda se etiqueta aparte
    opciones = coti.get("opciones", []) or []

    for op in opciones:
        items = op.get("incluye", []) or []
        # Cada item puede traer precio (opcional). Si ningún item trae precio,
        # usamos el precio_total declarado de la opción.
        suma_items = 0
        algun_precio = False
        for it in items:
            p = it.get("precio")
            if p is not None:
                try:
                    suma_items += float(p)
                    algun_precio = True
                except (TypeError, ValueError):
                    pass
        if algun_precio:
            op["_precio_calc"] = suma_items
        else:
            op["_precio_calc"] = op.get("precio_total")

    return {"moneda": moneda, "simbolo": simbolo}


def calc_anticipo(precio_total, pct):
    """Anticipo = precio_total * pct. Devuelve (anticipo, saldo) o (None, None)."""
    if precio_total is None or pct is None:
        return (None, None)
    try:
        anticipo = round(float(precio_total) * float(pct) / 100.0, 2)
        saldo = round(float(precio_total) - anticipo, 2)
        return (anticipo, saldo)
    except (TypeError, ValueError):
        return (None, None)


# ─────────────────────────────────────────────────────────────────────────────
# 2. LOGO SVG INLINE (idéntico a /diagnostico — coherencia de marca)
# ─────────────────────────────────────────────────────────────────────────────

LOGO_SVG = (
    '<svg width="34" height="34" viewBox="0 0 48 48" fill="none" '
    'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<circle cx="24" cy="21" r="9" stroke="#00E5FF" stroke-width="2.5"/>'
    '<path d="M6 34 H42" stroke="#00E5FF" stroke-width="2.5" stroke-linecap="round"/>'
    '</svg>'
)


# ─────────────────────────────────────────────────────────────────────────────
# 3. CSS (todo inline, dark + cyan, con print) — reusa el sistema de /diagnostico
# ─────────────────────────────────────────────────────────────────────────────

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap');

:root{
  --bg:#0a0a0c; --surface:#111317; --surface-2:#16191f;
  --border:rgba(255,255,255,.08);
  --text:#e6e6e6; --muted:#8b93a1;
  --cyan:#00E5FF; --cyan-2:#22d3ee; --cyan-soft:rgba(0,229,255,.10);
  --good:#34d399; --warn:#fbbf24; --orange:#fb923c; --dim:#64748b;
  --radius:16px; --radius-sm:10px;
  --shadow:0 20px 60px -20px rgba(0,0,0,.7);
  --glow:0 0 40px -8px rgba(0,229,255,.35);
}

*{box-sizing:border-box;}
html{-webkit-text-size-adjust:100%;}
body{
  margin:0; background:var(--bg); color:var(--text);
  font-family:'Space Grotesk',system-ui,-apple-system,sans-serif;
  font-size:16px; line-height:1.65; -webkit-font-smoothing:antialiased;
}
.wrap{max-width:840px; margin:0 auto; padding:0 28px;}
.accent{font-family:'Instrument Serif',Georgia,serif; font-style:italic; color:var(--cyan-2); font-weight:400;}
a{color:var(--cyan); text-decoration:none;}
.micro-label{display:block; font-size:11px; letter-spacing:.14em; text-transform:uppercase;
  color:var(--muted); margin-bottom:8px; font-weight:600;}

section{padding:52px 0; border-top:1px solid var(--border);}
section:first-of-type{border-top:none;}
.sec-head{margin-bottom:30px;}
.sec-head h2{font-size:29px; font-weight:700; margin:0; letter-spacing:-.02em;}
.sec-head .rule{display:block; width:54px; height:2px; background:var(--cyan); margin:14px 0 0;}
.sec-sub{color:var(--muted); margin:14px 0 0; font-size:15.5px;}
p{margin:0 0 14px;}
.lead{font-size:17px; line-height:1.7;}

/* ── PORTADA ── */
.cover{min-height:92vh; display:flex; flex-direction:column; justify-content:center;
  padding:60px 0; border-top:none; position:relative; overflow:hidden;}
.cover::before{content:""; position:absolute; inset:0;
  background:radial-gradient(ellipse 60% 50% at 18% 12%, rgba(0,229,255,.14), transparent 60%);
  pointer-events:none;}
.cover .wrap{position:relative; z-index:1;}
.lockup{display:flex; align-items:center; justify-content:space-between; margin-bottom:60px;}
.lockup-left{display:flex; align-items:center; gap:11px;}
.wordmark{font-size:12px; letter-spacing:.20em; text-transform:uppercase; color:var(--cyan); font-weight:600;}
.lockup-date{font-size:13px; color:var(--muted);}
.eyebrow{font-size:12px; letter-spacing:.20em; text-transform:uppercase; color:var(--cyan); font-weight:600; margin-bottom:20px;}
.cover h1{font-size:50px; font-weight:700; line-height:1.06; margin:0 0 18px; letter-spacing:-.03em;}
.cover-sub{font-size:24px; line-height:1.4; color:var(--text); max-width:680px; margin:0 0 28px;}
.cover-meta{font-size:14.5px; color:var(--muted); margin:0 0 14px;}
.cover-meta .sep{color:var(--cyan); margin:0 9px;}
.cover-para{display:flex; gap:48px; flex-wrap:wrap; margin-top:34px;}
.cover-para .cp-item .cp-k{font-size:11px; letter-spacing:.12em; text-transform:uppercase; color:var(--muted);}
.cover-para .cp-item .cp-v{font-size:16px; font-weight:600; margin-top:5px;}

/* ── callout / problema ── */
.callout{background:var(--surface); border:1px solid var(--border); border-left:3px solid var(--cyan);
  border-radius:var(--radius-sm); padding:22px 26px; margin-top:24px;}
.callout .micro-label{color:var(--cyan);}
.callout p{margin:0; font-size:15.5px;}
.recognition{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
  padding:28px 32px;}
.recognition .q{font-family:'Instrument Serif',Georgia,serif; font-style:italic; font-size:23px; line-height:1.45; color:var(--text); margin:0;}
.recognition .q::before{content:"\\201C"; color:var(--cyan);}
.recognition .q::after{content:"\\201D"; color:var(--cyan);}
.recognition .attr{font-size:13.5px; color:var(--muted); margin:14px 0 0;}

/* ── ROI band ── */
.roi-band{display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin:6px 0 22px;}
.roi-card{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:24px;}
.roi-num{font-family:'Instrument Serif',Georgia,serif; font-style:italic; font-size:38px; color:var(--cyan); line-height:1;}
.roi-label{font-size:12px; letter-spacing:.10em; text-transform:uppercase; color:var(--text); margin-top:10px; font-weight:600;}
.roi-ctx{font-size:13px; color:var(--muted); margin:8px 0 0; line-height:1.45;}

/* ── scope ── */
.scope-grid{display:grid; grid-template-columns:1fr 1fr; gap:18px;}
.scope-card{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:24px 26px;}
.scope-card h3{font-size:15px; margin:0 0 14px; display:flex; align-items:center; gap:9px;}
.scope-card.in h3{color:var(--good);}
.scope-card.out h3{color:var(--muted);}
.scope-list{list-style:none; margin:0; padding:0;}
.scope-list li{position:relative; padding:7px 0 7px 26px; font-size:14.5px; border-bottom:1px solid var(--border);}
.scope-list li:last-child{border-bottom:none;}
.scope-card.in .scope-list li::before{content:"\\2713"; position:absolute; left:0; top:7px; color:var(--good); font-weight:700;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.scope-card.out .scope-list li::before{content:"\\2014"; position:absolute; left:0; top:7px; color:var(--dim);}

/* ── proceso / fases ── */
.timeline{position:relative; margin-top:8px;}
.phase{display:flex; gap:20px; padding-bottom:8px;}
.phase-num{flex:none; width:40px; height:40px; border-radius:50%; background:var(--cyan-soft);
  border:1px solid rgba(0,229,255,.3); color:var(--cyan); font-weight:700; font-size:16px;
  display:flex; align-items:center; justify-content:center;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.phase-body{flex:1; padding-bottom:22px; border-bottom:1px solid var(--border); margin-bottom:22px;}
.phase:last-child .phase-body{border-bottom:none;}
.phase-body h3{font-size:17px; margin:6px 0 4px;}
.phase-body .phase-dur{font-size:12.5px; color:var(--cyan-2); letter-spacing:.04em; text-transform:uppercase;}
.phase-body p{font-size:14.5px; color:var(--muted); margin:8px 0 0;}

/* ── TIERS good/better/best ── */
.tiers{display:grid; grid-template-columns:repeat(3,1fr); gap:18px; margin-top:8px;}
.tier{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
  padding:28px 24px; display:flex; flex-direction:column; opacity:.96;}
.tier.featured{border:1.5px solid var(--cyan); box-shadow:var(--glow); opacity:1; position:relative;}
.tier-flag{position:absolute; top:-12px; left:50%; transform:translateX(-50%);
  background:var(--cyan); color:var(--bg); font-size:11px; font-weight:700; letter-spacing:.08em;
  text-transform:uppercase; padding:5px 16px; border-radius:99px; white-space:nowrap;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.tier-name{font-size:14px; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); font-weight:600;}
.tier.featured .tier-name{color:var(--cyan);}
.tier-price{font-family:'Instrument Serif',Georgia,serif; font-style:italic; font-size:40px; color:var(--text); line-height:1; margin:12px 0 2px;}
.tier.featured .tier-price{color:var(--cyan);}
.tier-price .cur{font-size:15px; font-style:normal; color:var(--muted); font-family:'Space Grotesk',sans-serif; margin-left:6px; letter-spacing:.04em;}
.tier-tagline{font-size:13.5px; color:var(--muted); margin:0 0 18px; min-height:38px;}
.tier-feats{list-style:none; margin:0 0 18px; padding:0; flex:1;}
.tier-feats li{position:relative; padding:7px 0 7px 24px; font-size:14px; border-bottom:1px solid var(--border);}
.tier-feats li:last-child{border-bottom:none;}
.tier-feats li::before{content:"\\2713"; position:absolute; left:0; top:7px; color:var(--cyan); font-weight:700; font-size:13px;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.tier-feats li.muted{color:var(--dim);}
.tier-feats li.muted::before{content:"\\2014"; color:var(--dim);}
.tier-pay{font-size:12.5px; color:var(--muted); padding-top:14px; border-top:1px solid var(--border);}
.tier-pay b{color:var(--text);}

/* ── retainer line ── */
.retainer{background:var(--surface); border:1px dashed rgba(0,229,255,.35); border-radius:var(--radius);
  padding:26px 30px; margin-top:22px; display:flex; align-items:center; justify-content:space-between; gap:24px; flex-wrap:wrap;}
.retainer .rt-l{flex:1; min-width:240px;}
.retainer h3{margin:0 0 6px; font-size:18px;}
.retainer p{margin:0; font-size:14px; color:var(--muted);}
.retainer .rt-price{font-family:'Instrument Serif',Georgia,serif; font-style:italic; font-size:30px; color:var(--cyan-2);}
.retainer .rt-price small{font-size:14px; color:var(--muted); font-style:normal; font-family:'Space Grotesk',sans-serif;}

/* ── términos ── */
.terms-grid{display:grid; grid-template-columns:1fr 1fr; gap:16px;}
.term{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-sm); padding:20px 22px;}
.term .micro-label{color:var(--cyan);}
.term .t-val{font-size:16px; font-weight:600;}
.term .t-ctx{font-size:13px; color:var(--muted); margin-top:6px;}
.vigencia{background:var(--cyan-soft); border:1px solid var(--cyan); border-radius:var(--radius);
  box-shadow:var(--glow); padding:24px 28px; margin-top:22px;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.vigencia .v-title{font-size:13px; letter-spacing:.10em; text-transform:uppercase; color:var(--cyan); font-weight:700;}
.vigencia .v-date{font-size:22px; font-weight:700; margin:8px 0 4px;}
.vigencia p{margin:0; font-size:14px; color:var(--text);}

/* ── cierre / firma ── */
.closing-card{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:36px 38px;}
.closing-card h2{font-size:26px; margin:0 0 12px; letter-spacing:-.02em;}
.closing-card p{font-size:15.5px; color:var(--muted);}
.cta-btn{display:inline-block; margin-top:18px; background:var(--cyan); color:var(--bg);
  font-weight:700; font-size:15px; padding:14px 28px; border-radius:99px; letter-spacing:.01em;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.sign-row{display:flex; gap:40px; margin-top:34px; flex-wrap:wrap;}
.sign-box{flex:1; min-width:220px;}
.sign-line{border-bottom:1px solid var(--muted); height:42px; margin-bottom:8px;}
.sign-box .sl{font-size:12.5px; color:var(--muted);}

.supuestos{background:var(--surface-2); border:1px solid var(--border); border-radius:var(--radius-sm); padding:22px 26px;}
.supuestos ul{margin:0; padding-left:18px;}
.supuestos li{font-size:13px; color:var(--muted); margin:6px 0; line-height:1.5;}

.doc-footer{text-align:center; padding:40px 0 64px; color:var(--muted); font-size:12.5px;}
.doc-footer .lf{display:inline-flex; align-items:center; gap:8px; margin-bottom:10px;}

@media (max-width:680px){
  .wrap{padding:0 20px;}
  .cover h1{font-size:37px;} .cover-sub{font-size:20px;}
  .tiers{grid-template-columns:1fr;} .roi-band{grid-template-columns:1fr;}
  .scope-grid,.terms-grid{grid-template-columns:1fr;}
  .sec-head h2{font-size:24px;}
}

@media print{
  *{-webkit-print-color-adjust:exact !important; print-color-adjust:exact !important;}
  @page{size:A4; margin:15mm;}
  body{background:var(--bg) !important; font-size:11.5pt;}
  .wrap{max-width:100%; padding:0;}
  section{padding:20px 0;}
  .cover{min-height:auto; padding:20px 0 14px;}
  .cover h1{font-size:38px;}
  .tier{break-inside:avoid;} .tiers{break-inside:avoid;}
  .roi-card,.scope-card,.term,.phase,.retainer{break-inside:avoid;}
  .vigencia,.recognition,.callout,.closing-card,.supuestos{break-inside:avoid;}
  .sec-head{break-after:avoid;}
}
"""


# ─────────────────────────────────────────────────────────────────────────────
# 4. ENSAMBLADO DEL HTML
# ─────────────────────────────────────────────────────────────────────────────

def build_html(coti):
    d = derivar(coti)
    moneda = d["moneda"]
    cli = coti.get("cliente", {}) or {}
    ag = coti.get("agencia", {}) or {}
    com = coti.get("comercial", {}) or {}

    nombre_cliente = cli.get("nombre_negocio") or cli.get("contacto") or "tu negocio"
    contacto = cli.get("contacto") or ""
    folio = com.get("folio") or ""
    fecha = com.get("fecha") or datetime.date.today().isoformat()
    nombre_agencia = ag.get("nombre") or "Tu Agencia"

    parts = []
    parts.append('<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    parts.append('<title>Cotizacion — {} — {}</title>'.format(esc(nombre_cliente), esc(nombre_agencia)))
    parts.append('<style>{}</style></head><body>'.format(CSS))

    # ── PORTADA ──
    titulo = com.get("titulo") or "Propuesta de automatizacion con IA"
    subtitulo = com.get("subtitulo") or "Una solucion a la medida de {}".format(nombre_cliente)
    parts.append('<header class="cover"><div class="wrap">')
    parts.append('<div class="lockup"><div class="lockup-left">{}<span class="wordmark">{}</span></div>'
                 '<span class="lockup-date">{}</span></div>'.format(LOGO_SVG, esc(nombre_agencia), esc(fecha)))
    parts.append('<div class="eyebrow">Cotizacion</div>')
    parts.append('<h1>{}</h1>'.format(esc(titulo)))
    parts.append('<p class="cover-sub">{}</p>'.format(esc(subtitulo)))
    meta_bits = ["Preparada para <b style='color:#e6e6e6'>{}</b>".format(esc(nombre_cliente))]
    if contacto:
        meta_bits.append(esc(contacto))
    if folio:
        meta_bits.append("Folio {}".format(esc(folio)))
    parts.append('<p class="cover-meta">' + '<span class="sep">·</span>'.join(meta_bits) + '</p>')
    # paratexto inferior (preparada por / vigencia)
    cp = []
    cp.append('<div class="cp-item"><div class="cp-k">Preparada por</div><div class="cp-v">{}</div></div>'.format(esc(nombre_agencia)))
    vig = com.get("vigencia_fecha")
    if vig:
        cp.append('<div class="cp-item"><div class="cp-k">Valida hasta</div><div class="cp-v">{}</div></div>'.format(esc(vig)))
    cp.append('<div class="cp-item"><div class="cp-k">Moneda</div><div class="cp-v">{}</div></div>'.format(esc(moneda)))
    parts.append('<div class="cover-para">' + "".join(cp) + '</div>')
    parts.append('</div></header>')

    # ── 1. RESUMEN EJECUTIVO ──
    resumen = com.get("resumen_ejecutivo")
    if resumen:
        parts.append('<section><div class="wrap"><div class="sec-head"><h2>Resumen</h2><span class="rule"></span></div>')
        parts.append('<p class="lead">{}</p>'.format(esc(resumen)))
        parts.append('</div></section>')

    # ── 2. EL PROBLEMA (en sus palabras) ──
    prob = coti.get("problema", {}) or {}
    if prob.get("texto") or prob.get("frase_cliente"):
        parts.append('<section><div class="wrap"><div class="sec-head"><h2>El problema que vamos a resolver</h2><span class="rule"></span></div>')
        if prob.get("frase_cliente"):
            parts.append('<div class="recognition"><p class="q">{}</p>'.format(esc(prob["frase_cliente"])))
            if prob.get("frase_attr"):
                parts.append('<p class="attr">{}</p>'.format(esc(prob["frase_attr"])))
            parts.append('</div>')
        if prob.get("texto"):
            parts.append('<p class="lead" style="margin-top:22px">{}</p>'.format(esc(prob["texto"])))
        parts.append('</div></section>')

    # ── 3. LA SOLUCIÓN ──
    sol = coti.get("solucion", {}) or {}
    if sol.get("texto"):
        parts.append('<section><div class="wrap"><div class="sec-head"><h2>La solucion</h2><span class="rule"></span></div>')
        parts.append('<p class="lead">{}</p>'.format(esc(sol["texto"])))
        ent = sol.get("entregables", []) or []
        if ent:
            parts.append('<div class="callout"><span class="micro-label">Lo que vas a tener funcionando</span><p>'
                         + " · ".join(esc(e) for e in ent) + '</p></div>')
        parts.append('</div></section>')

    # ── 4. RESULTADOS / ROI ──
    roi = coti.get("roi", {}) or {}
    cards = roi.get("cards", []) or []
    if cards:
        parts.append('<section><div class="wrap"><div class="sec-head"><h2>Lo que esto te regresa</h2><span class="rule"></span>')
        if roi.get("subtitulo"):
            parts.append('<p class="sec-sub">{}</p>'.format(esc(roi["subtitulo"])))
        parts.append('</div><div class="roi-band">')
        for c in cards[:3]:
            parts.append('<div class="roi-card"><div class="roi-num">{}</div>'
                         '<div class="roi-label">{}</div>'.format(esc(c.get("num", "")), esc(c.get("label", ""))))
            if c.get("ctx"):
                parts.append('<p class="roi-ctx">{}</p>'.format(esc(c["ctx"])))
            parts.append('</div>')
        parts.append('</div>')
        if roi.get("nota"):
            parts.append('<p class="sec-sub" style="margin-top:4px">{}</p>'.format(esc(roi["nota"])))
        parts.append('</div></section>')

    # ── 5. ALCANCE: incluye / no incluye ──
    sc = coti.get("alcance", {}) or {}
    incluye = sc.get("incluye", []) or []
    no_incluye = sc.get("no_incluye", []) or []
    if incluye or no_incluye:
        parts.append('<section><div class="wrap"><div class="sec-head"><h2>Alcance</h2><span class="rule"></span>'
                     '<p class="sec-sub">Que entra en este proyecto y que no. Asi evitamos malentendidos despues.</p></div>')
        parts.append('<div class="scope-grid">')
        if incluye:
            parts.append('<div class="scope-card in"><h3>Incluye</h3><ul class="scope-list">'
                         + "".join('<li>{}</li>'.format(esc(x)) for x in incluye) + '</ul></div>')
        if no_incluye:
            parts.append('<div class="scope-card out"><h3>No incluye (este proyecto)</h3><ul class="scope-list">'
                         + "".join('<li>{}</li>'.format(esc(x)) for x in no_incluye) + '</ul></div>')
        parts.append('</div></div></section>')

    # ── 6. PROCESO / FASES ──
    fases = coti.get("proceso", []) or []
    if fases:
        parts.append('<section><div class="wrap"><div class="sec-head"><h2>Como vamos a trabajar</h2><span class="rule"></span></div>')
        parts.append('<div class="timeline">')
        for i, f in enumerate(fases, 1):
            parts.append('<div class="phase"><div class="phase-num">{}</div><div class="phase-body">'.format(i))
            if f.get("duracion"):
                parts.append('<div class="phase-dur">{}</div>'.format(esc(f["duracion"])))
            parts.append('<h3>{}</h3>'.format(esc(f.get("titulo", ""))))
            if f.get("descripcion"):
                parts.append('<p>{}</p>'.format(esc(f["descripcion"])))
            parts.append('</div></div>')
        parts.append('</div></div></section>')

    # ── 7. PRECIO: TIERS good/better/best ──
    opciones = coti.get("opciones", []) or []
    if opciones:
        parts.append('<section><div class="wrap"><div class="sec-head"><h2>Tu inversion</h2><span class="rule"></span>'
                     '<p class="sec-sub">Tres formas de avanzar. La recomendada esta marcada — es el mejor balance entre alcance y resultado.</p></div>')
        parts.append('<div class="tiers">')
        for op in opciones:
            featured = op.get("recomendada", False)
            cls = "tier featured" if featured else "tier"
            precio = op.get("_precio_calc")
            parts.append('<div class="{}">'.format(cls))
            if featured:
                flag = op.get("flag") or "Recomendada"
                parts.append('<div class="tier-flag">{}</div>'.format(esc(flag)))
            parts.append('<div class="tier-name">{}</div>'.format(esc(op.get("nombre", ""))))
            parts.append('<div class="tier-price">{}<span class="cur">{}</span></div>'.format(
                esc(money(precio)), esc(moneda)))
            if op.get("tagline"):
                parts.append('<div class="tier-tagline">{}</div>'.format(esc(op["tagline"])))
            feats = op.get("incluye", []) or []
            if feats:
                parts.append('<ul class="tier-feats">')
                for it in feats:
                    if isinstance(it, dict):
                        txt = it.get("texto", "")
                        muted = it.get("muted", False)
                    else:
                        txt = it
                        muted = False
                    parts.append('<li class="{}">{}</li>'.format("muted" if muted else "", esc(txt)))
                parts.append('</ul>')
            # pago dentro del tier
            pct = op.get("anticipo_pct", com.get("anticipo_pct"))
            anticipo, saldo = calc_anticipo(precio, pct)
            if anticipo is not None:
                esquema = op.get("esquema_pago") or "{}% anticipo / {}% al entregar".format(
                    int(pct), 100 - int(pct))
                parts.append('<div class="tier-pay"><b>{}</b> de anticipo<br>{}</div>'.format(
                    esc(money(anticipo)), esc(esquema)))
            parts.append('</div>')
        parts.append('</div>')

        # retainer (línea aparte, SIEMPRE ofrecerlo — research)
        rt = coti.get("retainer")
        if rt and rt.get("precio_mes"):
            parts.append('<div class="retainer"><div class="rt-l"><h3>{}</h3><p>{}</p></div>'
                         '<div class="rt-price">{}<small>/mes</small></div></div>'.format(
                             esc(rt.get("titulo", "Mantenimiento mensual")),
                             esc(rt.get("descripcion", "Monitoreo, ajustes y mejoras continuas para que el sistema siga rindiendo.")),
                             esc(money(rt["precio_mes"]))))
        parts.append('</div></section>')

    # ── 8. TÉRMINOS + VIGENCIA ──
    parts.append('<section><div class="wrap"><div class="sec-head"><h2>Terminos</h2><span class="rule"></span></div>')
    parts.append('<div class="terms-grid">')
    terms = []
    if com.get("anticipo_pct") is not None:
        terms.append(("Anticipo", "{}% al firmar".format(int(com["anticipo_pct"])),
                      "El trabajo arranca cuando entra el anticipo."))
    if com.get("forma_pago"):
        terms.append(("Forma de pago", com["forma_pago"], com.get("forma_pago_nota", "")))
    if com.get("tiempo_entrega"):
        terms.append(("Tiempo de entrega", com["tiempo_entrega"], com.get("tiempo_entrega_nota", "")))
    if com.get("garantia"):
        terms.append(("Soporte incluido", com["garantia"], com.get("garantia_nota", "")))
    for k, v, ctx in terms:
        parts.append('<div class="term"><span class="micro-label">{}</span><div class="t-val">{}</div>'.format(esc(k), esc(v)))
        if ctx:
            parts.append('<div class="t-ctx">{}</div>'.format(esc(ctx)))
        parts.append('</div>')
    parts.append('</div>')
    if com.get("vigencia_fecha"):
        parts.append('<div class="vigencia"><div class="v-title">Vigencia de esta cotizacion</div>'
                     '<div class="v-date">{}</div>'
                     '<p>Despues de esta fecha los precios y el alcance pueden ajustarse. Si quieres avanzar, lo ideal es cerrar antes.</p></div>'.format(
                         esc(com["vigencia_fecha"])))
    parts.append('</div></section>')

    # ── 9. CIERRE + FIRMA ──
    cierre = coti.get("cierre", {}) or {}
    parts.append('<section><div class="wrap"><div class="closing-card">')
    parts.append('<h2>{}</h2>'.format(esc(cierre.get("titulo", "Damos el siguiente paso?"))))
    parts.append('<p>{}</p>'.format(esc(cierre.get("texto",
                 "Cuando elijas la opcion que mas te late, te mando el link de pago del anticipo y arrancamos. Cualquier duda, aqui estoy."))))
    if cierre.get("cta_label"):
        href = cierre.get("cta_url") or "#"
        parts.append('<a class="cta-btn" href="{}">{}</a>'.format(esc(href), esc(cierre["cta_label"])))
    # firmas
    parts.append('<div class="sign-row">'
                 '<div class="sign-box"><div class="sign-line"></div><div class="sl">Por {}</div></div>'
                 '<div class="sign-box"><div class="sign-line"></div><div class="sl">Por {} (cliente)</div></div>'
                 '</div>'.format(esc(nombre_agencia), esc(nombre_cliente)))
    parts.append('</div>')

    # supuestos / notas al pie
    sup = coti.get("supuestos", []) or []
    if sup:
        parts.append('<div class="supuestos" style="margin-top:26px"><span class="micro-label">Notas y supuestos</span><ul>'
                     + "".join('<li>{}</li>'.format(esc(s)) for s in sup) + '</ul></div>')
    parts.append('</div></section>')

    # ── FOOTER ──
    parts.append('<footer class="doc-footer"><div class="wrap">'
                 '<div class="lf">{}<span class="wordmark">{}</span></div>'
                 '<div>Cotizacion generada {} · Documento confidencial</div>'
                 '</div></footer>'.format(LOGO_SVG, esc(nombre_agencia), esc(fecha)))

    parts.append('</body></html>')
    return "".join(parts)


# ─────────────────────────────────────────────────────────────────────────────
# 5. VERSIÓN MARKDOWN (editable / archivable)
# ─────────────────────────────────────────────────────────────────────────────

def build_md(coti):
    d = derivar(coti)
    moneda = d["moneda"]
    cli = coti.get("cliente", {}) or {}
    ag = coti.get("agencia", {}) or {}
    com = coti.get("comercial", {}) or {}
    nombre_cliente = cli.get("nombre_negocio") or cli.get("contacto") or "el cliente"
    nombre_agencia = ag.get("nombre") or "Tu Agencia"
    L = []

    L.append("# {}".format(com.get("titulo", "Cotizacion")))
    L.append("")
    L.append("**Preparada para:** {}  ".format(nombre_cliente))
    if cli.get("contacto"):
        L.append("**Contacto:** {}  ".format(cli["contacto"]))
    L.append("**Preparada por:** {}  ".format(nombre_agencia))
    L.append("**Fecha:** {}  ".format(com.get("fecha", datetime.date.today().isoformat())))
    if com.get("folio"):
        L.append("**Folio:** {}  ".format(com["folio"]))
    if com.get("vigencia_fecha"):
        L.append("**Valida hasta:** {}  ".format(com["vigencia_fecha"]))
    L.append("**Moneda:** {}".format(moneda))
    L.append("")
    L.append("---")
    L.append("")

    if com.get("resumen_ejecutivo"):
        L.append("## Resumen")
        L.append("")
        L.append(com["resumen_ejecutivo"])
        L.append("")

    prob = coti.get("problema", {}) or {}
    if prob.get("frase_cliente") or prob.get("texto"):
        L.append("## El problema que vamos a resolver")
        L.append("")
        if prob.get("frase_cliente"):
            L.append("> *\"{}\"*".format(prob["frase_cliente"]))
            L.append("")
        if prob.get("texto"):
            L.append(prob["texto"])
            L.append("")

    sol = coti.get("solucion", {}) or {}
    if sol.get("texto"):
        L.append("## La solucion")
        L.append("")
        L.append(sol["texto"])
        L.append("")
        for e in (sol.get("entregables", []) or []):
            L.append("- {}".format(e))
        if sol.get("entregables"):
            L.append("")

    roi = coti.get("roi", {}) or {}
    if roi.get("cards"):
        L.append("## Lo que esto te regresa")
        L.append("")
        for c in roi["cards"]:
            L.append("- **{}** — {}{}".format(
                c.get("num", ""), c.get("label", ""),
                (": " + c["ctx"]) if c.get("ctx") else ""))
        L.append("")
        if roi.get("nota"):
            L.append("_{}_".format(roi["nota"]))
            L.append("")

    sc = coti.get("alcance", {}) or {}
    if sc.get("incluye") or sc.get("no_incluye"):
        L.append("## Alcance")
        L.append("")
        if sc.get("incluye"):
            L.append("**Incluye:**")
            L.append("")
            for x in sc["incluye"]:
                L.append("- {}".format(x))
            L.append("")
        if sc.get("no_incluye"):
            L.append("**No incluye (este proyecto):**")
            L.append("")
            for x in sc["no_incluye"]:
                L.append("- {}".format(x))
            L.append("")

    fases = coti.get("proceso", []) or []
    if fases:
        L.append("## Como vamos a trabajar")
        L.append("")
        for i, f in enumerate(fases, 1):
            dur = " ({})".format(f["duracion"]) if f.get("duracion") else ""
            L.append("{}. **{}**{}".format(i, f.get("titulo", ""), dur))
            if f.get("descripcion"):
                L.append("   {}".format(f["descripcion"]))
        L.append("")

    opciones = coti.get("opciones", []) or []
    if opciones:
        L.append("## Tu inversion")
        L.append("")
        L.append("| Opcion | Precio | Anticipo | Incluye |")
        L.append("|---|---|---|---|")
        for op in opciones:
            precio = op.get("_precio_calc")
            pct = op.get("anticipo_pct", com.get("anticipo_pct"))
            anticipo, _ = calc_anticipo(precio, pct)
            feats = []
            for it in (op.get("incluye", []) or []):
                feats.append(it.get("texto", "") if isinstance(it, dict) else it)
            marca = " ⭐" if op.get("recomendada") else ""
            L.append("| **{}**{} | {} {} | {} | {} |".format(
                op.get("nombre", ""), marca,
                money(precio), moneda,
                money(anticipo) if anticipo is not None else "—",
                "; ".join(feats)))
        L.append("")
        rt = coti.get("retainer")
        if rt and rt.get("precio_mes"):
            L.append("**{}:** {} /mes — {}".format(
                rt.get("titulo", "Mantenimiento mensual"),
                money(rt["precio_mes"]),
                rt.get("descripcion", "")))
            L.append("")

    L.append("## Terminos")
    L.append("")
    if com.get("anticipo_pct") is not None:
        L.append("- **Anticipo:** {}% al firmar. El trabajo arranca cuando entra el anticipo.".format(int(com["anticipo_pct"])))
    if com.get("forma_pago"):
        L.append("- **Forma de pago:** {}".format(com["forma_pago"]))
    if com.get("tiempo_entrega"):
        L.append("- **Tiempo de entrega:** {}".format(com["tiempo_entrega"]))
    if com.get("garantia"):
        L.append("- **Soporte incluido:** {}".format(com["garantia"]))
    if com.get("vigencia_fecha"):
        L.append("- **Vigencia:** esta cotizacion es valida hasta el {}.".format(com["vigencia_fecha"]))
    L.append("")

    cierre = coti.get("cierre", {}) or {}
    L.append("## {}".format(cierre.get("titulo", "Siguiente paso")))
    L.append("")
    L.append(cierre.get("texto", "Cuando elijas la opcion, te mando el link de pago del anticipo y arrancamos."))
    L.append("")

    sup = coti.get("supuestos", []) or []
    if sup:
        L.append("---")
        L.append("")
        L.append("**Notas y supuestos:**")
        L.append("")
        for s in sup:
            L.append("- {}".format(s))
        L.append("")

    L.append("---")
    L.append("")
    L.append("_Cotizacion generada por {} · Documento confidencial._".format(nombre_agencia))
    L.append("")
    return "\n".join(L)


# ─────────────────────────────────────────────────────────────────────────────
# 6. MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        die("Uso: python3 generar_cotizacion.py <cotizacion.json> <output_dir>")
    json_path = sys.argv[1]
    out_dir = sys.argv[2]

    if not os.path.isfile(json_path):
        die("No encuentro el JSON: " + json_path)
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            coti = json.load(f)
    except json.JSONDecodeError as e:
        die("El JSON tiene un error de sintaxis: " + str(e))

    os.makedirs(out_dir, exist_ok=True)

    html_out = _recolorear(build_html(coti), _color_marca())
    md_out = build_md(coti)

    html_path = os.path.join(out_dir, "cotizacion.html")
    md_path = os.path.join(out_dir, "cotizacion.md")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_out)

    print("✅ Cotizacion generada:")
    print("   " + html_path + "   (abre en el navegador → Imprimir → Guardar como PDF)")
    print("   " + md_path + "   (markdown editable)")


if __name__ == "__main__":
    main()
