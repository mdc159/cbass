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

## Current Todo

### In Progress
- [ ] Set up MCP servers for Claude Code integration
  - [x] n8n-mcp configured (`.mcp.json` created with API key)
  - [x] mcp-flowise configured (API key added)
  - [ ] Install n8n-skills plugin (`/plugin install czlonkowski/n8n-skills`)
  - [ ] Restart Claude Code to load MCP servers

### Next Up
- [ ] Create n8n owner account (user management was reset)
- [ ] Re-import backed up workflow from `/tmp/n8n-backup.json`
- [ ] Write services overview tutorial for biology student
- [ ] First biology project: Build a simple n8n workflow

### Completed
- [x] Video landing page added to dashboard
- [x] OpenCode service removed from dashboard
- [x] Local/GitHub/VPS repos synced
- [x] Added educational purpose to CLAUDE.md
- [x] Added .env sync reminder to constraints
- [x] UI Designer Pipeline workflow rebuilt (`CYfLRw6IPTJ7tfcD`)

## n8n MCP Issues (Needs Fix)

The `n8n-mcp` package has several issues discovered during workflow development:

### Issue 1: Incorrect/Non-existent Node Types

The MCP returns node information for types that don't exist or have incorrect capabilities:

| Claimed Node | Issue |
|--------------|-------|
| `@n8n/n8n-nodes-langchain.googleGemini` | Does NOT exist - only `lmChatGoogleGemini` exists |
| Image operations (`resource: "image"`, `operation: "analyze"`) | Not available on any Gemini node |

**Workaround**: Use `search_nodes` to verify node existence before using. The only Google Gemini node available is `@n8n/n8n-nodes-langchain.lmChatGoogleGemini` (a language model node for agents/chains).

### Issue 2: No Credential Management Tools

The n8n API supports credential operations, but n8n-mcp doesn't expose them:

**Missing tools needed**:
```
n8n_list_credentials     - List all credentials (id, name, type)
n8n_get_credential       - Get credential metadata by ID
n8n_assign_credential    - Assign credential to workflow nodes
```

**Current workaround**: Manually look up credential IDs in n8n UI, then use `n8n_update_partial_workflow` with:
```json
{
  "type": "updateNode",
  "nodeName": "OpenAI Chat Model",
  "updates": {
    "credentials": {
      "openAiApi": { "id": "CREDENTIAL_ID", "name": "OpenAI" }
    }
  }
}
```

### Known Credential IDs (CBass Instance)

| Service | Credential ID | Credential Type |
|---------|---------------|-----------------|
| OpenAI | `t6PNOhqfMP9ssxHr` | `openAiApi` |
| Google Gemini | `UwcFmvOdHdi8YhPh` | `googlePalmApi` |

### Proposed Fix: Fork n8n-mcp

1. Fork https://github.com/czlonkowski/n8n-mcp
2. Add credential management tools to `src/mcp/tools-n8n-manager.ts`
3. Fix node type validation against actual n8n node catalog
4. Update `.mcp.json` to use local fork

## Flowise Issues

### UI Import Fix Applied

The Flowise UI "Load Chatflow" feature was failing silently due to volume permissions and upload size limits. The following fixes were applied:

**Changes made**:
1. **Named volume**: Changed from `~/.flowise:/root/.flowise` to `flowise:/root/.flowise` (uses Docker named volume, fixes UID/GID mismatch)
2. **File size limit**: Added `FLOWISE_FILE_SIZE_LIMIT=50mb` environment variable
3. **Caddy body limit**: Added `request_body { max_size 50MB }` to Caddyfile for Flowise route

**VPS Migration Required**: When deploying to VPS, existing Flowise data needs to be migrated:
```bash
# 1. Backup existing data before deployment
cp -r ~/.flowise ~/flowise-backup-$(date +%Y%m%d)

# 2. After git pull and restart, if Flowise appears empty:
docker volume inspect localai_flowise
sudo cp -r ~/flowise-backup-*/* /var/lib/docker/volumes/localai_flowise/_data/
sudo chown -R 1000:1000 /var/lib/docker/volumes/localai_flowise/_data/
docker compose -p localai restart flowise
```

### Fallback: API Import

If UI import still fails, the API workaround remains available:

```bash
# The raw export format {nodes, edges} doesn't work
# Must wrap as {name, flowData, type} where flowData is STRINGIFIED JSON

curl -X POST "https://flowise.cbass.space/api/v1/chatflows" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FLOWISE_API_KEY" \
  -d @wrapped-flow.json
```

**Wrapper script**: `X:\GitHub\CBass\wrap_flowise.ps1` converts raw exports to API format.

### Template Import Note

The `flowise-masterclass` templates use invalid model names like `gpt-4.1-mini` (doesn't exist). Fixed version uses `gpt-4o-mini`.

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
- **Keep local and VPS `.env` files in sync manually** (they don't sync via git)

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

## Claude Code Commands

Three slash commands are installed globally that wrap Docker Compose and `start_services.py` with AI interpretation. They are available in any Claude Code session (not just this repo). Use them instead of running the CLI directly when you want analysis, not just raw output.

| Command | What it does |
|---------|-------------|
| `/cbass-status` | Runs `docker compose -p localai ps`, then categorizes every service as Healthy / Warning / Down with diagnosis and fix commands. Accepts optional focus (e.g., `/cbass-status "databases"`). |
| `/cbass-logs` | Fetches logs for a specific service, interprets errors, cross-references the service dependency chain, and suggests remediation. Usage: `/cbass-logs "n8n"` or `/cbass-logs "ollama" "model loading stuck"`. |
| `/cbass-deploy` | Guided deployment — runs pre-flight checks (Docker running, `.env` exists, disk space, port conflicts), lets you choose profile/environment, executes `start_services.py`, then validates all services came up healthy. |

### Recommended Workflows

**Check what's running:**
```
/cbass-status
```
Quick overview of all 28 services with health interpretation.

**Diagnose a failing service:**
```
/cbass-status
/cbass-logs "n8n"
```
Status first to identify the problem, then logs for the specific service.

**Start the stack:**
```
/cbass-deploy "gpu-nvidia" "private"
```
Guided deployment with pre-flight validation and post-deploy health check.

**Deep investigation:**
```
/rca "n8n returning 502 — container restarting"
```
For complex issues that span multiple services, use the general-purpose RCA command.

### How They Work

All commands call `docker compose -p localai` or `start_services.py` via Bash — they never reimplement Docker logic. The AI layer adds:
- **Categorization** — raw container states become prioritized tiers (Healthy/Warning/Down)
- **Dependency awareness** — knows that if `db` is down, `n8n`, `langfuse`, and `kong` will also fail
- **Error interpretation** — translates log patterns into plain-language diagnosis
- **Remediation** — provides exact fix commands for each issue
- **Pre-flight validation** — `/cbass-deploy` checks Docker, `.env`, disk space, and port conflicts before starting

The shared knowledge base lives in the `cbass-context` skill (installed globally at `~/.claude/skills/cbass-context/`). It contains the full 28-service inventory with ports, deployment profiles, subdomain routing, a domain glossary (RAG, vector stores, LLM terms), known issues with workarounds, and the service dependency chain.

### General-Purpose Commands

These commands work in any repo and are always available:

| Command | What it does |
|---------|-------------|
| `/quick-prime` | Fast 4-point project context |
| `/deep-prime "area" "focus"` | Deep analysis of a specific area |
| `/code-review` | Comprehensive code review with report |
| `/rca "error"` | Root cause analysis for issues |
| `/onboarding` | Interactive project introduction |
| `/remember "fact"` | Store a preference or decision |
| `/memory` | View and search stored memory |
