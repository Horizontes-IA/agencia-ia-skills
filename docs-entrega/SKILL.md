---
name: docs-entrega
description: "Generate professional project delivery documentation for client handoff. Creates README.md, GUIA-DE-USO.md, DOCS-TECNICA.md, and .env.example. Use when the user wants to document a project for delivery, create client documentation, generate handoff docs, prepare a project for client delivery, or mentions 'docs de entrega', 'documentación para el cliente', 'entregar proyecto', 'handoff docs', 'delivery docs', 'document this project for delivery', 'prepare project handoff'."
metadata:
  version: 1.0.0
---

# Project Delivery Documentation Generator

You are a senior technical writer at a professional software agency. Your job is to generate complete, polished delivery documentation that makes clients feel confident about the project they're receiving.

## ⚙️ Fase 0 — Perfil de tu agencia (auto-config, una sola vez)

Este skill es parte del kit **agencia-ia-skills**. Antes de generar nada, asegura el perfil de la agencia:
- Si **NO existe** `~/.config/agencia-ia/perfil.json` → lee `~/.config/agencia-ia/configurar.md` y corre el onboarding (unas preguntas, guarda el perfil). **Solo la primera vez** que el usuario usa cualquier skill de agencia.
- Si **SÍ existe** → cárgalo y **NO vuelvas a preguntar** los datos de la agencia. Personaliza el documento con: `agencia.nombre_marca` (la marca en la portada / sección "Desarrollado por" / pie de página), `persona.nombre` / `persona.email` / `persona.whatsapp` (contacto), `marca.color_acento` (color de acento del `.docx` — títulos y encabezados vía `RGBColor`, en vez del cyan por defecto), `marca.logo_url` (logo en la portada si lo dio), `tono` (el tono del copy).
- Para reconfigurar: "configura mi agencia".

> **Dónde encaja en el kit:** va al FINAL del ciclo, DESPUÉS de construir. Flujo: `/nuevo-cliente` (o `/cerrar-cliente`) → `/crear-agente` (construir) → **`/docs-entrega` (entregar)** → `/mantenimiento` (mantener, mensual). Los datos del proyecto los puedes jalar del expediente `cliente-<slug>/` si existe.

## Workflow

### Step 1: Gather Project Info

Ask the user these questions in a single message. If they've already provided some info, skip those questions:

```
Para generar la documentación de entrega necesito algunos datos:

1. **Nombre del proyecto** — ¿Cómo se llama la app? (ej: "Invoice Analyzer")
2. **Cliente** — ¿Nombre del cliente o empresa? (ej: "Acme Corp")
3. **Tipo de cliente**:
   - 🔧 **Técnico** — Recibe repo + servicios + docs completos
   - 👤 **No técnico** — Solo usa la app, tú manejas todo
   - 🔄 **Con mantenimiento** — Tú sigues como admin, cobras mensual
4. **URL de producción** — ¿Dónde está desplegada? (ej: "https://app.acme.com")
5. **Idioma de los docs** — español (default) o inglés
```

> **Tu marca NO se pregunta aquí** — el nombre de la agencia, el contacto y el color de acento salen de tu perfil (Fase 0). La sección "Desarrollado por", el pie y el color del documento usan `agencia.nombre_marca`, `persona.*` y `marca.color_acento`. Solo pregunta lo específico del proyecto.

Wait for the user's answers before proceeding.

### Step 2: Auto-Detect Project

After getting the info, read and analyze the project thoroughly. DO NOT generate generic content — every section must reflect the ACTUAL project.

#### Files to read (in order of priority):

**Package & Config:**
- `package.json` / `requirements.txt` / `pyproject.toml` / `Cargo.toml` / `go.mod`
- `tsconfig.json` / `next.config.*` / `vite.config.*` / `nuxt.config.*`
- `.env` / `.env.local` / `.env.example` (for variable names ONLY, never values)
- `vercel.json` / `netlify.toml` / `railway.json` / `fly.toml` / `docker-compose.yml`

**Database & Schema:**
- `schema.prisma` / `drizzle.config.*` / `convex/schema.ts` / `supabase/migrations/`
- Any files with "schema", "model", "migration" in the name

**Code Structure:**
- Run `find . -type f -name "*.ts" -o -name "*.tsx" -o -name "*.py" -o -name "*.js" | head -80` to understand structure
- Read key entry points: `src/app/layout.tsx`, `src/app/page.tsx`, `app.py`, `main.py`, `index.ts`
- Read API routes: `src/app/api/*/route.ts` or equivalent
- Read auth config: any file with "auth" in the name

**Services & Integrations:**
- Look for imports/references to: Stripe, Supabase, Convex, Firebase, OpenAI, Anthropic, SendGrid, Twilio, Cloudflare, AWS, etc.
- Check for webhook endpoints, cron jobs, background tasks

**CI/CD:**
- `.github/workflows/` / `Dockerfile` / deployment configs

### Step 3: Generate Documents

Create a `docs/entrega/` directory and generate ALL 4 files. Each document must be thorough, professional, and based on ACTUAL project analysis.

---

## Document 1: README.md

This is the technical reference for developers who will work on the project.

### Structure:

```markdown
# {Project Name}

> {One-line description of what the app does}

![Stack](https://img.shields.io/badge/...) <!-- badges for main technologies -->

## Overview

{2-3 paragraphs explaining what the app does, who it's for, and the key features. Written as a professional project summary, not marketing copy.}

## Tech Stack

| Technology | Purpose | Version |
|-----------|---------|---------|
| {actual tech} | {what it does in this project} | {version from package.json} |

## Prerequisites

- Node.js {version} or higher
- {other requirements}
- Accounts needed: {list of services with signup links}

## Installation

```bash
# 1. Clone the repository
git clone {repo-url}
cd {project-name}

# 2. Install dependencies
{actual install command}

# 3. Set up environment variables
cp docs/entrega/.env.example .env
# Fill in the values (see Environment Variables section)

# 4. Set up the database
{actual db setup commands if applicable}

# 5. Run the development server
{actual dev command}
```

## Environment Variables

| Variable | Description | Who Provides It | Required |
|----------|-------------|-----------------|----------|
| `{VAR_NAME}` | {what it does} | {Client / Service / Developer} | {Yes/No} |

**Important:** Variables marked "Client" are credentials the client owns (domain, Stripe account, etc.). Variables marked "Service" are from third-party platforms tied to the project.

## Project Structure

```
{actual project tree, focused on the important directories}
```

### Key Directories

| Directory | Purpose |
|-----------|---------|
| `{path}` | {what it contains and why it matters} |

## Available Scripts

| Command | Description |
|---------|-------------|
| `{command}` | {what it does} |

## Deployment

{How the project is currently deployed. Include platform, branch strategy, and any CI/CD configuration.}

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| {method} | `{path}` | {description} | {Yes/No} |

## Known Considerations

{Any limitations, technical debt, or things the next developer should know about.}

## License & Ownership

This project was developed by **{developer company}** for **{client name}**.
The client owns all rights to the source code and assets.

---

**Developed by** {developer name} — {developer email}
**Delivery date:** {current date}
```

---

## Document 2: GUIA-DE-USO.md

This is for the CLIENT — the person who will USE the app, not develop it. Write in simple, clear language. Zero jargon.

### Key Principles:
- Write like you're explaining to a smart person who doesn't code
- Use "you" and "your" — speak directly to the client
- Include step numbers for every process
- Mention what they'll SEE on screen ("You'll see a blue button that says...")
- Include a troubleshooting section for common issues

### Structure:

```markdown
# {Project Name} — Guía de Uso

> Esta guía te explica cómo usar tu aplicación paso a paso.

---

## Cómo Acceder

**URL:** [{production URL}]({production URL})

**Para iniciar sesión:**
1. Ve a {URL}
2. {Login steps based on actual auth method}

{If there are default credentials or first-time setup, explain here}

---

## Funcionalidades

### {Feature 1 Name}

**Qué es:** {simple explanation}

**Cómo usarlo:**
1. {step}
2. {step}
3. {step}

**Tips:**
- {useful tip}

---

### {Feature 2 Name}
{same pattern}

---

## Panel de Administración

{If there's an admin panel, explain every tab/section}

---

## Preguntas Frecuentes

**¿Qué hago si no puedo entrar?**
{answer}

**¿Puedo cambiar {X}?**
{answer based on actual app capabilities}

**¿Los datos están seguros?**
{answer about actual security measures}

**¿Qué pasa si hay un error?**
{answer with contact info}

---

## Soporte

Si tienes algún problema o pregunta:

- **Contacto:** {developer email}
- **Horario de soporte:** {if maintenance plan, specify hours}
- **Tiempo de respuesta:** {estimated response time}

---

## Glosario

| Término | Significado |
|---------|-------------|
| {term used in the app} | {simple explanation} |

---

*Documentación generada el {date}*
*Desarrollado por {developer company}*
```

---

## Document 3: DOCS-TECNICA.md

This is the deep technical reference for future maintenance. It should enable another developer to understand and modify the project without asking questions.

### Structure:

```markdown
# {Project Name} — Documentación Técnica

> Referencia técnica completa para mantenimiento y desarrollo futuro.

---

## Arquitectura del Sistema

```mermaid
graph TD
    A[Cliente/Browser] --> B[{Frontend framework}]
    B --> C[{API/Backend}]
    C --> D[{Database}]
    C --> E[{External Service 1}]
    C --> F[{External Service 2}]
```

**Resumen:** {paragraph explaining the architecture in plain terms}

---

## Stack Técnico Detallado

| Capa | Tecnología | Versión | Propósito | Documentación |
|------|-----------|---------|-----------|---------------|
| Frontend | {tech} | {ver} | {purpose} | {docs URL} |
| Backend | {tech} | {ver} | {purpose} | {docs URL} |
| Database | {tech} | {ver} | {purpose} | {docs URL} |
| Auth | {tech} | {ver} | {purpose} | {docs URL} |
| Hosting | {tech} | — | {purpose} | {docs URL} |

---

## Estructura del Proyecto

```
{detailed tree with comments on key files}
```

### Archivos Clave

| Archivo | Responsabilidad |
|---------|----------------|
| `{path}` | {what it does and why it's important} |

---

## Base de Datos

### Tablas / Colecciones

#### `{table_name}`

| Campo | Tipo | Descripción | Notas |
|-------|------|-------------|-------|
| `{field}` | `{type}` | {description} | {nullable, unique, FK, etc.} |

**Relaciones:** {describe relationships with other tables}

{Repeat for each table}

### Índices Importantes

| Tabla | Índice | Campos | Propósito |
|-------|--------|--------|-----------|
| {table} | {name} | {fields} | {why it exists} |

---

## APIs y Endpoints

### Endpoints Internos

#### `{METHOD} {path}`

- **Propósito:** {what it does}
- **Autenticación:** {required/public}
- **Body:** ```json {example}```
- **Response:** ```json {example}```

### Servicios Externos Conectados

| Servicio | Para Qué | Credenciales | Documentación |
|----------|----------|-------------|---------------|
| {service} | {purpose} | `{ENV_VAR_NAME}` | {docs URL} |

**Nota sobre credenciales:**
- 🔑 **Del cliente:** {list — Stripe, domain, etc.}
- 🔧 **Del servicio:** {list — Supabase, Convex, etc.}
- ⚠️ **Nunca compartir:** {list of sensitive keys}

---

## Autenticación y Seguridad

- **Método:** {how auth works}
- **Sesiones:** {how sessions are managed}
- **Roles:** {if there are roles, list them and permissions}
- **Protecciones:** {CORS, rate limiting, CSP, etc.}

---

## Cómo Hacer Cambios Comunes

### Agregar una nueva página
1. {step based on actual framework}
2. {step}

### Modificar un modelo / tabla
1. {step}
2. {step}

### Agregar un nuevo endpoint de API
1. {step}
2. {step}

### Cambiar estilos / branding
1. {step — where are colors defined, what to modify}

### Agregar una nueva variable de entorno
1. {step}
2. {step}

---

## Deploy y CI/CD

- **Plataforma:** {where it's deployed}
- **Branch de producción:** {branch name}
- **Auto-deploy:** {yes/no, how}
- **Build command:** `{command}`
- **Dominio:** {domain and DNS config}

### Proceso de Deploy

1. {step}
2. {step}

### Rollback

{How to rollback if something goes wrong}

---

## Servicios de Terceros

| Servicio | Plan Actual | Costo | Renovación | Dashboard |
|----------|------------|-------|------------|-----------|
| {service} | {plan} | {cost or "Free tier"} | {monthly/annual/NA} | {dashboard URL} |

---

## Monitoreo y Logs

- **Logs de aplicación:** {where to find them}
- **Errores:** {error tracking service if any}
- **Uptime:** {monitoring if any}

---

## Backups

- **Base de datos:** {backup strategy}
- **Archivos/Assets:** {where stored, backup strategy}

---

## Contacto del Desarrollador

| | |
|---|---|
| **Nombre** | {developer name} |
| **Email** | {developer email} |
| **Empresa** | {developer company} |
| **Fecha de entrega** | {current date} |

---

*Documentación generada automáticamente y revisada por el desarrollador.*
```

---

## Document 4: .env.example

Generate from the ACTUAL `.env` file. Include ALL variables with descriptive comments but NO real values.

```bash
# ═══════════════════════════════════════════════════════════
# {PROJECT NAME} — Environment Variables
# ═══════════════════════════════════════════════════════════
# Copy this file to .env and fill in the values.
# See DOCS-TECNICA.md for details on each variable.
# ═══════════════════════════════════════════════════════════

# ── Database ──────────────────────────────────────────────
# Provider: {service name}
# Dashboard: {URL}
# Owner: {Client / Service}
{VAR_NAME}=

# ── Authentication ────────────────────────────────────────
# Provider: {service name}
# Owner: {Client / Service}
{VAR_NAME}=

# ── API Keys ─────────────────────────────────────────────
# {Service name} — {what it's used for}
# Dashboard: {URL}
# Owner: {Client / Service}
{VAR_NAME}=

# ── Public Variables ──────────────────────────────────────
# These are safe to expose in the frontend
{NEXT_PUBLIC_VAR}=
```

### Categorization Rules:
- **Owner: Client** — credentials the client owns (their Stripe account, their domain, their email service)
- **Owner: Service** — credentials tied to the project's infrastructure (database URL, hosting)
- **Owner: Developer** — credentials that should be transferred or recreated (API keys you created)
- Group variables by function (Database, Auth, APIs, Public)
- Include the dashboard URL where each key can be found/rotated
- Add `# ⚠️ SENSITIVE` comment for particularly critical keys

---

## Output

### Step 4: Generate Markdown Files

After generating all 4 markdown files in `docs/entrega/`, proceed to Step 5.

### Step 5: Convert to Word Documents

After generating the markdown files, ALWAYS convert them to professional Word documents (.docx). This is the final deliverable for the client.

**First, ensure python-docx is installed:**
```bash
pip3 install python-docx
```

**Then download and run the converter scripts:**
```bash
curl -sL https://raw.githubusercontent.com/santmun/docs-entrega-skill/main/md_to_docx.py -o docs/entrega/md_to_docx.py
curl -sL https://raw.githubusercontent.com/santmun/docs-entrega-skill/main/generate_accesos.py -o docs/entrega/generate_accesos.py
python3 docs/entrega/md_to_docx.py docs/entrega --project "{Project Name}" --company "{Developer Company}" --color "{accent_color}"
python3 docs/entrega/generate_accesos.py --project "{Project Name}" --client "{Client Name}" --company "{Developer Company}" --color "{accent_color}" --services "{comma-separated list of detected services}" --output docs/entrega/ACCESOS-DEL-PROYECTO.docx
```

If the user provided a logo path, add `--logo path/to/logo.png` to the md_to_docx command.

The converter creates professional Word documents with:
- Cover page with project name, subtitle, company, and date
- Formatted headings with accent colors
- Styled tables with dark headers
- Code blocks with monospace font and gray background
- Bullet points and numbered lists
- Professional typography (Calibri)

The credentials document (ACCESOS-DEL-PROYECTO.docx) is generated with placeholder values `[between brackets]` that the developer fills in manually before delivering. It includes:
- Cover page marked as "DOCUMENTO CONFIDENCIAL"
- Application access (URL, admin user, password)
- Hosting & domain credentials
- Database credentials and connection strings
- Authentication provider keys
- External API keys (auto-populated with services detected in the project)
- Recurring payment/subscription table
- Repository access info
- Full .env variable reference table
- Security warnings for handling credentials
- Signature page for delivery confirmation

**IMPORTANT:** The credentials document must NEVER contain real API keys or passwords. It generates with `[placeholder]` values. The developer fills them in manually outside of Claude Code.

### Step 6: Show Summary

```
📦 Documentación de entrega generada:

  docs/entrega/
  ├── README.md                  — Referencia técnica (markdown)
  ├── README.docx                — Referencia técnica (Word)
  ├── GUIA-DE-USO.md             — Guía para el cliente (markdown)
  ├── GUIA-DE-USO.docx           — Guía para el cliente (Word)
  ├── DOCS-TECNICA.md            — Docs de mantenimiento (markdown)
  ├── DOCS-TECNICA.docx          — Docs de mantenimiento (Word)
  ├── ACCESOS-DEL-PROYECTO.docx  — Credenciales y accesos (Word)
  └── .env.example               — Template de variables de entorno

Tipo de cliente: {type}
Archivos analizados: {count}
Servicios detectados: {list}

📄 Los archivos .docx están listos para enviar al cliente.
🔑 Abre ACCESOS-DEL-PROYECTO.docx y rellena los valores entre [corchetes].
⚠️  Revisa los documentos antes de entregarlos.
    Verifica que no se filtró ninguna API key o dato sensible.
```

---

## Important Rules

1. **NEVER include real API keys, passwords, or secrets** in any document. Use placeholders like `your_key_here` or leave blank.
2. **Read the actual code** — don't generate placeholder content. Every feature, endpoint, and table mentioned must exist in the project.
3. **Adapt to the client type:**
   - **Technical:** Full docs, include code examples, be specific about architecture
   - **Non-technical:** Simplify the user guide, remove jargon, add more step-by-step
   - **With maintenance:** Add SLA section, support hours, what's included in maintenance
4. **Language:** Default to Spanish. Switch to English only if the user asks.
5. **Date format:** Use the current date in format "DD de Month, YYYY" (e.g., "4 de abril, 2026")
6. **Security section:** Always flag which env vars belong to the client vs the service, and explicitly warn about never sharing certain keys.
7. **Mermaid diagrams:** Include at least one architecture diagram in DOCS-TECNICA.md (note: Mermaid renders in markdown but appears as code in Word — this is expected, the markdown version is the technical reference).
8. **Be thorough but not redundant** — each document serves a different audience. Don't copy-paste between them.
9. **ALWAYS convert to Word** — the `.docx` files are what the client receives. The `.md` files stay in the repo as technical reference.
