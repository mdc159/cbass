# Commit Message Template

Every commit message should serve as a **changelog entry** — someone scanning
`git log` should be able to reconstruct the full project history, including
what failed and how it was fixed.

## Format

```
<subject line — imperative, ≤72 chars>

WHY:
Motivation or context. What gap, bug, or request led to this change?

WHAT:
Summary of changes across files/scripts.

HOW:
Implementation approach, constraints, and design choices.

ISSUES (if any):
What was tried first? What failed? How was it caught?
Include error messages, version constraints, or failed approaches.

VALIDATION:
How was this tested? On what environment? What was verified?

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

## Section Guidelines

| Section | Required? | When to skip |
|---------|-----------|-------------|
| WHY | Always | Never — even "Add X to Brewfile" should say why X was added |
| WHAT | Always | Never |
| HOW | Multi-file changes | Single-file additions (e.g., config entry) |
| ISSUES | When something failed | Clean implementations with no surprises |
| VALIDATION | Feature/bugfix commits | Config-only changes |

## Examples

### Feature commit (full detail)

```
Add webhook-triggered container updates

WHY:
Need automated deployments when pushing to main without SSH access
to the VPS for every change.

WHAT:
- scripts/hooks.json: webhook configuration for container updates
- scripts/update-container.sh: pulls latest image and restarts service
- docker-compose.yml: added updater service on port 9000

HOW:
Uses adnanh/webhook to listen for POST requests. Each hook maps a
service name to a docker compose restart. Rate-limited to prevent
abuse.

VALIDATION:
Tested with curl POST to localhost:9000, verified container restart
via docker compose logs.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

### Simple addition (minimal but complete)

```
Add Neo4j browser to Caddyfile routing

WHY:
Neo4j browser needs reverse proxy access through Caddy for the
cbass.space subdomain to work.

WHAT:
Added neo4j.cbass.space route to Caddyfile proxying to port 7474.
```

### Bugfix commit

```
Fix Flowise upload size limit causing silent import failures

WHY:
Flowise "Load Chatflow" was failing silently when importing
workflows larger than the default body size limit.

WHAT:
- Caddyfile: added request_body max_size 50MB for Flowise route
- docker-compose.yml: added FLOWISE_FILE_SIZE_LIMIT=50mb env var

HOW:
Two layers needed: Caddy was rejecting large POSTs before they
reached Flowise, and Flowise itself had an internal limit.

ISSUES:
Initially only fixed the Caddy limit, but imports still failed.
Discovered Flowise has its own upload cap via FLOWISE_FILE_SIZE_LIMIT.

VALIDATION:
Successfully imported a 12MB workflow export via Settings > Load Data.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```
