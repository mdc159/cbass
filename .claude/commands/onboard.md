---
description: Load CBass project context for a fresh Claude session. Use when starting work, switching focus areas, or when unfamiliar with the codebase.
argument-hint: [focus-area]
allowed-tools: Read, Glob, Grep
---

# CBass Project Onboarding

Load project context to work effectively on the CBass self-hosted AI stack.

## Usage

- `/onboard` - Full project context
- `/onboard n8n` - Focus on n8n workflows
- `/onboard flowise` - Focus on Flowise chatflows
- `/onboard deploy` - Focus on deployment
- `/onboard data` - Focus on data layer

## Context Loading

Based on the focus area (if provided: **$ARGUMENTS**), load the appropriate context:

### Default (No Focus)

Read these files to understand the project:

1. **@CLAUDE.md** - Project instructions, known issues, current todos
2. **@docs/README.md** - Documentation navigation
3. **@docs/services/README.md** - Service inventory

Then summarize:
- What CBass is (self-hosted AI Docker stack)
- Current state (check CLAUDE.md todos)
- How to help (based on context)

### n8n Focus

Read:
1. **@docs/services/n8n.md** - n8n documentation
2. **@CLAUDE.md** - Known credential IDs and MCP issues
3. **@n8n_pipe.py** - Open WebUI integration

Summarize n8n-specific:
- Credential configuration (container names)
- Pre-built workflows in `n8n/backup/workflows/`
- Known MCP tool issues

### Flowise Focus

Read:
1. **@docs/services/flowise.md** - Flowise documentation
2. **@CLAUDE.md** - Import/export issues
3. List files in `flowise/` directory

Summarize Flowise-specific:
- Import methods (Settings > Load Data recommended)
- ExportData vs raw format
- `wrap_flowise.ps1` usage

### Deployment Focus

Read:
1. **@docs/deployment/vps-setup.md** - VPS deployment
2. **@docs/deployment/local-dev.md** - Local development
3. **@docs/deployment/dns-ssl.md** - DNS and SSL

Summarize deployment-specific:
- GPU profiles and environment modes
- VPS setup at cbass.space
- Common deployment tasks

### Data Focus

Read:
1. **@docs/services/supabase.md** - PostgreSQL + pgvector
2. **@docs/services/qdrant.md** - Vector database
3. **@docs/services/neo4j.md** - Graph database

Summarize data layer-specific:
- Connection strings and container names
- Vector dimensions for different models
- Biology data modeling patterns

## Output Format

After loading context, provide:

```markdown
## CBass Project Context Loaded

**Project**: CBass - Self-hosted AI Docker Compose stack
**Live Site**: https://cbass.space
**Focus Area**: [area or "general"]

### Current State
[Summary from CLAUDE.md todos]

### Key Information
[Relevant details for focus area]

### How I Can Help
[Based on context and focus area]

### Quick Commands
[Relevant docker/git commands]
```

## Skill Reference

For detailed context, see:
- `.claude/skills/onboard-v1.0.0/SKILL.md` - Full skill documentation
- `.claude/skills/onboard-v1.0.0/CONTEXT.md` - Detailed project context
- `.claude/skills/onboard-v1.0.0/SERVICES.md` - Complete service reference
