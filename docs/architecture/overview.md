# Architecture Overview

High-level architecture of the CBass self-hosted AI stack.

## System Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Internet/Users                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Caddy Reverse Proxy                          │
│                 (HTTPS, Auto-TLS, Routing)                   │
│                 Port 80/443                                  │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Frontend Layer │ │   AI/Workflow   │ │   Data Layer    │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ Dashboard :3000 │ │ n8n :5678       │ │ Supabase :8000  │
│ Open WebUI:8080 │ │ Flowise :3001   │ │ Qdrant :6333    │
│                 │ │ Ollama :11434   │ │ Neo4j :7474     │
│                 │ │ Langfuse :3000  │ │ PostgreSQL:5432 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                 Docker Network (localai_default)             │
│                 Internal communication via container names   │
└─────────────────────────────────────────────────────────────┘
```

## Component Categories

### Frontend Layer

| Component | Purpose |
|-----------|---------|
| **Dashboard** | Next.js command center, service navigation |
| **Open WebUI** | ChatGPT-style interface for LLMs |

### AI/Workflow Layer

| Component | Purpose |
|-----------|---------|
| **n8n** | Workflow automation, AI agent orchestration |
| **Flowise** | Visual no-code AI agent builder |
| **Ollama** | Local LLM inference engine |
| **Langfuse** | LLM observability and tracing |

### Data Layer

| Component | Purpose |
|-----------|---------|
| **Supabase** | PostgreSQL + pgvector + Auth + Storage |
| **Qdrant** | Vector database for RAG |
| **Neo4j** | Graph database for knowledge graphs |

### Infrastructure

| Component | Purpose |
|-----------|---------|
| **Caddy** | Reverse proxy, automatic HTTPS |
| **Redis** | Caching layer |

### Utilities

| Component | Purpose |
|-----------|---------|
| **SearXNG** | Privacy-focused meta search |
| **Kali** | Security testing desktop |
| **Updater** | Webhook-triggered container updates |

## Data Flow

### Primary Chat Flow

```
User → Caddy → Open WebUI → n8n_pipe → n8n Webhook
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    ▼                      ▼                      ▼
               Ollama                 Supabase                 Qdrant
          (LLM inference)          (context/data)         (vector search)
                    │                      │                      │
                    └──────────────────────┼──────────────────────┘
                                           ▼
                                      n8n Webhook
                                           │
                                           ▼
User ← Caddy ← Open WebUI ← n8n_pipe ← Response
```

### RAG Flow

```
1. Document Ingestion:
   Document → Chunk → Embed (Ollama) → Store (Qdrant/Supabase)

2. Query Processing:
   Query → Embed → Search (Qdrant) → Retrieve Context
                                           │
                                           ▼
                              Prompt + Context → Ollama → Response
```

### Knowledge Graph Flow

```
Data → Extract Entities → Neo4j (store)
                              │
Query → Graph Traversal ← ────┘
              │
              ▼
         Enriched Response
```

## Docker Architecture

### Project Organization

- **Project name**: `localai`
- **Network**: `localai_default`
- **Volumes**: Named volumes prefixed with `localai_`

### Service Profiles

| Profile | Services Included |
|---------|-------------------|
| `cpu` | Ollama with CPU inference |
| `gpu-nvidia` | Ollama with NVIDIA GPU |
| `gpu-amd` | Ollama with AMD ROCm |
| `none` | No Ollama (external API) |

### Environment Modes

| Mode | Behavior |
|------|----------|
| `private` | All ports exposed locally |
| `public` | Only 80/443 through Caddy |

## File Organization

```
CBass/
├── docker-compose.yml              # Main service definitions
├── docker-compose.override.private.yml  # Dev mode
├── docker-compose.override.public.yml   # Prod mode
├── start_services.py               # Orchestration script
├── Caddyfile                       # Reverse proxy config
├── .env                            # Environment variables
├── dashboard/                      # Next.js frontend
├── n8n/backup/                     # Pre-built workflows
├── flowise/                        # Chatflows and tools
├── neo4j/                          # Graph database data
├── searxng/                        # Search engine config
└── supabase/                       # Auto-cloned on first run
```

## Security Architecture

### Network Isolation

- All services on isolated Docker network
- Only Caddy exposed to internet (80/443)
- Internal services use container DNS

### Authentication

- Caddy: HTTPS with Let's Encrypt
- Services: Individual authentication
- Supabase: JWT-based auth system

### Secrets

- Stored in `.env` (gitignored)
- Never exposed in containers
- Encrypted credentials in n8n

## Scaling Considerations

### Current Design

- Single-host deployment
- Suitable for personal/small team use
- Stateful services (not horizontally scalable)

### For Larger Scale

- Separate database hosts
- Load balance n8n workers
- Managed vector database (Pinecone, etc.)
- Managed LLM API (OpenAI, etc.)
