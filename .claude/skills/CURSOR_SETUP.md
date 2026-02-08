# Using n8n-skills with Cursor

This guide explains how to configure Cursor to use the n8n-skills effectively.

## Quick Start (Recommended)

The easiest approach is to use **Cursor Rules** (`.cursor/rules/` directory) with MDC format.

### Option 1: Project-Level Rules (`.cursor/rules/`)

Create a `.cursor/rules/` directory in your n8n project and add skill files:

```bash
your-n8n-project/
├── .cursor/
│   └── rules/
│       ├── n8n-expression-syntax.mdc
│       ├── n8n-mcp-tools.mdc
│       ├── n8n-workflow-patterns.mdc
│       ├── n8n-validation.mdc
│       ├── n8n-node-config.mdc
│       ├── n8n-code-javascript.mdc
│       └── n8n-code-python.mdc
├── workflows/
└── ...
```

### Option 2: User-Level Rules (Global)

Add rules to your global Cursor settings for all projects:

1. Open **Settings** → **Cursor Settings** → **Rules**
2. Add the skill content to **User Rules** section

---

## MDC File Format

MDC (Modular Context) files use YAML frontmatter to control when rules activate:

```markdown
---
description: Rule description (activates via semantic matching)
globs: ["*.json", "workflows/**"]  # Optional: file patterns
alwaysApply: false  # Optional: always include this context
---

# Rule Content Here

Your rule content in markdown...
```

### Activation Methods

| Method | When to Use |
|--------|-------------|
| `description` | Semantic matching - activates when query matches description |
| `globs` | File pattern matching - activates when editing matching files |
| `alwaysApply: true` | Always include this context in every query |

---

## Example MDC Files

### n8n-expression-syntax.mdc

```markdown
---
description: n8n expression syntax with {{}} braces, $json variables, $node references, webhook body data access
globs: ["*.json", "workflows/**/*.json"]
---

# n8n Expression Syntax

## Expression Format

All dynamic content in n8n uses **double curly braces**: `{{expression}}`

**Examples**:
- ✅ `{{$json.email}}`
- ✅ `{{$json.body.name}}` (webhook data!)
- ❌ `$json.email` (no braces)

## 🚨 CRITICAL: Webhook Data Structure

Webhook data is NOT at the root! It's under `.body`:

```javascript
// ❌ WRONG
{{$json.name}}

// ✅ CORRECT  
{{$json.body.name}}
```

## Core Variables

- `$json` - Current node output
- `$node["Name"]` - Reference other nodes
- `$now` - Current timestamp
- `$env` - Environment variables

## When NOT to Use Expressions

❌ **Code nodes**: Use direct JS access (`$json.email` not `{{$json.email}}`)
❌ **Webhook paths**: Static only
❌ **Credentials**: Use n8n credential system
```

### n8n-mcp-tools.mdc

```markdown
---
description: n8n-mcp MCP server tools, search_nodes, get_node, validate_node, workflow management, template search
globs: ["*.json", "workflows/**"]
---

# n8n MCP Tools Expert

## Critical: nodeType Formats

**Two different formats** for different tools!

### Search/Validate Tools (SHORT prefix)
```javascript
"nodes-base.slack"
"nodes-base.httpRequest"
"nodes-langchain.agent"
```

### Workflow Tools (FULL prefix)
```javascript
"n8n-nodes-base.slack"
"n8n-nodes-base.httpRequest"
"@n8n/n8n-nodes-langchain.agent"
```

## Tool Selection Guide

| Task | Tool | Success Rate |
|------|------|--------------|
| Find nodes | `search_nodes` | 99.9% |
| Get node details | `get_node` (mode: "info", detail: "standard") | 91.7% |
| Validate config | `validate_node` | ~97% |
| Create workflow | `n8n_create_workflow` | 96.8% |
| Edit workflow | `n8n_update_partial_workflow` | 99.0% |

## Common Mistakes

❌ Using full prefix with search tools:
```javascript
❌ get_node({nodeType: "n8n-nodes-base.slack"})
✅ get_node({nodeType: "nodes-base.slack"})
```

❌ Forgetting smart parameters for IF/Switch:
```javascript
// Use branch="true"/"false" for IF nodes
{type: "addConnection", source: "IF", target: "Handler", branch: "true"}
```
```

### n8n-workflow-patterns.mdc

```markdown
---
description: n8n workflow patterns, webhook processing, HTTP API integration, database sync, AI agents, scheduled tasks
globs: ["*.json", "workflows/**"]
---

# n8n Workflow Patterns

## 5 Core Patterns

### 1. Webhook Processing
`Webhook → Process → Respond`

### 2. HTTP API Integration  
`Trigger → HTTP Request → Transform → Output`

### 3. Database Sync
`Trigger → Fetch → Compare → Upsert`

### 4. AI Agent Workflow
`Trigger → AI Agent (+ Tools) → Output`

### 5. Scheduled Tasks
`Schedule Trigger → Process → Notify`

## Workflow Creation Checklist

1. ✅ Start with trigger node
2. ✅ Use correct nodeType format (n8n-nodes-base.*)
3. ✅ Set unique node IDs and names
4. ✅ Configure proper connections
5. ✅ Validate before activating
```

### n8n-code-javascript.mdc

```markdown
---
description: n8n Code node JavaScript, $input, $json, $helpers, httpRequest, return format, webhook body access
globs: ["*.json", "workflows/**"]
---

# n8n Code Node (JavaScript)

## Data Access

```javascript
// Get all items
const items = $input.all();

// Get first item
const first = $input.first();

// Current item (in "Run Once for Each Item" mode)
const item = $input.item;

// Access JSON data
const email = $json.email;
```

## 🚨 CRITICAL: Webhook Data

Webhook data is under `.body`:

```javascript
// ❌ WRONG
const name = $json.name;

// ✅ CORRECT
const name = $json.body.name;
```

## Return Format

**MUST return array of objects with `json` property**:

```javascript
// ✅ CORRECT
return [{
  json: {
    name: "John",
    email: "john@example.com"
  }
}];

// ❌ WRONG
return {name: "John"};
return [{name: "John"}];
```

## Built-in Functions

```javascript
// HTTP requests
const response = await $helpers.httpRequest({
  method: 'GET',
  url: 'https://api.example.com/data'
});

// JMESPath queries
const result = $jmespath(data, 'items[*].name');
```
```

---

## Full Installation

For complete skill content, copy the files from the `n8n-mcp-skills-v1.0.0/skills/` directory:

### Automated Setup Script

Create this script to set up all skills:

```powershell
# PowerShell: setup-cursor-rules.ps1
$skillsPath = ".\dist\n8n-mcp-skills-v1.0.0\skills"
$rulesPath = ".\.cursor\rules"

# Create rules directory
New-Item -ItemType Directory -Force -Path $rulesPath

# Copy each skill
$skills = @(
    @{name="n8n-expression-syntax"; desc="n8n expression syntax, {{}} braces, $json, $node, webhook body"},
    @{name="n8n-mcp-tools-expert"; desc="n8n-mcp tools, search_nodes, validate, workflow management"},
    @{name="n8n-workflow-patterns"; desc="n8n workflow patterns, webhook, HTTP, database, AI, scheduled"},
    @{name="n8n-validation-expert"; desc="n8n validation errors, false positives, auto-sanitization"},
    @{name="n8n-node-configuration"; desc="n8n node configuration, property dependencies, operations"},
    @{name="n8n-code-javascript"; desc="n8n Code node JavaScript, $input, $json, $helpers, return format"},
    @{name="n8n-code-python"; desc="n8n Code node Python, _input, _json, standard library only"}
)

foreach ($skill in $skills) {
    $skillDir = Join-Path $skillsPath $skill.name
    $skillFile = Join-Path $skillDir "SKILL.md"
    
    if (Test-Path $skillFile) {
        # Read skill content (skip YAML frontmatter)
        $content = Get-Content $skillFile -Raw
        $content = $content -replace "(?s)^---.*?---\s*", ""
        
        # Create MDC file with new frontmatter
        $mdcContent = @"
---
description: $($skill.desc)
globs: ["*.json", "workflows/**/*.json"]
---

$content
"@
        $outputFile = Join-Path $rulesPath "$($skill.name).mdc"
        $mdcContent | Out-File -FilePath $outputFile -Encoding utf8
        Write-Host "Created: $outputFile"
    }
}
```

### Bash Setup Script

```bash
#!/bin/bash
# setup-cursor-rules.sh

SKILLS_PATH="./dist/n8n-mcp-skills-v1.0.0/skills"
RULES_PATH="./.cursor/rules"

mkdir -p "$RULES_PATH"

# Skills to process
declare -A SKILLS=(
    ["n8n-expression-syntax"]="n8n expression syntax, braces, json, node, webhook body"
    ["n8n-mcp-tools-expert"]="n8n-mcp tools, search_nodes, validate, workflow management"
    ["n8n-workflow-patterns"]="n8n workflow patterns, webhook, HTTP, database, AI, scheduled"
    ["n8n-validation-expert"]="n8n validation errors, false positives, auto-sanitization"
    ["n8n-node-configuration"]="n8n node configuration, property dependencies, operations"
    ["n8n-code-javascript"]="n8n Code node JavaScript, input, json, helpers, return format"
    ["n8n-code-python"]="n8n Code node Python, input, json, standard library only"
)

for skill in "${!SKILLS[@]}"; do
    skill_file="$SKILLS_PATH/$skill/SKILL.md"
    if [[ -f "$skill_file" ]]; then
        # Extract content after YAML frontmatter
        content=$(sed '1,/^---$/d; 1,/^---$/d' "$skill_file")
        
        # Create MDC file
        cat > "$RULES_PATH/$skill.mdc" << EOF
---
description: ${SKILLS[$skill]}
globs: ["*.json", "workflows/**/*.json"]
---

$content
EOF
        echo "Created: $RULES_PATH/$skill.mdc"
    fi
done
```

---

## Alternative: User Rules

For global rules across all projects, add to Cursor Settings:

1. Open **Cursor Settings** (Ctrl/Cmd + ,)
2. Search for "Rules"
3. Under **User Rules**, add key knowledge:

```
## n8n Workflow Development Rules

### Expression Syntax
- Use {{expression}} for dynamic content
- Webhook data is under $json.body, NOT $json directly
- No expressions in Code nodes - use direct JS: $json.email

### MCP Tool Usage
- nodeType format: "nodes-base.slack" for search/validate
- nodeType format: "n8n-nodes-base.slack" for workflows
- Use get_node with detail: "standard" (not "full")

### Code Nodes
- Return format: [{json: {...}}]
- Use $input.all(), $input.first(), $input.item
- Use $helpers.httpRequest() for HTTP calls

### Workflow Patterns
- Always start with trigger node
- Validate workflows before activation
- Use smart parameters (branch="true") for IF nodes
```

---

## Best Practices

### 1. Use Semantic Descriptions

Write descriptions that match how you'd ask questions:

```markdown
---
description: How to access webhook data in n8n, webhook body structure, $json.body
---
```

### 2. Combine with MCP Server

These skills work best with the n8n-mcp MCP server. Configure in `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["-y", "@czlonkowski/n8n-mcp"],
      "env": {
        "N8N_API_URL": "http://localhost:5678/api/v1",
        "N8N_API_KEY": "your-api-key"
      }
    }
  }
}
```

### 3. Include Reference Files

For complete knowledge, also add reference files as additional rules:

```
.cursor/rules/
├── n8n-expression-syntax.mdc      # Main skill
├── n8n-expression-mistakes.mdc    # From COMMON_MISTAKES.md
├── n8n-expression-examples.mdc    # From EXAMPLES.md
└── ...
```

---

## Verification

Test your setup by asking Cursor:

1. **"How do I access webhook data in n8n?"**
   → Should mention `$json.body`

2. **"What's the nodeType format for search_nodes?"**
   → Should mention `nodes-base.slack` (short prefix)

3. **"How do I return data from a Code node?"**
   → Should mention `[{json: {...}}]` format

4. **"Build a webhook to Slack workflow"**
   → Should use correct patterns and tool calls

---

## Troubleshooting

### Rules Not Activating

1. Check file extension is `.mdc` (not `.md`)
2. Verify YAML frontmatter is valid
3. Make descriptions match your query patterns
4. Try `alwaysApply: true` for debugging

### Too Much Context

1. Use more specific `globs` patterns
2. Split large skills into smaller focused rules
3. Remove `alwaysApply` from non-essential rules

### MCP Tools Not Working

1. Verify n8n-mcp is configured in `.cursor/mcp.json`
2. Check N8N_API_URL and N8N_API_KEY are set
3. Ensure n8n instance is running

---

## Resources

- [n8n-mcp Repository](https://github.com/czlonkowski/n8n-mcp)
- [Cursor Rules Documentation](https://docs.cursor.com/context/rules-for-ai)
- [n8n Documentation](https://docs.n8n.io/)

