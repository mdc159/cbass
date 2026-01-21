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

The original n8n-mcp package provides comprehensive workflow management tools but lacks credential management capabilities. The n8n API supports credential operations, but n8n-mcp didn't expose them. This limitation required manual credential ID lookups in the n8n UI when assigning credentials to workflow nodes.

### Key Discovery

During implementation, we discovered that the n8n API client (`src/services/n8n-api-client.ts`) already had credential methods implemented:
- `listCredentials(params)`
- `getCredential(id)`
- `createCredential(credential)`
- `updateCredential(id, credential)`
- `deleteCredential(id)`

These just needed to be exposed as MCP tools with proper security measures.

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
      "args": ["./vendor/n8n-mcp/dist/index.js"],
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
      "args": ["./vendor/n8n-mcp/dist/index.js"],
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

### 1. `n8n_list_credentials`

**Purpose**: List all credentials with metadata only (never secrets).

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | number | No | Max credentials to return (1-100, default: 100) |
| `cursor` | string | No | Pagination cursor from previous response |
| `type` | string | No | Filter by credential type (e.g., "openAiApi", "slackApi") |

**Response Fields**:
- `id` - Credential identifier
- `name` - Human-readable name
- `type` - Credential type (e.g., "openAiApi", "googlePalmApi")
- `nodesAccess` - Array of node types that can use this credential
- `createdAt` - Creation timestamp
- `updatedAt` - Last update timestamp

**Example**:
```json
{
  "success": true,
  "data": {
    "credentials": [
      {
        "id": "t6PNOhqfMP9ssxHr",
        "name": "OpenAI",
        "type": "openAiApi",
        "createdAt": "2024-01-15T10:30:00.000Z",
        "updatedAt": "2024-01-15T10:30:00.000Z"
      }
    ],
    "returned": 1,
    "hasMore": false
  }
}
```

---

### 2. `n8n_get_credential`

**Purpose**: Get metadata for a specific credential by ID.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Credential ID to retrieve |

**Response**: Same fields as `n8n_list_credentials` for a single credential.

**Example**:
```json
{
  "success": true,
  "data": {
    "id": "t6PNOhqfMP9ssxHr",
    "name": "OpenAI",
    "type": "openAiApi",
    "nodesAccess": [
      { "nodeType": "n8n-nodes-base.openAi" }
    ],
    "createdAt": "2024-01-15T10:30:00.000Z",
    "updatedAt": "2024-01-15T10:30:00.000Z"
  }
}
```

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

### 4. `n8n_test_credential`

**Purpose**: Test if a credential exists and is accessible.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Credential ID to test |

**Limitation**: The n8n public API does not expose a direct credential testing endpoint. This tool verifies the credential exists but cannot test if it actually authenticates with the external service.

**Response**:
```json
{
  "success": true,
  "data": {
    "credential": {
      "id": "t6PNOhqfMP9ssxHr",
      "name": "OpenAI",
      "type": "openAiApi"
    },
    "status": "exists",
    "message": "Credential exists and is accessible. Note: To fully test the credential, use it in a workflow execution.",
    "hint": "The n8n API does not expose a direct credential testing endpoint."
  }
}
```

---

### 5. `n8n_assign_credential`

**Purpose**: Assign a credential to a workflow node. This is the most practical tool - it eliminates the need to manually look up credential IDs and construct update operations.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflowId` | string | Yes | Workflow ID containing the node |
| `nodeName` | string | Yes | Name of the node to assign the credential to |
| `credentialId` | string | Yes | Credential ID to assign |
| `credentialType` | string | Yes | Credential type (must match the node's expected type) |

**Validation**:
- Verifies the credential exists before assignment
- Validates that the credential type matches the requested type
- Returns a clear error if there's a type mismatch

**Example**:
```json
// Request
{
  "workflowId": "CYfLRw6IPTJ7tfcD",
  "nodeName": "OpenAI Chat Model",
  "credentialId": "t6PNOhqfMP9ssxHr",
  "credentialType": "openAiApi"
}

// Response
{
  "success": true,
  "data": {
    "workflowId": "CYfLRw6IPTJ7tfcD",
    "nodeName": "OpenAI Chat Model",
    "credential": {
      "id": "t6PNOhqfMP9ssxHr",
      "name": "OpenAI",
      "type": "openAiApi"
    }
  },
  "message": "Successfully assigned credential \"OpenAI\" to node \"OpenAI Chat Model\" in workflow CYfLRw6IPTJ7tfcD"
}
```

**Type Mismatch Error**:
```json
{
  "success": false,
  "error": "Credential type mismatch",
  "details": {
    "expected": "slackApi",
    "actual": "openAiApi",
    "hint": "The credential \"OpenAI\" is of type \"openAiApi\", not \"slackApi\". Use the correct credential type."
  }
}
```

---

## Usage Examples

### List All Credentials
```
n8n_list_credentials({})
```

### List Only OpenAI Credentials
```
n8n_list_credentials({ type: "openAiApi" })
```

### Get Credential Details
```
n8n_get_credential({ id: "t6PNOhqfMP9ssxHr" })
```

### Get Schema for a Credential Type
```
n8n_get_credential_schema({ credentialType: "openAiApi" })
```

### Test if a Credential Exists
```
n8n_test_credential({ id: "t6PNOhqfMP9ssxHr" })
```

### Assign Credential to a Workflow Node
```
n8n_assign_credential({
  workflowId: "CYfLRw6IPTJ7tfcD",
  nodeName: "OpenAI Chat Model",
  credentialId: "t6PNOhqfMP9ssxHr",
  credentialType: "openAiApi"
})
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
