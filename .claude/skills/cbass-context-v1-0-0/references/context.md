# CBass Context Reference

## Core Files

- `CLAUDE.md` - Current state, todos, and known issues.
- `docs/README.md` - Documentation index.
- `docs/services/README.md` - Service inventory and links.
- `docs/deployment/README.md` - Deployment overview.
- `docs/operations/README.md` - Operations overview.

## Key Services (Quick List)

- n8n, Open WebUI, Flowise, Ollama
- Supabase (Postgres + pgvector), Qdrant, Neo4j
- Langfuse, SearXNG, Caddy

## Common Commands

```bash
# Start stack (example: GPU NVIDIA, private)
python start_services.py --profile gpu-nvidia --environment private

# Stop stack
docker compose -p localai --profile gpu-nvidia -f docker-compose.yml down

# Service logs
docker compose -p localai logs -f <service>
```

## Documentation Paths by Task

- **Deployment**: `docs/deployment/`
- **Ops / Troubleshooting**: `docs/operations/`
- **Per-service setup**: `docs/services/`
- **Architecture diagrams**: `docs/architecture/`
