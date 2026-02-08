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
python start_services.py --profile gpu-nvidia --environment private

# Or start with CPU only
python start_services.py --profile cpu --environment private
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
ANON_KEY=
SERVICE_ROLE_KEY=

# Neo4j
NEO4J_AUTH=neo4j/yourpassword
```

For local development, leave hostname variables commented out.

## Access Services

After startup completes:

| Service | URL |
|---------|-----|
| n8n | http://localhost:5678 |
| Open WebUI | http://localhost:8080 |
| Flowise | http://localhost:3001 |
| Supabase Studio | http://localhost:8000 |
| Neo4j Browser | http://localhost:7474 |
| Langfuse | http://localhost:3000 |
| SearXNG | http://localhost:8081 |

## GPU Profiles

| Profile | Command | Use Case |
|---------|---------|----------|
| `gpu-nvidia` | `--profile gpu-nvidia` | NVIDIA GPU (recommended) |
| `gpu-amd` | `--profile gpu-amd` | AMD GPU (Linux only) |
| `cpu` | `--profile cpu` | CPU only |
| `none` | `--profile none` | No local LLM (use external API) |

### Windows GPU Setup

1. Enable WSL 2 backend in Docker Desktop
2. Install NVIDIA Container Toolkit in WSL
3. Use `--profile gpu-nvidia`

### Mac Users

Docker on Mac cannot access GPU. Options:
1. Use `--profile cpu` (slow inference)
2. Run Ollama locally outside Docker, use `--profile none`
3. Use external API (OpenAI, Anthropic)

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
