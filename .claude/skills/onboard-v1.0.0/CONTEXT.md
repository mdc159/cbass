# CBass Project Context

Detailed context for Claude agents working on the CBass project.

## Project Identity

**CBass** = Self-hosted AI Docker Compose orchestration platform

- **Origin**: Fork of [coleam00/local-ai-packaged](https://github.com/coleam00/local-ai-packaged), which builds on [n8n-io/self-hosted-ai-starter-kit](https://github.com/n8n-io/self-hosted-ai-starter-kit)
- **Purpose**: Educational platform for teaching AI tools to a biology student
- **Live Site**: https://cbass.space

## Infrastructure

| Component | Value |
|-----------|-------|
| Domain | cbass.space (Route 53) |
| VPS Provider | Hostinger |
| VPS IP | 191.101.0.164 |
| VPS Hostname | sebastian |
| SSH Alias | `ssh cbass` |
| Deploy Path | /opt/cbass |
| Docker Project | `localai` |

## Educational Purpose

The primary learner is studying **biology**. All examples and projects should:
1. Teach AI/automation tool usage
2. Apply to biology-related problems

### Biology + AI Integration Ideas

| Tool | Biology Application |
|------|---------------------|
| n8n | Automate PubMed searches, monitor for new papers |
| Open WebUI | Chat with textbooks, explain concepts |
| Neo4j | Build gene interaction graphs, metabolic pathways |
| Supabase | Store experimental data, species databases |
| Flowise | Create study assistants, flashcard generators |
| SearXNG | Privacy-focused academic research |
| Qdrant | Semantic search over biology papers |
| Langfuse | Track learning progress |

## Architecture Patterns

### Service Communication

All services communicate on Docker network `localai_default`:

```
# Use container names, not localhost
http://ollama:11434     # Ollama API
http://qdrant:6333      # Qdrant REST
bolt://neo4j:7687       # Neo4j Bolt
postgresql://db:5432    # Supabase PostgreSQL
```

### Data Flow

```
User → Caddy → Open WebUI → n8n_pipe → n8n webhook
                                           ↓
                    ┌──────────────────────┼──────────────────────┐
                    ↓                      ↓                      ↓
               Ollama                 Supabase                 Qdrant
          (LLM inference)          (DB/vectors)           (vector search)
```

### Environment Modes

| Mode | Flag | Behavior |
|------|------|----------|
| private | `--environment private` | All ports exposed locally |
| public | `--environment public` | Only 80/443 via Caddy |

### GPU Profiles

| Profile | Flag | Use Case |
|---------|------|----------|
| gpu-nvidia | `--profile gpu-nvidia` | NVIDIA GPU |
| gpu-amd | `--profile gpu-amd` | AMD GPU (Linux) |
| cpu | `--profile cpu` | CPU only |
| none | `--profile none` | No local LLM |

## Known Issues

### n8n MCP Issues

The n8n-mcp tool has inaccuracies:
1. Claims non-existent nodes exist (e.g., `googleGemini`)
2. No credential management tools

**Workaround**: Verify nodes with `search_nodes` before using.

### Known Credential IDs (CBass Instance)

| Service | Credential ID | Type |
|---------|---------------|------|
| OpenAI | `t6PNOhqfMP9ssxHr` | openAiApi |
| Google Gemini | `UwcFmvOdHdi8YhPh` | googlePalmApi |

### Flowise Import Issues

- Use **Settings > Load Data** for reliable imports
- "Load Chatflow" button only loads to canvas, doesn't save
- Use `wrap_flowise.ps1` to convert raw workflows to ExportData format

### Critical Constraints

- **Never use `@` in POSTGRES_PASSWORD** - breaks URI parsing
- **Keep local and VPS .env in sync manually** - not git-tracked
- **Flowise templates may have invalid model names** - check and fix

## File Organization

```
CBass/
├── CLAUDE.md               # Claude Code instructions
├── README.md               # Project overview
├── docker-compose.yml      # Service definitions
├── start_services.py       # Main entry point
├── Caddyfile              # Reverse proxy
├── n8n_pipe.py            # Open WebUI → n8n bridge
├── dashboard/              # Next.js Command Center
├── docs/                   # Documentation
│   ├── deployment/        # Setup guides
│   ├── services/          # Per-service docs
│   └── operations/        # Day-to-day tasks
├── n8n/backup/            # Pre-built workflows
├── flowise/               # Chatflows and tools
├── .claude/               # Claude Code config
│   ├── skills/           # Reusable skills
│   ├── commands/         # Slash commands
│   └── agents/           # Sub-agents
└── supabase/              # Auto-cloned on first run
```

## Common Tasks

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

### Restart Service
```bash
docker compose -p localai restart <service-name>
```

### Stop All
```bash
docker compose -p localai down
```

## VPS Operations

### SSH Access
```bash
ssh cbass  # Uses ~/.ssh/cbass_vps key
```

### Deploy Updates
```bash
cd /opt/cbass
git pull
python3 start_services.py --profile cpu --environment public
```

### Sync .env Changes
Local and VPS `.env` must be synced manually - they're gitignored.

## Security Notes

- All external traffic through Caddy (HTTPS enforced)
- Internal services on Docker network only
- Only ports 80, 443, 22 exposed on VPS
- Supabase handles authentication
- Never commit `.env` or secrets
