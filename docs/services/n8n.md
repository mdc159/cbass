# n8n - Workflow Automation

**URL**: https://n8n.cbass.space | **Container**: n8n | **Port**: 5678

## Overview

n8n is a visual workflow automation platform with 400+ integrations. It serves as the central orchestration hub for CBass, connecting AI models, databases, and external services into automated pipelines.

## Quick Access

| Environment | URL |
|-------------|-----|
| Production | https://n8n.cbass.space |
| Local | http://localhost:5678 |

## First-Time Setup

1. Navigate to n8n URL
2. Create admin account (first user becomes owner)
3. Set up credentials for internal services (see below)

### Internal Service Credentials

| Service | Connection Type | Host | Port |
|---------|-----------------|------|------|
| Ollama | Ollama | `ollama` | 11434 |
| PostgreSQL | Postgres | `db` | 5432 |
| Qdrant | Qdrant | `qdrant` | 6333 |
| Neo4j | Neo4j | `neo4j` | 7687 |

**Important**: Use container names (not localhost) for internal connections.

## Common Tasks

### Import a Workflow

```bash
# Pre-built workflows are in:
ls n8n/backup/workflows/
```

1. Open n8n
2. Click "Add workflow" > "Import from file"
3. Select JSON file

### Activate a Workflow

1. Open workflow
2. Toggle "Active" switch (top right)
3. Note the Production webhook URL

### View Execution History

1. Open workflow
2. Click "Executions" tab
3. View past runs and debug errors

### Export a Workflow

1. Open workflow
2. Click menu (...) > "Export"
3. Save JSON file

## Pre-built Workflows

Located in `n8n/backup/workflows/`:

| Workflow | Purpose |
|----------|---------|
| `V1_Local_RAG_AI_Agent.json` | Basic RAG with local LLM |
| `V2_Local_Supabase_RAG_AI_Agent.json` | RAG using Supabase vectors |
| `V3_Local_Agentic_RAG_AI_Agent.json` | Advanced agentic RAG |

## Integration with Other Services

| Connects To | Purpose | Credential Type |
|-------------|---------|-----------------|
| Ollama | LLM inference | Ollama |
| Supabase | Database, vectors | Postgres |
| Qdrant | Vector search | Qdrant |
| Neo4j | Knowledge graphs | Neo4j |
| Open WebUI | Chat interface via n8n_pipe | Webhook |

### Open WebUI Integration

The `n8n_pipe.py` script bridges Open WebUI to n8n:

1. Import workflow with webhook trigger
2. Activate workflow, copy Production URL
3. In Open WebUI: Workspace > Functions > Add Function
4. Paste `n8n_pipe.py` code
5. Configure valve: set `n8n_url` to webhook URL
6. Enable function - appears in model dropdown

## Known Credential IDs (CBass Instance)

| Service | Credential ID | Type |
|---------|---------------|------|
| OpenAI | `t6PNOhqfMP9ssxHr` | openAiApi |
| Google Gemini | `UwcFmvOdHdi8YhPh` | googlePalmApi |

## Troubleshooting

### Problem: Webhook not responding
**Solution**:
- Check workflow is activated
- Use Production URL (not Test URL)
- Check n8n logs: `docker compose -p localai logs -f n8n`

### Problem: Credential connection failed
**Solution**:
- Use container name, not localhost
- Verify target service is running
- Check credentials match service configuration

### Problem: Execution stuck
**Solution**:
- Check execution in history
- Review error details
- Verify external service availability

## Biology Applications

| Use Case | Implementation |
|----------|----------------|
| Literature monitoring | Schedule workflow to check PubMed, email new papers |
| PDF parsing | Use Document Loader node with biology papers |
| Data pipeline | Import experimental data to Supabase |
| Study flashcards | Generate from textbook content via LLM |
| Concept explanations | RAG workflow over biology documents |

## Backup

n8n workflows are stored in Docker volume `localai_n8n_data`.

```bash
# Export all workflows via API
curl -X GET "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-KEY: your-api-key" > workflows-backup.json
```

## Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n AI Tutorial](https://docs.n8n.io/advanced-ai/intro-tutorial/)
- [n8n Templates](https://n8n.io/workflows/)
