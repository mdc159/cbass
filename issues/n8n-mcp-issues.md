# n8n-MCP Issues Investigation

## Issue Status

| Issue | Status | Solution |
|-------|--------|----------|
| 1. Windows `cmd /c` wrapper warning | ✅ **FIXED** | Updated `.mcp.json` |
| 2. Suboptimal node selection | 🔍 **Documented** | Workarounds + fork proposal |
| 3. Missing credential management | 🔍 **Documented** | Workarounds + fork proposal |

---

## Issue 1: Windows Configuration Warning (FIXED)

### Problem
```
[Warning] [n8n-mcp] mcpServers.n8n-mcp: Windows requires 'cmd /c' wrapper to execute npx
```

### Root Cause
On Windows, `npx` is not a native executable - it requires a shell to interpret it. Node's `child_process.spawn` doesn't invoke a shell by default.

### Solution Applied
Updated `.mcp.json` from:
```json
{
  "command": "npx",
  "args": ["n8n-mcp"]
}
```

To:
```json
{
  "command": "cmd",
  "args": ["/c", "npx", "-y", "n8n-mcp"]
}
```

**Note**: Restart Claude Code to apply the change.

---

## Issue 2: Suboptimal Node Selection

### Problem
The MCP builds custom Code nodes with functions instead of using existing official n8n nodes.

### Root Cause Analysis

The n8n-mcp package uses a **pre-built SQLite database** with:
- 1,084 nodes (537 core + 547 community)
- 99% property coverage but only 63.6% operation coverage
- Database may be outdated vs current n8n versions

**Key issues discovered:**

1. **Node name inaccuracies**: MCP returns incorrect node type names
   - Example: Returns `@n8n/n8n-nodes-langchain.googleGemini` but actual name is `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`

2. **No live validation**: Doesn't verify nodes exist in your actual n8n instance

3. **Incomplete operation data**: Many nodes have schemas but missing operation details

4. **Search ranking**: Doesn't prefer exact matches over partial matches

### Workarounds

**Always verify nodes before using:**

```
1. Use search_nodes({ query: "keyword", includeExamples: true })
2. Check the exact nodeType in results
3. Use get_node({ nodeType: "exact-type", mode: "docs" }) to see capabilities
4. Use validate_node() before creating workflows
```

**Example - Finding Google Gemini nodes:**
```javascript
// Search for Gemini
search_nodes({ query: "Google Gemini" })

// Results show two different nodes:
// - @n8n/n8n-nodes-langchain.lmChatGoogleGemini (Chat Model - round sub-node)
// - @n8n/n8n-nodes-langchain.googleGemini (App node - square, multi-resource)
```

### Long-term Solution: Fork n8n-mcp

Add node validation in forked version:
1. Validate node types against live n8n instance before suggesting
2. Improve search ranking algorithm
3. Keep node database in sync with n8n releases

---

## Issue 3: Missing Credential Management

### Problem
Cannot programmatically assign credentials to workflow nodes. Must manually look up credential IDs in n8n UI.

### Root Cause

The n8n-mcp package provides **17 tools** but **zero credential tools**, despite the n8n API supporting:

| n8n API Endpoint | Purpose | MCP Support |
|------------------|---------|-------------|
| `GET /credentials` | List all credentials | ❌ Missing |
| `GET /credentials/{id}` | Get credential by ID | ❌ Missing |
| `POST /credentials` | Create credential | ❌ Missing |
| `PATCH /credentials/{id}` | Update credential | ❌ Missing |
| `DELETE /credentials/{id}` | Delete credential | ❌ Missing |
| `POST /credentials/test` | Test credential | ❌ Missing |

### Current Workaround

**Step 1**: Look up credential IDs in n8n UI
- Go to n8n Settings → Credentials
- Click credential → URL shows ID (e.g., `/credentials/t6PNOhqfMP9ssxHr`)

**Step 2**: Document known IDs (in CLAUDE.md)

| Service | Credential ID | Credential Type |
|---------|---------------|-----------------|
| OpenAI | `t6PNOhqfMP9ssxHr` | `openAiApi` |
| Google Gemini | `UwcFmvOdHdi8YhPh` | `googlePalmApi` |

**Step 3**: Use `n8n_update_partial_workflow` to assign:
```json
{
  "id": "workflow-id",
  "operations": [{
    "type": "updateNode",
    "nodeName": "OpenAI Chat Model",
    "updates": {
      "credentials": {
        "openAiApi": { "id": "t6PNOhqfMP9ssxHr", "name": "OpenAI" }
      }
    }
  }]
}
```

### Long-term Solution: Fork n8n-mcp

Add these tools to forked version:

```typescript
// Tools to add in src/mcp/tools-n8n-manager.ts

n8n_list_credentials     // List all credentials (id, name, type)
n8n_get_credential       // Get credential metadata by ID
n8n_create_credential    // Create new credential
n8n_assign_credential    // Assign credential to workflow node
n8n_test_credential      // Test credential connectivity
```

---

## Proposed Fork Implementation

### Repository
Fork: https://github.com/czlonkowski/n8n-mcp

### Changes Required

1. **Add credential tools** (`src/mcp/tools-n8n-manager.ts`)
   - Implement `n8n_list_credentials`, `n8n_get_credential`, etc.
   - Use n8n REST API `/api/v1/credentials` endpoints

2. **Fix node validation** (`src/mcp/node-search.ts`)
   - Add live validation against n8n instance
   - Improve search ranking for exact matches

3. **Keep database updated** (`data/nodes.db`)
   - Script to sync with n8n releases
   - Include operation coverage improvements

### Update .mcp.json for Fork

```json
{
  "n8n-mcp": {
    "command": "cmd",
    "args": ["/c", "npx", "-y", "file:X:/GitHub/n8n-mcp-fork"]
  }
}
```

Or use Docker:
```json
{
  "n8n-mcp": {
    "command": "docker",
    "args": [
      "run", "-i", "--rm", "--init",
      "-e", "MCP_MODE=stdio",
      "-e", "N8N_API_URL=https://n8n.cbass.space",
      "-e", "N8N_API_KEY=your-key",
      "ghcr.io/your-username/n8n-mcp-fork:latest"
    ]
  }
}
```

---

## Best Practices (Until Fork)

### For Node Selection
1. **Always search first**: `search_nodes({ query: "...", includeExamples: true })`
2. **Verify exact type**: Check `nodeType` field in results
3. **Read docs**: `get_node({ nodeType: "...", mode: "docs" })`
4. **Validate before deploy**: `validate_node({ nodeType: "...", config: {...} })`

### For Credential Management
1. **Document IDs**: Keep credential table in CLAUDE.md updated
2. **Create in UI**: Create credentials in n8n UI first
3. **Assign via update**: Use `n8n_update_partial_workflow` with `updateNode`
4. **Test workflow**: Run `n8n_test_workflow` to verify credentials work

### For Windows Development
1. **Use cmd wrapper**: Always `"command": "cmd", "args": ["/c", "npx", ...]`
2. **Consider Docker**: Avoids Windows-specific issues entirely
3. **Manual .mcp.json edits**: Safer than CLI due to parser bugs

---

## References

- [n8n-mcp GitHub](https://github.com/czlonkowski/n8n-mcp)
- [n8n API Documentation](https://docs.n8n.io/api/)
- [Claude Code MCP Issue #9594](https://github.com/anthropics/claude-code/issues/9594) - Windows npx wrapper
- [Claude Code MCP Issue #4158](https://github.com/anthropics/claude-code/issues/4158) - /c flag parsing bug
