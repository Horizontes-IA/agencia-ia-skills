#!/usr/bin/env node
/**
 * factura-html.mjs — genera la factura/recibo del cliente como HTML self-contained,
 * profesional, A4, con el acento cyan de Horizontes IA (#00E5FF), listo para
 * imprimir a PDF (abrir en el navegador → Cmd/Ctrl+P → "Guardar como PDF").
 *
 * Recibe los datos por un archivo JSON (--data factura.json) o por stdin.
 * Escupe el HTML a --out factura-<fase>.html (o a stdout si no se da --out).
 *
 * USO:
 *   node factura-html.mjs --data factura.json --out factura-anticipo.html
 *   cat factura.json | node factura-html.mjs > factura-anticipo.html
 *
 * Forma del JSON (todos los strings ya formateados; los montos como string "1,500.00"):
 * {
 *   "folio": "HZ-2026-001",
 *   "fecha_emision": "25 jun 2026",
 *   "fecha_vencimiento": "Al firmar (inmediato)",
 *   "fase_label": "Anticipo 50%",
 *   "moneda": "USD",
 *   "emisor":  { "nombre": "Tu Nombre", "marca_agencia": "Tu Agencia IA", "email": "tu@correo.com", "telefono": "+52 ...", "rfc_o_id_fiscal": "" },
 *   "cliente": { "nombre_negocio": "Sabores de Casa", "contacto": "Marisol", "pais": "México", "rfc_o_id_fiscal": "" },
 *   "conceptos": [
 *     { "descripcion": "Anticipo 50% — Asistente de WhatsApp que cotiza", "cantidad": "1", "precio_unitario": "750.00", "subtotal": "750.00" }
 *   ],
 *   "subtotal": "750.00",
 *   "impuestos_label": "",          // ej. "IVA 16%" — vacío si no aplica
 *   "impuestos_monto": "",          // vacío si no aplica
 *   "total": "750.00",
 *   "saldo_pendiente": "750.00",    // lo que falta del proyecto; vacío si no aplica
 *   "metodo_pago": "Stripe (tarjeta)",
 *   "link_pago": "https://buy.stripe.com/...",     // o "" si es manual
 *   "instrucciones_pago": "",       // texto si es transferencia/manual; "" si hay link
 *   "condiciones_pago": "Anticipo del 50% para iniciar. El 50% restante se factura al entregar.",
 *   "nota": "Este anticipo confirma el inicio del proyecto. El acceso final se entrega cubierto el saldo."
 * }
 */

import { readFileSync } from "node:fs";
import { writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

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
  for (const lit of ["#00E5FF", "#00e5ff", "#22d3ee", "#22D3EE", "#00B8CC", "#00b8cc", "#0e7490", "#0E7490", "#06808f", "#06808F", "#0aa6bd", "#0AA6BD"]) s = s.split(lit).join(hex);
  return s.split("0,229,255").join(rgb).split("0, 229, 255").join(rgb).split("0,184,204").join(rgb).split("0, 184, 204").join(rgb);
}

function parseArgs(argv) {
  const a = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      const k = argv[i].slice(2);
      const n = argv[i + 1];
      if (n === undefined || n.startsWith("--")) a[k] = true;
      else { a[k] = n; i++; }
    }
  }
  return a;
}

const args = parseArgs(process.argv.slice(2));

let raw;
if (args.data) {
  raw = readFileSync(args.data, "utf8");
} else {
  raw = readFileSync(0, "utf8"); // stdin
}

let d;
try {
  d = JSON.parse(raw);
} catch (e) {
  console.error("❌ El JSON de entrada no es válido:", e.message);
  process.exit(1);
}

const esc = (s) =>
  String(s ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");

const moneda = esc(d.moneda || "USD");

const conceptosRows = (d.conceptos || [])
  .map(
    (c) => `
        <tr>
          <td>${esc(c.descripcion)}</td>
          <td class="num">${esc(c.cantidad)}</td>
          <td class="num">${moneda} ${esc(c.precio_unitario)}</td>
          <td class="num">${moneda} ${esc(c.subtotal)}</td>
        </tr>`
  )
  .join("");

const impuestosRow =
  d.impuestos_label && d.impuestos_monto
    ? `<tr><td>${esc(d.impuestos_label)}</td><td class="num">${moneda} ${esc(d.impuestos_monto)}</td></tr>`
    : "";

const saldoRow = d.saldo_pendiente
  ? `<tr class="muted"><td>Saldo pendiente del proyecto</td><td class="num">${moneda} ${esc(d.saldo_pendiente)}</td></tr>`
  : "";

// Sin botón de "Pagar": la mayoría cobra por transferencia o pega su propio link
// (de Stripe/Mercado Pago). Mostramos las instrucciones/datos y, si hay link, como texto.
const pagoBlock = `
      <div class="pay-manual">
        ${d.instrucciones_pago ? `<p class="pay-label">Instrucciones de pago</p>
        <div class="pay-manual-body">${esc(d.instrucciones_pago).replaceAll("\n", "<br>")}</div>` : ""}
        ${d.link_pago ? `<p class="pay-url">Link de pago: <a href="${esc(d.link_pago)}">${esc(d.link_pago)}</a></p>` : ""}
      </div>`;

const emisorFiscal = d.emisor?.rfc_o_id_fiscal
  ? `<div class="small">${esc(d.emisor.rfc_o_id_fiscal)}</div>`
  : "";
const clienteFiscal = d.cliente?.rfc_o_id_fiscal
  ? `<div class="small">${esc(d.cliente.rfc_o_id_fiscal)}</div>`
  : "";

const html = `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Factura ${esc(d.folio)} — ${esc(d.cliente?.nombre_negocio || "")}</title>
<style>
  :root {
    --cyan: #00E5FF;
    --ink: #0c1116;
    --muted: #5b6675;
    --line: #e6eaf0;
    --bg: #ffffff;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: #f4f6f9; color: var(--ink);
    font-family: "Space Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  .page { max-width: 820px; margin: 24px auto; background: var(--bg); padding: 56px 56px 44px;
    box-shadow: 0 6px 30px rgba(12,17,22,.08); border-radius: 14px; }
  .topbar { height: 6px; background: linear-gradient(90deg, var(--cyan), #0aa6bd); border-radius: 6px; margin-bottom: 36px; }
  header { display: flex; justify-content: space-between; align-items: flex-start; gap: 24px; }
  .brand .agency { font-size: 20px; font-weight: 700; letter-spacing: -.2px; }
  .brand .who { color: var(--muted); font-size: 14px; margin-top: 4px; line-height: 1.5; }
  .doc-meta { text-align: right; }
  .doc-meta .label { text-transform: uppercase; letter-spacing: 2px; font-size: 11px; color: var(--cyan); font-weight: 700; }
  .doc-meta .folio { font-size: 22px; font-weight: 700; margin-top: 2px; }
  .doc-meta .fase { display: inline-block; margin-top: 10px; background: rgba(0,229,255,.12); color: #06808f;
    border: 1px solid rgba(0,229,255,.4); padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 600; }
  .parties { display: flex; gap: 40px; margin: 36px 0 8px; }
  .parties .col { flex: 1; }
  .parties .tag { text-transform: uppercase; letter-spacing: 1.5px; font-size: 10px; color: var(--muted); font-weight: 700; margin-bottom: 6px; }
  .parties .name { font-size: 15px; font-weight: 600; }
  .parties .small { font-size: 13px; color: var(--muted); margin-top: 2px; }
  .dates { display: flex; gap: 32px; margin: 18px 0 28px; flex-wrap: wrap; }
  .dates .item .k { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }
  .dates .item .v { font-size: 14px; font-weight: 600; margin-top: 2px; }
  table.items { width: 100%; border-collapse: collapse; margin-top: 8px; }
  table.items thead th { text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;
    color: var(--muted); border-bottom: 2px solid var(--line); padding: 0 0 10px; }
  table.items thead th.num, table.items td.num { text-align: right; }
  table.items td { padding: 14px 0; border-bottom: 1px solid var(--line); font-size: 14px; vertical-align: top; }
  .totals { margin-top: 22px; display: flex; justify-content: flex-end; }
  .totals table { border-collapse: collapse; min-width: 320px; }
  .totals td { padding: 8px 0; font-size: 14px; }
  .totals td.num { text-align: right; }
  .totals tr.muted td { color: var(--muted); font-size: 13px; }
  .totals tr.grand td { border-top: 2px solid var(--ink); padding-top: 14px; font-size: 18px; font-weight: 700; }
  .totals tr.grand td.num { color: #06808f; }
  .pay { margin-top: 36px; border: 1px solid var(--line); border-radius: 12px; padding: 24px; background: #fbfdff; }
  .pay h3 { margin: 0 0 4px; font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--muted); }
  .pay .metodo { font-size: 15px; font-weight: 600; margin-bottom: 14px; }
  .pay-label { font-size: 14px; color: var(--muted); margin: 0 0 12px; }
  .pay-url { font-size: 13px; color: var(--ink); word-break: break-all; margin: 12px 0 4px; }
  .pay-manual-body { font-size: 14px; line-height: 1.6; }
  .conds { margin-top: 16px; font-size: 13px; color: var(--muted); line-height: 1.6; }
  .note { margin-top: 28px; border-left: 3px solid var(--cyan); background: rgba(0,229,255,.06);
    padding: 14px 18px; font-size: 13px; color: #2a3340; border-radius: 0 8px 8px 0; line-height: 1.6; }
  footer { margin-top: 34px; padding-top: 18px; border-top: 1px solid var(--line);
    font-size: 13px; color: var(--muted); display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
  footer .thanks { font-weight: 600; color: var(--ink); }
  @media print {
    html, body { background: #fff; }
    .page { box-shadow: none; margin: 0; max-width: none; border-radius: 0; padding: 24px 28px; }
    @page { size: A4; margin: 14mm; }
  }
</style>
</head>
<body>
  <div class="page">
    <div class="topbar"></div>
    <header>
      <div class="brand">
        <div class="agency">${esc(d.emisor?.marca_agencia || d.emisor?.nombre || "")}</div>
        <div class="who">
          ${esc(d.emisor?.nombre || "")}<br>
          ${esc(d.emisor?.email || "")} · ${esc(d.emisor?.telefono || "")}
          ${emisorFiscal}
        </div>
      </div>
      <div class="doc-meta">
        <div class="label">Factura</div>
        <div class="folio">${esc(d.folio)}</div>
        <div class="fase">${esc(d.fase_label)}</div>
      </div>
    </header>

    <div class="parties">
      <div class="col">
        <div class="tag">Para</div>
        <div class="name">${esc(d.cliente?.nombre_negocio || "")}</div>
        <div class="small">Atención: ${esc(d.cliente?.contacto || "")}</div>
        <div class="small">${esc(d.cliente?.pais || "")}</div>
        ${clienteFiscal}
      </div>
      <div class="col">
        <div class="dates">
          <div class="item"><div class="k">Emisión</div><div class="v">${esc(d.fecha_emision)}</div></div>
          <div class="item"><div class="k">Vence</div><div class="v">${esc(d.fecha_vencimiento)}</div></div>
        </div>
      </div>
    </div>

    <table class="items">
      <thead>
        <tr><th>Descripción</th><th class="num">Cant.</th><th class="num">P. unitario</th><th class="num">Subtotal</th></tr>
      </thead>
      <tbody>${conceptosRows}
      </tbody>
    </table>

    <div class="totals">
      <table>
        <tr><td>Subtotal</td><td class="num">${moneda} ${esc(d.subtotal)}</td></tr>
        ${impuestosRow}
        <tr class="grand"><td>Total a pagar</td><td class="num">${moneda} ${esc(d.total)}</td></tr>
        ${saldoRow}
      </table>
    </div>

    <div class="pay">
      <h3>Cómo pagar</h3>
      <div class="metodo">${esc(d.metodo_pago)}</div>
      ${pagoBlock}
      <div class="conds">${esc(d.condiciones_pago)}</div>
    </div>

    ${d.nota ? `<div class="note">${esc(d.nota)}</div>` : ""}

    <footer>
      <div class="thanks">Gracias por la confianza 🚀</div>
      <div>${esc(d.emisor?.nombre || "")} · ${esc(d.emisor?.marca_agencia || "")} · ${esc(d.emisor?.email || "")}</div>
    </footer>
  </div>
</body>
</html>`;

const htmlFinal = _recolorear(html, _colorMarca());

if (args.out) {
  writeFileSync(args.out, htmlFinal, "utf8");
  console.error(`✅ Factura HTML escrita en ${args.out}`);
  console.error("   Ábrela en el navegador y haz Cmd/Ctrl+P → 'Guardar como PDF' para mandarla al cliente.");
} else {
  process.stdout.write(htmlFinal);
}
