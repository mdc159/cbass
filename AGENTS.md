# CBass - Self-hosted AI Package

**Fork of n8n's self-hosted-ai-starter-kit by coleam00**

## OVERVIEW

Docker Compose orchestration for local AI stack: n8n + Supabase + Ollama + Open WebUI + Flowise + Qdrant + Neo4j + SearXNG + Langfuse + Caddy reverse proxy.

## STRUCTURE

```
CBass/
├── docker-compose.yml          # Main orchestration (includes supabase)
├── docker-compose.override.*.yml  # Environment-specific overrides
├── start_services.py           # Entry point - clones supabase, starts stack
├── Caddyfile                    # Reverse proxy routes
├── env.example                  # Required env vars template
├── n8n_pipe.py                  # Open WebUI → n8n integration function
├── flowise/                     # Flowise custom tool configs (JSON)
├── n8n/backup/workflows/        # Pre-built n8n RAG workflows (JSON)
├── n8n-tool-workflows/          # Additional n8n tool workflows (JSON)
├── searxng/                     # SearXNG settings
└── supabase/                    # Auto-cloned on first run
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Start the stack | `python start_services.py --profile gpu-nvidia` | Profiles: cpu, gpu-nvidia, gpu-amd, none |
| Add env vars | `.env` (copy from `env.example`) | NEVER commit `.env` |
| Expose new service | `Caddyfile` + add `*_HOSTNAME` to `.env` | Auto-TLS via Let's Encrypt |
| Add n8n workflow | `n8n/backup/workflows/*.json` | Auto-imported on container start |
| Add Flowise tool | `flowise/*.json` | Manual import in Flowise UI |
| Modify service | `docker-compose.yml` | x-n8n, x-ollama = YAML anchors |
| Public deployment | `--environment public` | Closes all ports except 80/443 |

## SERVICES & PORTS

| Service | Internal Port | Default Local | Container Name |
|---------|---------------|---------------|----------------|
| n8n | 5678 | :8001 | n8n |
| Open WebUI | 8080 | :8002 | open-webui |
| Flowise | 3001 | :8003 | flowise |
| Ollama | 11434 | :8004 | ollama |
| Supabase (Kong) | 8000 | :8005 | kong |
| SearXNG | 8080 | :8006 | searxng |
| Langfuse | 3000 | :8007 | langfuse-web |
| Neo4j | 7474 | :8008 | neo4j |
| Qdrant | 6333/6334 | internal | qdrant |
| Postgres | 5432 | internal | postgres |
| Redis/Valkey | 6379 | internal | redis |

## CONVENTIONS

### Environment Variables
- Hostnames: `{SERVICE}_HOSTNAME` (e.g., `N8N_HOSTNAME=n8n.example.com`)
- Local dev: Leave hostnames commented → uses `:800X` ports
- Production: Set hostnames → Caddy auto-provisions TLS
- **NEVER use `@` in `POSTGRES_PASSWORD`** - breaks connection strings

### Docker Compose Patterns
- Project name: `localai` (all services share network)
- YAML anchors: `x-n8n`, `x-ollama`, `x-init-ollama` for DRY configs
- Profiles: `cpu`, `gpu-nvidia`, `gpu-amd` for Ollama variants
- Override files: `private` (exposes ports), `public` (locks down)

### Service Communication
- Internal DNS: Use container names (e.g., `http://ollama:11434`)
- n8n credentials:
  - Ollama: `http://ollama:11434`
  - Postgres: Host is `db` (Supabase container)
  - Qdrant: `http://qdrant:6333`

## ANTI-PATTERNS

| Don't | Why | Do Instead |
|-------|-----|------------|
| Edit `supabase/` directly | Auto-cloned, changes lost on update | Fork supabase repo |
| Commit `.env` | Contains secrets | Use `env.example` as template |
| Use `@` in Postgres password | Breaks URI parsing | Use alphanumeric + safe symbols |
| Run `docker compose` directly | Missing project name/includes | Use `start_services.py` |
| Expose ports in production | Security risk | Use Caddy reverse proxy |

## COMMANDS

```bash
# Start (first time or update)
python start_services.py --profile gpu-nvidia

# Start for cloud/VPS
python start_services.py --profile gpu-nvidia --environment public

# Stop all
docker compose -p localai --profile gpu-nvidia -f docker-compose.yml down

# Update containers
docker compose -p localai --profile gpu-nvidia -f docker-compose.yml pull
python start_services.py --profile gpu-nvidia

# View logs
docker compose -p localai logs -f n8n
docker compose -p localai logs -f ollama

# Pull new Ollama model
docker exec -it ollama ollama pull llama3.1
```

## STARTUP SEQUENCE

1. `start_services.py` clones/updates `supabase/` repo (sparse checkout)
2. Copies root `.env` → `supabase/docker/.env`
3. Generates SearXNG secret key (replaces `ultrasecretkey`)
4. Stops existing `localai` containers
5. Starts Supabase stack first (needs 10s init)
6. Starts local AI stack with selected profile

## NOTES

- **First run**: Ollama pulls `qwen2.5:7b-instruct-q4_K_M` + `nomic-embed-text` automatically
- **Mac users**: Can't expose GPU to Docker; run Ollama locally, use `--profile none`
- **SearXNG first run**: May need `chmod 755 searxng` for uwsgi.ini creation
- **Supabase pooler restart loop**: See [GitHub issue #30210](https://github.com/supabase/supabase/issues/30210)
- **n8n shared folder**: `/data/shared` inside container maps to `./shared` on host
- **Open WebUI + n8n**: Paste `n8n_pipe.py` as function, set webhook URL in valve settings
