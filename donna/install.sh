#!/bin/bash
# Donna VPS Installer — bare metal bot + Dockerized Telegram Bot API
#
# Run as root on the VPS:
#   bash /opt/cbass/donna/install.sh
#
# What this does:
#   1. Creates a 'donna' user (no sudo)
#   2. Copies the donna/ folder to /home/donna/app
#   3. Installs uv + ffmpeg
#   4. Syncs Python deps
#   5. Starts self-hosted Telegram Bot API (Docker)
#   6. Installs + starts donna.service (systemd)
#
# Prerequisites:
#   - Docker + Docker Compose (for Telegram Bot API only)
#   - Claude Code CLI installed system-wide (claude in PATH)
#   - /opt/cbass/donna/.env with required tokens

set -euo pipefail

DONNA_HOME="/home/donna"
APP_DIR="$DONNA_HOME/app"
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Donna VPS Installer ==="
echo "  Source: $SOURCE_DIR"
echo ""

# --- Must be root ---
if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: Run as root (needed to create user + install service)"
    exit 1
fi

# --- Pre-flight checks ---
echo "[1/8] Pre-flight checks..."
command -v docker >/dev/null 2>&1 || { echo "ERROR: docker not found"; exit 1; }
command -v docker compose >/dev/null 2>&1 || { echo "ERROR: docker compose not found"; exit 1; }

# Check Claude Code is available
CLAUDE_BIN=$(command -v claude 2>/dev/null || true)
if [ -z "$CLAUDE_BIN" ]; then
    echo "WARNING: 'claude' not found in PATH"
    echo "  Donna needs Claude Code CLI. Install it or set CLAUDE_BIN in .env"
fi

# --- Create donna user (no sudo) ---
echo "[2/8] Creating donna user..."
if id donna &>/dev/null; then
    echo "  User 'donna' already exists"
else
    useradd -m -s /bin/bash -c "Donna - Telegram AI Agent" donna
    echo "  Created user 'donna' (no sudo)"
fi

# --- Copy app files ---
echo "[3/8] Copying app files to $APP_DIR..."
mkdir -p "$APP_DIR"
# Copy everything except .venv, __pycache__, .git
rsync -a --delete \
    --exclude '.venv' \
    --exclude '__pycache__' \
    --exclude '.git' \
    --exclude '*.pyc' \
    --exclude 'miniapp/node_modules' \
    "$SOURCE_DIR/" "$APP_DIR/"

# Copy .env if it exists in source but not in app dir
if [ -f "$SOURCE_DIR/.env" ] && [ ! -f "$APP_DIR/.env" ]; then
    cp "$SOURCE_DIR/.env" "$APP_DIR/.env"
    echo "  Copied .env"
elif [ -f "$APP_DIR/.env" ]; then
    echo "  Keeping existing .env in $APP_DIR"
fi

# --- Set ownership ---
chown -R donna:donna "$DONNA_HOME"
chmod 600 "$APP_DIR/.env" 2>/dev/null || true

# --- Install uv + ffmpeg ---
echo "[4/8] Installing dependencies..."
if ! command -v uv &>/dev/null; then
    echo "  Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | su - donna -c "sh"
fi

# ffmpeg for voice note conversion
if ! command -v ffmpeg &>/dev/null; then
    apt-get update -qq && apt-get install -y -qq ffmpeg
fi

# --- Python deps ---
echo "[5/8] Syncing Python dependencies..."
su - donna -c "cd $APP_DIR && ~/.local/bin/uv sync --frozen 2>&1" || \
su - donna -c "cd $APP_DIR && ~/.local/bin/uv sync 2>&1"

# --- Validate .env ---
echo "[6/8] Validating configuration..."
if [ ! -f "$APP_DIR/.env" ]; then
    cat > "$APP_DIR/.env" <<'ENVEOF'
# === Required ===
DONNA_BOT_TOKEN=
TELEGRAM_API_ID=
TELEGRAM_API_HASH=

# === Donna Config ===
DONNA_PROMPT=default
DONNA_AUTOPOLL=0
DONNA_WORKDIR=/home/donna/app

# === Self-hosted Telegram Bot API ===
TELEGRAM_BASE_URL=http://127.0.0.1:8081/bot
TELEGRAM_BASE_FILE_URL=http://127.0.0.1:8081/file/bot
TELEGRAM_LOCAL_MODE=1

# === Claude CLI ===
CLAUDE_BIN=claude
CLAUDE_ARGS=--dangerously-skip-permissions

# === Voice ===
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=JBFqnCBsd6RMkjVDRZzb
FFMPEG_BIN=/usr/bin/ffmpeg
ENVEOF
    chown donna:donna "$APP_DIR/.env"
    chmod 600 "$APP_DIR/.env"
    echo ""
    echo "  Created $APP_DIR/.env — EDIT IT NOW:"
    echo "    nano $APP_DIR/.env"
    echo ""
    echo "  Required:"
    echo "    DONNA_BOT_TOKEN   - from @BotFather"
    echo "    TELEGRAM_API_ID   - from https://my.telegram.org"
    echo "    TELEGRAM_API_HASH - from https://my.telegram.org"
    echo "    ELEVENLABS_API_KEY - from elevenlabs.io"
    echo ""
    echo "  Then re-run this script."
    exit 0
fi

# Source and validate
set -a
source "$APP_DIR/.env"
set +a
MISSING=""
[ -z "${DONNA_BOT_TOKEN:-}" ] && MISSING="$MISSING DONNA_BOT_TOKEN"
[ -z "${TELEGRAM_API_ID:-}" ] && MISSING="$MISSING TELEGRAM_API_ID"
[ -z "${TELEGRAM_API_HASH:-}" ] && MISSING="$MISSING TELEGRAM_API_HASH"
if [ -n "$MISSING" ]; then
    echo "ERROR: Missing required vars in .env:$MISSING"
    echo "  Edit: nano $APP_DIR/.env"
    exit 1
fi

# --- Start self-hosted Telegram Bot API (Docker) ---
echo "[7/8] Starting self-hosted Telegram Bot API..."

# Create a minimal compose file for just the Telegram Bot API
cat > "$APP_DIR/docker-compose.telegram-api.yml" <<DCEOF
services:
  telegram-bot-api:
    image: aiogram/telegram-bot-api:latest
    restart: unless-stopped
    environment:
      TELEGRAM_API_ID: "${TELEGRAM_API_ID}"
      TELEGRAM_API_HASH: "${TELEGRAM_API_HASH}"
      TELEGRAM_LOCAL: "1"
    volumes:
      - telegram-data:/var/lib/telegram-bot-api
    ports:
      - "127.0.0.1:8081:8081"
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:8081"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  telegram-data:
DCEOF

# Log out from official API (required migration step, safe to repeat)
echo "  Logging out from official Telegram API..."
curl -sf "https://api.telegram.org/bot${DONNA_BOT_TOKEN}/logOut" >/dev/null 2>&1 || true
sleep 3

docker compose -f "$APP_DIR/docker-compose.telegram-api.yml" -p donna-tg up -d

# --- Install systemd service ---
echo "[8/8] Installing donna.service..."
cat > /etc/systemd/system/donna.service <<SVCEOF
[Unit]
Description=Donna - Telegram AI Agent (Donna Summer voice)
After=network-online.target docker.service
Wants=network-online.target

[Service]
Type=simple
User=donna
Group=donna
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$DONNA_HOME/.local/bin/uv run python bot.py
Restart=on-failure
RestartSec=10

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=donna

# Security hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$APP_DIR $DONNA_HOME/.local $DONNA_HOME/.cache
PrivateTmp=true

[Install]
WantedBy=multi-user.target
SVCEOF

systemctl daemon-reload
systemctl enable donna.service
systemctl restart donna.service

echo ""
echo "=== Donna is live! ==="
echo ""
echo "  User:              donna (no sudo)"
echo "  App:               $APP_DIR"
echo "  Config:            $APP_DIR/.env"
echo "  Telegram Bot API:  http://127.0.0.1:8081 (Docker)"
echo "  Bot:               systemd donna.service"
echo "  Voice:             Donna Summer (JBFqnCBsd6RMkjVDRZzb)"
echo "  Claude:            claude --print (Max plan)"
echo ""
echo "  Commands:"
echo "    systemctl status donna          # Check status"
echo "    journalctl -u donna -f          # Follow logs"
echo "    systemctl restart donna         # Restart bot"
echo "    systemctl stop donna            # Stop bot"
echo "    su - donna                      # Switch to donna user"
echo ""
echo "  Telegram Bot API:"
echo "    docker compose -f $APP_DIR/docker-compose.telegram-api.yml -p donna-tg logs -f"
echo "    docker compose -f $APP_DIR/docker-compose.telegram-api.yml -p donna-tg restart"
echo ""
echo "  Send a message to @dante_claude_bot on Telegram to test!"
