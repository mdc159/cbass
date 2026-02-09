# Documentation Standards

Use this guide to keep CBass documentation consistent, current, and easy to navigate.

## Goals

- **Single source of truth**: Prefer one authoritative location per topic and link to it elsewhere.
- **Fast onboarding**: Make it easy for a new contributor or agent to orient quickly.
- **Operational accuracy**: Ensure deployment and ops docs reflect the current stack.

## Information Architecture

- **docs/README.md** is the entry point for all documentation.
- **docs/getting-started/** for first-time setup and tutorials.
- **docs/deployment/** for local and VPS deployment.
- **docs/services/** for per-service pages.
- **docs/architecture/** for system diagrams and flows.
- **docs/operations/** for day-to-day operations, backups, and troubleshooting.
- **docs/archive/** for deprecated material (keep a short redirect note).

## Ownership & Review

- **Service owners**: Update the matching file in `docs/services/` when changing a service.
- **Infrastructure owners**: Update `docs/deployment/` and `docs/operations/` for infra changes.
- **Architecture changes**: Update `docs/architecture/` and diagrams as part of the change.

## Update Triggers (Required)

Update docs when you change:

- **docker-compose.yml** → service inventory, ports, and dependencies.
- **Caddyfile** → routing, subdomains, TLS, or body size limits.
- **start_services.py** → deployment or startup steps.
- **env.example** → required/optional environment variables.
- **Service-specific files** (e.g., `n8n_pipe.py`, `flowise/`) → corresponding service page.

## Content Standards

- **Lead with purpose**: Start each doc with a short summary of why it exists.
- **Use templates**: New service/runbook docs should follow the templates in `docs/templates/`.
- **Prefer links over duplication**: Link to canonical pages instead of copy/pasting.
- **Command blocks**: Use fenced code blocks and specify the shell when relevant (bash/powershell).

## Doc Freshness Checklist

Before merging or deploying:

- [ ] Docs reflect current service list and port mappings.
- [ ] Deployment steps match `start_services.py`.
- [ ] Environment variable lists are accurate.
- [ ] Any new constraints or warnings are captured in the relevant doc.

## Templates

- **Service template**: `docs/templates/service.md`
- **Runbook template**: `docs/templates/runbook.md`

## Claude/Agent Onboarding

- Keep onboarding content aligned with `docs/README.md` and `CLAUDE.md`.
- If updating core architecture or deployment, update the onboarding command and skill references.
