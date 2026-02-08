# CBass Service Reference

Complete reference for all services in the CBass stack.

## Service Inventory

| Service | Container | Port | Category | Status |
|---------|-----------|------|----------|--------|
| n8n | n8n | 5678 | Core | Production |
| Flowise | flowise | 3001 | Core | Production |
| Open WebUI | open-webui | 8080 | Core | Production |
| Ollama | ollama | 11434 | Core | Production |
| Supabase | kong | 8000 | Data | Production |
| Qdrant | qdrant | 6333 | Data | Production |
| Neo4j | neo4j | 7474 | Data | Production |
| Langfuse | langfuse-web | 3000 | Observability | Production |
| SearXNG | searxng | 8080 | Utility | Production |
| Kali | kali | 6901 | Utility | Production |
| Caddy | caddy | 80/443 | Infrastructure | Production |
| Dashboard | dashboard | 3000 | Frontend | Production |

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
| SearXNG | http://localhost:8081 |
| Qdrant Dashboard | http://localhost:6333/dashboard |

## Service Details

### n8n (Workflow Automation)

**Purpose**: Visual workflow automation, AI agent orchestration

**Key Files**:
- `docs/services/n8n.md` - Full documentation
- `n8n/backup/workflows/` - Pre-built RAG workflows
- `n8n_pipe.py` - Open WebUI integration

**Credentials** (use container names):
| Service | Host | Port |
|---------|------|------|
| Ollama | `ollama` | 11434 |
| PostgreSQL | `db` | 5432 |
| Qdrant | `qdrant` | 6333 |
| Neo4j | `neo4j` | 7687 |

---

### Flowise (Visual AI Builder)

**Purpose**: No-code AI agent and chatbot creation

**Key Files**:
- `docs/services/flowise.md` - Full documentation
- `flowise/` - Pre-built tools and chatflows
- `wrap_flowise.ps1` - Import format converter

**Import Methods**:
| Method | Location | Format | Saves |
|--------|----------|--------|-------|
| Load Data | Settings > Load Data | ExportData | Yes |
| Load Chatflow | Canvas > Settings | Raw | No |

---

### Open WebUI (Chat Interface)

**Purpose**: ChatGPT-style interface for local LLMs

**Key Files**:
- `docs/services/open-webui.md` - Full documentation
- `n8n_pipe.py` - n8n integration function

**n8n Integration**:
1. Activate n8n workflow with webhook trigger
2. Copy Production webhook URL
3. Add n8n_pipe as Open WebUI function
4. Configure webhook URL in valve settings

---

### Ollama (LLM Inference)

**Purpose**: Run LLMs locally

**Default Models**:
- `qwen2.5:7b-instruct-q4_K_M` - General purpose
- `nomic-embed-text` - Embeddings for RAG

**Commands**:
```bash
# List models
docker exec -it ollama ollama list

# Pull model
docker exec -it ollama ollama pull llama3.1

# Remove model
docker exec -it ollama ollama rm modelname
```

---

### Supabase (Database Platform)

**Purpose**: PostgreSQL + pgvector + Auth + Storage

**Containers**: kong, db, auth, rest, realtime, storage, studio, pooler

**Connection**:
```
postgresql://postgres:PASSWORD@db:5432/postgres
```

**Warning**: No `@` in POSTGRES_PASSWORD

**Login**:
- Username: `DASHBOARD_USERNAME` from .env
- Password: `DASHBOARD_PASSWORD` from .env

---

### Qdrant (Vector Database)

**Purpose**: Similarity search for RAG applications

**API**: `http://qdrant:6333`

**Dashboard**: `http://localhost:6333/dashboard`

**Vector Dimensions**:
| Model | Dimensions |
|-------|------------|
| OpenAI text-embedding-3-small | 1536 |
| nomic-embed-text | 768 |
| all-MiniLM-L6-v2 | 384 |

---

### Neo4j (Graph Database)

**Purpose**: Knowledge graphs, relationship modeling

**URLs**:
- Browser: `http://localhost:7474`
- Bolt: `bolt://neo4j:7687`

**Auth**: From `NEO4J_AUTH` (format: `neo4j/password`)

---

### Langfuse (LLM Observability)

**Purpose**: Track LLM usage, costs, and performance

**Setup**:
1. Create account at Langfuse URL
2. Create project
3. Generate API keys
4. Integrate via SDK or HTTP

---

### SearXNG (Meta Search)

**Purpose**: Privacy-respecting search aggregation

**URL**: `http://localhost:8081` or `https://searxng.cbass.space`

**API**: `GET /search?q=query&format=json`

**Troubleshooting**:
```bash
chmod 755 searxng
docker compose -p localai restart searxng
```

---

### Kali (Security Desktop)

**Purpose**: Browser-based Kali Linux via KasmWeb

**URL**: `https://localhost:6901` (self-signed cert)

**Login**: VNC password from `VNC_PW` in .env

---

### Caddy (Reverse Proxy)

**Purpose**: HTTPS termination, automatic SSL, routing

**Config**: `Caddyfile`

**Adding Service**:
1. Add DNS A record
2. Add to Caddyfile: `{$HOSTNAME} { reverse_proxy service:port }`
3. Add to .env: `HOSTNAME=subdomain.cbass.space`
4. Restart: `docker compose -p localai restart caddy`

## Biology Applications by Service

| Service | Biology Use Case |
|---------|------------------|
| n8n | Automate PubMed monitoring, parse papers |
| Flowise | Biology study assistants, flashcards |
| Open WebUI | Chat with textbooks, explain concepts |
| Ollama | Local inference for privacy |
| Supabase | Experimental data, species databases |
| Qdrant | Semantic search over papers |
| Neo4j | Gene interactions, metabolic pathways |
| Langfuse | Track learning interactions |
| SearXNG | Academic literature search |
