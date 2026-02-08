---
name: onboard
description: Load CBass project context for a fresh Claude session. Use when starting work, switching focus areas, or when unfamiliar with the codebase. Provides architecture overview, service inventory, and current project state.
user-invocable: true
allowed-tools: Read, Glob, Grep
---

# CBass Project Onboarding

Quickly bring a fresh Claude agent up to speed on the CBass self-hosted AI stack.

## Usage

```
/onboard           # Full project context
/onboard n8n       # Focus on n8n workflows and automation
/onboard flowise   # Focus on Flowise chatflows and agents
/onboard deploy    # Focus on deployment and operations
/onboard data      # Focus on data layer (Supabase, Qdrant, Neo4j)
```

## What This Skill Provides

### 1. Project Overview
- CBass is a self-hosted AI Docker Compose orchestration platform
- Fork of n8n's self-hosted-ai-starter-kit
- Educational platform for teaching AI tools (primary learner: biology student)
- Live deployment at cbass.space

### 2. Architecture Summary

```
Internet → Caddy (:443) → Internal Services
                              ↓
┌─────────────────────────────┼─────────────────────────────┐
│ Core               │ Data Layer        │ Utilities       │
├────────────────────┼───────────────────┼─────────────────┤
│ n8n (:5678)        │ Supabase (:8000)  │ Langfuse (:3000)│
│ Flowise (:3001)    │ Qdrant (:6333)    │ SearXNG (:8081) │
│ Open WebUI (:8080) │ Neo4j (:7474)     │ Kali (:6901)    │
│ Ollama (:11434)    │ PostgreSQL (:5432)│ Caddy (:80/443) │
└────────────────────┴───────────────────┴─────────────────┘
```

### 3. Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Claude Code instructions and known issues |
| `README.md` | Project overview and quick start |
| `docker-compose.yml` | Service definitions |
| `start_services.py` | Main entry point |
| `Caddyfile` | Reverse proxy routing |
| `.env` | Environment variables (secrets - gitignored) |

### 4. Documentation Structure

```
docs/
├── README.md           # Documentation index
├── getting-started/    # First-time setup guides
├── deployment/         # Local and VPS deployment
├── services/           # Per-service documentation (11 services)
├── architecture/       # System design and diagrams
├── operations/         # Day-to-day tasks
└── archive/            # Deprecated docs
```

## Focus Areas

### n8n Focus (`/onboard n8n`)

Read these files:
- `docs/services/n8n.md` - n8n service documentation
- `n8n/backup/workflows/` - Pre-built RAG workflows
- `n8n_pipe.py` - Open WebUI integration

Key concepts:
- Webhook triggers for external integration
- Credential configuration (use container names: `ollama`, `db`, `qdrant`)
- Known credential IDs in CLAUDE.md

### Flowise Focus (`/onboard flowise`)

Read these files:
- `docs/services/flowise.md` - Flowise service documentation
- `flowise/` - Pre-built tools and chatflows
- `wrap_flowise.ps1` - Import format converter

Key concepts:
- ExportData format vs raw workflow format
- Settings > Load Data for reliable imports
- Named volume for data persistence

### Deployment Focus (`/onboard deploy`)

Read these files:
- `docs/deployment/vps-setup.md` - Production deployment
- `docs/deployment/local-dev.md` - Local development
- `docs/deployment/dns-ssl.md` - DNS and SSL setup

Key concepts:
- GPU profiles: `gpu-nvidia`, `gpu-amd`, `cpu`, `none`
- Environment modes: `private` (dev), `public` (prod)
- Caddy handles automatic HTTPS

### Data Layer Focus (`/onboard data`)

Read these files:
- `docs/services/supabase.md` - PostgreSQL + pgvector
- `docs/services/qdrant.md` - Vector database
- `docs/services/neo4j.md` - Graph database

Key concepts:
- Supabase: Use container name `db` for PostgreSQL
- Qdrant: Vector dimensions must match embedding model
- Neo4j: Auth format is `neo4j/password`

## Current Project State

Check `CLAUDE.md` for:
- Current todo items
- Known issues and workarounds
- Credential IDs for CBass instance

## Quick Reference

### Start Services
```bash
python start_services.py --profile gpu-nvidia --environment private
```

### Check Status
```bash
docker compose -p localai ps
```

### View Logs
```bash
docker compose -p localai logs -f <service-name>
```

### Service URLs (Local)

| Service | URL |
|---------|-----|
| n8n | http://localhost:5678 |
| Open WebUI | http://localhost:8080 |
| Flowise | http://localhost:3001 |
| Supabase | http://localhost:8000 |
| Neo4j | http://localhost:7474 |

## Additional Context Files

For deeper understanding:
- [CONTEXT.md](CONTEXT.md) - Detailed project context
- [SERVICES.md](SERVICES.md) - Complete service reference
