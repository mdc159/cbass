# CBass Documentation

Welcome to the CBass documentation. This guide covers setup, deployment, and operation of the self-hosted AI stack.

## Quick Navigation

| Section | Description |
|---------|-------------|
| [Getting Started](./getting-started/) | First-time setup and tutorials |
| [Deployment](./deployment/) | Local and VPS deployment guides |
| [Services](./services/) | Per-service documentation |
| [Architecture](./architecture/) | System design and diagrams |
| [Operations](./operations/) | Day-to-day tasks and troubleshooting |

## Getting Started

New to CBass? Follow these guides in order:

1. **[Quick Start](./getting-started/quick-start.md)** - Get running in 5 minutes
2. **[First Workflow](./getting-started/first-workflow.md)** - Build your first n8n automation
3. **[Biology Projects](./getting-started/biology-projects.md)** - Apply AI tools to biology learning

## Deployment

| Guide | Use Case |
|-------|----------|
| [Local Development](./deployment/local-dev.md) | Development on your machine |
| [VPS Setup](./deployment/vps-setup.md) | Production deployment guide |
| [DNS & SSL](./deployment/dns-ssl.md) | Domain and certificate setup |

## Services

CBass includes 11+ services. See the [Services Index](./services/README.md) for the complete inventory.

**Core Services**: [n8n](./services/n8n.md) | [Flowise](./services/flowise.md) | [Open WebUI](./services/open-webui.md) | [Ollama](./services/ollama.md)

**Data Layer**: [Supabase](./services/supabase.md) | [Qdrant](./services/qdrant.md) | [Neo4j](./services/neo4j.md)

**Utilities**: [Langfuse](./services/langfuse.md) | [SearXNG](./services/searxng.md) | [Kali](./services/kali.md) | [Caddy](./services/caddy.md)

## Operations

| Guide | Content |
|-------|---------|
| [Common Tasks](./operations/common-tasks.md) | Start, stop, restart, logs |
| [Backup & Restore](./operations/backup-restore.md) | Data protection procedures |
| [Troubleshooting](./operations/troubleshooting.md) | Known issues and fixes |
| [Security](./operations/security.md) | Security checklist |

## For Claude Code Users

Claude Code agents can use the `/onboard` command to load project context:

```
/onboard           # Full project context
/onboard n8n       # Focus on n8n workflows
/onboard deploy    # Focus on deployment
```

See [CLAUDE.md](../CLAUDE.md) for Claude Code-specific configuration.

## Educational Purpose

CBass serves as a tutorial platform for learning AI tools. The primary learner is studying biology, so examples throughout the documentation connect AI capabilities to biology applications.

## Archive

Deprecated documentation is preserved in [docs/archive/](./archive/) for historical reference.
