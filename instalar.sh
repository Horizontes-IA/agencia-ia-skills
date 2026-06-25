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

# Los 5 skills de agencia (cada uno es un skill independiente de Claude Code)
for s in cotizacion propuesta contrato cobro cerrar-cliente; do
  rm -rf "$SKILLS_DIR/$s"
  cp -R "$TMP/agencia/$s" "$SKILLS_DIR/$s"
  echo "  ✓ /$s"
done

# El onboarding + ejemplo de perfil, compartidos (los skills los leen de aquí)
cp "$TMP/agencia/configurar.md" "$CONF_DIR/configurar.md"
cp "$TMP/agencia/perfil.ejemplo.json" "$CONF_DIR/perfil.ejemplo.json"

rm -rf "$TMP"
echo ""
echo "✅ Listo. Abre Claude Code y escribe, por ejemplo:  /cotizacion"
echo "   La primera vez te hará unas preguntas para configurar tu agencia (1 sola vez)."
echo "   Para conectar las cuentas de tus clientes sin pedir API keys, instala también /conectar-cliente."
