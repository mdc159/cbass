# Open WebUI - Chat Interface

**URL**: https://openwebui.cbass.space | **Container**: open-webui | **Port**: 8080

## Overview

Open WebUI provides a ChatGPT-style interface for interacting with local LLMs via Ollama. It supports multi-model conversations, document uploads, and custom functions for extending capabilities.

## Quick Access

| Environment | URL |
|-------------|-----|
| Production | https://openwebui.cbass.space |
| Local | http://localhost:8080 |

## First-Time Setup

1. Navigate to Open WebUI URL
2. Click "Sign up" to create account (first user becomes admin)
3. Ollama connection is pre-configured

## Common Tasks

### Start a Chat

1. Select model from dropdown
2. Type message and press Enter
3. View response with streaming

### Upload Documents

1. Click paperclip icon in chat
2. Select PDF, TXT, or other document
3. Chat about document contents

### Change Models

1. Click model name in chat header
2. Select different model
3. Previous context remains

### Pull New Models

```bash
# From host machine
docker exec -it ollama ollama pull llama3.1

# List available models
docker exec -it ollama ollama list
```

## n8n Integration (n8n_pipe)

Route messages through n8n for advanced AI agents:

1. **In n8n**: Import and activate a webhook workflow
2. **Copy** the Production webhook URL
3. **In Open WebUI**:
   - Go to Workspace > Functions > Add Function
   - Paste code from `n8n_pipe.py`
   - Click gear icon, set `n8n_url` to webhook URL
   - Enable the function
4. **Use**: Select n8n_pipe from model dropdown

Also available at: [openwebui.com/f/coleam/n8n_pipe](https://openwebui.com/f/coleam/n8n_pipe/)

## Integration with Other Services

| Connects To | Purpose |
|-------------|---------|
| Ollama | LLM inference (automatic) |
| n8n | Advanced agents via n8n_pipe |

## Admin Features

Access admin panel (admin users only):

- User management
- Model settings
- System configuration
- Usage statistics

## Troubleshooting

### Problem: No models available
**Solution**:
- Verify Ollama is running: `docker compose -p localai ps ollama`
- Check Ollama has models: `docker exec -it ollama ollama list`
- Pull a model: `docker exec -it ollama ollama pull llama3.1`

### Problem: Slow responses
**Solution**:
- Use GPU profile for faster inference
- Use smaller models (3B instead of 7B)
- Check system resources: `docker stats`

### Problem: Connection refused
**Solution**:
- Ollama configured automatically via environment
- Verify Ollama container is healthy
- Check logs: `docker compose -p localai logs ollama`

### Problem: Document upload fails
**Solution**:
- Check file size limits
- Verify supported format (PDF, TXT, MD)
- Check container logs for errors

## Biology Applications

| Use Case | How To |
|----------|--------|
| Study Q&A | Upload biology textbook PDF, ask questions |
| Concept explanation | Ask to explain complex topics simply |
| Quiz prep | Request practice questions on topics |
| Paper summarization | Upload research paper, request summary |
| Lab report writing | Discuss experiment, draft report |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Enter | Send message |
| Shift+Enter | New line |
| Ctrl+/ | Focus chat input |
| Esc | Cancel generation |

## Data Storage

User data and chat history stored in Docker volume:

```bash
docker volume inspect localai_open-webui
```

## Resources

- [Open WebUI Documentation](https://docs.openwebui.com/)
- [Open WebUI GitHub](https://github.com/open-webui/open-webui)
- [Open WebUI Functions](https://openwebui.com/functions/)
