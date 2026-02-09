# Quick Start

Get CBass running in 5 minutes.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) or Docker + Docker Compose (Linux)
- [Python 3.x](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- 8GB RAM minimum (16GB recommended)

## Step 1: Clone Repository

```bash
git clone https://github.com/mdc159/cbass.git
cd cbass
```

## Step 2: Create Environment File

```bash
cp env.example .env
```

Edit `.env` and set required variables:

```bash
# Generate encryption keys (run these commands)
# openssl rand -hex 32

N8N_ENCRYPTION_KEY=your_generated_key_here
N8N_USER_MANAGEMENT_JWT_SECRET=another_generated_key

POSTGRES_PASSWORD=choose_a_password    # No @ symbol!
JWT_SECRET=another_key
PG_META_CRYPTO_KEY=another_key
ANON_KEY=see_supabase_docs
SERVICE_ROLE_KEY=see_supabase_docs
NEXT_PUBLIC_SUPABASE_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_ANON_KEY=same_as_ANON_KEY

NEO4J_AUTH=neo4j/your_neo4j_password
```

## Step 3: Start Services

**With NVIDIA GPU (Linux/WSL):**
```bash
python start_services.py --profile gpu-nvidia --environment private --open-dashboard
```

**Apple Silicon (M-series Mac):**
```bash
# First: install system Ollama for Metal GPU acceleration
brew install ollama && brew services start ollama
ollama pull qwen2.5:7b-instruct-q4_K_M && ollama pull nomic-embed-text

# Then start CBass without Docker Ollama
python start_services.py --profile none --environment private --open-dashboard
```

**CPU Only:**
```bash
python start_services.py --profile cpu --environment private --open-dashboard
```

First startup takes 10-15 minutes to download images and models.
With `--open-dashboard`, your browser opens `http://localhost:3002` automatically when startup completes.

## Step 4: Access Services

| Service | URL |
|---------|-----|
| n8n | http://localhost:5678 |
| Open WebUI | http://localhost:8080 |
| Flowise | http://localhost:3001 |
| Supabase | http://localhost:8000 |
| Neo4j | http://localhost:7474 |

## Step 5: Create Accounts

1. **n8n**: Go to http://localhost:5678, create admin account
2. **Open WebUI**: Go to http://localhost:8080, sign up (first user = admin)
3. **Supabase**: Login with `DASHBOARD_USERNAME` and `DASHBOARD_PASSWORD` from .env

## What's Running?

After startup, you have:

- **n8n** - Build AI workflows and automations
- **Open WebUI** - Chat with local AI models
- **Flowise** - Visual AI agent builder
- **Ollama** - Local LLM inference (models auto-downloaded)
- **Supabase** - Database with vector search
- **Qdrant** - Vector database for RAG
- **Neo4j** - Knowledge graphs
- **SearXNG** - Privacy-focused search

## Common Commands

```bash
# Check status
docker compose -p localai ps

# View logs
docker compose -p localai logs -f n8n

# Stop all
docker compose -p localai down

# Restart a service
docker compose -p localai restart n8n
```

## Next Steps

1. [Build your first workflow](./first-workflow.md)
2. [Explore biology projects](./biology-projects.md)
3. [Review service documentation](../services/README.md)

## Troubleshooting

### Services not starting?

```bash
docker compose -p localai logs -f
```

### Out of memory?

Use `--profile cpu` or increase Docker memory allocation.

### Port in use?

Check what's using the port:
- Windows: `netstat -ano | findstr :5678`
- Linux/Mac: `lsof -i :5678`
