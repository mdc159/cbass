# Flowise - Visual AI Builder

**URL**: https://flowise.cbass.space | **Container**: flowise | **Port**: 3001

## Overview

Flowise is a drag-and-drop UI for building LLM applications. Create chatbots, AI agents, and RAG pipelines without writing code by connecting nodes visually.

## Quick Access

| Environment | URL |
|-------------|-----|
| Production | https://flowise.cbass.space |
| Local | http://localhost:3001 |

## First-Time Setup

1. Navigate to Flowise URL
2. If authentication is enabled, login with credentials from `.env`:
   - `FLOWISE_USERNAME`
   - `FLOWISE_PASSWORD`

## Common Tasks

### Create a New Chatflow

1. Click "Add New" > "Chatflow"
2. Drag nodes from sidebar onto canvas
3. Connect nodes by dragging between ports
4. Click "Save" then "Chat" to test

### Import a Workflow

**Recommended method (Settings > Load Data):**

1. Go to Settings (gear icon) > "Load Data"
2. Select ExportData JSON file
3. Data imports to database

**Canvas method (less reliable):**

1. Open canvas > Settings > "Load Chatflow"
2. Select raw workflow JSON
3. Note: Only loads to canvas, doesn't save to DB

### Export All Data

1. Go to Settings > "Export All"
2. Saves all chatflows, tools, and config
3. Creates ExportData format JSON

## Import/Export Formats

| Format | Use Case | Structure |
|--------|----------|-----------|
| ExportData | Full backup/restore | 15 arrays including AgentFlowV2, ChatFlow, Tool |
| Raw Workflow | Single chatflow | `{nodes, edges}` only |

### Converting Raw to ExportData

Use the wrapper script:

```powershell
# Convert all files in directory
.\wrap_flowise.ps1 -Path "flowise"

# Convert single file
.\wrap_flowise.ps1 -Path "flowise\MyWorkflow.json"
```

Auto-detects flow type:
- `type: "agentFlow"` nodes → AgentFlowV2
- `type: "customNode"` nodes → ChatFlow
- Files with `func` and `schema` → Tool

### Working Examples

The `flowise/` directory contains wrapped examples ready for import:

| File | Type | Description |
|------|------|-------------|
| `Deep Research Tutorial Agents-wrapped.json` | AgentFlowV2 | Multi-agent research workflow |
| `Web Search + n8n Agent Chatflow-wrapped.json` | ChatFlow | Web search with n8n integration |

These demonstrate the correct ExportData format output from `wrap_flowise.ps1`. Import via Settings > Load Data.

## Integration with Other Services

| Connects To | Purpose | Configuration |
|-------------|---------|---------------|
| Ollama | Local LLM inference | Base URL: `http://ollama:11434` |
| Supabase | Vector storage | Connection string with `db` host |
| Qdrant | Vector database | URL: `http://qdrant:6333` |
| OpenAI | Cloud LLM | API key in credentials |

## Pre-built Tools

Located in `flowise/`:

- Google Docs creation
- PostgreSQL queries
- Slack integration
- Web search tools

## Troubleshooting

### Problem: Import fails silently
**Solution**:
- Use Settings > Load Data (not Load Chatflow)
- Verify JSON is valid ExportData format
- Check browser console for errors

### Problem: Model not found
**Solution**:
- For Ollama: verify model is pulled
- Check model name matches exactly
- Use valid model names (e.g., `gpt-4o-mini` not `gpt-4.1-mini`)

### Problem: UI upload fails
**Solution**:
This was fixed by:
- Using Docker named volume for Flowise data
- Setting `FLOWISE_FILE_SIZE_LIMIT=50mb`
- Adding Caddy body limit for uploads

### Problem: Canvas not saving
**Solution**:
- Click "Save" button explicitly
- Check for validation errors
- Verify credentials are configured

## Biology Applications

| Use Case | Implementation |
|----------|----------------|
| Study assistant | Build chatbot with biology textbook context |
| Flashcard generator | LLM chain to create Q&A from notes |
| Concept explainer | RAG pipeline over biology papers |
| Lab notebook | Document QA over experimental notes |

## Data Location

Flowise data is stored in Docker named volume `flowise`:

```bash
# Volume location
docker volume inspect localai_flowise
```

## VPS Migration

If existing Flowise data needs migration:

```bash
# Backup before deployment
cp -r ~/.flowise ~/flowise-backup-$(date +%Y%m%d)

# After deployment, if data missing:
docker volume inspect localai_flowise
sudo cp -r ~/flowise-backup-*/* /var/lib/docker/volumes/localai_flowise/_data/
sudo chown -R 1000:1000 /var/lib/docker/volumes/localai_flowise/_data/
docker compose -p localai restart flowise
```

## Resources

- [Flowise Documentation](https://docs.flowiseai.com/)
- [Flowise GitHub](https://github.com/FlowiseAI/Flowise)
