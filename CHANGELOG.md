# Changelog

All notable changes to this project will be documented in this file.

## 2026-02-27

### Fixed
- **Updater service** — dashboard "Update" buttons were silently failing due to three issues:
  1. `update-container.sh` was mounted read-only with `644` permissions (not executable)
  2. The `almir/webhook` Alpine image had no `docker` or `docker compose` CLI
  3. The update script ran bare `docker compose up -d` without the override files, so recreated containers lost their environment config (ports, `OLLAMA_BASE_URL`, etc.)

### Changed
- Updater now builds a custom image (`scripts/Dockerfile`) extending `almir/webhook` with `bash`, `docker-cli`, and `docker-cli-compose` baked in
- Update script baked into the image with `chmod +x` — eliminates host permission issues
- `COMPOSE_FILE` env var set on the updater in both override files so `docker compose` commands automatically use the correct base + override config
- `update-container.sh` hardened with `set -euo pipefail` and quoted variable expansion

### Technical details
- Container runs as root (required for Docker socket access; socket mount is already equivalent to host root)
- `scripts/Dockerfile` adds ~50MB (bash + docker CLI + compose plugin) to the webhook base image
- Verified end-to-end: Playwright browser test logs into dashboard, clicks Update, confirms API 200 + success banner, and validates the container was recreated with correct override labels

## 2026-02-11

### Added
- Environment-aware dashboard service URLs via `NEXT_PUBLIC_*_URL` build args
  - Private mode: cards link to `localhost:PORT`
  - Public mode: cards link to `*.cbass.space`
  - URLs driven by `--environment` flag (no manual env var editing)
- Shared service config at `dashboard/lib/services.ts` (single source of truth)
- Health check rewrites `localhost` to `host.docker.internal` for Docker-internal checks
- `docker-compose.override.private.supabase.yml` for local Supabase port bindings
- `neo4j/` added to `.gitignore`

### Changed
- Dashboard port changed from 3001 to 3002 in private mode
- Kali URL uses HTTPS locally (`https://localhost:6901`) — KasmWeb requires TLS
- n8n private mode now sets `N8N_SECURE_COOKIE=false` and `WEBHOOK_URL=http://localhost:5678`
- Dashboard private mode sets `NODE_TLS_REJECT_UNAUTHORIZED=0` for self-signed cert health checks
- Neo4j `NEO4J_AUTH` username must be `neo4j` (Community Edition constraint)
- Kali VNC env var renamed from `VNC_PW` to `KALI_VNC_PW`
- `.gitignore` scoped `/lib/` and `/lib64/` to root only (was blocking `dashboard/lib/`)

### Fixed
- Dashboard cards no longer hardcode production URLs when running locally
- Health checks now work for all services including Kali (self-signed TLS)
- n8n login blocked by secure cookie when accessed via `http://localhost`

### Removed
- `N8N_BASIC_AUTH_*` env vars are deprecated since n8n v1.0 (silently ignored)
- Cleaned up `.env.bak.*` backup files
- Deleted `codex/repack-local-2` branch (merged into `local`)

## 2026-02-09

### Added
- Startup convenience flags in `start_services.py`:
  - `--open-dashboard`
  - `--dashboard-url`
- Environment guidance for Supabase public/dashboard variables:
  - `PG_META_CRYPTO_KEY`
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Explicit documentation that dashboard Supabase target is controlled by `NEXT_PUBLIC_SUPABASE_URL`.

### Changed
- Dashboard Docker build now receives Supabase public values at build time through Compose build args.
- Dashboard runtime/default Supabase URL handling now supports local-first defaults (`http://localhost:8000`) when not overridden.
- Local deployment has been reconfigured to use local Supabase endpoints for dashboard auth/API:
  - `NEXT_PUBLIC_SUPABASE_URL=http://localhost:8000`
  - `SITE_URL=http://localhost:8000`
  - `API_EXTERNAL_URL=http://localhost:8000`
  - `SUPABASE_PUBLIC_URL=http://localhost:8000`
- Supabase derived keys were regenerated from current `JWT_SECRET`:
  - `ANON_KEY`
  - `SERVICE_ROLE_KEY`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### Fixed
- Dashboard build failure caused by missing `NEXT_PUBLIC_SUPABASE_ANON_KEY` at build time.
- Supabase warning about blank `PG_META_CRYPTO_KEY`.
- Realtime healthcheck `403` caused by JWT/key mismatch.
