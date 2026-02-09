---
description: Load a concise CBass context summary for a fresh agent before starting work.
argument-hint: [focus-area]
allowed-tools: Read, Glob, Grep
---

# CBass Context Snapshot

Load a short, actionable overview of the CBass repo, services, and operational posture.

## Usage

- `/cbass-context` - Core context
- `/cbass-context deploy` - Deployment-focused context
- `/cbass-context services` - Service inventory focus
- `/cbass-context ops` - Operations and troubleshooting focus

## Context Loading

Based on the focus area (if provided: **$ARGUMENTS**), load the appropriate context:

### Default (No Focus)

Read:
1. **@CLAUDE.md** - Current state, todos, and known issues
2. **@docs/README.md** - Documentation index
3. **@docs/services/README.md** - Service inventory

Summarize:
- What CBass is and its primary goals
- Current state from CLAUDE.md
- Where to find deployment and ops docs

### Deploy Focus

Read:
1. **@docs/deployment/README.md**
2. **@docs/deployment/vps-setup.md**
3. **@docs/deployment/local-dev.md**

Summarize:
- Profiles and environment modes
- Key deployment steps and prerequisites
- Common deployment pitfalls

### Services Focus

Read:
1. **@docs/services/README.md**
2. **@docs/services/n8n.md**
3. **@docs/services/flowise.md**
4. **@docs/services/open-webui.md**

Summarize:
- Core service roles and dependencies
- Service URLs and ports
- Known caveats

### Ops Focus

Read:
1. **@docs/operations/README.md**
2. **@docs/operations/common-tasks.md**
3. **@docs/operations/troubleshooting.md**

Summarize:
- Common commands
- Recovery steps
- Where to log issues

## Output Format

```markdown
## CBass Context Snapshot

**Focus**: [area or "general"]

### Current State
[Summary from CLAUDE.md]

### Key Facts
[Bullet list of essential details]

### Next Actions
[Suggested next steps based on focus]
```

## Skill Reference

For deeper context, see:
- `.claude/skills/cbass-context-v1-0-0/SKILL.md`
