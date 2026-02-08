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
- [ ] Create n8n owner account (user management was reset)

### Next Up
- [ ] Re-import backed up workflow from `/tmp/n8n-backup.json`
- [ ] Write services overview tutorial for biology student
- [ ] First biology project: Build a simple n8n workflow

### Completed
- [x] Add node building tools to flowise-enhanced MCP server
  - [x] Added 4 new tools: `list_node_types`, `get_node_schema`, `create_node`, `create_edge`
  - [x] Nodes can now be built programmatically with full UI schema
- [x] Fork n8n-mcp to add credential management tools (see `docs/n8n-mcp-credential-tools.md`)
  - [x] Added 5 credential tools: list, get, schema, test, assign
  - [x] Set up as git submodule in `vendor/n8n-mcp`
- [x] MCP servers configured and working
  - [x] n8n-mcp configured (forked with credential tools)
  - [x] mcp-flowise configured
  - [x] flowise-enhanced local MCP server created (11 tools total)
- [x] n8n-mcp issues investigated (see `issues/n8n-mcp-issues.md`)
- [x] Documentation restructured (consolidated 5 deployment guides, added 11 service docs)
- [x] Onboarding skill created (`/onboard` command)
- [x] Video landing page added to dashboard
- [x] OpenCode service removed from dashboard
- [x] Local/GitHub/VPS repos synced
- [x] Added educational purpose to CLAUDE.md
- [x] Added .env sync reminder to constraints
- [x] UI Designer Pipeline workflow rebuilt (`CYfLRw6IPTJ7tfcD`)
- [x] Unified .env file for local and VPS (synced via `scp cbass:/opt/cbass/.env`)
  - [x] Fixed broken Supabase keys (ANON_KEY, SERVICE_ROLE_KEY)
  - [x] Added KALI_HOSTNAME to both environments
  - [x] Generated new SSH key (`~/.ssh/cbass_vps`) and updated SSH config

## n8n MCP Issues (Needs Fix)

The `n8n-mcp` package has several issues discovered during workflow development:

### Issue 1: Incorrect/Non-existent Node Types

The MCP returns node information for types that don't exist or have incorrect capabilities:

| Claimed Node | Issue |
|--------------|-------|
| `@n8n/n8n-nodes-langchain.googleGemini` | Does NOT exist - only `lmChatGoogleGemini` exists |
| Image operations (`resource: "image"`, `operation: "analyze"`) | Not available on any Gemini node |

**Workaround**: Use `search_nodes` to verify node existence before using. The only Google Gemini node available is `@n8n/n8n-nodes-langchain.lmChatGoogleGemini` (a language model node for agents/chains).

### Issue 2: Credential Management Tools - PARTIALLY WORKING

**Status**: ⚠️ Partially fixed (see `docs/n8n-mcp-credential-tools.md`)

The forked n8n-mcp in `vendor/n8n-mcp` adds 5 credential management tools, but **n8n's Public API intentionally blocks GET requests to `/credentials` endpoints for security**:

| Tool | Status | Notes |
|------|--------|-------|
| `n8n_list_credentials` | ❌ Blocked | n8n API returns "GET method not allowed" |
| `n8n_get_credential` | ❌ Blocked | n8n API returns "GET method not allowed" |
| `n8n_get_credential_schema` | ✅ Works | Uses local data, not API |
| `n8n_test_credential` | ❌ Blocked | Depends on blocked GET endpoint |
| `n8n_assign_credential` | ✅ Works | Skips validation, uses known credential IDs |

**Workaround**: Use the manual credential registry below with `n8n_assign_credential`:
```
n8n_assign_credential({
  workflowId: "CYfLRw6IPTJ7tfcD",
  nodeName: "OpenAI Chat Model",
  credentialId: "t6PNOhqfMP9ssxHr",
  credentialType: "openAiApi",
  credentialName: "OpenAI API"  // optional display name
})
```

### Known Credential IDs (CBass Instance)

| Service | Credential ID | Credential Type |
|---------|---------------|-----------------|
| OpenAI | `t6PNOhqfMP9ssxHr` | `openAiApi` |
| Google Gemini | `UwcFmvOdHdi8YhPh` | `googlePalmApi` |

## Flowise MCP Server

Unified local MCP server for all Flowise operations - chatflow querying, workflow management, and validation.

### Quick Reference

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `list_node_types` | Get catalog of available nodes | `category`, `search`, `refresh` |
| `get_node_schema` | Get complete schema for a node type | `node_name`, `summary` |
| `create_node` | Build properly structured node from schema | `node_name`, `position`, `inputs`, `index` |
| `create_edge` | Build edge between two nodes | `source_node`, `target_node`, `target_input` |
| `create_prediction` | Send questions to chatflows | `question`, `chatflow_id`, `history` |
| `list_chatflows` | List all chatflows | None |
| `get_chatflow` | Get chatflow details | `chatflow_id` |
| `validate_workflow` | Local + server-side validation | `workflow`, `chatflow_id`, `strict` |
| `wrap_workflow` | Convert raw workflow to ExportData | `workflow`, `name`, `generate_id` |
| `create_chatflow` | Create workflow via API | `workflow`, `name`, `deployed`, `validate_first` |
| `import_workflow` | Import ExportData via API | `exportdata` |

### Tool Details

#### `list_node_types`

Get catalog of available Flowise node types with basic metadata. Use to discover what nodes are available for building workflows.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `category` | string | No | Filter by category (e.g., 'Chat Models', 'Agents', 'Tools', 'Memory') |
| `search` | string | No | Search nodes by name, label, or description |
| `refresh` | boolean | No | Force refresh from API (default: use cache) |

**Example:**
```json
{
  "category": "Chat Models"
}
```

**Returns:** List of nodes with `name`, `label`, `category`, `description`, `version`, `baseClasses`, plus `available_categories` list.

#### `get_node_schema`

Get complete schema for a specific Flowise node type. Returns inputParams, inputAnchors, outputAnchors needed for building nodes.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `node_name` | string | Yes | Node name (e.g., 'chatOllama', 'toolAgent', 'bufferMemory') |
| `summary` | boolean | No | Return simplified summary instead of full schema |

**Example:**
```json
{
  "node_name": "chatOllama",
  "summary": true
}
```

#### `create_node`

Build a properly structured Flowise node instance from schema. Creates a complete node with all required fields for UI rendering.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `node_name` | string | Yes | Node type name (e.g., 'chatOllama', 'toolAgent') |
| `position` | object | No | Node position `{x: number, y: number}` |
| `inputs` | object | No | Input values to set (e.g., `{modelName: 'qwen2.5:latest'}`) |
| `node_id` | string | No | Custom node ID (auto-generated if not provided) |
| `index` | integer | No | Index for auto-generated ID (e.g., 0 for chatOllama_0) |

**Example:**
```json
{
  "node_name": "chatOllama",
  "position": {"x": 200, "y": 100},
  "inputs": {"modelName": "qwen2.5:latest", "temperature": 0.7}
}
```

**Returns:** Complete node structure with `inputParams`, `inputAnchors`, `outputAnchors`, and proper IDs for Flowise UI.

#### `create_edge`

Build a properly structured edge connecting two Flowise nodes. Validates anchor compatibility and generates proper handle IDs.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source_node` | object | Yes | Source node instance (from create_node result) |
| `target_node` | object | Yes | Target node instance (from create_node result) |
| `target_input` | string | Yes | Name of input anchor on target (e.g., 'model', 'tools', 'memory') |
| `source_output` | string | No | Name of output anchor on source (auto-detected if not provided) |
| `validate_only` | boolean | No | Only validate connection, don't create edge |

**Example:**
```json
{
  "source_node": {"id": "chatOllama_0", "data": {...}},
  "target_node": {"id": "toolAgent_0", "data": {...}},
  "target_input": "model"
}
```

**Returns:** Edge structure with `source`, `target`, `sourceHandle`, `targetHandle`, plus type compatibility validation.

#### `create_prediction`

Send a question to a Flowise chatflow and get an AI response.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `question` | string | Yes | The question or prompt to send |
| `chatflow_id` | string | Yes | The chatflow ID to query |
| `history` | array | No | Conversation history as `[{role, content}, ...]` |

**Example:**
```json
{
  "question": "What is photosynthesis?",
  "chatflow_id": "abc-123-def"
}
```

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
"flowise": {
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

### Biology Applications

| Use Case | How |
|----------|-----|
| Quick biology Q&A | Query a biology-tuned chatflow with `create_prediction` |
| Test chatflows | Verify chatflow works before UI testing |
| Batch questions | Script multiple questions to a chatflow |
| Create study assistants | Use `create_chatflow` to build new chatflows programmatically |

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

### Environment File Sync

**One `.env` to rule them all** - The same `.env` file is used for both local development and VPS production. The VPS copy at `/opt/cbass/.env` is the source of truth.

**Why this works:**
- Hostnames like `n8n.cbass.space` work from anywhere (local browser hits VPS)
- All secrets are shared between environments
- No drift between local and production configs

**Sync Commands:**
```bash
# Pull latest from VPS to local
scp cbass:/opt/cbass/.env /home/mdc159/projects/cbass/.env

# Push local changes to VPS
scp /home/mdc159/projects/cbass/.env cbass:/opt/cbass/.env

# After changes on VPS, restart affected services
ssh cbass "cd /opt/cbass && docker compose -p localai restart [service]"
```

**SSH Setup:**
```bash
# SSH config (~/.ssh/config)
Host cbass
    HostName 191.101.0.164
    User root
    IdentityFile ~/.ssh/cbass_vps
```

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
