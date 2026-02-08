# n8n-mcp Credential Management Tools

## Overview

This document describes the credential management tools added to a forked version of [n8n-mcp](https://github.com/czlonkowski/n8n-mcp). The fork is included as a **git submodule** in CBass at `vendor/n8n-mcp` and adds 5 new MCP tools for managing n8n credentials.

### Repository Information

| Item | Value |
|------|-------|
| Submodule Location | `vendor/n8n-mcp` |
| GitHub Fork | https://github.com/1215-Labs/n8n-mcp |
| Upstream | https://github.com/czlonkowski/n8n-mcp |
| Branch | `feature/credential-management-tools` |

### Motivation

The original n8n-mcp package provides comprehensive workflow management tools but lacks credential management capabilities. This fork adds credential assignment capabilities to eliminate the need for manual credential ID lookups in the n8n UI.

---

## ⚠️ n8n API Limitation

### Important: GET /credentials is Blocked by Design

**n8n's Public API intentionally blocks GET requests to `/credentials` endpoints for security reasons.** This is not a configuration issue - it's a deliberate security decision by n8n.

| Endpoint | Method | Status | Reason |
|----------|--------|--------|--------|
| `/credentials` | GET | ❌ **Blocked** | Security - prevents credential enumeration |
| `/credentials/{id}` | GET | ❌ **Blocked** | Security - prevents credential exposure |
| `/credentials` | POST | ✅ Works | Create new credentials |
| `/credentials/{id}` | PATCH | ✅ Works | Update credentials |
| `/credentials/{id}` | DELETE | ✅ Works | Delete credentials |
| `/credentials/schema/{type}` | GET | ✅ Works | Get credential type schema |

### Tool Availability

| Tool | Status | Notes |
|------|--------|-------|
| `n8n_list_credentials` | ❌ **Non-functional** | Blocked by n8n API |
| `n8n_get_credential` | ❌ **Non-functional** | Blocked by n8n API |
| `n8n_test_credential` | ❌ **Non-functional** | Blocked by n8n API |
| `n8n_get_credential_schema` | ✅ **Works** | Uses local data, not API |
| `n8n_assign_credential` | ✅ **Works** | Skips validation, uses known IDs |

### Recommended Workflow

Since credential listing is blocked, use the **manual credential registry** approach:

1. Look up credential IDs once in the n8n UI (Settings → Credentials)
2. Document them in `CLAUDE.md` or this file (see "Known CBass Credentials" below)
3. Use `n8n_assign_credential` with the known credential IDs

---

## Setup

### Initial Clone (New Installation)

```bash
# Clone CBass with submodules
git clone --recursive https://github.com/1215-Labs/CBass.git
cd CBass

# Build the n8n-mcp submodule
cd vendor/n8n-mcp
npm install
npm run build
cd ../..

# Configure MCP
cp .mcp.json.example .mcp.json
# Edit .mcp.json with your paths and API keys
```

### Existing Installation (Add Submodule)

```bash
cd CBass

# Initialize and fetch submodule
git submodule update --init --recursive

# Build the submodule
cd vendor/n8n-mcp
npm install
npm run build
cd ../..
```

### MCP Configuration

The `.mcp.json` file is gitignored (contains API keys). Copy the example and configure:

```bash
cp .mcp.json.example .mcp.json
```

**Windows Configuration:**
```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "node",
      "args": ["./vendor/n8n-mcp/dist/mcp/index.js"],
      "cwd": "X:\\GitHub\\CBass",
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "https://n8n.cbass.space",
        "N8N_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**Linux/VPS Configuration:**
```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "node",
      "args": ["./vendor/n8n-mcp/dist/mcp/index.js"],
      "cwd": "/opt/cbass",
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "https://n8n.cbass.space",
        "N8N_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

> **Note**: The entry point is `dist/mcp/index.js` (not `dist/index.js`). The `mcp/index.js` contains the `main()` function that starts the MCP server.

### Update Submodule

To pull the latest changes from the fork:

```bash
cd vendor/n8n-mcp
git pull origin feature/credential-management-tools
npm install
npm run build
cd ../..
git add vendor/n8n-mcp
git commit -m "chore: update n8n-mcp submodule"
```

---

## Security Architecture

### Critical Security Requirement

**The `data` field in credentials contains secrets (API keys, passwords, tokens) and must NEVER be returned to users through the MCP interface.**

### Implementation: `sanitizeCredential()`

A security-critical function was added to `handlers-n8n-manager.ts`:

```typescript
/**
 * SECURITY CRITICAL: Remove sensitive data from credentials before returning.
 * The `data` field contains secrets (API keys, passwords, tokens) and must NEVER
 * be returned to the user through the MCP interface.
 */
function sanitizeCredential(credential: Credential): Omit<Credential, 'data'> {
  const { data, ...safeCredential } = credential;
  return safeCredential;
}
```

This function is called on every credential before it is returned to the user, ensuring that:
- API keys are never exposed
- Passwords are never exposed
- OAuth tokens are never exposed
- Any other secret data is never exposed

---

## New Tools

### 1. `n8n_list_credentials` ❌

> **⚠️ Non-functional**: n8n's Public API blocks GET requests to `/credentials` for security.

**Purpose**: List all credentials with metadata only (never secrets).

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | number | No | Max credentials to return (1-100, default: 100) |
| `cursor` | string | No | Pagination cursor from previous response |
| `type` | string | No | Filter by credential type (e.g., "openAiApi", "slackApi") |

**Error Response**:
```json
{
  "success": false,
  "error": "GET method not allowed",
  "code": "API_ERROR"
}
```

**Workaround**: Use the manual credential registry in CLAUDE.md or this document.

---

### 2. `n8n_get_credential` ❌

> **⚠️ Non-functional**: n8n's Public API blocks GET requests to `/credentials/{id}` for security.

**Purpose**: Get metadata for a specific credential by ID.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Credential ID to retrieve |

**Error Response**:
```json
{
  "success": false,
  "error": "GET method not allowed",
  "code": "API_ERROR"
}
```

**Workaround**: Look up credential details in n8n UI (Settings → Credentials).

---

### 3. `n8n_get_credential_schema`

**Purpose**: Get the schema/required fields for a credential type. Useful for understanding what fields are needed when creating credentials manually in n8n.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `credentialType` | string | Yes | Credential type name (e.g., "openAiApi", "slackApi") |

**Known Credential Schemas**:

| Type | Required Fields | Description |
|------|-----------------|-------------|
| `openAiApi` | `apiKey` | OpenAI API credentials |
| `googlePalmApi` | `apiKey` | Google AI (Gemini/PaLM) API credentials |
| `anthropicApi` | `apiKey` | Anthropic API credentials |
| `slackApi` | `accessToken` | Slack Bot Token or User Token |
| `httpBasicAuth` | `user`, `password` | HTTP Basic Authentication |
| `httpHeaderAuth` | `name`, `value` | HTTP Header Authentication |
| `oAuth2Api` | `clientId`, `clientSecret`, `accessToken`, `refreshToken` | OAuth2 credentials |
| `postgresApi` | `host`, `database`, `user`, `password`, `port`, `ssl` | PostgreSQL database |
| `mysqlApi` | `host`, `database`, `user`, `password`, `port` | MySQL database |
| `awsApi` | `accessKeyId`, `secretAccessKey`, `region` | AWS API credentials |

**Example**:
```json
{
  "success": true,
  "data": {
    "credentialType": "openAiApi",
    "description": "Credential type: openAiApi",
    "schema": {
      "fields": ["apiKey"],
      "description": "OpenAI API credentials"
    },
    "usedByNodes": [
      { "nodeType": "@n8n/n8n-nodes-langchain.lmChatOpenAi", "displayName": "OpenAI Chat Model" }
    ]
  }
}
```

---

### 4. `n8n_test_credential` ❌

> **⚠️ Non-functional**: Depends on `n8n_get_credential` which is blocked.

**Purpose**: Test if a credential exists and is accessible.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Credential ID to test |

**Error Response**:
```json
{
  "success": false,
  "error": "GET method not allowed",
  "code": "API_ERROR"
}
```

**Workaround**: Test credentials by running a workflow that uses them.

---

### 5. `n8n_assign_credential` ✅

**Purpose**: Assign a credential to a workflow node. This is the **primary working tool** - use it with known credential IDs from the manual registry.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflowId` | string | Yes | Workflow ID containing the node |
| `nodeName` | string | Yes | Name of the node to assign the credential to |
| `credentialId` | string | Yes | Credential ID to assign |
| `credentialType` | string | Yes | Credential type (must match the node's expected type) |
| `credentialName` | string | No | Display name for the credential (defaults to `"{type} credential"`) |

**Note**: This tool skips credential validation because n8n's API blocks GET requests. It trusts the provided credential ID. Use the known credential IDs from the registry below.

**Example**:
```json
// Request
{
  "workflowId": "CYfLRw6IPTJ7tfcD",
  "nodeName": "OpenAI Chat Model",
  "credentialId": "t6PNOhqfMP9ssxHr",
  "credentialType": "openAiApi",
  "credentialName": "OpenAI API"
}

// Response
{
  "success": true,
  "data": {
    "workflowId": "CYfLRw6IPTJ7tfcD",
    "nodeName": "OpenAI Chat Model",
    "credential": {
      "id": "t6PNOhqfMP9ssxHr",
      "name": "OpenAI API",
      "type": "openAiApi"
    }
  },
  "message": "Successfully assigned credential \"OpenAI API\" to node \"OpenAI Chat Model\" in workflow CYfLRw6IPTJ7tfcD"
}
```

**Node Not Found Error**:
```json
{
  "success": false,
  "error": "Failed to assign credential to node",
  "details": {
    "workflowId": "CYfLRw6IPTJ7tfcD",
    "nodeName": "Nonexistent Node",
    "credentialId": "t6PNOhqfMP9ssxHr",
    "hint": "Verify the workflow ID and node name are correct. The node must exist in the workflow."
  }
}
```

---

## Usage Examples

### ✅ Working Tools

#### Get Schema for a Credential Type
```
n8n_get_credential_schema({ credentialType: "openAiApi" })
```

#### Assign Credential to a Workflow Node
```
n8n_assign_credential({
  workflowId: "CYfLRw6IPTJ7tfcD",
  nodeName: "OpenAI Chat Model",
  credentialId: "t6PNOhqfMP9ssxHr",
  credentialType: "openAiApi",
  credentialName: "OpenAI API"
})
```

#### Assign Multiple Credentials to a Workflow
```
// Assign OpenAI to all OpenAI Chat Model nodes
n8n_assign_credential({
  workflowId: "CYfLRw6IPTJ7tfcD",
  nodeName: "OpenAI Chat Model (Planner)",
  credentialId: "t6PNOhqfMP9ssxHr",
  credentialType: "openAiApi",
  credentialName: "OpenAI API"
})

// Assign Gemini to analysis nodes
n8n_assign_credential({
  workflowId: "CYfLRw6IPTJ7tfcD",
  nodeName: "Gemini Model (Background)",
  credentialId: "UwcFmvOdHdi8YhPh",
  credentialType: "googlePalmApi",
  credentialName: "Google Gemini"
})
```

### ❌ Non-Working Tools (Blocked by n8n API)

These tools are implemented but will return "GET method not allowed" errors:

```
n8n_list_credentials({})                              // ❌ Blocked
n8n_list_credentials({ type: "openAiApi" })           // ❌ Blocked
n8n_get_credential({ id: "t6PNOhqfMP9ssxHr" })        // ❌ Blocked
n8n_test_credential({ id: "t6PNOhqfMP9ssxHr" })       // ❌ Blocked
```

---

## Known CBass Credentials

For reference, these are the credentials configured in the CBass n8n instance:

| Service | Credential ID | Credential Type |
|---------|---------------|-----------------|
| OpenAI | `t6PNOhqfMP9ssxHr` | `openAiApi` |
| Google Gemini | `UwcFmvOdHdi8YhPh` | `googlePalmApi` |

---

## Files Modified (in n8n-mcp fork)

### 1. `src/mcp/tools-n8n-manager.ts`

**Changes**: +91 lines

Added 5 tool definitions to the `n8nManagementTools` array. Each tool definition includes:
- `name` - Tool identifier
- `description` - What the tool does
- `inputSchema` - JSON Schema for parameters with `type`, `properties`, and `required` fields

---

### 2. `src/mcp/handlers-n8n-manager.ts`

**Changes**: +400 lines

#### New Import
```typescript
import {
  // ... existing imports ...
  Credential  // Added
} from '../types/n8n-api';
```

#### New Functions Added

1. **`sanitizeCredential()`** - Security function to remove secret data
2. **`handleListCredentials()`** - Handler for n8n_list_credentials
3. **`handleGetCredential()`** - Handler for n8n_get_credential
4. **`handleGetCredentialSchema()`** - Handler for n8n_get_credential_schema
5. **`handleTestCredential()`** - Handler for n8n_test_credential
6. **`handleAssignCredential()`** - Handler for n8n_assign_credential

#### Zod Validation Schemas

```typescript
const listCredentialsSchema = z.object({
  limit: z.number().min(1).max(100).optional(),
  cursor: z.string().optional(),
  type: z.string().optional(),
});

const getCredentialSchema = z.object({
  id: z.string(),
});

const getCredentialSchemaSchema = z.object({
  credentialType: z.string(),
});

const testCredentialSchema = z.object({
  id: z.string(),
});

const assignCredentialSchema = z.object({
  workflowId: z.string(),
  nodeName: z.string(),
  credentialId: z.string(),
  credentialType: z.string(),
  credentialName: z.string().optional(),
});
```

---

### 3. `src/mcp/server.ts`

**Changes**: +49 lines

Added validation cases and switch cases to route tool calls to handlers.

---

### 4. `tests/unit/mcp/handlers-credentials.test.ts`

**New File**: 14 unit tests

Tests cover:

1. **sanitizeCredential Security** (3 tests)
   - Verifies `data` field is NEVER in returned credentials
   - Handles credentials with undefined data field
   - Handles credentials with empty data object

2. **handleListCredentials** (2 tests)
   - Sanitizes ALL credentials in the response
   - Filters by type when specified

3. **handleGetCredentialSchema** (2 tests)
   - Returns known schema for common credential types
   - Returns appropriate message for unknown credential types

4. **handleTestCredential** (2 tests)
   - Returns exists status when credential is found
   - Returns not_found status when credential does not exist

5. **handleAssignCredential** (2 tests)
   - Detects credential type mismatch
   - Constructs correct updateNode operation

6. **Input Validation** (3 tests)
   - Validates limit bounds for listCredentials
   - Requires id for getCredential
   - Requires all fields for assignCredential

---

## Build and Test

### Build the Submodule
```bash
cd vendor/n8n-mcp
npm install
npm run build
```

### Run Tests
```bash
cd vendor/n8n-mcp

# Run only credential tests
npm test -- --run tests/unit/mcp/handlers-credentials.test.ts

# Run all tests
npm test -- --run
```

### Verify Tools are Registered
```bash
cd vendor/n8n-mcp
node -e "
const { n8nManagementTools } = require('./dist/mcp/tools-n8n-manager');
const credTools = n8nManagementTools.filter(t => t.name.includes('credential'));
console.log('Credential tools found:', credTools.length);
credTools.forEach(t => console.log(' -', t.name));
"
```

Expected output:
```
Credential tools found: 5
 - n8n_list_credentials
 - n8n_get_credential
 - n8n_get_credential_schema
 - n8n_test_credential
 - n8n_assign_credential
```

---

## Future Improvements

### Potential Enhancements

1. **Create Credential Tool** - Allow creating credentials via MCP (would require secure secret handling)
2. **Delete Credential Tool** - Allow deleting credentials via MCP
3. **Update Credential Tool** - Allow updating credential metadata (not secrets)
4. **Credential Testing** - Implement actual credential testing by making test API calls

### Pull Request to Upstream

The changes could be contributed back to the upstream n8n-mcp repository. Key considerations:
- Security review of `sanitizeCredential()` implementation
- Documentation updates
- Additional test coverage for edge cases
