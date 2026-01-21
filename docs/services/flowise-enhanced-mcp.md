# Flowise Enhanced MCP Server

> Local MCP server providing workflow validation, wrapping, and creation capabilities for Flowise.

## Overview

The `flowise-enhanced` MCP server complements the existing `mcp-flowise` server by adding workflow management capabilities that were previously missing:

| Capability | mcp-flowise | flowise-enhanced |
|------------|-------------|------------------|
| List chatflows | Yes | Yes (enhanced) |
| Query chatflows | Yes | Yes |
| Validate workflows | No | **Yes** |
| Wrap raw workflows | No | **Yes** |
| Create chatflows via API | No | **Yes** |
| Import ExportData | No | **Yes** |

## Installation

The server is located at `mcp/flowise-enhanced/` and installed via pip:

```bash
cd X:\GitHub\CBass
pip install -e mcp/flowise-enhanced
```

## Configuration

Added to `.mcp.json`:

```json
"flowise-enhanced": {
  "command": "python",
  "args": ["-m", "mcp_flowise_enhanced"],
  "cwd": "X:\\GitHub\\CBass\\mcp\\flowise-enhanced",
  "env": {
    "FLOWISE_API_KEY": "...",
    "FLOWISE_API_ENDPOINT": "https://flowise.cbass.space"
  }
}
```

## Tools Reference

### validate_workflow

Two-stage validation: fast local structural checks + optional server-side validation.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflow` | object | Yes | Raw workflow JSON with `nodes` and `edges` arrays |
| `chatflow_id` | string | No | If provided, also runs server-side validation |
| `strict` | boolean | No | Enable strict mode for additional checks |

**Local Validation Checks:**
- `nodes` array exists and is non-empty
- `edges` array exists
- Each node has: `id`, `type`, `position`, `data`
- Each edge has: `source`, `target`, `id`
- Edge source/target reference existing nodes
- No duplicate node or edge IDs
- Flow type detection (CHATFLOW vs AGENTFLOW)
- AgentFlow: Start node presence check

**Example:**
```json
{
  "workflow": {
    "nodes": [
      {"id": "node1", "type": "chatOpenAI", "position": {"x": 0, "y": 0}, "data": {...}}
    ],
    "edges": []
  },
  "strict": true
}
```

**Response:**
```json
{
  "valid": true,
  "flow_type": "CHATFLOW",
  "local_errors": [],
  "local_warnings": ["Workflow has multiple nodes but no edges"],
  "server_validation": null,
  "summary": {"node_count": 3, "edge_count": 2, "node_types": 3}
}
```

---

### wrap_workflow

Converts raw workflow (nodes/edges) or tool definition to ExportData format. This is the Python equivalent of `wrap_flowise.ps1`.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflow` | object | Yes | Raw workflow or tool definition |
| `name` | string | No | Workflow/tool name |
| `generate_id` | boolean | No | Generate new UUID (default: true) |

**Auto-Detection Logic:**
1. Has `func`, `schema`, `name` → **Tool**
2. Any node with `type: "agentFlow"` or `type: "iteration"` → **AGENTFLOW**
3. Otherwise → **CHATFLOW**

**Example:**
```json
{
  "workflow": {
    "nodes": [...],
    "edges": [...]
  },
  "name": "Biology Study Assistant",
  "generate_id": true
}
```

**Response:**
```json
{
  "success": true,
  "detected_type": "CHATFLOW",
  "exportdata": {
    "AgentFlow": [],
    "AgentFlowV2": [],
    "ChatFlow": [{"id": "uuid", "name": "Biology Study Assistant", "flowData": "...", "type": "CHATFLOW"}],
    "Tool": [],
    ... (15 arrays total)
  },
  "wrapped": {"id": "uuid", "name": "Biology Study Assistant", "flowData": "...", "type": "CHATFLOW"}
}
```

---

### create_chatflow

Creates a new workflow in Flowise via the REST API.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflow` | object | Yes | Raw (nodes/edges) or wrapped (flowData) workflow |
| `name` | string | Yes | Workflow name |
| `deployed` | boolean | No | Deploy immediately (default: false) |
| `validate_first` | boolean | No | Run local validation first (default: true) |

**Example:**
```json
{
  "workflow": {
    "nodes": [...],
    "edges": [...]
  },
  "name": "Cell Division Tutor",
  "validate_first": true,
  "deployed": false
}
```

**Response:**
```json
{
  "success": true,
  "chatflow_id": "abc-123-def",
  "validation_result": {...},
  "api_response": {...}
}
```

---

### import_workflow

Imports workflows, tools, and other items via Flowise API using ExportData format. Equivalent to using Settings → Load Data in the UI.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `exportdata` | object | Yes | Full 15-array ExportData structure |

**Example:**
```json
{
  "exportdata": {
    "AgentFlow": [],
    "AgentFlowV2": [],
    "ChatFlow": [{"id": "...", "name": "...", "flowData": "...", "type": "CHATFLOW"}],
    "Tool": [{"name": "...", "func": "...", "schema": "..."}],
    ... (all 15 arrays)
  }
}
```

**Response:**
```json
{
  "success": true,
  "imported": {"chatflows": 1, "agentflows": 0, "tools": 2},
  "api_response": {...}
}
```

---

### list_chatflows

Lists all chatflows with summary information.

**Parameters:** None

**Response:**
```json
{
  "success": true,
  "count": 5,
  "chatflows": [
    {"id": "...", "name": "Biology Tutor", "type": "CHATFLOW", "deployed": true, "createdDate": "..."},
    ...
  ]
}
```

---

### get_chatflow

Gets detailed information about a specific chatflow.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chatflow_id` | string | Yes | The chatflow ID to retrieve |

**Response:**
```json
{
  "success": true,
  "chatflow": {
    "id": "...",
    "name": "...",
    "flowData": "...",
    "deployed": true,
    ...
  }
}
```

---

## Architecture

```
mcp/flowise-enhanced/
├── pyproject.toml                    # Package configuration
├── README.md                         # Quick reference
└── mcp_flowise_enhanced/
    ├── __init__.py                   # Package init, exports main()
    ├── __main__.py                   # Entry point for python -m
    ├── server.py                     # MCP server with tool handlers
    ├── api/
    │   ├── __init__.py
    │   └── client.py                 # Flowise REST API client
    ├── converters/
    │   ├── __init__.py
    │   ├── types.py                  # FlowType enum, detection logic
    │   └── wrapper.py                # Raw → wrapped → ExportData
    └── validators/
        ├── __init__.py
        └── local.py                  # Structural validation
```

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

## Relationship to wrap_flowise.ps1

The `wrap_workflow` tool is a Python port of the PowerShell script `wrap_flowise.ps1`:

| PowerShell Function | Python Equivalent |
|---------------------|-------------------|
| `Get-FlowType` | `converters.types.detect_flow_type()` |
| `Test-IsRawFlowFile` | `converters.types.is_raw_flow_file()` |
| `Test-IsToolFile` | `converters.types.is_tool_file()` |
| `New-EmptyExportData` | `converters.wrapper.create_empty_exportdata()` |
| `Convert-FlowToExportFormat` | `converters.wrapper.convert_flow_to_export_format()` |
| `Convert-ToolToExportFormat` | `converters.wrapper.convert_tool_to_export_format()` |

Both produce identical ExportData output suitable for Flowise import.

## Flowise API Endpoints Used

| Endpoint | Method | Tool |
|----------|--------|------|
| `/api/v1/chatflows` | GET | `list_chatflows` |
| `/api/v1/chatflows/:id` | GET | `get_chatflow` |
| `/api/v1/chatflows` | POST | `create_chatflow` |
| `/api/v1/validation/:id` | GET | `validate_workflow` (server-side) |
| `/api/v1/export-import/import` | POST | `import_workflow` |

## Usage Patterns

### Pattern 1: Validate Before Import

```
1. wrap_workflow(workflow, name="My Flow")
2. validate_workflow(workflow)  # Check for errors
3. import_workflow(exportdata)   # If valid, import
```

### Pattern 2: Direct Creation

```
1. create_chatflow(workflow, name="My Flow", validate_first=true)
   # Validates, wraps, and creates in one call
```

### Pattern 3: Bulk Import

```
1. wrap_workflow(flow1, name="Flow 1")
2. wrap_workflow(flow2, name="Flow 2")
3. Combine exportdata arrays
4. import_workflow(combined_exportdata)
```

## Troubleshooting

### Server Won't Start

1. Check Python path: `python -m mcp_flowise_enhanced` should run without errors
2. Verify environment variables in `.mcp.json`
3. Check Flowise API endpoint is accessible

### Validation Errors

- **"Missing 'nodes' array"**: Workflow JSON structure is incorrect
- **"Edge references non-existent source node"**: Node was deleted but edge remains
- **"AgentFlow may be missing a Start node"**: Add a startAgentFlow node

### API Errors

- **401 Unauthorized**: Check `FLOWISE_API_KEY` is correct
- **404 Not Found**: Check `FLOWISE_API_ENDPOINT` URL
- **Connection refused**: Flowise service may not be running

## Dependencies

```
mcp[cli] >= 1.2.0    # MCP server framework
requests >= 2.28.0   # HTTP client
pydantic >= 2.0.0    # Data validation
```

## Related Documentation

- [Flowise Service Guide](flowise.md)
- [CLAUDE.md - Flowise MCP Tools section](../../CLAUDE.md#flowise-mcp-tools)
- [wrap_flowise.ps1](../../wrap_flowise.ps1)
