# Changelog

All notable changes to this project will be documented in this file.

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
