# OpenCode Tutorial: Clone, Modify, Trim & Deploy a Repository to VPS

A comprehensive guide for using OpenCode to clone a repository, detach it, modify and trim the codebase, and deploy to a cloud-hosted VPS.

---

## Table of Contents

1. [Installation & Initial Setup](#phase-1-installation--initial-setup)
2. [Clone & Detach the Repository](#phase-2-clone--detach-the-repository)
3. [Modify & Trim the Codebase](#phase-3-modify--trim-the-codebase)
4. [Configure for VPS Deployment](#phase-4-configure-for-vps-deployment)
5. [Useful MCP Servers & Plugins](#phase-5-useful-mcp-servers--plugins)
6. [Sample Project Configuration](#phase-6-sample-project-configuration)
7. [VPS Deployment Workflow](#phase-7-vps-deployment-workflow)
8. [Quick Reference](#quick-reference)

---

## Phase 1: Installation & Initial Setup

### Install OpenCode

Choose your preferred installation method:
```bash
# Quick install script
curl -fsSL https://opencode.ai/install | bash

# Or via npm/bun/pnpm
npm install opencode-ai

# Or via Chocolatey (Windows)
choco install opencode

# Or via Scoop (Windows)
scoop bucket add extras
scoop install extras/opencode
```

### Configure Your LLM Provider

Run OpenCode and connect to a provider:
```bash
opencode
```

Then use the `/connect` command within the TUI, or set up API keys via environment variables:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Alternatively, use `opencode auth login` to configure API keys for any provider.

---

## Phase 2: Clone & Detach the Repository

### Step 1: Clone the Source Repository

Use OpenCode's built-in `bash` tool to clone the repository. Within the TUI, prompt:
```
Clone the repository at https://github.com/original/repo into a new folder called my-project
```

OpenCode will execute:
```bash
git clone https://github.com/original/repo my-project
```

### Step 2: Detach Git History

To create a fresh, detached repository with no connection to the original:
```
Navigate to my-project, remove the .git folder entirely, then initialize a fresh git repository. 
Make the first commit with message "Initial commit - forked from original"
```

OpenCode will execute:
```bash
cd my-project
rm -rf .git
git init
git add .
git commit -m "Initial commit - forked from original"
```

### Step 3: Initialize OpenCode for the Project
```bash
cd my-project
opencode
```

Then run the initialization command:
```
/init
```

This creates an `AGENTS.md` file that helps OpenCode understand your project structure. This file should be committed to Git for team consistency.

---

## Phase 3: Modify & Trim the Codebase

### Understanding Plan Mode vs Build Mode

OpenCode has two primary modes:

| Mode | Purpose | Tools Available |
|------|---------|-----------------|
| **Plan** | Analysis and planning without making changes | Read-only tools |
| **Build** | Full development with all tools enabled | All tools including write/edit |

Press `Tab` to switch between modes.

### Use Plan Mode First

Switch to **Plan Mode** by pressing `Tab`, then analyze the codebase:
```
Analyze this codebase and identify:
1. Files and directories that are unnecessary for a production deployment
2. Development-only dependencies that can be removed
3. Configuration files that need to be updated
4. Any hardcoded values that should become environment variables
```

### Create Custom Commands for Your Workflow

Create the command directory structure:
```
.opencode/
└── command/
    ├── cleanup.md
    ├── envify.md
    └── trim-deps.md
```

#### .opencode/command/cleanup.md
```markdown
---
description: Remove unnecessary files and trim the codebase
agent: build
---

Remove the following from the codebase:
- Test files and test directories (keep essential tests)
- CI/CD configs not needed for VPS deployment
- Documentation that's not user-facing
- Example files and demo content
- Unused dependencies in package.json

Show me what you plan to remove before executing.
```

#### .opencode/command/envify.md
```markdown
---
description: Convert hardcoded values to environment variables
agent: build
---

Find all hardcoded configuration values (API URLs, ports, secrets, database connections) 
and convert them to environment variables. Create a .env.example file with all required variables.
```

#### .opencode/command/trim-deps.md
```markdown
---
description: Remove unused dependencies
agent: build
---

Analyze package.json (or equivalent dependency file) and identify:
1. Dependencies that are not imported anywhere in the codebase
2. DevDependencies that can be removed for production
3. Duplicate or conflicting packages

Remove unused dependencies and update lock files accordingly.
```

### Execute Your Custom Commands

Switch to **Build Mode** by pressing `Tab`, then run:
```
/cleanup
```

Review the proposed changes, then:
```
/envify
```

And finally:
```
/trim-deps
```

### Undo/Redo Changes

If changes aren't what you wanted:
```
/undo
```

Run multiple times to undo multiple changes. To restore undone changes:
```
/redo
```

---

## Phase 4: Configure for VPS Deployment

### Create a Deployment Agent

Create the agent directory structure:
```
.opencode/
└── agent/
    └── deploy.md
```

#### .opencode/agent/deploy.md
```markdown
---
description: Handles deployment configuration and scripts for VPS
mode: subagent
model: anthropic/claude-sonnet-4-20250514
tools:
  write: true
  edit: true
  bash: true
---

You are a deployment specialist. Focus on:
- Creating production-ready configurations
- Setting up environment-based configs
- Creating deployment scripts for Linux VPS
- Configuring process managers (PM2, systemd)
- Setting up reverse proxies (nginx, caddy)
- Ensuring security best practices

When creating deployment configurations:
1. Always use environment variables for sensitive data
2. Include health checks where applicable
3. Set up proper logging
4. Configure automatic restarts on failure
5. Use non-root users for running applications
```

### Create Deployment Commands

#### .opencode/command/deploy-prep.md
```markdown
---
description: Prepare project for VPS deployment
agent: deploy
---

Prepare this project for VPS deployment:

1. Create a production Dockerfile if using containers
2. Create a docker-compose.yml for easy deployment
3. Create a systemd service file OR PM2 ecosystem config
4. Create an nginx reverse proxy configuration
5. Create a deployment script (deploy.sh) that handles:
   - Pulling latest code
   - Installing dependencies
   - Building the project
   - Restarting services
6. Create a .env.production.example with all required environment variables
```

#### .opencode/command/docker-setup.md
```markdown
---
description: Create Docker configuration for the project
agent: deploy
---

Create a complete Docker setup:

1. Multi-stage Dockerfile optimized for production
2. docker-compose.yml with:
   - Application service
   - Database service (if needed)
   - Redis/cache service (if needed)
   - Reverse proxy service
3. .dockerignore file
4. Docker health checks

Ensure the setup follows security best practices and uses minimal base images.
```

#### .opencode/command/systemd-setup.md
```markdown
---
description: Create systemd service configuration
agent: deploy
---

Create a systemd service file for this application:

1. Service unit file with proper dependencies
2. Automatic restart on failure
3. Environment file integration
4. Logging to journald
5. Resource limits (memory, CPU)
6. Installation instructions

Target path: /etc/systemd/system/myapp.service
```

### Invoke the Deploy Agent

You can invoke the deploy agent directly using @ mention:
```
@deploy Create nginx configuration for this Node.js application running on port 3000
```

Or run your custom commands:
```
/deploy-prep
/docker-setup
/systemd-setup
```

---

## Phase 5: Useful MCP Servers & Plugins

### MCP Servers

MCP (Model Context Protocol) servers add external tools to OpenCode. Add them to your `opencode.json`:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "enabled": true
    },
    "gh_grep": {
      "type": "remote",
      "url": "https://mcp.grep.app",
      "enabled": true
    },
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp",
      "oauth": {}
    }
  }
}
```

#### Recommended MCP Servers

| Server | Purpose | Usage |
|--------|---------|-------|
| **Context7** | Search through documentation | `use context7` in prompts |
| **Grep by Vercel** | Search code examples on GitHub | `use gh_grep` in prompts |
| **Sentry** | Error tracking and monitoring | `use sentry` in prompts |

#### Using MCP Servers in Prompts
```
How do I configure nginx as a reverse proxy for a Node.js app? use context7
```
```
Show me examples of PM2 ecosystem configs for production deployments. use gh_grep
```

### Recommended Plugins

Add plugins to your `opencode.json`:
```json
{
  "plugin": [
    "opencode-notify",
    "opencode-worktree"
  ]
}
```

#### Plugin Directory

| Plugin | Purpose | Repository |
|--------|---------|------------|
| **opencode-notify** | Native OS notifications when tasks complete | [View](https://github.com/user/opencode-notify) |
| **opencode-worktree** | Zero-friction git worktrees for parallel work | [View](https://github.com/user/opencode-worktree) |
| **CC Safety Net** | Blocks destructive git/filesystem commands | [View](https://github.com/user/cc-safety-net) |
| **Dynamic Context Pruning** | Optimizes token usage | [View](https://github.com/user/dynamic-context-pruning) |
| **Shell Strategy** | Helps avoid interactive shell hangs | [View](https://github.com/user/shell-strategy) |
| **Opencode Ignore** | Ignore files based on patterns | [View](https://github.com/user/opencode-ignore) |
| **Smart Title** | Auto-generate meaningful session titles | [View](https://github.com/user/smart-title) |

### Installing Plugins

Plugins from npm are installed automatically at startup. Local plugins can be placed in:

- Project-level: `.opencode/plugin/`
- Global: `~/.config/opencode/plugin/`

---

## Phase 6: Sample Project Configuration

### Complete opencode.json

Create this file in your project root:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-20250514",
  "small_model": "anthropic/claude-haiku-4-20250514",
  "theme": "opencode",
  "autoupdate": true,
  
  "permission": {
    "edit": "allow",
    "bash": "ask",
    "webfetch": "allow"
  },
  
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "enabled": true
    },
    "gh_grep": {
      "type": "remote",
      "url": "https://mcp.grep.app",
      "enabled": true
    }
  },
  
  "plugin": [
    "opencode-notify"
  ],
  
  "agent": {
    "deploy": {
      "description": "Handles deployment configuration and scripts",
      "mode": "subagent",
      "prompt": "{file:.opencode/prompts/deploy.txt}",
      "tools": {
        "write": true,
        "edit": true,
        "bash": true
      }
    },
    "security": {
      "description": "Reviews code for security issues",
      "mode": "subagent",
      "tools": {
        "write": false,
        "edit": false
      }
    }
  },
  
  "command": {
    "cleanup": {
      "description": "Remove unnecessary files",
      "template": "Remove test files, CI configs, examples, and unused dependencies. Show what will be removed first.",
      "agent": "build"
    },
    "deploy-prep": {
      "description": "Prepare for VPS deployment",
      "template": "Create Dockerfile, docker-compose.yml, nginx config, systemd service, and deploy.sh script.",
      "agent": "deploy"
    },
    "security-check": {
      "description": "Run security audit",
      "template": "Audit this codebase for security vulnerabilities, exposed secrets, and unsafe configurations.",
      "agent": "security"
    }
  },
  
  "instructions": [
    "AGENTS.md",
    "CONTRIBUTING.md",
    "docs/*.md"
  ],
  
  "tools": {
    "bash": true,
    "edit": true,
    "write": true,
    "read": true,
    "grep": true,
    "glob": true,
    "webfetch": true
  },
  
  "share": "manual"
}
```

### Sample AGENTS.md
```markdown
# Project: My Forked Application

## Overview
This is a forked and trimmed version of [original-repo], prepared for VPS deployment.

## Project Structure
- `src/` - Application source code
- `config/` - Configuration files
- `scripts/` - Deployment and utility scripts
- `docker/` - Docker-related files

## Deployment Target
- Platform: Linux VPS (Ubuntu 22.04)
- Process Manager: PM2 or systemd
- Reverse Proxy: nginx
- Runtime: Node.js 20.x

## Code Standards
- Use TypeScript with strict mode
- Environment variables for all configuration
- No hardcoded secrets or URLs
- Docker-ready architecture

## Deployment Notes
- All sensitive configuration via environment variables
- Health check endpoint at /health
- Logging to stdout/stderr for container compatibility
- Graceful shutdown handling

## Commands
- `/cleanup` - Remove unnecessary files
- `/deploy-prep` - Generate deployment configurations
- `/security-check` - Run security audit
```

---

## Phase 7: VPS Deployment Workflow

### Create a Custom Deployment Tool

Create the tool directory structure:
```
.opencode/
└── tool/
    └── ssh-deploy.ts
```

#### .opencode/tool/ssh-deploy.ts
```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Generate SSH deployment commands for VPS",
  args: {
    host: tool.schema.string().describe("VPS hostname or IP"),
    user: tool.schema.string().describe("SSH username"),
    path: tool.schema.string().describe("Deployment path on server")
  },
  async execute(args) {
    return `
## Deployment Commands for ${args.host}

### 1. Copy files to server
\\`\\`\\`bash
rsync -avz --exclude 'node_modules' --exclude '.git' --exclude '.env' \\\\
  ./ ${args.user}@${args.host}:${args.path}
\\`\\`\\`

### 2. SSH and run deployment
\\`\\`\\`bash
ssh ${args.user}@${args.host} 'cd ${args.path} && ./deploy.sh'
\\`\\`\\`

### 3. Check service status
\\`\\`\\`bash
ssh ${args.user}@${args.host} 'systemctl status myapp'
\\`\\`\\`

### 4. View logs
\\`\\`\\`bash
ssh ${args.user}@${args.host} 'journalctl -u myapp -f'
\\`\\`\\`
    `
  }
})
```

#### .opencode/tool/server-setup.ts
```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Generate server setup commands for fresh VPS",
  args: {
    os: tool.schema.enum(["ubuntu", "debian", "centos"]).describe("Server OS"),
    runtime: tool.schema.enum(["node", "python", "go"]).describe("Application runtime")
  },
  async execute(args) {
    const commands = {
      ubuntu: {
        node: `
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install PM2
sudo npm install -g pm2

# Install nginx
sudo apt install -y nginx

# Configure firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
        `
      }
    }
    
    return commands[args.os]?.[args.runtime] || "Configuration not available for this combination"
  }
})
```

### Non-Interactive Deployment via CLI

Use OpenCode's CLI for automation in scripts:
```bash
# Generate deployment files
opencode run "Prepare this project for VPS deployment with nginx and PM2"

# Run a specific command
opencode run "/deploy-prep"

# Run with specific model
opencode run --model anthropic/claude-sonnet-4-20250514 "Create a production Dockerfile"

# Continue a previous session
opencode run --continue "Add SSL configuration to the nginx setup"
```

### Headless Server Mode

For CI/CD or remote access:
```bash
# Start headless server
opencode serve --port 4096 --hostname 0.0.0.0

# Attach from another terminal
opencode attach http://localhost:4096

# Or run commands against the server
opencode run --attach http://localhost:4096 "Check deployment status"
```

### Generated Deployment Files

After running `/deploy-prep`, you should have:
```
my-project/
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── deploy.sh
├── ecosystem.config.js (PM2)
├── myapp.service (systemd)
├── .env.example
└── .env.production.example
```

---

## Quick Reference

### Key TUI Commands

| Command | Purpose |
|---------|---------|
| `/init` | Initialize OpenCode, create AGENTS.md |
| `/undo` | Undo last change |
| `/redo` | Redo undone change |
| `/share` | Share conversation with team |
| `/connect` | Connect to LLM provider |
| `/help` | Show available commands |

### Key Keybinds

| Key | Action |
|-----|--------|
| `Tab` | Switch between Plan/Build modes |
| `@` | Mention/invoke a subagent |
| `Ctrl+C` | Cancel current operation |
| `Leader+Right` | Cycle through child sessions |
| `Leader+Left` | Cycle backward through sessions |

### CLI Commands

| Command | Purpose |
|---------|---------|
| `opencode` | Start TUI |
| `opencode run "prompt"` | Non-interactive single prompt |
| `opencode serve` | Start headless HTTP server |
| `opencode attach <url>` | Attach to running server |
| `opencode models` | List available models |
| `opencode auth login` | Configure provider credentials |
| `opencode mcp list` | List MCP servers |
| `opencode agent list` | List available agents |

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `OPENAI_API_KEY` | OpenAI API key |
| `OPENCODE_CONFIG` | Path to custom config file |
| `OPENCODE_AUTO_SHARE` | Automatically share sessions |
| `OPENCODE_DISABLE_AUTOUPDATE` | Disable automatic updates |

### Built-in Tools

| Tool | Purpose |
|------|---------|
| `bash` | Execute shell commands |
| `read` | Read file contents |
| `write` | Create/overwrite files |
| `edit` | Modify existing files |
| `grep` | Search file contents |
| `glob` | Find files by pattern |
| `list` | List directory contents |
| `webfetch` | Fetch web content |

---

## Summary Workflow

1. **Install OpenCode** and configure your LLM provider
2. **Clone & detach** the repository using bash commands through OpenCode
3. **Run `/init`** to analyze the project and create AGENTS.md
4. **Use Plan mode** (`Tab`) to analyze what needs trimming
5. **Create custom commands** in `.opencode/command/` for cleanup and deployment
6. **Switch to Build mode** (`Tab`) and execute your commands
7. **Add MCP servers** (Context7, gh_grep) for documentation lookups
8. **Create a deploy agent** in `.opencode/agent/` specialized for VPS configuration
9. **Run `/deploy-prep`** to generate deployment files
10. **Deploy** using the generated scripts and tools

---

## Additional Resources

- [OpenCode Documentation](https://opencode.ai/docs/)
- [OpenCode GitHub Repository](https://github.com/anomalyco/opencode)
- [Awesome OpenCode](https://github.com/awesome-opencode/awesome-opencode) - Community plugins, themes, and resources
- [OpenCode Discord](https://opencode.ai/discord) - Community support

---

*This guide was compiled from the official OpenCode documentation at opencode.ai/docs and community resources from awesome-opencode.*