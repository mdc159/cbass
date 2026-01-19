# CBass - Self-Hosted AI Stack

## Project Overview

CBass is a self-hosted AI Docker Compose orchestration platform - a fork/enhancement of n8n's self-hosted-ai-starter-kit. It combines 10+ AI and database services into a cohesive local infrastructure stack.

## Educational Purpose

**This site serves as an educational tutorial platform for teaching AI tools and services.**

The primary learner is studying **biology**, so projects and examples should interweave:
- Learning how to use the AI/automation tools (n8n, Flowise, Open WebUI, etc.)
- Applying them to biology-related problems and workflows

### Biology + AI Project Ideas

| Tool | Biology Application |
|------|---------------------|
| **n8n** | Automate literature searches, monitor PubMed for new papers, parse research PDFs |
| **Open WebUI + Ollama** | Chat with biology textbooks, explain complex concepts, quiz preparation |
| **Neo4j** | Build knowledge graphs of metabolic pathways, gene interactions, taxonomies |
| **Supabase** | Store and query experimental data, species databases, lab inventory |
| **Flowise** | Create study assistants, flashcard generators, concept explainers |
| **SearXNG** | Privacy-focused research searches across academic sources |
| **Qdrant** | Semantic search over biology papers, find similar research |
| **Langfuse** | Track learning progress, analyze chat interactions |

### Learning Progression
1. **Basics**: Navigate dashboard, understand what each service does
2. **Chat**: Use Open WebUI to ask biology questions, learn prompt engineering
3. **Automation**: Build first n8n workflow (e.g., daily biology fact emailer)
4. **Data**: Store biology data in Supabase, query it
5. **Knowledge Graphs**: Model biological relationships in Neo4j
6. **RAG**: Build a biology study assistant with document retrieval
7. **Advanced**: Combine multiple services into complex biology research tools

## Infrastructure

- **Domain**: `cbass.space` - registered and managed at Amazon (Route 53)
- **VPS Hosting**: Hostinger
- **VPS IP**: `191.101.0.164`
- **VPS Hostname**: `sebastian`
- **SSH Access**: `ssh cbass` (uses key at `~/.ssh/cbass_vps`)
- **Deployment Path**: `/opt/cbass`
- **Orchestration**: Docker Compose with project name `localai`

## Live Services (cbass.space)

| Subdomain | Service | Status |
|-----------|---------|--------|
| `cbass.space` | Dashboard (Next.js AI Command Center) | Running |
| `www.cbass.space` | Redirect to cbass.space | Running |
| `n8n.cbass.space` | n8n Workflow Automation | Running |
| `openwebui.cbass.space` | Open WebUI Chat | Running |
| `flowise.cbass.space` | Flowise Visual Builder | Running |
| `supabase.cbass.space` | Supabase Studio | Running |
| `langfuse.cbass.space` | Langfuse Observability | Running |
| `neo4j.cbass.space` | Neo4j Browser | Running |
| `searxng.cbass.space` | SearXNG Search | Running |
| `kali.cbass.space` | Kali Linux Desktop (KasmWeb) | Running |

## VPS Resources

- **OS**: Ubuntu (Linux 5.15.0-164-generic)
- **Disk**: 97GB total, ~46GB used (48%)
- **Memory**: 7.8GB total, ~5.2GB used
- **Containers**: 28 running services

## Core Services

| Service | Port | Purpose |
|---------|------|---------|
| **Dashboard** | 3001 | Next.js AI Command Center with video landing |
| **n8n** | 5678 | Workflow automation & AI agent building |
| **Open WebUI** | 8080 | Chat interface for LLMs |
| **Supabase** | 8000 | Postgres DB, vector store (pgvector), auth |
| **Ollama** | 11434 | Local LLM inference |
| **Flowise** | 3000 | Visual no-code AI builder |
| **Qdrant** | 6333 | Vector database for RAG |
| **Neo4j** | 7474/7687 | Knowledge graphs |
| **SearXNG** | 8081 | Meta search engine |
| **Langfuse** | 3000 | LLM observability & tracing |
| **Kali** | 6901 | Browser-based Kali Linux (KasmWeb) |
| **Updater** | 9000 | Webhook-triggered container updates |
| **Caddy** | 80/443 | Reverse proxy with auto-TLS |

## Key Files

| File | Purpose |
|------|---------|
| `start_services.py` | Main entry point - clones Supabase, starts stack |
| `docker-compose.yml` | Container orchestration with profile support |
| `docker-compose.override.private.yml` | Development mode (all ports exposed) |
| `docker-compose.override.public.yml` | Production mode (only 80/443 via Caddy) |
| `Caddyfile` | Reverse proxy routing with auto-TLS |
| `n8n_pipe.py` | Open WebUI to n8n integration bridge |
| `env.example` | Environment template (copy to `.env`) |

## Directory Structure

```
CBass/
├── start_services.py        # Main orchestrator
├── docker-compose.yml       # Service definitions
├── Caddyfile               # Reverse proxy config
├── n8n_pipe.py             # Open WebUI → n8n bridge
├── dashboard/              # Next.js AI Command Center
│   ├── app/               # Next.js app router pages
│   ├── components/        # UI components (shadcn/ui)
│   ├── public/            # Static assets (bg.mp4 video)
│   └── Dockerfile         # Container build
├── scripts/                # Webhook automation
│   ├── hooks.json         # Webhook configuration
│   └── update-container.sh # Container update script
├── supabase/               # Auto-cloned on first run
├── n8n/backup/             # Pre-built RAG workflows
├── n8n-tool-workflows/     # Additional workflow imports
├── flowise/                # Flowise tools & chatflows
├── searxng/                # SearXNG config (generated)
└── .claude/                # Claude Code config
    ├── agents/            # LSP-aware agents
    ├── skills/            # Reusable patterns
    └── hooks/             # Automated checks
```

## Deployment

### Profiles (GPU Support)
- `cpu` - CPU-only inference
- `gpu-nvidia` - NVIDIA GPU acceleration
- `gpu-amd` - AMD GPU acceleration
- `none` - No local LLM (external API only)

### Environment Modes
- **Private** (development): All ports exposed locally
- **Public** (production): Only 80/443 via Caddy with auto-TLS

### Commands
```bash
# Development (local)
python start_services.py --profile gpu-nvidia --environment private

# Production (VPS)
python start_services.py --profile gpu-nvidia --environment public
```

## User Flow

```
Open WebUI (:8080) → n8n_pipe.py → n8n webhook (:5678)
                                        ↓
                    ┌───────────────────┼───────────────────┐
                    ↓                   ↓                   ↓
               Ollama             Supabase              Qdrant
            (LLM inference)    (DB/vectors)        (vector search)
```

## Configuration

### Environment Variables (in `.env`)
- **Required**: `N8N_ENCRYPTION_KEY`, `POSTGRES_PASSWORD`, `JWT_SECRET`, `ANON_KEY`, `SERVICE_ROLE_KEY`
- **Hostnames**: `N8N_HOSTNAME`, `WEBUI_HOSTNAME`, `FLOWISE_HOSTNAME`, `DASHBOARD_HOSTNAME`, `KALI_HOSTNAME`, etc.
- **Dashboard**: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- **Kali**: `VNC_PW` (VNC password for Kali desktop)
- **Langfuse**: `CLICKHOUSE_PASSWORD`, `MINIO_ROOT_PASSWORD`
- **Neo4j**: `NEO4J_AUTH=username/password`

### Important Constraints
- Never use `@` in `POSTGRES_PASSWORD` (breaks URI parsing)
- `.env` is gitignored - never commit secrets
- Copy from `env.example` as template

## Pre-built Workflows

### n8n RAG Agents
- `V1_Local_RAG_AI_Agent.json` - Basic RAG with local LLM
- `V2_Local_Supabase_RAG_AI_Agent.json` - RAG using Supabase vectors
- `V3_Local_Agentic_RAG_AI_Agent.json` - Advanced agentic RAG

### Flowise Tools
- Google Docs creation
- Postgres queries
- Slack integration
- Web search

## Common Tasks

### Check Service Health
```bash
docker compose -p localai ps
```

### View Logs
```bash
docker compose -p localai logs -f [service-name]
```

### Restart a Service
```bash
docker compose -p localai restart [service-name]
```

### Stop All Services
```bash
docker compose -p localai down
```

## Security Notes

- All services communicate on internal Docker network
- Caddy enforces HTTPS in public mode
- Supabase handles JWT authentication
- Never expose `.env` or commit secrets
