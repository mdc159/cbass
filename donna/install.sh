#!/bin/bash
# Donna VPS Installer — Self-hosted Telegram Bot API + Donna Agent
# Usage: curl -sL <raw-url>/donna/install.sh | bash
#
# Prerequisites:
#   - Docker + Docker Compose
#   - Claude Code CLI (for the AI bridge)
#
# Required env vars (set in /opt/donna/.env):
#   DONNA_BOT_TOKEN      - Telegram bot token from @BotFather
#   TELEGRAM_API_ID      - From https://my.telegram.org
#   TELEGRAM_API_HASH    - From https://my.telegram.org

set -euo pipefail

INSTALL_DIR="/opt/donna"
REPO_URL="https://github.com/mdc159/cbass.git"
BRANCH="claude/connect-hostinger-vps-UqH0y"

echo "=== Donna VPS Installer ==="
echo ""

# --- Pre-flight checks ---
command -v docker >/dev/null 2>&1 || { echo "ERROR: docker not found. Install Docker first."; exit 1; }
command -v docker compose >/dev/null 2>&1 || { echo "ERROR: docker compose not found."; exit 1; }

# --- Clone or update repo ---
if [ -d "$INSTALL_DIR" ]; then
    echo "[1/5] Updating existing installation..."
    cd "$INSTALL_DIR"
    git pull origin "$BRANCH" 2>/dev/null || true
else
    echo "[1/5] Cloning cbass repo..."
    git clone --branch "$BRANCH" --depth 1 "$REPO_URL" /tmp/cbass-clone
    mkdir -p "$INSTALL_DIR"
    cp -r /tmp/cbass-clone/donna/* "$INSTALL_DIR/"
    cp -r /tmp/cbass-clone/donna/.env.example "$INSTALL_DIR/" 2>/dev/null || true
    rm -rf /tmp/cbass-clone
fi

cd "$INSTALL_DIR"

# --- Check for .env ---
echo "[2/5] Checking configuration..."
if [ ! -f ".env" ]; then
    cat > .env <<'ENVEOF'
# === Required ===
DONNA_BOT_TOKEN=
TELEGRAM_API_ID=
TELEGRAM_API_HASH=

# === Donna Config ===
DONNA_PROMPT=default
DONNA_AUTOPOLL=0
DONNA_WORKDIR=/app

# === Self-hosted Telegram Bot API (auto-configured) ===
TELEGRAM_BASE_URL=http://telegram-bot-api:8081/bot
TELEGRAM_BASE_FILE_URL=http://telegram-bot-api:8081/file/bot
TELEGRAM_LOCAL_MODE=1

# === Claude CLI ===
CLAUDE_BIN=claude
CLAUDE_ARGS=--dangerously-skip-permissions

# === Voice (optional) ===
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=JBFqnCBsd6RMkjVDRZzb
FFMPEG_BIN=/usr/bin/ffmpeg
ENVEOF
    echo ""
    echo "  Created $INSTALL_DIR/.env"
    echo "  EDIT IT NOW with your tokens:"
    echo ""
    echo "    nano $INSTALL_DIR/.env"
    echo ""
    echo "  Required:"
    echo "    DONNA_BOT_TOKEN   - from @BotFather"
    echo "    TELEGRAM_API_ID   - from https://my.telegram.org"
    echo "    TELEGRAM_API_HASH - from https://my.telegram.org"
    echo ""
    echo "  Then re-run this script."
    exit 0
fi

# Validate required vars
source .env
if [ -z "${DONNA_BOT_TOKEN:-}" ] || [ -z "${TELEGRAM_API_ID:-}" ] || [ -z "${TELEGRAM_API_HASH:-}" ]; then
    echo "ERROR: Missing required vars in .env"
    echo "  DONNA_BOT_TOKEN=${DONNA_BOT_TOKEN:-(empty)}"
    echo "  TELEGRAM_API_ID=${TELEGRAM_API_ID:-(empty)}"
    echo "  TELEGRAM_API_HASH=${TELEGRAM_API_HASH:-(empty)}"
    echo ""
    echo "  Edit: nano $INSTALL_DIR/.env"
    exit 1
fi

# --- Log out from official API (migration step) ---
echo "[3/5] Migrating bot to self-hosted API..."
echo "  (Logging out from official Telegram API — required for self-hosted)"
curl -s "https://api.telegram.org/bot${DONNA_BOT_TOKEN}/logOut" || true
echo ""
sleep 3  # Telegram requires a short wait after logOut

# --- Build and start ---
echo "[4/5] Building containers..."
docker compose build --quiet

echo "[5/5] Starting Donna + Telegram Bot API..."
docker compose up -d

echo ""
echo "=== Donna is live! ==="
echo ""
echo "  Telegram Bot API: http://localhost:8081"
echo "  Donna:            running as docker service"
echo ""
echo "  Commands:"
echo "    docker compose -f $INSTALL_DIR/docker-compose.yml logs -f donna"
echo "    docker compose -f $INSTALL_DIR/docker-compose.yml restart donna"
echo "    docker compose -f $INSTALL_DIR/docker-compose.yml down"
echo ""
echo "  Send a message to your bot on Telegram to test!"
