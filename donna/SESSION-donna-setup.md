# Donna Setup Session — 2026-03-26

## User

not CBASS! FUCK!
Just Donna, running in a non sudo account named Donna, claude code --print, skipping permissions, bot.py, telegram self hosted, Dante folder, 5 layer memory

## Claude

Got it — totally different thing. Let me find what exists in the repo for this.

*[Explored the full `/home/user/cbass/donna/` directory structure, read install.sh, .env, Dockerfile, docker-compose.yml, bot.py, prompts/default.md, and searched for memory layer references]*

Here's your prompt — just Donna, nothing else:

---

You are deploying Donna — a Telegram bot that bridges messages to Claude Code via `claude --print`. Nothing else. No CBass, no dashboard, no AI stack.

## What Donna Is
A Python bot (bot.py) that receives Telegram messages and pipes them to `claude --print --dangerously-skip-permissions`. Self-hosted Telegram Bot API runs in Docker. The bot runs bare metal under a non-sudo `donna` user via systemd.

## Step 1: Prerequisites
Make sure these exist (install if missing):
- Docker + Docker Compose V2 (for Telegram Bot API container only)
- Python 3.13+
- git, curl, ffmpeg, openssl
- Claude Code CLI (`claude` in PATH) — confirm with `claude --version`

## Step 2: Clone & copy
```bash
cd /opt
git clone https://github.com/mdc159/cbass.git
```
Only the `donna/` folder matters. Run the installer:
```bash
bash /opt/cbass/donna/install.sh
```
This will:
1. Create a `donna` user (no sudo)
2. Copy donna/ to /home/donna/app
3. Install uv + ffmpeg
4. Sync Python deps
5. Start self-hosted Telegram Bot API (Docker)
6. Install + start donna.service (systemd)

It will fail on first run if .env is missing tokens. It creates a template at `/home/donna/app/.env` — fill in and re-run.

## Step 3: .env — required tokens
Edit `/home/donna/app/.env`:
```
DONNA_BOT_TOKEN=<from @BotFather — the bot is @dante_claude_bot>
TELEGRAM_API_ID=<from https://my.telegram.org>
TELEGRAM_API_HASH=<from https://my.telegram.org>
```

Optional (voice):
```
ELEVENLABS_API_KEY=<from elevenlabs.io>
ELEVENLABS_VOICE_ID=JBFqnCBsd6RMkjVDRZzb
```

Leave the rest at defaults:
```
DONNA_PROMPT=default
DONNA_WORKDIR=/home/donna/app
CLAUDE_BIN=claude
CLAUDE_ARGS=--dangerously-skip-permissions
TELEGRAM_BASE_URL=http://127.0.0.1:8081/bot
TELEGRAM_BASE_FILE_URL=http://127.0.0.1:8081/file/bot
TELEGRAM_LOCAL_MODE=1
```

## Step 4: Re-run installer after .env is filled
```bash
bash /opt/cbass/donna/install.sh
```

## Step 5: Verify
```bash
systemctl status donna
journalctl -u donna -f
docker compose -f /home/donna/app/docker-compose.telegram-api.yml -p donna-tg ps
```

Then send a message to @dante_claude_bot on Telegram.

## 5-Layer Memory Architecture
Donna uses a 5-layer memory system. The layers are:
1. **System prompt** — `prompts/default.md` (persona, role, team context)
2. **Conversation history** — in-memory per-chat, last 20 message pairs
3. **CLAUDE.md / project files** — Claude Code reads these automatically from DONNA_WORKDIR
4. **MEMORY.md** — persistent file-based memory for escalations, decisions, learnings
5. **Archon MCP** — external task/project state via MCP client at localhost:8051

If Archon isn't running, Donna works fine without it — layers 1-4 are self-contained.

## Key paths
- App: `/home/donna/app/`
- Config: `/home/donna/app/.env`
- Prompts: `/home/donna/app/prompts/`
- Bot: `/home/donna/app/bot.py`
- Service: `systemctl {status|restart|stop} donna`
- Telegram API logs: `docker compose -f /home/donna/app/docker-compose.telegram-api.yml -p donna-tg logs -f`

## Rules
- Run as root only for install.sh. Everything else runs as the donna user.
- NEVER echo .env contents
- Ask before restarting the service
- The donna user has NO sudo — that's intentional

---

## User

can you export this entire session to a text or md file?

## Claude

*(exported to this file)*

---

## Key Files Referenced

| File | Purpose |
|------|---------|
| `donna/bot.py` | Main Telegram bot (37KB), bridges messages to `claude --print` |
| `donna/archon.py` | Async MCP client for Archon task management |
| `donna/voice.py` | ElevenLabs STT/TTS integration |
| `donna/tg_client.py` | Persistent Telethon user-session client |
| `donna/install.sh` | VPS installer — creates user, installs deps, starts services |
| `donna/.env` | Configuration (tokens, URLs, Claude CLI settings) |
| `donna/Dockerfile` | Python 3.13-slim, uv, ffmpeg, non-root donna user |
| `donna/docker-compose.yml` | Telegram Bot API + Donna bot services |
| `donna/prompts/default.md` | Donna's persona — disco queen agent with sass |
| `donna/prompts/shizzle-onboarding-coach.md` | Coach prompt for Shizzle onboarding |
| `donna/prompts/1215-oversight-judge.md` | Oversight judge for autonomous builder tests |
| `donna/gateway/server.py` | FastAPI voice gateway (Phase 2) |
| `donna/gateway/auth.py` | Telegram Mini App HMAC auth |
| `donna/ARCHON_ACCESS_PLAN.md` | Architecture decision doc for Archon integration |
| `donna/AGENT_COORDINATION_PROTOCOL.md` | Multi-agent task flow protocol |
| `donna/miniapp/` | React frontend for "Dante Voice" Mini App |

## Architecture Summary

```
Telegram User → @dante_claude_bot
                    ↓
        Self-hosted Telegram Bot API (Docker, port 8081)
                    ↓
        bot.py (systemd, donna user)
                    ↓
        claude --print --dangerously-skip-permissions
                    ↓
        Response back to Telegram
```

### Memory Layers

```
Layer 5: Archon MCP (localhost:8051) — external task/project state
Layer 4: MEMORY.md — persistent file-based memory
Layer 3: CLAUDE.md / project files — auto-read by Claude Code
Layer 2: Conversation history — in-memory, last 20 pairs per chat
Layer 1: System prompt — prompts/default.md (persona + role)
```
