# Local Development Setup

Get CBass running on your local machine for development and learning.

## Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)
- 16GB RAM recommended (8GB minimum)
- 20GB free disk space

## Quick Start

```bash
# Clone the repository
git clone https://github.com/mdc159/cbass.git
cd cbass

# Create environment file
cp env.example .env

# Start with NVIDIA GPU
python start_services.py --profile gpu-nvidia --environment private --open-dashboard

# Or start with CPU only
python start_services.py --profile cpu --environment private --open-dashboard
```

## Environment Configuration

Edit `.env` with your settings. Required variables:

```bash
# n8n (generate with: openssl rand -hex 32)
N8N_ENCRYPTION_KEY=
N8N_USER_MANAGEMENT_JWT_SECRET=

# Supabase
POSTGRES_PASSWORD=yourpassword    # NO '@' character!
JWT_SECRET=
PG_META_CRYPTO_KEY=               # Can reuse JWT_SECRET
ANON_KEY=
SERVICE_ROLE_KEY=
NEXT_PUBLIC_SUPABASE_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_ANON_KEY=    # same value as ANON_KEY

# Neo4j
NEO4J_AUTH=neo4j/yourpassword
```

For local development, leave hostname variables commented out.

Optional convenience flags for startup:
- `--open-dashboard` to auto-open the dashboard in your browser
- `--dashboard-url <url>` to override the default `http://localhost:3002`

## Access Services

After startup completes:

| Service | URL | Login Notes |
|---------|-----|-------------|
| Dashboard | http://localhost:3002 | Supabase auth |
| n8n | http://localhost:5678 | Create account on first visit |
| Open WebUI | http://localhost:8080 | Create account on first visit |
| Flowise | http://localhost:3001 | `FLOWISE_USERNAME` / `FLOWISE_PASSWORD` from `.env` |
| Supabase Studio | http://localhost:8000 | `DASHBOARD_USERNAME` / `DASHBOARD_PASSWORD` from `.env` |
| Neo4j Browser | http://localhost:7474 | Username must be `neo4j`, password from `NEO4J_AUTH` |
| Langfuse | http://localhost:3000 | `LANGFUSE_INIT_USER_EMAIL` / `LANGFUSE_INIT_USER_PASSWORD` (first run only) |
| SearXNG | http://localhost:8081 | No auth |
| Kali | https://localhost:6901 | HTTPS required, user: `kasm_user`, password: `KALI_VNC_PW` |

The `--environment private` flag configures:
- All service ports bound to `127.0.0.1`
- Dashboard card links pointing to `localhost` URLs (built into the Next.js app)
- n8n secure cookies disabled for plain HTTP access
- `NODE_TLS_REJECT_UNAUTHORIZED=0` on dashboard for Kali health checks (self-signed cert)

## GPU Profiles

| Profile | Command | Use Case |
|---------|---------|----------|
| `gpu-nvidia` | `--profile gpu-nvidia` | NVIDIA GPU (recommended for Linux/WSL) |
| `gpu-amd` | `--profile gpu-amd` | AMD GPU (Linux only) |
| `cpu` | `--profile cpu` | CPU only (no GPU acceleration) |
| `none` | `--profile none` | System Ollama (Apple Silicon) or external API |

### Windows GPU Setup

1. Enable WSL 2 backend in Docker Desktop
2. Install NVIDIA Container Toolkit in WSL
3. Use `--profile gpu-nvidia`

### Apple Silicon (M-series Macs)

Docker on Mac cannot access the Metal GPU. Use system Ollama instead:

1. **Install Ollama**: `brew install ollama && brew services start ollama`
2. **Pull models**: `ollama pull qwen2.5:7b-instruct-q4_K_M && ollama pull nomic-embed-text`
3. **Start CBass**: `python start_services.py --profile none --environment private`

Services connect to system Ollama via `http://host.docker.internal:11434` (pre-configured in `docker-compose.override.private.yml`).

See [Ollama service docs](../services/ollama.md#apple-silicon-m-series-macs) for full setup including launchd plist configuration and memory guide.

## First Run Notes

On first startup:
- Ollama downloads `qwen2.5:7b-instruct-q4_K_M` (~4GB)
- Ollama downloads `nomic-embed-text` (~275MB)
- Supabase initializes database (~30 seconds)
- Total first-run time: 5-15 minutes

## Common Commands

```bash
# Check status
docker compose -p localai ps

# View logs
docker compose -p localai logs -f n8n

# Restart a service
docker compose -p localai restart n8n

# Stop all services
docker compose -p localai down

# Update containers
docker compose -p localai -f docker-compose.yml --profile <profile> pull
python start_services.py --profile <profile> --environment private
```

## Troubleshooting

### Supabase Pooler Restarting

Known issue. See [GitHub #30210](https://github.com/supabase/supabase/issues/30210).
Services still work - pooler is optional for local dev.

### SearXNG Restarting

```bash
chmod 755 searxng
docker compose -p localai restart searxng
```

### Port Conflicts

If a port is in use, check what's running:

```bash
# Windows
netstat -ano | findstr :5678

# Linux/Mac
lsof -i :5678
```

### Out of Disk Space

```bash
# Clean unused Docker resources
docker system prune -a
```

### Slow Inference

- Use GPU profile if available
- Use smaller models: `ollama pull llama3.2:3b`
- Increase Docker memory allocation

## Development Workflow

1. **Start services**: `python start_services.py --profile gpu-nvidia`
2. **Open n8n**: http://localhost:5678
3. **Create/import workflows**
4. **Test with Open WebUI**: http://localhost:8080
5. **Stop when done**: `docker compose -p localai down`

## Pulling New Models

```bash
# Connect to Ollama container
docker exec -it ollama ollama pull llama3.1

# List installed models
docker exec -it ollama ollama list
```

## File Locations

| Resource | Path |
|----------|------|
| n8n workflows | `./n8n/backup/workflows/` |
| Flowise tools | `./flowise/` |
| Shared files (n8n) | `./shared/` → `/data/shared` in container |
| Docker volumes | `/var/lib/docker/volumes/localai_*` |
