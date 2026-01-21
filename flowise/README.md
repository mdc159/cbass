# Flowise Workflows & Tools

This directory contains Flowise chatflows, agentflows, and custom tools for the CBass stack.

## File Types

| Pattern | Type | Import Method |
|---------|------|---------------|
| `*.json` (with nodes/edges) | Raw workflow | Convert first with `wrap_flowise.ps1` |
| `*-wrapped.json` | Legacy wrapped format | Deprecated - use ExportData instead |
| `*-CustomTool.json` | Tool definition | Settings → Load Data |
| `flowise-import.json` | Combined ExportData | Settings → Load Data |

## Current Contents

### Workflows
- **Web Search + n8n Agent Chatflow** - ChatFlow integrating web search with n8n
- **Deep Research Tutorial Agents** - AgentFlow for deep research tasks

### Custom Tools
- `create_google_doc-CustomTool.json` - Create Google Docs
- `get_postgres_tables-CustomTool.json` - Query Postgres tables
- `send_slack_message_through_n8n-CustomTool.json` - Send Slack messages via n8n
- `summarize_slack_conversation-CustomTool.json` - Summarize Slack conversations

## Converting Raw Files

Raw workflow exports (with `{nodes, edges}` format) must be converted to ExportData format before importing.

```powershell
# From CBass root directory
.\wrap_flowise.ps1 -Path "flowise"
# Creates: flowise/flowise-import.json

# Convert single file
.\wrap_flowise.ps1 -Path "flowise\MyWorkflow.json"
# Creates: flowise/MyWorkflow-exportdata.json
```

## Importing Workflows

1. Open Flowise UI at https://flowise.cbass.space
2. Click **Settings** (gear icon in sidebar)
3. Click **Load Data**
4. Select `flowise-import.json` (or any `*-exportdata.json` file)

**Important**: Do NOT use "Load Chatflow" from the canvas - it fails silently and doesn't save to database.

## Adding New Workflows

1. Create/export your workflow in Flowise
2. Save raw JSON to this directory
3. Run `.\wrap_flowise.ps1 -Path "flowise"` to regenerate `flowise-import.json`
4. Commit changes to git

## Backup

The generated `flowise-import.json` serves as a portable backup. For full instance backup:

```bash
# Export everything from Flowise UI
Settings → Export Data → Save as ExportData.json

# Or backup Docker volume on VPS
ssh cbass "docker cp flowise:/root/.flowise ./flowise-backup"
```
