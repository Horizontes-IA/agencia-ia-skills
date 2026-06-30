#!/usr/bin/env python3
"""
generar_contrato_html.py — Convierte un contrato.json lleno en un HTML self-contained,
profesional, dark + acento cyan (#00E5FF), que imprime limpio a PDF (Cmd+P → Guardar como PDF).

Uso:
    python3 generar_contrato_html.py <ruta>/contrato.json [<ruta>/contrato.html]

El JSON describe los datos del trato (ver scripts/contrato.schema.json para el contrato de campos).
Markdown del cuerpo de cláusulas: se pasa ya armado en data["clausulas"] (lista de {titulo, cuerpo_md}).
Si falta data["clausulas"], el script usa el cuerpo embebido por defecto (las 19 secciones investigadas)
y reemplaza placeholders con data["campos"].

FALLBACK: si no hay Python o el script falla, el SKILL.md instruye a Claude a escribir el HTML a mano
replicando este diseño. Este script es la vía cómoda, no la única.
"""
import json
import os
import re
import sys
import html as _html
from pathlib import Path


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


# ---------- helpers ----------
def esc(s):
    return _html.escape(str(s if s is not None else ""))


def md_inline(s):
    """markdown inline mínimo: **bold**, `code`, escapa el resto."""
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


def md_block(text):
    """Convierte un bloque markdown sencillo (párrafos, listas -, tablas |, subtítulos ###) a HTML."""
    out = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        # blockquote
        if line.lstrip().startswith(">"):
            buf = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                buf.append(lines[i].lstrip()[1:].strip())
                i += 1
            out.append('<blockquote>' + md_inline(" ".join(buf)) + '</blockquote>')
            continue
        # subtítulo ###
        if line.startswith("### "):
            out.append("<h4>" + md_inline(line[4:]) + "</h4>")
            i += 1
            continue
        # tabla
        if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", lines[i + 1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and "|" in lines[i]:
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ['<table><thead><tr>'] + ["<th>" + md_inline(h) + "</th>" for h in header] + ["</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join("<td>" + md_inline(c) + "</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue
        # lista
        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append("<li>" + md_inline(re.sub(r"^\s*[-*]\s+", "", lines[i])) + "</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        # párrafo
        out.append("<p>" + md_inline(line) + "</p>")
        i += 1
    return "\n".join(out)


def fill(text, campos):
    """Reemplaza {{PLACEHOLDER}} con campos['PLACEHOLDER'] (deja el placeholder marcado si falta)."""
    def rep(m):
        k = m.group(1).strip()
        if k in campos and campos[k] not in (None, ""):
            return str(campos[k])
        return "<span class='ph'>[" + k.lower().replace("_", " ") + "]</span>"
    return re.sub(r"\{\{([A-Z0-9_]+)\}\}", rep, text)


CSS = """
:root{
  --bg:#080810; --surface:#0f0f1a; --surface-2:#15151f; --border:#23232f;
  --text:#e8e8ef; --dim:#9a9ab0; --cyan:#00E5FF; --cyan-2:#22d3ee;
  --cyan-soft:rgba(0,229,255,.10); --warn:#fbbf24;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);
  font-family:'Space Grotesk',system-ui,-apple-system,sans-serif;
  font-size:15px;line-height:1.65;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
.page{max-width:820px;margin:0 auto;padding:56px 60px 80px;}
.accent{font-family:'Instrument Serif',Georgia,serif;font-style:italic;color:var(--cyan-2);font-weight:400;}
code{font-family:ui-monospace,'SF Mono',Menlo,monospace;background:var(--surface-2);
  border:1px solid var(--border);border-radius:5px;padding:1px 6px;font-size:.86em;color:var(--cyan-2);}
.ph{color:var(--warn);font-style:italic;font-weight:600;}

header.cover{border-bottom:1px solid var(--border);padding-bottom:28px;margin-bottom:36px;
  background:radial-gradient(ellipse 70% 60% at 12% 0%, rgba(0,229,255,.10), transparent 60%);}
.brandmark{display:flex;align-items:center;gap:10px;margin-bottom:22px;}
.brandmark .nm{font-weight:700;letter-spacing:.5px;}
.brandmark .nm b{color:var(--cyan);}
h1{font-size:30px;line-height:1.2;margin:0 0 8px;font-weight:700;}
.cover .meta{color:var(--dim);font-size:13.5px;margin-top:14px;display:flex;gap:18px;flex-wrap:wrap;}
.cover .meta b{color:var(--text);font-weight:600;}

h2{font-size:19px;margin:38px 0 4px;font-weight:700;display:flex;align-items:baseline;gap:10px;}
h2 .n{color:var(--cyan);font-family:'Instrument Serif',Georgia,serif;font-style:italic;
  font-size:22px;min-width:30px;}
h2 + .rule{display:block;width:46px;height:2px;background:var(--cyan);margin:0 0 14px 40px;}
h4{font-size:15.5px;margin:20px 0 4px;color:var(--cyan-2);font-weight:600;}
p{margin:9px 0;}
ul{margin:9px 0 9px 4px;padding-left:20px;}
li{margin:5px 0;}
strong{color:#fff;font-weight:600;}

blockquote{border-left:3px solid var(--cyan);background:var(--cyan-soft);
  margin:14px 0;padding:11px 18px;border-radius:0 8px 8px 0;color:var(--text);font-size:14px;}

table{width:100%;border-collapse:collapse;margin:14px 0;font-size:14px;
  border:1px solid var(--border);border-radius:10px;overflow:hidden;}
th{background:var(--cyan-soft);color:var(--cyan-2);text-align:left;padding:10px 13px;
  font-weight:600;font-size:13px;}
td{padding:10px 13px;border-top:1px solid var(--border);vertical-align:top;}

.sign{margin-top:40px;display:grid;grid-template-columns:1fr 1fr;gap:26px;}
.sign .box{border:1px solid var(--border);border-radius:12px;padding:22px;background:var(--surface);}
.sign .line{border-bottom:1px solid var(--dim);height:46px;margin-bottom:8px;}
.sign .role{color:var(--cyan);font-weight:700;font-size:13px;text-transform:uppercase;
  letter-spacing:.5px;margin-bottom:14px;}
.sign .who{font-weight:600;}
.sign .org{color:var(--dim);font-size:13px;}

.disclaimer{margin-top:44px;border:1px solid var(--border);border-left:3px solid var(--warn);
  background:rgba(251,191,36,.06);border-radius:0 10px 10px 0;padding:16px 20px;
  color:var(--dim);font-size:13px;}
.disclaimer strong{color:var(--warn);}

.preambulo{margin:8px 0 6px;font-size:14.5px;line-height:1.7;}
.declaraciones,.firmas{margin-top:30px;}
.sign-row{display:flex;gap:48px;margin-top:30px;flex-wrap:wrap;}
.sign{flex:1;min-width:220px;text-align:center;}
.sign-line{border-top:1.5px solid var(--text);margin:48px 0 8px;}
.sign-sub{color:var(--dim);font-size:12.5px;margin-top:2px;}

footer{margin-top:40px;padding-top:18px;border-top:1px solid var(--border);
  color:var(--dim);font-size:12px;text-align:center;}

@page{margin:14mm;}
@media print{
  /* El contrato se firma en papel/PDF claro. Forzamos tinta OSCURA: si solo
     invertimos el fondo a blanco, el texto y las negritas (heredados del tema
     dark) quedan blancos sobre blanco = ilegibles. Esto lo evita. */
  body{background:#fff !important; color:#111 !important;}
  .page{padding:0;max-width:100%;}
  h1,h2,h3,h4,h5,p,li,td,th,div,span,em{color:#111 !important;}
  strong,b{color:#000 !important;}
  .accent,[class*="accent"]{color:#0e7490 !important;}
  .disclaimer{background:#fff8e1 !important; color:#5b4a00 !important;}
  *{-webkit-print-color-adjust:exact; print-color-adjust:exact;}
  /* cortes de página: el título de cláusula nunca se queda huérfano ni se parte;
     las firmas y declaraciones no se cortan a la mitad. */
  h2,h3{break-after:avoid; page-break-after:avoid; break-inside:avoid;}
  .firmas,.sign-row,.declaraciones h2{break-inside:avoid;}
  section{break-inside:auto;}
}
"""

LOGO_SVG = (
    '<svg width="34" height="34" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<circle cx="24" cy="21" r="9" stroke="#00E5FF" stroke-width="2.5"/>'
    '<path d="M6 34 H42" stroke="#00E5FF" stroke-width="2.5" stroke-linecap="round"/>'
    '</svg>'
)


def build_html(data):
    campos = data.get("campos", {})
    agencia = campos.get("NOMBRE_LEGAL_AGENCIA") or data.get("agencia", "Tu Agencia")
    titulo = data.get("titulo", "Contrato de Prestación de Servicios de Automatización con IA")
    clausulas = data.get("clausulas")  # lista de {titulo, cuerpo_md}; si None, el SKILL la arma

    sections_html = []
    if clausulas:
        for idx, c in enumerate(clausulas, 1):
            t = fill(c.get("titulo", f"Cláusula {idx}"), campos)
            body = md_block(fill(c.get("cuerpo_md", ""), campos))
            sections_html.append(
                f'<section><h2><span class="n">{idx}</span>{t}</h2><span class="rule"></span>{body}</section>'
            )
    else:
        sections_html.append(
            '<section><blockquote>El cuerpo de cláusulas no se incluyó en el JSON. '
            'Pasa <code>data["clausulas"]</code> con las 19 secciones del template '
            '<code>templates/contrato.md</code>, o deja que el skill las arme.</blockquote></section>'
        )

    body = "\n".join(sections_html)

    # Preámbulo (recital de las partes) y Declaraciones — opcionales, antes de las cláusulas.
    preambulo = data.get("preambulo", "")
    preambulo_html = f'<section class="preambulo">{md_block(fill(preambulo, campos))}</section>' if preambulo else ""
    declaraciones = data.get("declaraciones", "")
    declaraciones_html = (
        '<section class="declaraciones"><h2>Declaraciones</h2><span class="rule"></span>'
        + md_block(fill(declaraciones, campos)) + '</section>'
    ) if declaraciones else ""

    # Firmas (2 columnas) — desde campos, salvo que data["firmas"] traiga texto propio.
    rep_ag = campos.get("REPRESENTANTE_AGENCIA") or campos.get("NOMBRE_LEGAL_AGENCIA") or agencia
    leg_ag = campos.get("NOMBRE_LEGAL_AGENCIA") or agencia
    leg_cl = campos.get("NOMBRE_LEGAL_CLIENTE", "EL CLIENTE")
    rep_cl = campos.get("REPRESENTANTE_CLIENTE", "") or leg_cl
    firmas_html = (
        '<section class="firmas"><h2>Firmas</h2><span class="rule"></span>'
        '<div class="sign-row">'
        f'<div class="sign"><div class="sign-line"></div><b>{esc(rep_ag)}</b>'
        f'<div class="sign-sub">{esc(leg_ag)} · EL PRESTADOR</div></div>'
        f'<div class="sign"><div class="sign-line"></div><b>{esc(rep_cl)}</b>'
        f'<div class="sign-sub">{esc(leg_cl)} · EL CLIENTE</div></div>'
        '</div></section>'
    )

    meta = [
        ('Folio', campos.get("FOLIO", "—")),
        ('Fecha', campos.get("FECHA", "—")),
        ('Lugar', campos.get("CIUDAD_PAIS", "—")),
    ]
    meta_html = "".join(f'<span><b>{esc(m[0])}:</b> {esc(m[1])}</span>' for m in meta)

    return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(titulo)} — {esc(agencia)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><div class="page">
<header class="cover">
  <div class="brandmark">{LOGO_SVG}<span class="nm"><b>{esc(agencia)}</b></span></div>
  <h1>{esc(titulo)}</h1>
  <div class="meta">{meta_html}</div>
</header>
{preambulo_html}
{declaraciones_html}
{body}
{firmas_html}
<div class="disclaimer"><strong>Aviso importante — esto no es asesoría legal.</strong>
Este documento es un modelo de trabajo, no constituye asesoría jurídica. Las leyes de prestación de
servicios, propiedad intelectual y protección de datos varían según el país. Para tratos de monto alto
o de riesgo elevado, haz que un abogado de tu país lo revise antes de firmar.</div>
<footer>{agencia} · <span class="accent">documento de prestación de servicios</span></footer>
</div></body></html>"""


def main():
    if len(sys.argv) < 2:
        print("uso: python3 generar_contrato_html.py <contrato.json> [salida.html]")
        sys.exit(1)
    src = Path(sys.argv[1])
    data = json.loads(src.read_text(encoding="utf-8"))
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".html")
    html_out = _recolorear(build_html(data), _color_marca())
    out.write_text(html_out, encoding="utf-8")
    print(f"OK -> {out}")


if __name__ == "__main__":
    main()
