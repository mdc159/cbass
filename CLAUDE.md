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

## Documentation

Comprehensive documentation is available in the `docs/` directory:

| Section | Content |
|---------|---------|
| [docs/getting-started/](docs/getting-started/) | Quick start, first workflow, biology projects |
| [docs/deployment/](docs/deployment/) | Local dev and VPS deployment guides |
| [docs/services/](docs/services/) | Per-service documentation (11 services) |
| [docs/architecture/](docs/architecture/) | System design and diagrams |
| [docs/operations/](docs/operations/) | Common tasks, backup, troubleshooting |

### Claude Code Onboarding

Use the `/onboard` command to quickly load project context:

```
/onboard           # Full project context
/onboard n8n       # Focus on n8n workflows
/onboard flowise   # Focus on Flowise
/onboard deploy    # Focus on deployment
/onboard data      # Focus on data layer
```

## Current Todo

### In Progress
- [ ] Fork n8n-mcp to add credential management tools (see `issues/n8n-mcp-issues.md`)

### Next Up
- [ ] Create n8n owner account (user management was reset)
- [ ] Re-import backed up workflow from `/tmp/n8n-backup.json`
- [ ] Write services overview tutorial for biology student
- [ ] First biology project: Build a simple n8n workflow

### Completed
- [x] MCP servers configured and working
  - [x] n8n-mcp configured with Windows `cmd /c` wrapper
  - [x] mcp-flowise configured
  - [x] flowise-enhanced local MCP server created
- [x] n8n-mcp issues investigated (see `issues/n8n-mcp-issues.md`)
- [x] Documentation restructured (consolidated 5 deployment guides, added 11 service docs)
- [x] Onboarding skill created (`/onboard` command)
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

## Flowise MCP Tools

The `mcp-flowise` server provides tools for interacting with Flowise chatflows programmatically.

### Quick Reference

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `list_chatflows` | List all available chatflows | None |
| `create_prediction` | Send a question to a chatflow | `question`, `chatflow_id` (optional) |

### Tool Details

#### `list_chatflows`

Lists all chatflows available in the Flowise instance.

```
No parameters required
```

**Returns**: JSON array of chatflows with IDs and names.

**Use when**: You need to discover available chatflows or find a chatflow ID.

#### `create_prediction`

Sends a question to a chatflow and returns the AI response.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `question` | string | Yes | The question or prompt to send |
| `chatflow_id` | string | No | Specific chatflow ID (uses default if not provided) |

**Example**:
```json
{
  "question": "What is photosynthesis?",
  "chatflow_id": "abc-123-def"
}
```

**Use when**: You want to query a Flowise chatflow from Claude Code.

### Usage Patterns

#### Pattern 1: Discover and Query

```
1. Call list_chatflows to see available chatflows
2. Note the chatflow_id you want to use
3. Call create_prediction with your question and chatflow_id
```

#### Pattern 2: Use Default Chatflow

If `FLOWISE_CHATFLOW_ID` is configured in the MCP settings, you can omit `chatflow_id`:

```json
{
  "question": "Explain DNA replication"
}
```

### Configuration

The MCP server is configured in `.mcp.json`:

```json
{
  "mcpServers": {
    "mcp-flowise": {
      "command": "uvx",
      "args": ["mcp-flowise"],
      "env": {
        "FLOWISE_API_KEY": "your-api-key",
        "FLOWISE_API_ENDPOINT": "http://localhost:3001",
        "FLOWISE_CHATFLOW_ID": "optional-default-chatflow-id"
      }
    }
  }
}
```

### Known Limitations

1. **No chatflow creation** - Cannot create or modify chatflows via MCP (use Flowise UI)
2. **No conversation history** - Each `create_prediction` is stateless
3. **Single response** - No streaming support

### Biology Applications

| Use Case | How |
|----------|-----|
| Quick biology Q&A | Query a biology-tuned chatflow |
| Test chatflows | Verify chatflow works before UI testing |
| Batch questions | Script multiple questions to a chatflow |

## Flowise Enhanced MCP Server

The `flowise-enhanced` server (local) provides workflow validation, wrapping, and creation capabilities that complement the basic `mcp-flowise` server.

### Quick Reference

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `validate_workflow` | Local + server-side validation | `workflow`, `chatflow_id`, `strict` |
| `wrap_workflow` | Convert raw workflow to ExportData | `workflow`, `name`, `generate_id` |
| `create_chatflow` | Create workflow via API | `workflow`, `name`, `deployed`, `validate_first` |
| `import_workflow` | Import ExportData via API | `exportdata` |
| `list_chatflows` | List all chatflows with details | None |
| `get_chatflow` | Get chatflow details | `chatflow_id` |

### Tool Details

#### `validate_workflow`

Two-stage validation: fast local checks + optional server-side validation.

**Local validation checks:**
- `nodes` array exists and non-empty
- `edges` array exists
- Each node has: `id`, `type`, `position`, `data`
- Each edge has: `source`, `target`, `id`
- Edge source/target nodes exist
- Flow type detection (CHATFLOW vs AGENTFLOW)
- AgentFlow: Start node presence

**Example:**
```json
{
  "workflow": {"nodes": [...], "edges": [...]},
  "strict": true
}
```

#### `wrap_workflow`

Converts raw workflow to ExportData format (Python port of `wrap_flowise.ps1`).

**Auto-detection logic:**
- Has `func`, `schema`, `name` → Tool
- Any node with `type: "agentFlow"` or `type: "iteration"` → AGENTFLOW
- Otherwise → CHATFLOW

**Example:**
```json
{
  "workflow": {"nodes": [...], "edges": [...]},
  "name": "My Biology Chatbot",
  "generate_id": true
}
```

#### `create_chatflow`

Creates workflow via Flowise API with optional validation.

**Example:**
```json
{
  "workflow": {"nodes": [...], "edges": [...]},
  "name": "Cell Division Tutor",
  "validate_first": true,
  "deployed": false
}
```

#### `import_workflow`

Imports full ExportData via Flowise API (equivalent to Settings → Load Data).

**Example:**
```json
{
  "exportdata": {
    "ChatFlow": [...],
    "AgentFlowV2": [...],
    "Tool": [...],
    ...
  }
}
```

### Configuration

Located in `.mcp.json`:
```json
"flowise-enhanced": {
  "command": "python",
  "args": ["-m", "mcp_flowise_enhanced"],
  "cwd": "X:\\GitHub\\CBass\\mcp\\flowise-enhanced",
  "env": {
    "FLOWISE_API_KEY": "...",
    "FLOWISE_API_ENDPOINT": "https://flowise.cbass.space"
  }
}
```

### Setup

```bash
cd mcp/flowise-enhanced
pip install -e .
# Then restart Claude Code
```

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

### Import Methods

Flowise has two different import mechanisms:

| Method | Location | Format Required | Saves to DB | Notes |
|--------|----------|-----------------|-------------|-------|
| **Load Data** | Settings → Load Data | ExportData (15 arrays) | YES | **RECOMMENDED** |
| **Load Chatflow** | Canvas → Settings → Load | Raw `{nodes, edges}` | NO | Errors silently, canvas only |

**Recommendation**: Always use **Settings → Load Data** for reliable imports. The "Load Chatflow" button only loads into the visual canvas without saving, and errors fail silently.

### ExportData Format

The full ExportData format (used by "Export All" and "Load Data"):

```json
{
  "AgentFlow": [],
  "AgentFlowV2": [{ "id": "uuid", "name": "...", "flowData": "stringified JSON", "type": "AGENTFLOW" }],
  "ChatFlow": [{ "id": "uuid", "name": "...", "flowData": "stringified JSON", "type": "CHATFLOW" }],
  "Tool": [{ "name": "...", "description": "...", "schema": "...", "func": "..." }],
  ...15 total arrays...
}
```

### Wrapper Script

The `wrap_flowise.ps1` script converts raw workflow files to ExportData format:

```powershell
# Convert all files in directory (creates flowise-import.json)
.\wrap_flowise.ps1 -Path "flowise"

# Convert single file (creates *-exportdata.json)
.\wrap_flowise.ps1 -Path "flowise\MyWorkflow.json"

# Then import via: Settings → Load Data
```

**Auto-detection**: The script detects flow type based on node types:
- Nodes with `type: "agentFlow"` or `type: "iteration"` → AgentFlowV2
- Nodes with `type: "customNode"` → ChatFlow
- Files with `func` and `schema` → Tool

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
├── mcp/                    # Local MCP servers
│   └── flowise-enhanced/   # Flowise validation/wrapping MCP
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
