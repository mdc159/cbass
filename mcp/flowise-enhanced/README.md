# Flowise Enhanced MCP Server

Local MCP server that adds workflow validation, wrapping, and creation capabilities for Flowise.

## Features

| Tool | Purpose |
|------|---------|
| `validate_workflow` | Local structural validation + optional server-side validation |
| `wrap_workflow` | Convert raw workflow (nodes/edges) to ExportData format |
| `create_chatflow` | Create workflow via Flowise API with validation |
| `import_workflow` | Import ExportData directly via Flowise API |
| `list_chatflows` | List all chatflows with details |
| `get_chatflow` | Get detailed chatflow information |

## Installation

```bash
cd mcp/flowise-enhanced
pip install -e .
```

## Configuration

Add to `.mcp.json`:

```json
"flowise-enhanced": {
  "command": "python",
  "args": ["-m", "mcp_flowise_enhanced"],
  "cwd": "X:\\GitHub\\CBass\\mcp\\flowise-enhanced",
  "env": {
    "FLOWISE_API_KEY": "your-api-key",
    "FLOWISE_API_ENDPOINT": "https://flowise.cbass.space"
  }
}
```

## Tool Details

### validate_workflow

Two-stage validation for Flowise workflows.

**Parameters:**
- `workflow` (object, required): Raw workflow JSON with `nodes` and `edges`
- `chatflow_id` (string, optional): Run server-side validation (workflow must be saved)
- `strict` (boolean): Enable strict mode

**Local checks:**
- Nodes array exists and non-empty
- Edges array exists
- Each node has: id, type, position, data
- Each edge has: source, target, id
- Edge references valid node IDs
- AgentFlow Start node check

### wrap_workflow

Convert raw workflow to ExportData format (equivalent to `wrap_flowise.ps1`).

**Parameters:**
- `workflow` (object, required): Raw workflow or tool definition
- `name` (string): Workflow name
- `generate_id` (boolean): Generate new UUID (default: true)

**Auto-detection:**
- Has `func`, `schema`, `name` → Tool
- Any node with `type: "agentFlow"` or `type: "iteration"` → AGENTFLOW
- Otherwise → CHATFLOW

### create_chatflow

Create workflow via Flowise API.

**Parameters:**
- `workflow` (object, required): Raw or wrapped workflow
- `name` (string, required): Workflow name
- `deployed` (boolean): Deploy immediately (default: false)
- `validate_first` (boolean): Run validation (default: true)

### import_workflow

Import ExportData via Flowise API.

**Parameters:**
- `exportdata` (object, required): Full 15-array ExportData structure

## ExportData Format

The 15-array structure expected by Flowise "Load Data":

```json
{
  "AgentFlow": [],
  "AgentFlowV2": [],
  "AssistantFlow": [],
  "AssistantCustom": [],
  "AssistantOpenAI": [],
  "AssistantAzure": [],
  "ChatFlow": [],
  "ChatMessage": [],
  "ChatMessageFeedback": [],
  "CustomTemplate": [],
  "DocumentStore": [],
  "DocumentStoreFileChunk": [],
  "Execution": [],
  "Tool": [],
  "Variable": []
}
```

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run directly
python -m mcp_flowise_enhanced
```
