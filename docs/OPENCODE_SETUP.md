# OpenCode Setup for CBass VPS

Complete guide for installing and integrating OpenCode with the CBass AI stack - designed for learning and development.

## Why OpenCode for Learning AI?

OpenCode is an excellent teaching tool because:
- **Interactive AI assistance** - Learn by doing with AI guidance
- **Safe experimentation** - Undo/redo changes easily
- **Built-in documentation** - AGENTS.md provides project context
- **Command automation** - Custom workflows for common tasks
- **Multi-agent system** - Understand how AI agents collaborate

## Installation on VPS

### Option 1: Quick Install (Recommended)

```bash
# SSH into your VPS
ssh root@your-vps-ip

# Install OpenCode
curl -fsSL https://opencode.ai/install | bash

# Verify installation
opencode --version
```

### Option 2: NPM Install

```bash
# Install Node.js if not present
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# Install OpenCode globally
npm install -g opencode-ai

# Verify
opencode --version
```

## Remote Access Setup

### OpenCode Web Interface

OpenCode has a **web interface** that allows remote access from any browser:

```bash
# On VPS: Start OpenCode web server
cd /opt/cbass
opencode web --port 4096 --hostname 0.0.0.0

# Access from your local machine
# http://your-vps-ip:4096
```

### Secure with Caddy (Recommended)

Add OpenCode to your Caddyfile for HTTPS access:

```caddy
# Add to Caddyfile
{$OPENCODE_HOSTNAME} {
    reverse_proxy localhost:4096
}
```

Then set in `.env`:
```bash
OPENCODE_HOSTNAME=opencode.yourdomain.com
```

Now access at: `https://opencode.yourdomain.com`

### Systemd Service (Auto-start)

Create `/etc/systemd/system/opencode-web.service`:

```ini
[Unit]
Description=OpenCode Web Interface
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/cbass
ExecStart=/usr/local/bin/opencode web --port 4096 --hostname 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
systemctl enable opencode-web
systemctl start opencode-web
systemctl status opencode-web
```

## Integration with CBass Services

### 1. n8n Integration

**Use Case**: Automate OpenCode commands from n8n workflows

Create an n8n workflow that:
- Monitors GitHub for new issues
- Uses OpenCode CLI to analyze and fix issues
- Creates pull requests automatically

**Example n8n Execute Command node:**
```bash
cd /opt/cbass && opencode run "Analyze the error in logs and suggest a fix"
```

### 2. Open WebUI Integration

**Use Case**: Chat with OpenCode through Open WebUI

Create a custom function in Open WebUI that calls OpenCode:

```python
# File: opencode_pipe.py
"""
title: OpenCode Integration
author: Your Name
version: 0.1.0
"""

import subprocess
import json

class Pipe:
    def __init__(self):
        self.type = "pipe"
        self.id = "opencode_pipe"
        self.name = "OpenCode Assistant"
    
    async def pipe(self, body: dict, __user__: dict = None):
        messages = body.get("messages", [])
        if messages:
            question = messages[-1]["content"]
            
            # Run OpenCode command
            result = subprocess.run(
                ["opencode", "run", question],
                cwd="/opt/cbass",
                capture_output=True,
                text=True
            )
            
            response = result.stdout if result.returncode == 0 else result.stderr
            body["messages"].append({"role": "assistant", "content": response})
        
        return body
```

### 3. Custom OpenCode Commands for CBass

We've already created these commands - here's how to use them:

```bash
# Check environment configuration
opencode run "/env-check"

# Validate Docker Compose stack
opencode run "/validate-stack"

# Check service health
opencode run "/service-status"

# Comprehensive health check
opencode run "/stack-health"

# Troubleshoot issues
opencode run "/troubleshoot"

# Quick start guide
opencode run "/quick-start"

# Prepare for deployment
opencode run "/deploy-prep"
```

### 4. Learning Workflows

**For Sebastian - Structured Learning Path:**

#### Week 1: Understanding the Stack
```bash
# Learn about the project
opencode run "Explain what each service in CBass does"

# Explore the codebase
opencode run "Show me how n8n connects to Ollama"

# Understand Docker Compose
opencode run "Explain the docker-compose.yml structure"
```

#### Week 2: Making Changes
```bash
# Safe experimentation
opencode run "Add a new environment variable for a custom service"

# If something breaks
opencode run "/undo"

# Learn from mistakes
opencode run "Why did that change break the stack?"
```

#### Week 3: Automation
```bash
# Create custom commands
opencode run "Create a command to backup all Docker volumes"

# Build workflows
opencode run "Create an n8n workflow that monitors system health"
```

## Educational Features

### 1. Interactive Learning Mode

Create a learning command:

```bash
# .opencode/command/learn.md
---
description: Interactive learning assistant for CBass
agent: build
---

You are a patient teacher helping someone learn about self-hosted AI stacks.

When asked a question:
1. Explain the concept clearly
2. Show relevant code examples from this project
3. Suggest hands-on exercises
4. Provide resources for deeper learning

Focus on:
- Docker and containerization
- AI/LLM concepts (Ollama, embeddings, RAG)
- Workflow automation (n8n)
- Database concepts (Supabase, Qdrant, Neo4j)
- Web development (APIs, reverse proxies)
```

Usage:
```bash
opencode run "/learn What is RAG and how does n8n implement it?"
```

### 2. Safe Experimentation Environment

Create a sandbox command:

```bash
# .opencode/command/sandbox.md
---
description: Create a safe environment for experimentation
agent: build
---

Create a sandbox environment for testing:

1. Create a new branch: git checkout -b sandbox/experiment
2. Document what we're about to try
3. Make the changes
4. Test thoroughly
5. If successful: merge back
6. If failed: discard and explain what went wrong
```

### 3. Progress Tracking

Create a learning journal:

```bash
# .opencode/command/journal.md
---
description: Track learning progress and insights
agent: build
---

Maintain a learning journal at docs/learning-journal.md:

1. Date and topic
2. What was learned
3. Code examples tried
4. Challenges encountered
5. Solutions found
6. Next steps

Format each entry clearly and encourage reflection.
```

## Multi-User Setup

### For Father-Son Collaboration:

#### Option 1: Shared Session
```bash
# Dad starts session on VPS
opencode web --port 4096 --hostname 0.0.0.0

# Sebastian connects from his computer
# Both can see the same session in real-time
```

#### Option 2: Separate Workspaces
```bash
# Create user directories
mkdir -p /opt/cbass/workspaces/dad
mkdir -p /opt/cbass/workspaces/sebastian

# Dad's session
cd /opt/cbass/workspaces/dad
opencode web --port 4096

# Sebastian's session
cd /opt/cbass/workspaces/sebastian
opencode web --port 4097
```

Add both to Caddyfile:
```caddy
opencode-dad.yourdomain.com {
    reverse_proxy localhost:4096
}

opencode-sebastian.yourdomain.com {
    reverse_proxy localhost:4097
}
```

## Useful MCP Servers for Learning

Add these to `opencode.json`:

```json
{
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
    "docker": {
      "type": "local",
      "command": "docker-mcp",
      "enabled": true
    }
  }
}
```

## Learning Resources Integration

### 1. Documentation Command

```bash
# .opencode/command/docs.md
---
description: Search and explain documentation
agent: build
---

Help find and explain documentation:

1. Use context7 to search official docs for:
   - Docker
   - n8n
   - Supabase
   - Ollama
2. Provide clear explanations
3. Show relevant examples from CBass
4. Suggest related topics to explore
```

### 2. Example Finder

```bash
# .opencode/command/examples.md
---
description: Find real-world examples on GitHub
agent: build
---

Use gh_grep to find real-world examples:

1. Search GitHub for similar implementations
2. Show code snippets
3. Explain how they work
4. Suggest how to adapt for CBass
```

## Best Practices for Teaching

### 1. Start Simple
```bash
# Begin with read-only exploration
opencode run "Show me the project structure"
opencode run "Explain what start_services.py does"
```

### 2. Gradual Complexity
```bash
# Move to safe modifications
opencode run "Add a comment explaining this function"
opencode run "Create a new environment variable"
```

### 3. Real Projects
```bash
# Build something useful
opencode run "Create a health monitoring dashboard"
opencode run "Add a new AI model to Ollama"
```

### 4. Learn from Mistakes
```bash
# When things break
opencode run "/troubleshoot"
opencode run "Explain what went wrong and how to fix it"
opencode run "/undo"
```

## Security Considerations

### For Production Learning Environment:

1. **Firewall Rules**:
```bash
# Only allow OpenCode web access from specific IPs
ufw allow from YOUR_HOME_IP to any port 4096
```

2. **Authentication**:
```bash
# Use Caddy basic auth
opencode.yourdomain.com {
    basicauth {
        sebastian <hashed-password>
    }
    reverse_proxy localhost:4096
}
```

3. **Read-Only Mode** (for initial learning):
```json
{
  "permission": {
    "edit": "ask",
    "bash": "ask",
    "write": "ask"
  }
}
```

## Monitoring OpenCode Usage

### View OpenCode Logs
```bash
# If running as systemd service
journalctl -u opencode-web -f

# View session history
opencode stats
```

### Track Learning Progress
```bash
# Export sessions for review
opencode export > learning-session-$(date +%Y%m%d).json
```

## Quick Reference

### Essential Commands
```bash
# Start OpenCode web interface
opencode web --port 4096 --hostname 0.0.0.0

# Run a command
opencode run "your question or command"

# Use a custom command
opencode run "/env-check"

# View help
opencode --help

# Check status
opencode stats
```

### For Sebastian's Learning
```bash
# Daily learning routine
opencode run "/learn What should I learn today?"
opencode run "/journal Document today's learning"

# When stuck
opencode run "/troubleshoot"
opencode run "Explain this error: [paste error]"

# Experimentation
opencode run "/sandbox Try adding a new service"
```

## Next Steps

1. **Install OpenCode** on VPS
2. **Set up web interface** with Caddy
3. **Create learning commands** (learn, journal, sandbox)
4. **Start with basics** - explore the codebase
5. **Build projects** - create something useful
6. **Share knowledge** - document what you learn

## Support Resources

- **OpenCode Docs**: https://opencode.ai/docs
- **CBass AGENTS.md**: Project-specific knowledge
- **n8n Community**: https://community.n8n.io
- **Docker Docs**: https://docs.docker.com
- **This Repository**: https://github.com/mdc159/cbass

---

**Remember**: The best way to learn is by doing. OpenCode makes it safe to experiment, easy to undo mistakes, and fun to explore AI-powered development!
