#!/usr/bin/env node
/**
 * generar_propuesta.mjs — Genera el HTML cliente-facing (premium, imprime a PDF)
 * de una propuesta de agencia de automatización con IA, a partir de propuesta.json.
 *
 * Uso:
 *   node generar_propuesta.mjs <ruta/propuesta.json> [ruta/salida.html]
 *
 * Diseño: documento LIMPIO (papel blanco, tinta oscura) con acento cyan #00E5FF
 * de la marca Horizontes IA. Fuentes Space Grotesk (cuerpo) + Instrument Serif
 * italic (acentos). Pensado para imprimir a PDF (A4) y verse de agencia seria.
 *
 * NO inventa datos: solo renderiza lo que viene en el JSON. Degrada con gracia
 * (si una sección falta, la omite). Es la fuente única del HTML; si este script
 * no corre, el SKILL.md tiene el fallback para que Claude escriba el HTML a mano.
 *
 * Contrato de propuesta.json: ver templates/propuesta.schema.md
 */

import { readFileSync, writeFileSync } from "node:fs";
import { resolve, dirname, join } from "node:path";
import { homedir } from "node:os";

// ---------- color de marca (perfil compartido) ----------
function _colorMarca() {
  try {
    const p = JSON.parse(readFileSync(join(homedir(), ".config", "agencia-ia", "perfil.json"), "utf8"));
    const c = ((p.marca || {}).color_acento || "").trim();
    return (c.length === 7 && c[0] === "#") ? c : null;
  } catch { return null; }
}
function _recolorear(s, hex) {
  if (!hex || hex.length !== 7 || hex[0] !== "#") return s;
  const r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16), b = parseInt(hex.slice(5, 7), 16);
  const rgb = `${r},${g},${b}`;
  if (0.299 * r + 0.587 * g + 0.114 * b < 150) s = s.split("--on-accent:#15181e").join("--on-accent:#ffffff");
  for (const lit of ["#00E5FF", "#00e5ff", "#22d3ee", "#22D3EE", "#00B8CC", "#00b8cc", "#0e7490", "#0E7490", "#06808f", "#06808F", "#0aa6bd", "#0AA6BD"]) s = s.split(lit).join(hex);
  return s.split("0,229,255").join(rgb).split("0, 229, 255").join(rgb).split("0,184,204").join(rgb).split("0, 184, 204").join(rgb);
}

// ---------- helpers ----------
const esc = (s) =>
  String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

const money = (n, cur = "USD") => {
  if (n === null || n === undefined || n === "") return "";
  const num = typeof n === "number" ? n : Number(n);
  if (Number.isNaN(num)) return esc(n);
  return "$" + num.toLocaleString("en-US") + (cur && cur !== "USD" ? " " + cur : "");
};

const has = (v) =>
  v !== null && v !== undefined && v !== "" && !(Array.isArray(v) && v.length === 0);

// markdown-lite: **bold**, saltos de línea
const mdLite = (s) =>
  esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/\n/g, "<br>");

// ---------- argumentos ----------
const args = process.argv.slice(2);
if (args.length < 1) {
  console.error("Uso: node generar_propuesta.mjs <propuesta.json> [salida.html]");
  process.exit(1);
}
const jsonPath = resolve(args[0]);
let data;
try {
  data = JSON.parse(readFileSync(jsonPath, "utf8"));
} catch (e) {
  console.error("No pude leer/parsear el JSON:", e.message);
  process.exit(1);
}
const outPath = args[1]
  ? resolve(args[1])
  : join(dirname(jsonPath), "propuesta.html");

// ---------- datos ----------
const cur = data?.meta?.moneda_display || "USD";
const cli = data.cliente || {};
const ag = data.agencia || {};
const opciones = Array.isArray(data.opciones) ? data.opciones : [];
const recomendada = opciones.find((o) => o.recomendada) || opciones[1] || opciones[0];

// ---------- bloques ----------
function logoSVG() {
  // mismo glifo de horizonte que /diagnostico, en cyan
  return (
    '<svg width="46" height="46" viewBox="0 0 48 48" fill="none" aria-hidden="true">' +
    '<circle cx="24" cy="21" r="9" stroke="#00E5FF" stroke-width="2.5"/>' +
    '<path d="M6 34 H42" stroke="#00E5FF" stroke-width="2.5" stroke-linecap="round"/>' +
    "</svg>"
  );
}

function portada() {
  const fecha = data?.meta?.fecha || "";
  const validez = data?.meta?.validez_dias || 14;
  return `
  <header class="cover">
    <div class="brand">
      ${logoSVG()}
      <div class="brand-txt">
        <div class="brand-name">${esc(ag.nombre || "Tu Agencia")}</div>
        <div class="brand-tag">${esc(ag.tagline || "Automatización con IA")}</div>
      </div>
    </div>
    <div class="cover-body">
      <div class="cover-kicker">Propuesta de automatización con IA</div>
      <h1 class="cover-title">${esc(data.titulo || "Propuesta para " + (cli.nombre_negocio || cli.nombre || ""))}</h1>
      ${has(data.subtitulo) ? `<p class="cover-sub accent">${esc(data.subtitulo)}</p>` : ""}
    </div>
    <div class="cover-meta">
      <div><span class="lbl">Preparada para</span><span class="val">${esc(cli.nombre_negocio || cli.nombre || "—")}</span></div>
      ${has(cli.contacto) ? `<div><span class="lbl">Atención</span><span class="val">${esc(cli.contacto)}</span></div>` : ""}
      <div><span class="lbl">Por</span><span class="val">${esc(ag.contacto || ag.nombre || "—")}</span></div>
      ${has(fecha) ? `<div><span class="lbl">Fecha</span><span class="val">${esc(fecha)}</span></div>` : ""}
      <div><span class="lbl">Válida por</span><span class="val">${esc(validez)} días</span></div>
    </div>
  </header>`;
}

function resumenEjecutivo() {
  const r = data.resumen_ejecutivo;
  if (!has(r)) return "";
  const kpis = Array.isArray(r.kpis) ? r.kpis : [];
  return `
  <section class="sec exec">
    <div class="sec-num">01</div>
    <h2>Resumen</h2>
    <p class="exec-lead">${mdLite(r.parrafo || "")}</p>
    ${
      kpis.length
        ? `<div class="kpi-row">${kpis
            .map(
              (k) => `<div class="kpi">
                <div class="kpi-num">${esc(k.valor)}</div>
                <div class="kpi-lbl">${esc(k.etiqueta)}</div>
              </div>`
            )
            .join("")}</div>`
        : ""
    }
    ${
      has(r.costo_del_problema)
        ? `<p class="exec-cost">El costo de no resolverlo: <strong>${mdLite(r.costo_del_problema)}</strong></p>`
        : ""
    }
  </section>`;
}

function problema() {
  const p = data.problema;
  if (!has(p)) return "";
  const puntos = Array.isArray(p.puntos) ? p.puntos : [];
  return `
  <section class="sec">
    <div class="sec-num">02</div>
    <h2>${esc(p.titulo || "El reto que estás viviendo hoy")}</h2>
    ${has(p.intro) ? `<p>${mdLite(p.intro)}</p>` : ""}
    ${
      has(p.cita_cliente)
        ? `<blockquote class="quote"><p class="accent">“${esc(p.cita_cliente)}”</p>${
            has(p.cita_fuente) ? `<cite>— ${esc(p.cita_fuente)}</cite>` : ""
          }</blockquote>`
        : ""
    }
    ${
      puntos.length
        ? `<ul class="pain">${puntos
            .map(
              (pt) =>
                `<li><strong>${esc(pt.titulo || "")}</strong>${
                  has(pt.detalle) ? ` — ${mdLite(pt.detalle)}` : ""
                }</li>`
            )
            .join("")}</ul>`
        : ""
    }
  </section>`;
}

function solucion() {
  const s = data.solucion;
  if (!has(s)) return "";
  const fases = Array.isArray(s.fases) ? s.fases : [];
  return `
  <section class="sec">
    <div class="sec-num">03</div>
    <h2>${esc(s.titulo || "Cómo lo vamos a resolver")}</h2>
    ${has(s.intro) ? `<p class="sol-intro">${mdLite(s.intro)}</p>` : ""}
    ${
      fases.length
        ? `<div class="phases">${fases
            .map(
              (f, i) => `<div class="phase">
                <div class="phase-n">${esc(f.numero || i + 1)}</div>
                <div class="phase-body">
                  <h3>${esc(f.nombre)}</h3>
                  <p>${mdLite(f.descripcion || "")}</p>
                </div>
              </div>`
            )
            .join("")}</div>`
        : ""
    }
    ${
      has(s.nota_confianza_ia)
        ? `<div class="trust"><span class="trust-ico">🛡️</span><p>${mdLite(s.nota_confianza_ia)}</p></div>`
        : ""
    }
  </section>`;
}

function entregables() {
  const e = data.entregables;
  if (!has(e)) return "";
  const items = Array.isArray(e.items) ? e.items : Array.isArray(e) ? e : [];
  if (!items.length) return "";
  return `
  <section class="sec">
    <div class="sec-num">04</div>
    <h2>Lo que recibes</h2>
    <ul class="deliver">${items
      .map(
        (it) =>
          `<li><span class="check">✓</span><div><strong>${esc(
            it.titulo || it
          )}</strong>${has(it.detalle) ? `<span class="d-det">${mdLite(it.detalle)}</span>` : ""}</div></li>`
      )
      .join("")}</ul>
    ${
      has(e.revisiones)
        ? `<p class="fine">Incluye <strong>${esc(e.revisiones)}</strong> de revisiones por entregable.</p>`
        : ""
    }
    ${
      has(e.fuera_de_alcance) && Array.isArray(e.fuera_de_alcance) && e.fuera_de_alcance.length
        ? `<div class="oos"><div class="oos-h">No incluye (para mantener todo claro)</div><ul>${e.fuera_de_alcance
            .map((x) => `<li>${esc(x)}</li>`)
            .join("")}</ul></div>`
        : ""
    }
  </section>`;
}

function timeline() {
  const t = data.timeline;
  if (!has(t)) return "";
  const hitos = Array.isArray(t.hitos) ? t.hitos : Array.isArray(t) ? t : [];
  if (!hitos.length) return "";
  return `
  <section class="sec">
    <div class="sec-num">05</div>
    <h2>El plan, semana por semana</h2>
    ${has(t.intro) ? `<p>${mdLite(t.intro)}</p>` : ""}
    <div class="tl">${hitos
      .map(
        (h) => `<div class="tl-row">
          <div class="tl-when">${esc(h.cuando)}</div>
          <div class="tl-dot"></div>
          <div class="tl-what"><strong>${esc(h.titulo)}</strong>${
            has(h.detalle) ? `<span>${mdLite(h.detalle)}</span>` : ""
          }</div>
        </div>`
      )
      .join("")}</div>
    ${
      has(t.nota_pausa)
        ? `<p class="fine">⏳ ${mdLite(t.nota_pausa)}</p>`
        : ""
    }
  </section>`;
}

function inversion() {
  if (!opciones.length) return "";
  // ordena: muestra de izquierda a derecha tal cual vienen (ancla alta puede ir 1ª en la llamada)
  const cards = opciones
    .map((o) => {
      const incl = Array.isArray(o.incluye) ? o.incluye : [];
      const rec = !!o.recomendada;
      return `<div class="tier ${rec ? "tier-rec" : ""}">
        ${rec ? `<div class="tier-flag">Más elegido</div>` : ""}
        <div class="tier-name">${esc(o.nombre)}</div>
        ${has(o.para_quien) ? `<div class="tier-for">${esc(o.para_quien)}</div>` : ""}
        <div class="tier-price">${money(o.precio_usd, cur)}<span class="tier-cur"> ${esc(o.precio_nota || cur)}</span></div>
        ${
          has(o.retainer_mes_usd)
            ? `<div class="tier-ret">+ ${money(o.retainer_mes_usd, cur)}/mes de soporte</div>`
            : ""
        }
        <ul class="tier-incl">${incl
          .map((x) => `<li>${esc(x)}</li>`)
          .join("")}</ul>
        ${has(o.pago) ? `<div class="tier-pay">${esc(o.pago)}</div>` : ""}
      </div>`;
    })
    .join("");

  const inv = data.inversion || {};
  return `
  <section class="sec invest">
    <div class="sec-num">06</div>
    <h2>Inversión</h2>
    ${has(inv.intro) ? `<p>${mdLite(inv.intro)}</p>` : ""}
    <div class="tiers">${cards}</div>
    ${
      has(inv.ancla_valor)
        ? `<div class="anchor"><p>${mdLite(inv.ancla_valor)}</p></div>`
        : ""
    }
    ${
      has(inv.nota_anticipo)
        ? `<p class="fine">${mdLite(inv.nota_anticipo)}</p>`
        : ""
    }
  </section>`;
}

function pruebaSocial() {
  const ps = data.prueba_social;
  if (!has(ps)) return "";
  const casos = Array.isArray(ps.casos) ? ps.casos : [];
  const logos = Array.isArray(ps.logos) ? ps.logos : [];
  if (!casos.length && !logos.length && !has(ps.intro)) return "";
  return `
  <section class="sec proof">
    <div class="sec-num">07</div>
    <h2>${esc(ps.titulo || "Por qué confiar en nosotros")}</h2>
    ${has(ps.intro) ? `<p>${mdLite(ps.intro)}</p>` : ""}
    ${
      casos.length
        ? `<div class="cases">${casos
            .map(
              (c) => `<div class="case">
                ${has(c.metrica) ? `<div class="case-metric accent">${esc(c.metrica)}</div>` : ""}
                <p class="case-txt">${mdLite(c.texto || "")}</p>
                ${has(c.fuente) ? `<cite>— ${esc(c.fuente)}</cite>` : ""}
              </div>`
            )
            .join("")}</div>`
        : ""
    }
    ${
      logos.length
        ? `<div class="logos">${logos.map((l) => `<span>${esc(l)}</span>`).join("")}</div>`
        : ""
    }
  </section>`;
}

function sobreAgencia() {
  const s = data.sobre_agencia;
  if (!has(s)) return "";
  const tools = Array.isArray(s.herramientas) ? s.herramientas : [];
  return `
  <section class="sec about">
    <div class="sec-num">08</div>
    <h2>Sobre ${esc(ag.nombre || "nosotros")}</h2>
    <p>${mdLite(s.parrafo || "")}</p>
    ${
      tools.length
        ? `<div class="tools"><span class="tools-lbl">Trabajamos con</span>${tools
            .map((t) => `<span class="tool">${esc(t)}</span>`)
            .join("")}</div>`
        : ""
    }
  </section>`;
}

function terminos() {
  const t = data.terminos;
  if (!has(t)) return "";
  const items = Array.isArray(t) ? t : Array.isArray(t.items) ? t.items : [];
  if (!items.length) return "";
  return `
  <section class="sec terms">
    <h2 class="terms-h">Términos clave</h2>
    <ul>${items
      .map(
        (it) =>
          `<li><strong>${esc(it.titulo || "")}:</strong> ${mdLite(it.detalle || it)}</li>`
      )
      .join("")}</ul>
  </section>`;
}

function cta() {
  const c = data.cta;
  if (!has(c)) return "";
  const pasos = Array.isArray(c.pasos) ? c.pasos : [];
  return `
  <section class="sec cta">
    <h2>${esc(c.titulo || "Para empezar")}</h2>
    ${
      pasos.length
        ? `<ol class="steps">${pasos
            .map((p) => `<li>${mdLite(p)}</li>`)
            .join("")}</ol>`
        : ""
    }
    ${
      has(c.boton_url)
        ? `<a class="cta-btn" href="${esc(c.boton_url)}">${esc(c.boton_label || "Aceptar y empezar")}</a>`
        : ""
    }
    ${has(c.urgencia) ? `<p class="cta-fine">${mdLite(c.urgencia)}</p>` : ""}
    ${
      has(c.contacto)
        ? `<p class="cta-contact">${mdLite(c.contacto)}</p>`
        : ""
    }
  </section>`;
}

function footer() {
  return `
  <footer class="foot">
    <div>${esc(ag.nombre || "")}${has(ag.contacto) ? " · " + esc(ag.contacto) : ""}</div>
    <div class="foot-fine">Propuesta válida por ${esc(data?.meta?.validez_dias || 14)} días desde su emisión. Los precios están en ${esc(cur)}.</div>
  </footer>`;
}

// ---------- CSS (documento claro, premium, imprimible) ----------
const CSS = `
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap');
:root{
  --paper:#ffffff; --paper-2:#f6f8fa; --ink:#0f1419; --ink-soft:#3d4753; --muted:#6b7480;
  --line:#e3e8ee; --cyan:#00B8CC; --cyan-bright:#00E5FF; --cyan-soft:#e6fbff;
  --on-accent:#15181e;
  --radius:16px; --radius-sm:11px;
}
*{box-sizing:border-box;}
html{-webkit-print-color-adjust:exact; print-color-adjust:exact;}
body{margin:0; background:var(--paper-2); color:var(--ink);
  font-family:'Space Grotesk',system-ui,-apple-system,sans-serif; font-size:15px; line-height:1.62;}
.doc{max-width:820px; margin:0 auto; background:var(--paper); padding:0 0 8px;
  box-shadow:0 1px 40px rgba(15,20,25,.06);}
.accent{font-family:'Instrument Serif',Georgia,serif; font-style:italic; color:var(--cyan); font-weight:400;}
p{margin:0 0 13px;} strong{font-weight:600;}
h2{font-size:23px; font-weight:600; letter-spacing:-.01em; margin:0 0 14px;}
h3{font-size:16px; font-weight:600; margin:0 0 4px;}
cite{font-style:normal; color:var(--muted); font-size:13px;}
.fine{font-size:13px; color:var(--muted); margin-top:10px;}

/* portada (clara, consistente con el cuerpo) */
.cover{background:#f7f9fc; color:#15181e; padding:42px 54px 40px; border-bottom:1px solid var(--line);}
.brand{display:flex; align-items:center; gap:13px; margin-bottom:42px;}
.brand-name{font-weight:700; font-size:17px; letter-spacing:-.01em; color:#15181e;}
.brand-tag{font-size:12.5px; color:#5b6573; letter-spacing:.02em;}
.cover-kicker{font-size:12px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:var(--cyan-bright); margin-bottom:14px;}
.cover-title{font-size:38px; line-height:1.12; font-weight:700; letter-spacing:-.02em; margin:0 0 12px; max-width:16ch; color:#15181e;}
.cover-sub{font-size:22px; line-height:1.4; color:#5b6573; margin:0; max-width:42ch;}
.cover-sub.accent{color:var(--cyan-bright);}
.cover-meta{display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:14px 26px;
  margin-top:40px; padding-top:24px; border-top:1px solid rgba(17,24,39,.12);}
.cover-meta .lbl{display:block; font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:#5b6573; margin-bottom:3px;}
.cover-meta .val{display:block; font-size:14.5px; font-weight:500; color:#15181e;}

/* secciones */
.sec{position:relative; padding:34px 54px; border-top:1px solid var(--line);}
.sec:first-of-type{border-top:none;}
.sec-num{font-family:'Instrument Serif',Georgia,serif; font-style:italic; font-size:15px; color:var(--cyan);
  position:absolute; left:54px; top:36px; letter-spacing:.02em;}
.sec h2{padding-left:34px;}
.sec p, .sec ul, .sec ol, .sec .phases, .sec .tiers, .sec .tl, .sec .cases, .sec blockquote,
.sec .kpi-row, .sec .deliver, .sec .trust, .sec .anchor, .sec .oos, .sec .tools, .sec .logos{margin-left:34px;}

/* resumen */
.exec-lead{font-size:17px; line-height:1.6;}
.kpi-row{display:flex; flex-wrap:wrap; gap:14px; margin-top:6px; margin-bottom:14px;}
.kpi{flex:1; min-width:140px; background:var(--cyan-soft); border:1px solid #c8f1f7; border-radius:var(--radius-sm); padding:16px 18px;}
.kpi-num{font-family:'Instrument Serif',Georgia,serif; font-style:italic; font-size:34px; color:var(--cyan); line-height:1;}
.kpi-lbl{font-size:12.5px; color:var(--ink-soft); margin-top:6px;}
.exec-cost{background:var(--paper-2); border-left:3px solid var(--cyan); padding:11px 16px; border-radius:0 8px 8px 0;}

/* problema */
.quote{margin:14px 0 14px 34px; padding:4px 0 4px 20px; border-left:3px solid var(--cyan);}
.quote p{font-size:21px; line-height:1.45; margin:0 0 6px;}
.pain{list-style:none; padding:0;}
.pain li{position:relative; padding:8px 0 8px 26px; border-bottom:1px dashed var(--line);}
.pain li:before{content:""; position:absolute; left:4px; top:16px; width:8px; height:8px; border-radius:50%; background:var(--cyan);}

/* solución / fases */
.sol-intro{font-size:16px;}
.phases{display:flex; flex-direction:column; gap:12px; margin-top:6px;}
.phase{display:flex; gap:16px; background:var(--paper-2); border:1px solid var(--line); border-radius:var(--radius-sm); padding:16px 18px;}
.phase-n{flex:none; width:34px; height:34px; border-radius:50%; background:var(--cyan); color:#fff;
  display:flex; align-items:center; justify-content:center; font-weight:700; font-size:16px;}
.phase-body h3{margin-bottom:3px;} .phase-body p{margin:0; color:var(--ink-soft);}
.trust{display:flex; gap:12px; align-items:flex-start; background:var(--cyan-soft); border:1px solid #c8f1f7;
  border-radius:var(--radius-sm); padding:14px 18px; margin-top:14px;}
.trust-ico{font-size:18px; line-height:1.4;} .trust p{margin:0; font-size:14px;}

/* entregables */
.deliver{list-style:none; padding:0;}
.deliver li{display:flex; gap:12px; padding:9px 0; border-bottom:1px solid var(--line);}
.deliver .check{flex:none; width:22px; height:22px; border-radius:50%; background:var(--cyan); color:#fff;
  display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; margin-top:1px;}
.deliver .d-det{display:block; color:var(--ink-soft); font-size:14px;}
.oos{margin-top:16px; background:var(--paper-2); border-radius:var(--radius-sm); padding:14px 18px;}
.oos-h{font-size:12px; font-weight:600; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); margin-bottom:7px;}
.oos ul{margin:0; padding-left:18px; color:var(--ink-soft); font-size:14px;}

/* timeline */
.tl{position:relative; margin-top:6px;}
.tl-row{display:grid; grid-template-columns:96px 22px 1fr; align-items:start; gap:0;}
.tl-when{font-size:13px; font-weight:600; color:var(--cyan); padding:8px 0;}
.tl-dot{position:relative;}
.tl-dot:before{content:""; position:absolute; left:7px; top:12px; width:9px; height:9px; border-radius:50%; background:var(--cyan); z-index:1;}
.tl-row:not(:last-child) .tl-dot:after{content:""; position:absolute; left:11px; top:16px; bottom:-8px; width:1.5px; background:var(--line);}
.tl-what{padding:6px 0 14px;}
.tl-what span{display:block; color:var(--ink-soft); font-size:14px;}

/* inversión */
.tiers{display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:8px;}
.tier{border:1px solid var(--line); border-radius:var(--radius); padding:22px 18px; background:var(--paper); position:relative;}
.tier-rec{border:2px solid var(--cyan); box-shadow:0 8px 28px rgba(0,184,204,.14);}
.tier-flag{position:absolute; top:-11px; left:50%; transform:translateX(-50%); background:var(--cyan); color:#fff;
  font-size:11px; font-weight:700; letter-spacing:.05em; padding:4px 12px; border-radius:20px; white-space:nowrap;}
.tier-name{font-weight:700; font-size:16px;}
.tier-for{font-size:12.5px; color:var(--muted); margin-top:2px; min-height:32px;}
.tier-price{font-family:'Instrument Serif',Georgia,serif; font-style:italic; font-size:33px; color:var(--ink); margin:10px 0 2px; line-height:1;}
.tier-cur{font-family:'Space Grotesk',sans-serif; font-style:normal; font-size:12px; color:var(--muted);}
.tier-ret{font-size:12.5px; color:var(--cyan); font-weight:500; margin-bottom:8px;}
.tier-incl{list-style:none; padding:0; margin:12px 0 0; font-size:13.5px;}
.tier-incl li{padding:6px 0 6px 20px; position:relative; color:var(--ink-soft); border-top:1px solid var(--line);}
.tier-incl li:before{content:"✓"; position:absolute; left:0; top:6px; color:var(--cyan); font-weight:700;}
.tier-pay{margin-top:12px; font-size:12px; color:var(--muted); padding-top:10px; border-top:1px dashed var(--line);}
.anchor{background:var(--paper-2); border-left:3px solid var(--cyan); padding:13px 18px; border-radius:0 8px 8px 0; margin-top:16px;}
.anchor p{margin:0; font-size:14.5px;}

/* prueba social */
.cases{display:grid; gap:13px; margin-top:6px;}
.case{background:var(--paper-2); border:1px solid var(--line); border-radius:var(--radius-sm); padding:18px 20px;}
.case-metric{font-size:27px; line-height:1; margin-bottom:8px;}
.case-txt{margin:0 0 6px; font-size:15px;}
.logos{display:flex; flex-wrap:wrap; gap:10px; margin-top:14px;}
.logos span{font-size:13px; color:var(--ink-soft); background:var(--paper-2); border:1px solid var(--line); border-radius:20px; padding:6px 14px;}

/* sobre / tools */
.tools{margin-top:12px; display:flex; flex-wrap:wrap; gap:8px; align-items:center;}
.tools-lbl{font-size:12px; color:var(--muted); margin-right:4px;}
.tool{font-size:12.5px; font-weight:500; background:var(--cyan-soft); color:var(--cyan); border:1px solid #c8f1f7; border-radius:7px; padding:4px 11px;}

/* términos */
.terms{background:var(--paper-2);}
.terms-h{padding-left:0; font-size:16px;}
.terms ul{margin:0; padding-left:18px; font-size:13.5px; color:var(--ink-soft);}
.terms ul li{margin-bottom:6px;}

/* CTA */
.cta{background:var(--paper-2); color:var(--ink); border-radius:0; padding:38px 54px 40px; border-top:3px solid var(--cyan);}
.cta h2{padding-left:0; color:var(--ink);}
.cta .steps{margin-left:0; padding-left:0; list-style:none; counter-reset:s; margin-bottom:22px;}
.cta .steps li{counter-increment:s; position:relative; padding:8px 0 8px 42px; font-size:15.5px; color:var(--ink);}
.cta .steps li:before{content:counter(s); position:absolute; left:0; top:7px; width:27px; height:27px; border-radius:50%;
  background:var(--cyan-bright); color:var(--on-accent); font-weight:700; font-size:14px; display:flex; align-items:center; justify-content:center;}
.cta-btn{display:inline-block; background:var(--cyan-bright); color:var(--on-accent); font-weight:700; font-size:16px;
  padding:14px 34px; border-radius:11px; text-decoration:none;}
.cta-fine{color:var(--muted); font-size:13px; margin-top:16px;}
.cta-contact{color:var(--ink-soft); font-size:14px; margin-top:6px;}

/* footer */
.foot{padding:22px 54px 30px; font-size:12.5px; color:var(--muted); border-top:1px solid var(--line);}
.foot-fine{margin-top:4px; font-size:11.5px;}

/* print */
@media print{
  p,li{orphans:3; widows:3;}  /* sin líneas sueltas al pie/inicio de página */
  /* fuerza fondo blanco total: sin franja oscura del body/--paper-2 en los bordes */
  body{background:#fff; font-size:11.5pt;}
  .doc{box-shadow:none; max-width:none; margin:0; width:100%; background:#fff;}
  @page{size:A4; margin:15mm 0;}
  /* margen vertical 15mm = respiro arriba/abajo en cada página; el padding lateral propio
     de cada bloque (54px ≈ 14mm) da el margen horizontal, sin texto pegado al borde */
  .cover, .cta{-webkit-print-color-adjust:exact; print-color-adjust:exact;}
  /* las secciones FLUYEN entre páginas (antes break-inside:avoid empujaba secciones largas
     a una página nueva y dejaba medio folio en blanco) */
  .sec{break-inside:auto;}
  /* bloques atómicos: nunca se parten a la mitad entre páginas */
  .tier, .phase, .case, .tl-row, .kpi, .kpi-row, .deliver li,
  .exec-cost, blockquote, .quote, .trust, .oos, .anchor, .terms, .logos, .tools{break-inside:avoid;}
  /* ningún título se queda huérfano al final de la página: va con su contenido */
  h2,h3{break-after:avoid; page-break-after:avoid; break-inside:avoid;}
  /* la intro que sigue al título se pega al título Y a su primer bloque:
     el encabezado nunca queda solo (con su intro) al pie de una página */
  .sec h2 + p{break-after:avoid; page-break-after:avoid;}
  /* los contenedores grid/flex-column NO se fragmentan entre páginas (el motor los
     trata como bloque atómico y empujan todo a la hoja siguiente dejando un hueco):
     en print los volvemos flujo para que sus tarjetas se repartan y llenen la página */
  .cases, .phases{display:block;}
  .cases .case, .phases .phase{margin-bottom:12px;}
  .cases .case:last-child, .phases .phase:last-child{margin-bottom:0;}
  a[href]:after{content:"";}
}
@media (max-width:680px){
  .sec, .cover, .cta, .foot{padding-left:22px; padding-right:22px;}
  .sec-num{left:22px;} .sec h2{padding-left:0;}
  .sec p,.sec ul,.sec ol,.sec .phases,.sec .tiers,.sec .tl,.sec .cases,.sec blockquote,
  .sec .kpi-row,.sec .deliver,.sec .trust,.sec .anchor,.sec .oos,.sec .tools,.sec .logos{margin-left:0;}
  .tiers{grid-template-columns:1fr;}
  .cover-title{font-size:30px;}
}
`;

// ---------- ensamble ----------
const html = `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(data.titulo || "Propuesta")} — ${esc(ag.nombre || "")}</title>
<style>${CSS}</style>
</head>
<body>
<div class="doc">
${portada()}
${resumenEjecutivo()}
${problema()}
${solucion()}
${entregables()}
${timeline()}
${inversion()}
${pruebaSocial()}
${sobreAgencia()}
${terminos()}
${cta()}
${footer()}
</div>
</body>
</html>`;

writeFileSync(outPath, _recolorear(html, _colorMarca()), "utf8");
console.log(outPath);
