#!/usr/bin/env node
/**
 * crear-link-stripe.mjs — genera un link de pago de Stripe vía Composio.
 *
 * Envuelve STRIPE_CREATE_PAYMENT_LINK (y STRIPE_CREATE_PRICE para suscripciones)
 * para que el operador NO se equivoque con el pitfall clásico: el monto va en la
 * unidad mínima (centavos). Aquí pasas el monto NORMAL (1500) y el script lo
 * convierte a centavos (150000) por ti.
 *
 * Fuente de los slugs y pitfalls: _research/cobro.md (search real de Composio,
 * toolkit `stripe`). STRIPE_CREATE_PAYMENT_LINK requiere line_items[].quantity y
 * unit_amount en centavos; para suscripciones se omiten invoice/customer creation.
 *
 * USO:
 *   node crear-link-stripe.mjs \
 *     --monto 750 \
 *     --moneda usd \
 *     --descripcion "Anticipo 50% — Asistente de WhatsApp · Sabores de Casa" \
 *     --cliente "Sabores de Casa" \
 *     --fase anticipo
 *
 *   # Retainer mensual (suscripción que cobra sola cada mes):
 *   node crear-link-stripe.mjs --monto 500 --moneda usd \
 *     --descripcion "Mantenimiento mensual · Sabores de Casa" \
 *     --cliente "Sabores de Casa" --fase retainer --recurring month
 *
 *   # Solo ver qué se enviaría, sin ejecutar:
 *   node crear-link-stripe.mjs --monto 750 --moneda usd --descripcion "..." --dry-run
 *
 * Requiere: ~/.composio/composio (CLI) con una cuenta de Stripe conectada.
 */

import { execFileSync } from "node:child_process";
import { homedir } from "node:os";
import { join } from "node:path";

const COMPOSIO = join(homedir(), ".composio", "composio");

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith("--")) {
        args[key] = true; // flag booleano
      } else {
        args[key] = next;
        i++;
      }
    }
  }
  return args;
}

function die(msg) {
  console.error(`\n❌ ${msg}\n`);
  process.exit(1);
}

function runComposio(slug, data, { dryRun } = {}) {
  const payload = JSON.stringify(data);
  const argsList = ["execute", slug, "-d", payload];
  if (dryRun) argsList.push("--dry-run");
  try {
    const out = execFileSync(COMPOSIO, argsList, { encoding: "utf8" });
    return out;
  } catch (err) {
    const stderr = (err.stderr || "").toString();
    const stdout = (err.stdout || "").toString();
    die(
      `Composio falló al ejecutar ${slug}.\n` +
        (stdout ? `\n[salida]\n${stdout}` : "") +
        (stderr ? `\n[error]\n${stderr}` : "") +
        `\n\nProbables causas:\n` +
        `  • No tienes una cuenta de Stripe conectada en Composio → conéctala primero.\n` +
        `  • El monto no quedó en centavos (este script lo maneja, pero revisa el dato).\n` +
        `  • Falta line_items[].quantity (este script lo agrega).\n`
    );
  }
}

const args = parseArgs(process.argv.slice(2));

const montoNum = Number(args.monto);
if (!args.monto || Number.isNaN(montoNum) || montoNum <= 0) {
  die("Falta --monto (en unidad normal, ej. 750 para $750.00).");
}
const moneda = (args.moneda || "usd").toLowerCase();
const descripcion = args.descripcion;
if (!descripcion) die('Falta --descripcion (ej. "Anticipo 50% — ... · Cliente").');

const cliente = args.cliente || "";
const fase = args.fase || "";
const recurring = args.recurring; // "month" | "year" | undefined
const dryRun = Boolean(args["dry-run"]);

// PITFALL #1: Stripe usa la unidad mínima (centavos). 750 → 75000.
const unitAmount = Math.round(montoNum * 100);

const metadata = {};
if (cliente) metadata.cliente = cliente;
if (fase) metadata.fase = fase;

console.log("\n💳 Generando link de pago de Stripe vía Composio");
console.log(`   Monto:       ${moneda.toUpperCase()} ${montoNum.toFixed(2)}  (unit_amount: ${unitAmount} centavos)`);
console.log(`   Concepto:    ${descripcion}`);
if (recurring) console.log(`   Recurrencia: cada ${recurring} (suscripción)`);
if (Object.keys(metadata).length) console.log(`   Metadata:    ${JSON.stringify(metadata)}`);
if (dryRun) console.log("   Modo:        DRY-RUN (no se ejecuta de verdad)");
console.log("");

let lineItem;

if (recurring) {
  // Suscripción: primero un Price recurrente, luego el link con ese price.
  const priceData = {
    currency: moneda,
    unit_amount: unitAmount,
    recurring: { interval: recurring },
    product_data: { name: descripcion },
  };
  const priceOut = runComposio("STRIPE_CREATE_PRICE", priceData, { dryRun });
  console.log("[STRIPE_CREATE_PRICE]\n" + priceOut);

  if (dryRun) {
    console.log("\n(En dry-run no hay price_id real; en ejecución real se usaría data.id del Price.)");
    lineItem = { quantity: 1, price: "price_DRYRUN" };
  } else {
    let priceId;
    try {
      const parsed = JSON.parse(priceOut);
      priceId = parsed?.data?.id || parsed?.id;
    } catch {
      // Si la salida no es JSON puro, intenta extraer price_xxx del texto.
      const m = priceOut.match(/price_[A-Za-z0-9]+/);
      priceId = m ? m[0] : null;
    }
    if (!priceId) {
      die("No pude capturar el price_id del Price recurrente. Revisa la salida de STRIPE_CREATE_PRICE arriba.");
    }
    lineItem = { quantity: 1, price: priceId };
  }
} else {
  // Pago único: price_data inline.
  lineItem = {
    quantity: 1,
    price_data: {
      currency: moneda,
      unit_amount: unitAmount,
      product_data: { name: descripcion },
    },
  };
}

const linkPayload = { line_items: [lineItem] };
if (Object.keys(metadata).length) linkPayload.metadata = metadata;
// Para suscripciones se omiten invoice_creation/customer_creation (chocan con precios recurrentes).

const linkOut = runComposio("STRIPE_CREATE_PAYMENT_LINK", linkPayload, { dryRun });
console.log("[STRIPE_CREATE_PAYMENT_LINK]\n" + linkOut);

// Intenta extraer y resaltar la URL del link.
let url = null;
let livemode = null;
try {
  const parsed = JSON.parse(linkOut);
  url = parsed?.data?.url || parsed?.url;
  livemode = parsed?.data?.livemode ?? parsed?.livemode ?? null;
} catch {
  const m = linkOut.match(/https?:\/\/\S*pay\S*|https?:\/\/buy\.stripe\.com\/\S+/);
  url = m ? m[0] : null;
}

console.log("\n──────────────────────────────────────────────");
if (url) {
  console.log(`✅ LINK DE PAGO (mándaselo al cliente):\n   ${url}`);
} else {
  console.log("⚠️  No pude extraer la URL automáticamente. Búscala como data.url en la salida de arriba.");
}
if (livemode === false) {
  console.log("\n⚠️  livemode = false → este link está en MODO DE PRUEBA (test).");
  console.log("   NO cobra dinero real hasta que actives el modo 'live' en tu cuenta de Stripe.");
}
console.log("──────────────────────────────────────────────\n");
