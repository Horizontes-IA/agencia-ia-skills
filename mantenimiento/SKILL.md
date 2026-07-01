---
name: mantenimiento
description: "Generate a monthly maintenance health report for a project. Runs automated checks (dependencies, security, build, git activity) and produces a professional Word document (.docx) to send to the client. Use when the user mentions 'mantenimiento', 'maintenance report', 'health check', 'reporte de mantenimiento', 'project health', 'monthly report', 'reporte mensual', 'cómo está el proyecto', 'revisar proyecto', 'audit del proyecto'."
metadata:
  version: 1.0.0
---

# Project Maintenance Report Generator

You are a professional project maintainer. Your job is to run a comprehensive health check on the project, identify issues, and generate a polished Word report that the developer can send to their client as proof of maintenance.

## ⚙️ Fase 0 — Perfil de tu agencia (auto-config, una sola vez)

Este skill es parte del kit **agencia-ia-skills**. Antes de generar nada, asegura el perfil de la agencia:
- Si **NO existe** `~/.config/agencia-ia/perfil.json` → lee `~/.config/agencia-ia/configurar.md` y corre el onboarding (unas preguntas, guarda el perfil). **Solo la primera vez** que el usuario usa cualquier skill de agencia.
- Si **SÍ existe** → cárgalo y **NO vuelvas a preguntar** los datos de la agencia. Personaliza el reporte con: `agencia.nombre_marca` (la marca en la portada / pie), `persona.nombre` / `persona.email` (contacto), `marca.color_acento` (color de acento del `.docx` — títulos y encabezados vía `RGBColor`, en vez del cyan por defecto), `marca.logo_url` (logo si lo dio), `tono` (el tono del copy).
- Para reconfigurar: "configura mi agencia".

> **Dónde encaja en el kit:** es el paso RECURRENTE del final. Flujo: `/nuevo-cliente` (o `/cerrar-cliente`) → `/crear-agente` → `/docs-entrega` → **`/mantenimiento` (cada mes, justifica la mensualidad)**. Cobra el retainer con `/cobro` cuando mandes el reporte.

## Workflow

### Step 1: Gather Info

Ask the user (skip if already provided):

```
Para generar el reporte de mantenimiento necesito:

1. **Nombre del proyecto** — (ej: "Invoice Analyzer")
2. **Cliente** — (ej: "Acme Corp")
3. **URL de producción** — (ej: "https://app.acme.com")
```

> **Tu marca NO se pregunta aquí** — el nombre de la agencia, el contacto y el color de acento del reporte salen de tu perfil (Fase 0): `agencia.nombre_marca`, `persona.*` y `marca.color_acento`. Solo pregunta lo específico del proyecto.

### Step 2: Run Health Checks

Execute ALL of the following checks. Run independent checks in parallel using Bash tool.

#### Check 1: Dependencies & Security
```bash
# Node.js projects
npm audit --json 2>/dev/null || echo '{"vulnerabilities":{}}'
npm outdated --json 2>/dev/null || echo '{}'

# Python projects
pip3 audit 2>/dev/null || pip3 list --outdated --format=json 2>/dev/null || echo '[]'
```

#### Check 2: Build Health
```bash
# Check if project builds successfully (don't keep the process running)
npm run build 2>&1 | tail -20
echo "EXIT_CODE: $?"
```

#### Check 3: Git Activity
```bash
# Recent activity
git log --oneline --since="30 days ago" --no-walk=sorted 2>/dev/null | wc -l
git log --oneline -10 --format="%h %s (%cr)" 2>/dev/null

# Branches
git branch -a 2>/dev/null | wc -l
git branch --merged main 2>/dev/null | grep -v main | wc -l

# Uncommitted changes
git status --porcelain 2>/dev/null | wc -l
```

#### Check 4: Project Size
```bash
# Build/output size
du -sh .next 2>/dev/null || du -sh dist 2>/dev/null || du -sh build 2>/dev/null || echo "No build dir"
du -sh node_modules 2>/dev/null || echo "No node_modules"

# Lines of code (approximate)
find src -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" 2>/dev/null | xargs wc -l 2>/dev/null | tail -1
```

#### Check 5: Environment & Config
```bash
# Check .env exists
test -f .env && echo ".env exists" || echo ".env MISSING"

# Check important config files
for f in package.json tsconfig.json next.config.* vercel.json netlify.toml convex.json; do
  test -f "$f" && echo "✓ $f" || true
done
```

#### Check 6: Package.json Analysis
Read `package.json` to check:
- Node/npm version requirements (engines field)
- Script definitions
- Dependency count
- Whether there's a lockfile (package-lock.json or yarn.lock)

### Step 3: Analyze Results

After running all checks, categorize findings into:

**Status Levels:**
- 🟢 **Saludable** — No action needed
- 🟡 **Atención** — Should be addressed soon (non-critical)
- 🔴 **Urgente** — Needs immediate attention

**Categories:**
1. **Seguridad** — vulnerabilities, exposed secrets
2. **Dependencias** — outdated packages, deprecated libraries
3. **Build** — compilation errors, warnings
4. **Repositorio** — git health, stale branches
5. **Rendimiento** — build size, bundle analysis
6. **Infraestructura** — hosting, domain, SSL status

### Step 4: Generate the Report

Create the report as a markdown file at `docs/reporte-mantenimiento-{YYYY-MM}.md` with this structure:

```markdown
# Reporte de Mantenimiento

**Proyecto:** {name}
**Cliente:** {client}
**Período:** {month year}
**Fecha del reporte:** {date}
**Realizado por:** {developer}

---

## Resumen Ejecutivo

{2-3 sentences summarizing the overall health of the project. Written for a non-technical client.}

**Estado general:** 🟢 Saludable / 🟡 Requiere atención / 🔴 Urgente

| Área | Estado | Notas |
|------|--------|-------|
| Seguridad | 🟢/🟡/🔴 | {one-line summary} |
| Dependencias | 🟢/🟡/🔴 | {one-line summary} |
| Build | 🟢/🟡/🔴 | {one-line summary} |
| Repositorio | 🟢/🟡/🔴 | {one-line summary} |
| Rendimiento | 🟢/🟡/🔴 | {one-line summary} |

---

## Seguridad

**Estado:** 🟢/🟡/🔴

{Explain in simple terms. "No se encontraron vulnerabilidades" or "Se encontraron X vulnerabilidades que requieren atención"}

| Vulnerabilidad | Severidad | Paquete | Acción |
|---------------|-----------|---------|--------|
| {description} | Alta/Media/Baja | {package} | {what to do} |

**Acciones realizadas:**
- {what you did or recommend}

---

## Dependencias

**Estado:** 🟢/🟡/🔴

**Paquetes desactualizados:** {count}

| Paquete | Versión actual | Última versión | Prioridad |
|---------|---------------|----------------|-----------|
| {name} | {current} | {latest} | Alta/Media/Baja |

**Recomendación:** {update strategy}

---

## Build y Compilación

**Estado:** 🟢/🟡/🔴

- **Resultado:** Exitoso / Fallido
- **Warnings:** {count}
- **Tamaño del build:** {size}

{If there are warnings or errors, list them}

---

## Repositorio

**Estado:** 🟢/🟡/🔴

- **Commits este mes:** {count}
- **Último commit:** {date and message}
- **Branches activos:** {count}
- **Branches para limpiar:** {count}
- **Cambios sin commitear:** {yes/no}

---

## Rendimiento

**Estado:** 🟢/🟡/🔴

- **Tamaño de node_modules:** {size}
- **Líneas de código:** {count}
- **Tamaño del proyecto:** {estimate}

---

## Servicios Externos

{Check if key services are operational. Just list what the project uses.}

| Servicio | Para qué | Estado | Dashboard |
|----------|----------|--------|-----------|
| {service} | {purpose} | Verificar | {URL} |

**Nota:** Revisa los dashboards para confirmar que los planes y facturación están al día.

---

## Acciones Realizadas Este Mes

{List any maintenance actions taken. If this is just a health check, say so.}

- ✅ Revisión completa de seguridad
- ✅ Verificación de build exitoso
- ✅ Análisis de dependencias
- {any other actions}

---

## Recomendaciones

{Prioritized list of what should be done, written for a non-technical client}

### Urgente (hacer ahora)
- {if any}

### Próximo mes
- {recommendations}

### A futuro
- {nice-to-haves}

---

## Próximo Reporte

**Fecha estimada:** {next month, same day}

---

*Reporte generado el {date}*
*{developer company}*
```

### Step 5: Convert to Word

After generating the markdown, convert it to a professional Word document:

```bash
pip3 install python-docx --quiet
curl -sL https://raw.githubusercontent.com/santmun/docs-entrega-skill/main/md_to_docx.py -o docs/md_to_docx.py
python3 docs/md_to_docx.py docs --project "{Project Name}" --company "{Developer Company}" --color "{accent_color}"
```

The file to convert is `docs/reporte-mantenimiento-{YYYY-MM}.md`.

If the md_to_docx.py script doesn't find the file automatically (it looks for README.md, GUIA-DE-USO.md, DOCS-TECNICA.md), then convert it manually:

```python
python3 -c "
import sys
sys.path.insert(0, 'docs')
from md_to_docx import convert_file
convert_file(
    'docs/reporte-mantenimiento-{YYYY-MM}.md',
    'docs/reporte-mantenimiento-{YYYY-MM}.docx',
    '{Project Name}',
    'Reporte de Mantenimiento — {Month Year}',
    '{accent_color}',
    '{Developer Company}'
)
"
```

### Step 6: Show Summary

```
📊 Reporte de mantenimiento generado:

  docs/
  ├── reporte-mantenimiento-{YYYY-MM}.md    — Reporte (markdown)
  └── reporte-mantenimiento-{YYYY-MM}.docx  — Reporte (Word)

Estado general: 🟢/🟡/🔴
Vulnerabilidades: {count}
Dependencias desactualizadas: {count}
Build: Exitoso/Fallido

📄 El .docx está listo para enviar al cliente.
```

## Important Rules

1. **Write for a non-technical audience.** The client reading this report may not understand "npm audit found 3 high severity vulnerabilities in transitive dependencies." Instead say: "Se encontraron 3 problemas de seguridad importantes que ya fueron corregidos."
2. **Be honest but not alarmist.** A few outdated packages is normal. Don't make it sound like the project is falling apart.
3. **Always provide context.** Don't just list numbers — explain what they mean and whether action is needed.
4. **Include what you DID, not just what you found.** The client is paying for maintenance. Show them the value.
5. **Date the report.** Use format "Abril 2026" for the period, "{day} de {month}, {year}" for specific dates.
6. **Keep the executive summary to 2-3 sentences.** The client reads this first and may not read the rest.
7. **The services table should list actual services** detected in the project (read package.json, .env), not generic placeholders.
8. **Don't run destructive commands.** This is a health CHECK, not a fix. If something needs fixing, put it in recommendations.
9. **After the build check, make sure to kill any running processes** (next dev, next build, etc.) — never leave them running.
10. **ALWAYS convert to Word.** The .docx is what the client receives.
