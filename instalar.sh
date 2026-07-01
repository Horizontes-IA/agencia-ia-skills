#!/usr/bin/env bash
# Instalador del Sistema de Agencia IA (Horizontes IA).
# Instala TODOS los skills de agencia de un jalón y deja listo el auto-config.
#
# Uso (1 comando):
#   curl -fsSL https://raw.githubusercontent.com/Horizontes-IA/agencia-ia-skills/main/instalar.sh | bash
#
# Qué hace:
#   - Clona/actualiza el repo.
#   - Copia cada skill a ~/.claude/skills/ (para que Claude Code los descubra).
#   - Copia el onboarding compartido a ~/.config/agencia-ia/.
# La PRIMERA vez que uses cualquier skill (ej. /cotizacion), te hará unas preguntas
# y guardará el perfil de tu agencia — UNA sola vez. Después todo sale personalizado.
set -e

REPO="https://github.com/Horizontes-IA/agencia-ia-skills.git"
TMP="$(mktemp -d)"
SKILLS_DIR="$HOME/.claude/skills"
CONF_DIR="$HOME/.config/agencia-ia"

echo "📦 Instalando el Sistema de Agencia IA…"
git clone --depth 1 -q "$REPO" "$TMP/agencia"

mkdir -p "$SKILLS_DIR" "$CONF_DIR"

# Los 10 skills de agencia (cada uno es un skill independiente de Claude Code).
# /nuevo-cliente es la puerta de entrada que orquesta a los demás.
for s in nuevo-cliente diagnostico cotizacion propuesta contrato cobro conectar-cliente cerrar-cliente docs-entrega mantenimiento; do
  rm -rf "$SKILLS_DIR/$s"
  cp -R "$TMP/agencia/$s" "$SKILLS_DIR/$s"
  echo "  ✓ /$s"
done

# /conectar-cliente usa Composio (Node): deja sus dependencias listas desde el inicio.
# (La llave de Composio NO se pide aquí — el skill te la pide la primera vez que lo usas.)
if command -v npm >/dev/null 2>&1; then
  echo "  ⏳ instalando dependencias de /conectar-cliente…"
  ( cd "$SKILLS_DIR/conectar-cliente" && npm install --silent --no-audit --no-fund ) \
    && echo "  ✓ dependencias de /conectar-cliente listas" \
    || echo "  ⚠️ no pude instalar las deps de /conectar-cliente; corre 'npm install' en $SKILLS_DIR/conectar-cliente cuando puedas."
else
  echo "  ⚠️ No encontré npm. /conectar-cliente necesita Node: instálalo y corre 'npm install' en $SKILLS_DIR/conectar-cliente."
fi

# El CLI de Composio: lo usan /cobro (link de pago de Stripe) y /conectar-cliente (descubrir
# tools para el curl de n8n/Make). Se instala UNA vez; la autenticación la hace el usuario
# después con `composio login` (abre el navegador, no se puede automatizar aquí).
if command -v composio >/dev/null 2>&1 || [ -x "$HOME/.composio/composio" ]; then
  echo "  ✓ Composio CLI ya instalado"
else
  echo "  ⏳ instalando el Composio CLI…"
  if curl -fsSL https://composio.dev/install | bash >/dev/null 2>&1; then
    echo "  ✓ Composio CLI instalado (autentícalo después con: composio login)"
  else
    echo "  ⚠️ no pude instalar el Composio CLI. Instálalo tú (macOS/Linux; Windows con WSL):"
    echo "       curl -fsSL https://composio.dev/install | bash"
  fi
fi

# El onboarding + ejemplo de perfil + el conversor HTML→PDF, compartidos (los skills los leen de aquí)
cp "$TMP/agencia/configurar.md" "$CONF_DIR/configurar.md"
cp "$TMP/agencia/perfil.ejemplo.json" "$CONF_DIR/perfil.ejemplo.json"
cp "$TMP/agencia/html2pdf.py" "$CONF_DIR/html2pdf.py"

rm -rf "$TMP"
echo ""
echo "✅ Listo. Abre Claude Code y escribe:  /nuevo-cliente   (la puerta de entrada — arma todo el kit)"
echo "   O usa un skill suelto: /diagnostico, /cotizacion, /propuesta, /contrato, /cobro."
echo "   La primera vez te hará unas preguntas para configurar tu agencia (1 sola vez)."
echo ""
echo "🔑 Un paso más — autentícate en Composio (una sola vez, gratis):"
echo "     composio login"
echo "   Lo usan /cobro (para el link de pago de Stripe) y /conectar-cliente (cuentas del cliente)."
echo "   Si 'composio' no se reconoce, cierra y reabre la terminal (o corre: source ~/.zshrc)."
