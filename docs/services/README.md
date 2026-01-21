# CBass Service Inventory

This directory contains documentation for each service in the CBass stack.

## Service Overview

| Service | Container | Port | Status | Documentation |
|---------|-----------|------|--------|---------------|
| **n8n** | n8n | 5678 | Core | [n8n.md](./n8n.md) |
| **Flowise** | flowise | 3001 | Core | [flowise.md](./flowise.md) |
| **Open WebUI** | open-webui | 8080 | Core | [open-webui.md](./open-webui.md) |
| **Ollama** | ollama | 11434 | Core | [ollama.md](./ollama.md) |
| **Supabase** | kong | 8000 | Data | [supabase.md](./supabase.md) |
| **Qdrant** | qdrant | 6333 | Data | [qdrant.md](./qdrant.md) |
| **Neo4j** | neo4j | 7474 | Data | [neo4j.md](./neo4j.md) |
| **Langfuse** | langfuse-web | 3000 | Observability | [langfuse.md](./langfuse.md) |
| **SearXNG** | searxng | 8080 | Utility | [searxng.md](./searxng.md) |
| **Kali** | kali | 6901 | Utility | [kali.md](./kali.md) |
| **Caddy** | caddy | 80/443 | Infrastructure | [caddy.md](./caddy.md) |

## Service Categories

### Core Services (AI & Automation)

| Service | Purpose | Biology Use Case |
|---------|---------|------------------|
| **n8n** | Visual workflow automation | Automate PubMed searches, parse research PDFs |
| **Flowise** | No-code AI agent builder | Create biology study assistants |
| **Open WebUI** | Chat interface for LLMs | Chat with biology textbooks, explain concepts |
| **Ollama** | Local LLM inference | Run models locally for privacy |

### Data Layer

| Service | Purpose | Biology Use Case |
|---------|---------|------------------|
| **Supabase** | PostgreSQL + Auth + Storage | Store experimental data, species databases |
| **Qdrant** | Vector database for RAG | Semantic search over biology papers |
| **Neo4j** | Graph database | Model metabolic pathways, gene interactions |

### Observability

| Service | Purpose | Biology Use Case |
|---------|---------|------------------|
| **Langfuse** | LLM tracing & analytics | Track learning progress, analyze interactions |

### Utilities

| Service | Purpose | Biology Use Case |
|---------|---------|------------------|
| **SearXNG** | Privacy-focused meta search | Research across academic sources |
| **Kali** | Security testing desktop | Learn security fundamentals |
| **Caddy** | Reverse proxy with auto-TLS | Secure HTTPS for all services |

## Quick Access URLs

### Production (cbass.space)

| Service | URL |
|---------|-----|
| Dashboard | https://cbass.space |
| n8n | https://n8n.cbass.space |
| Open WebUI | https://openwebui.cbass.space |
| Flowise | https://flowise.cbass.space |
| Supabase | https://supabase.cbass.space |
| Langfuse | https://langfuse.cbass.space |
| Neo4j | https://neo4j.cbass.space |
| SearXNG | https://searxng.cbass.space |
| Kali | https://kali.cbass.space |

### Local Development

| Service | URL |
|---------|-----|
| n8n | http://localhost:5678 |
| Open WebUI | http://localhost:8080 |
| Flowise | http://localhost:3001 |
| Supabase | http://localhost:8000 |
| Neo4j | http://localhost:7474 |
| Langfuse | http://localhost:3000 |

## Container Communication

Services communicate internally using container names:

```
http://ollama:11434      # Ollama API
http://qdrant:6333       # Qdrant REST API
bolt://neo4j:7687        # Neo4j Bolt protocol
http://db:5432           # Supabase PostgreSQL
```

## Common Operations

```bash
# Check all services
docker compose -p localai ps

# Restart a service
docker compose -p localai restart <service-name>

# View service logs
docker compose -p localai logs -f <service-name>
```
