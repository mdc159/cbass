# Skill Priorities

## Always (invoke proactively every session)
- `/catchup` - Resume session with briefing (run first thing)
- `/cbass-status` - Quick health check of all services

## Context-Triggered (invoke when topic matches)
- `/cbass-logs "<service>"` - When diagnosing service issues or errors
- `/cbass-deploy` - When starting/restarting the stack
- `/deep-prime "area"` - When diving into a specific service or component
- `/code-review` - Before committing or merging changes
- `/rca "error"` - When diagnosing complex multi-service failures

## Available (use when explicitly relevant)
- `/remember "fact"` - When discovering reusable knowledge (credential IDs, workarounds)
- `/memory` - When checking stored context or searching for past decisions
- `/quick-prime` - When needing fast project overview

## Repo Context
- **Primary domain**: Docker Compose AI infrastructure, service orchestration
- **Key commands prefix**: `/cbass-*`
- **Context skill**: `cbass-context` (global, service inventory + dependency chains)
