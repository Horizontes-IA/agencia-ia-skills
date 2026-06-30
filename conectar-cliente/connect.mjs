// Onboarding de cuentas de clientes con Composio (1 cuenta tuya + 1 userId por cliente).
// Acciones:
//   link   <cliente> <app[,app2,...]>   genera el/los link(s) de conexión + mensaje listo
//   estado <cliente> <app>              ¿ya conectó esa app?
//   apps   <cliente>                    qué tiene conectado
//   revoke <cliente> <app>              desconecta (offboarding)
import { config as loadEnv } from "dotenv";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { Composio } from "@composio/core";

// Carga el .env que vive JUNTO a este script (no el del directorio actual),
// para que funcione sin importar desde dónde se invoque el skill.
const __dir = dirname(fileURLToPath(import.meta.url));
loadEnv({ path: join(__dir, ".env") });

const ALIAS = {
  correo: "gmail", mail: "gmail", gmail: "gmail",
  calendario: "googlecalendar", calendar: "googlecalendar", googlecalendar: "googlecalendar",
  hojas: "googlesheets", sheets: "googlesheets", drive: "googledrive",
  whatsapp: "whatsapp", instagram: "instagram", slack: "slack", notion: "notion",
  hubspot: "hubspot", github: "github", outlook: "outlook", trello: "trello",
};
const resolveApp = (a) => ALIAS[(a || "").toLowerCase().trim()] ?? (a || "").toLowerCase().trim();

const key = process.env.COMPOSIO_API_KEY;
if (!key) {
  console.error("❌ Falta COMPOSIO_API_KEY. Crea el archivo .env junto a este script con:\n   COMPOSIO_API_KEY=tu_llave\n   (llave gratis en https://app.composio.dev → Settings → API Keys)");
  process.exit(1);
}
const composio = new Composio({ apiKey: key });

function asArray(res) {
  const x = res?.items ?? res?.data ?? res ?? [];
  return Array.isArray(x) ? x : [];
}

// Reusa una auth config existente (managed) para el toolkit; si no hay, la crea.
async function getAuthConfig(toolkit) {
  try {
    const found = asArray(await composio.authConfigs.list({})).find(
      (c) => (c.toolkit || c.toolkitSlug || "").toLowerCase() === toolkit,
    );
    if (found?.id) return found.id;
  } catch {}
  const ac = await composio.authConfigs.create(toolkit);
  return ac.id;
}

async function conns(cliente) {
  const items = asArray(await composio.connectedAccounts.list({}));
  return items
    .filter((c) => (c.userId || c.user_id || "") === cliente)
    .map((c) => ({
      toolkit: (c.toolkit || c.toolkitSlug || c.appName || "?"),
      status: (c.status || "?"),
      id: (c.id || c.nanoid),
    }));
}

async function cmdLink(cliente, appsCsv) {
  const apps = (appsCsv || "").split(",").map(resolveApp).filter(Boolean);
  const out = [];
  for (const app of apps) {
    const acId = await getAuthConfig(app);
    const req = await composio.connectedAccounts.link(cliente, acId);
    out.push({ app, link: req?.redirectUrl ?? req?.redirect_url ?? req?.url });
  }
  console.log(`\n🔗 Link(s) para "${cliente}":`);
  out.forEach((o) => console.log(`   ${o.app}: ${o.link}`));
  console.log(`\n📩 Mensaje listo para mandarle al cliente:\n`);
  console.log(`Hola 👋 para activar tu asistente, conecta tu cuenta con un clic (no me das tu contraseña, solo autorizas):`);
  out.forEach((o) => console.log(`• ${o.app}: ${o.link}`));
}

async function cmdEstado(cliente, app) {
  const t = resolveApp(app);
  const hit = (await conns(cliente)).find((c) => c.toolkit.toLowerCase() === t);
  if (hit && /active/i.test(hit.status)) console.log(`✅ "${cliente}" YA tiene ${t} conectado.`);
  else console.log(`❌ "${cliente}" NO tiene ${t} conectado. Genera el link:  link ${cliente} ${app}`);
}

async function cmdApps(cliente) {
  const list = await conns(cliente);
  if (!list.length) return console.log(`"${cliente}" no tiene cuentas conectadas todavía.`);
  console.log(`Cuentas conectadas de "${cliente}":`);
  list.forEach((c) => console.log(`• ${c.toolkit} (${c.status})`));
}

async function cmdRevoke(cliente, app) {
  const t = resolveApp(app);
  const hit = (await conns(cliente)).find((c) => c.toolkit.toLowerCase() === t);
  if (!hit?.id) return console.log(`No encontré ${t} conectado en "${cliente}".`);
  await composio.connectedAccounts.delete(hit.id);
  console.log(`🗑️ Desconectado ${t} de "${cliente}".`);
}

const [accion, ...rest] = process.argv.slice(2);
try {
  if (accion === "link") { if (!rest[0] || !rest[1]) throw new Error("uso: link <cliente> <app[,app2]>"); await cmdLink(rest[0], rest[1]); }
  else if (accion === "estado") { await cmdEstado(rest[0], rest[1]); }
  else if (accion === "apps") { await cmdApps(rest[0]); }
  else if (accion === "revoke") { await cmdRevoke(rest[0], rest[1]); }
  else { console.log("Acciones: link <cliente> <app[,app2]> | estado <cliente> <app> | apps <cliente> | revoke <cliente> <app>"); }
} catch (e) { console.error("❌", e?.message ?? e); process.exit(1); }
