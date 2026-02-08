# Project Context

## Architecture
- Self-hosted AI Docker Compose stack (fork of n8n self-hosted-ai-starter-kit)
- 28+ services orchestrated via `docker-compose.yml` with project name `localai`
- Caddy reverse proxy with auto-TLS for production (`cbass.space`)
- Profile-based GPU support: cpu, gpu-nvidia, gpu-amd, none
- Two environment modes: private (dev, all ports exposed) and public (prod, Caddy only)

## Stack
- **Orchestration**: Docker Compose, Python `start_services.py`
- **Core AI**: n8n, Open WebUI, Ollama, Flowise
- **Databases**: Postgres (Supabase/pgvector), Qdrant (vectors), Neo4j (graphs), Redis (cache)
- **Observability**: Langfuse + ClickHouse + MinIO
- **Infrastructure**: Caddy (reverse proxy), SearXNG (search), Kali (security)
- **Dashboard**: Next.js with shadcn/ui, video landing page

## Conventions
- Domain: `cbass.space` with per-service subdomains (n8n.cbass.space, etc.)
- VPS: Hostinger, IP 191.101.0.164, hostname `sebastian`, SSH via `ssh cbass`
- Deployment path on VPS: `/opt/cbass`
- `.env` is gitignored; never use `@` in POSTGRES_PASSWORD (use `%40`)
- Keep local and VPS `.env` files in sync manually
- Docker project name: `localai` (all compose commands use `-p localai`)

## Recent Activity
- [2026-01-20] Last code commits: Flowise UI import fix (named volumes + 50MB limit), n8n MCP issue docs
- [2026-01-19] UI Designer workflow planning, Flowise best practices docs
- [2026-02-07] Persistent memory + skill-router bootstrapped from claude-code-templates
- [2026-02-07] CLAUDE.md updated with Claude Code command docs (staged, uncommitted)

## Notes
- [2026-02-07] Educational platform — primary learner studying biology
- [2026-02-07] n8n-mcp has known issues: returns non-existent node types, no credential management tools
- [2026-02-07] Flowise upload fix: named volumes + 50MB file size limit + Caddy body limit
- [2026-02-07] Known credential IDs: OpenAI=t6PNOhqfMP9ssxHr, Google Gemini=UwcFmvOdHdi8YhPh
- [2026-02-07] Three `/cbass-*` commands available globally: status, logs, deploy
