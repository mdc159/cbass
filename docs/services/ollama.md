# Ollama - Local LLM Inference

**URL**: Internal only | **Container**: ollama | **Port**: 11434

## Overview

Ollama runs large language models locally. It provides the inference backend for Open WebUI, n8n, and Flowise, enabling AI capabilities without external API calls.

## Quick Access

| Environment | URL |
|-------------|-----|
| Internal | http://ollama:11434 |
| Local (dev) | http://localhost:11434 |

Ollama has no web UI - access via API or other services.

## First-Time Setup

On first startup, Ollama automatically pulls:
- `qwen2.5:7b-instruct-q4_K_M` (~4GB) - General purpose
- `nomic-embed-text` (~275MB) - Embeddings

## Common Tasks

### List Models

```bash
docker exec -it ollama ollama list
```

### Pull a New Model

```bash
docker exec -it ollama ollama pull llama3.1
docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama pull codellama
```

### Remove a Model

```bash
docker exec -it ollama ollama rm modelname
```

### Test a Model

```bash
docker exec -it ollama ollama run llama3.1 "What is DNA?"
```

### Check Model Info

```bash
docker exec -it ollama ollama show llama3.1
```

## Recommended Models

| Model | Size | Use Case |
|-------|------|----------|
| `qwen2.5:7b-instruct` | 4GB | General purpose (default) |
| `llama3.1:8b` | 4.7GB | High quality general |
| `llama3.2:3b` | 2GB | Fast, lower memory |
| `codellama:7b` | 3.8GB | Code generation |
| `nomic-embed-text` | 275MB | Embeddings (required for RAG) |
| `mixtral:8x7b` | 26GB | Most capable (needs 32GB RAM) |

## Integration with Other Services

| Service | Configuration |
|---------|---------------|
| Open WebUI | Automatic (same Docker network) |
| n8n | Credential: Host `ollama`, Port `11434` |
| Flowise | Base URL: `http://ollama:11434` |

## GPU Configuration

### NVIDIA GPU

Start with:
```bash
python start_services.py --profile gpu-nvidia
```

Verify GPU access:
```bash
docker exec -it ollama nvidia-smi
```

### AMD GPU (Linux only)

Start with:
```bash
python start_services.py --profile gpu-amd
```

### CPU Only

Start with:
```bash
python start_services.py --profile cpu
```

### Mac Users

Docker on Mac cannot access GPU. Options:
1. Run Ollama outside Docker (locally)
2. Use `--profile none` and external API
3. Accept slower CPU inference

If running Ollama locally on Mac:
```bash
# In .env or docker-compose
OLLAMA_HOST=host.docker.internal:11434
```

## Troubleshooting

### Problem: Model download stuck
**Solution**:
- Check disk space: `df -h`
- Restart download: `docker exec -it ollama ollama pull modelname`
- Check network connectivity

### Problem: Out of memory
**Solution**:
- Use smaller model (3B instead of 7B)
- Close other applications
- Increase Docker memory allocation
- Use quantized models (q4_K_M)

### Problem: Slow inference
**Solution**:
- Verify GPU is being used
- Use GPU profile
- Use smaller/quantized models
- Check `docker stats` for resource usage

### Problem: Model not found in Open WebUI
**Solution**:
- Pull model first: `docker exec -it ollama ollama pull modelname`
- Refresh Open WebUI page
- Check Ollama is running

## API Usage

Ollama provides an OpenAI-compatible API:

```bash
# Generate completion
curl http://localhost:11434/api/generate \
  -d '{"model": "llama3.1", "prompt": "What is photosynthesis?"}'

# Chat
curl http://localhost:11434/api/chat \
  -d '{"model": "llama3.1", "messages": [{"role": "user", "content": "Hello"}]}'

# List models
curl http://localhost:11434/api/tags
```

## Biology Applications

| Use Case | Recommended Model |
|----------|-------------------|
| General biology Q&A | llama3.1:8b |
| Quick answers | llama3.2:3b |
| Code for data analysis | codellama:7b |
| Embeddings for RAG | nomic-embed-text |

## Data Storage

Models stored in Docker volume:

```bash
docker volume inspect localai_ollama
# Typically: /var/lib/docker/volumes/localai_ollama/_data
```

## Resources

- [Ollama Documentation](https://ollama.ai/)
- [Ollama Model Library](https://ollama.ai/library)
- [Ollama GitHub](https://github.com/ollama/ollama)
