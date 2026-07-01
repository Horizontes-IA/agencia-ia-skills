#!/usr/bin/env node
// curl-tool.mjs — arma el `curl` (para n8n / Make) que ejecuta una app conectada vía Composio.
// Usa el SDK @composio/core (que ya instala el kit) — NO requiere el CLI de composio.
//
// Uso:
//   node curl-tool.mjs <app> [búsqueda]        → lista los tools de la app (para elegir un SLUG)
//   node curl-tool.mjs --slug <SLUG> [userId]  → imprime el curl listo para ese SLUG
//
// La API key se lee del .env (COMPOSIO_API_KEY = la del dashboard, ak_...). En el curl
// que imprime va como placeholder — nunca se filtra la key.

import { config as loadEnv } from "dotenv";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { Composio } from "@composio/core";

const __dir = dirname(fileURLToPath(import.meta.url));
loadEnv({ path: join(__dir, ".env") });
const key = process.env.COMPOSIO_API_KEY;
if (!key) {
  console.error("Falta COMPOSIO_API_KEY en el .env del skill (la del dashboard, empieza con ak_).");
  process.exit(1);
}
const composio = new Composio({ apiKey: key });
const EXEC = "https://backend.composio.dev/api/v3/tools/execute";

// nombres comunes → slug de toolkit de Composio
const APPS = { correo: "gmail", gmail: "gmail", calendario: "googlecalendar", calendar: "googlecalendar",
  whatsapp: "whatsapp", hojas: "googlesheets", sheets: "googlesheets", drive: "googledrive",
  notion: "notion", slack: "slack", hubspot: "hubspot", github: "github", outlook: "outlook", trello: "trello" };

const argv = process.argv.slice(2);

function asArray(x) { return Array.isArray(x) ? x : (x?.items || []); }

if (argv[0] === "--slug") {
  const slug = (argv[1] || "").toUpperCase();
  const userId = argv[2] || "<userId-del-cliente>";
  const t = await composio.tools.getRawComposioToolBySlug(slug);
  const tool = Array.isArray(t) ? t[0] : t;
  if (!tool?.slug) { console.error("No encontré el tool:", slug); process.exit(1); }
  const props = tool.inputParameters?.properties || {};
  const required = tool.inputParameters?.required || [];
  const args = {};
  for (const [k, v] of Object.entries(props)) {
    if (k === "user_id") continue; // user_id va al nivel de arriba del body
    args[k] = v.default ?? v.example ??
      (v.type === "boolean" ? false : (v.type === "integer" || v.type === "number" ? 0 : `<${k}>`));
  }
  const body = { user_id: userId, arguments: args };
  console.log(`# ${tool.slug} — ${(tool.description || "").split("\n")[0]}`);
  if (required.length) console.log(`# requeridos: ${required.join(", ")}`);
  console.log(`curl -X POST '${EXEC}/${tool.slug}' \\
  -H 'x-api-key: <TU_ak_KEY_DEL_DASHBOARD>' \\
  -H 'Content-Type: application/json' \\
  -d '${JSON.stringify(body, null, 2)}'`);
} else {
  const app = APPS[(argv[0] || "").toLowerCase()] || (argv[0] || "").toLowerCase();
  const query = (argv[1] || "").toLowerCase();
  if (!app) {
    console.error("Uso:\n  node curl-tool.mjs <app> [búsqueda]        (lista tools)\n  node curl-tool.mjs --slug <SLUG> [userId]  (arma el curl)");
    process.exit(1);
  }
  const tools = asArray(await composio.tools.getRawComposioTools({ toolkits: [app], limit: 50 }));
  const list = query ? tools.filter(t => (t.slug + " " + (t.description || "")).toLowerCase().includes(query)) : tools;
  console.log(`Tools de '${app}'${query ? ` que coinciden con "${query}"` : ""}:`);
  for (const t of list.slice(0, 15)) console.log(`  ${t.slug}  —  ${(t.description || "").split("\n")[0].slice(0, 70)}`);
  if (!list.length) console.log("  (ninguno; revisa el nombre de la app o quita la búsqueda)");
  console.log(`\nLuego:  node curl-tool.mjs --slug <SLUG> <userId>`);
}
