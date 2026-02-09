---
name: cbass-context-v1-0-0
description: Provide concise CBass repo onboarding context and a fast-start workflow. Use when starting work in the cbass repo, onboarding a fresh agent, or needing a quick summary of architecture, services, deployment, and operations with optional focus areas (deploy, services, ops, n8n, flowise).
---

# CBass Context Snapshot

## Overview

Load a short, actionable summary of CBass so a fresh agent can start work safely and with the right context.

## Quick Start Workflow

1. Read **@CLAUDE.md** for current state, todos, and known issues.
2. Read **@docs/README.md** for the documentation map.
3. Read **@docs/services/README.md** for service inventory.
4. If the task is deployment-related, read **@docs/deployment/README.md**.
5. If the task is ops-related, read **@docs/operations/README.md**.

## Focused Context Paths

Use these paths when the user gives a focus area:

- **deploy**: `@docs/deployment/README.md`, `@docs/deployment/vps-setup.md`, `@docs/deployment/local-dev.md`
- **services**: `@docs/services/README.md`, then the specific service page
- **ops**: `@docs/operations/README.md`, `@docs/operations/common-tasks.md`, `@docs/operations/troubleshooting.md`
- **n8n**: `@docs/services/n8n.md`, `@n8n_pipe.py`, `@CLAUDE.md` (MCP notes)
- **flowise**: `@docs/services/flowise.md`, `@flowise/` directory listing

## Output Format

After loading context, respond with:

```markdown
## CBass Context Snapshot

**Focus**: [area or "general"]

### Current State
[Summary from CLAUDE.md]

### Key Facts
[Bulleted list of essential details]

### Recommended Next Steps
[Actionable next steps based on focus]
```

## References

Read `references/context.md` when you need the canonical list of key files, services, and deployment commands.
