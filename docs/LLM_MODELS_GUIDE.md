# LLM Models Guide for CBass VPS

A guide to choosing and running local AI models on the CBass server using Ollama.

## What is Ollama?

Ollama is a tool that lets you run large language models (LLMs) locally on your own hardware - no cloud API needed. It's like having your own ChatGPT that runs on your server.

**Why run models locally?**
- Privacy - your data never leaves your server
- No API costs - run unlimited queries
- No rate limits - use it as much as you want
- Learning - understand how AI actually works

## Our VPS Specs

| Resource | Value | Impact on AI |
|----------|-------|--------------|
| **CPU** | 2 vCPUs (AMD EPYC 9354P) | Decent for small models |
| **RAM** | 7.8GB total (~2GB available) | Limits model size |
| **GPU** | None | CPU inference only (slower) |

### What This Means

- **No GPU** = Models run on CPU, which is 10-50x slower than GPU
- **Limited RAM** = Can only load models that fit in memory
- **2 vCPUs** = Parallel processing is limited

## Understanding Model Sizes

Models are measured in **parameters** (billions):

| Size | Parameters | RAM Needed | Speed on our VPS |
|------|------------|------------|------------------|
| Tiny | 1-2B | ~1-2GB | Fast (1-3 sec) |
| Small | 3-4B | ~2-3GB | Good (2-5 sec) |
| Medium | 7-8B | ~4-6GB | Slow (5-15 sec) |
| Large | 13B+ | ~8-16GB | Won't fit |

### Quantization (Making Models Smaller)

Models can be **quantized** (compressed) to use less RAM:

- `q4_K_M` = 4-bit quantization (good balance)
- `q8_0` = 8-bit (better quality, more RAM)
- `q2_K` = 2-bit (smaller, lower quality)

Example: `qwen2.5:7b-instruct-q4_K_M`
- `qwen2.5` = Model family
- `7b` = 7 billion parameters
- `instruct` = Fine-tuned to follow instructions
- `q4_K_M` = 4-bit quantization

## Currently Installed Models

```bash
# Check what's installed
docker exec ollama ollama list
```

| Model | Size | Purpose |
|-------|------|---------|
| `qwen2.5:7b-instruct-q4_K_M` | 4.7GB | Main chat/coding model |
| `nomic-embed-text` | 274MB | Text embeddings for RAG |

## Recommended Models for This VPS

### Best Overall: Qwen 2.5 (Already Installed!)

```bash
# You already have this one
docker exec ollama ollama pull qwen2.5:7b-instruct-q4_K_M
```

- Great at coding, math, and general knowledge
- Made by Alibaba, open source
- Best 7B model available right now

### For Faster Responses: Qwen 2.5 3B

```bash
docker exec ollama ollama pull qwen2.5:3b
```

- Same family, half the size
- Much faster responses
- Good for quick questions

### Alternative Options

```bash
# Meta's latest small model
docker exec ollama ollama pull llama3.2:3b

# Microsoft's efficient model
docker exec ollama ollama pull phi3:mini

# Google's compact model
docker exec ollama ollama pull gemma2:2b
```

## How to Use Ollama

### Pull (Download) a Model

```bash
docker exec ollama ollama pull qwen2.5:3b
```

### List Installed Models

```bash
docker exec ollama ollama list
```

### Run a Model Directly

```bash
docker exec -it ollama ollama run qwen2.5:7b
```

### Delete a Model

```bash
docker exec ollama ollama rm model-name
```

### Check What's Running

```bash
docker exec ollama ollama ps
```

## Using Models with n8n

In n8n, you can connect to Ollama using:

- **URL**: `http://ollama:11434`
- **Model**: `qwen2.5:7b-instruct-q4_K_M` (or any installed model)

The Ollama node in n8n lets you:
1. Send prompts to the model
2. Get AI-generated responses
3. Build automated AI workflows

## Using Models with Open WebUI

Open WebUI (https://openwebui.cbass.space) provides a ChatGPT-like interface:

1. Open WebUI connects to Ollama automatically
2. Select your model from the dropdown
3. Chat naturally like you would with ChatGPT

## Performance Expectations

With our current setup:

| Task | Model | Expected Time |
|------|-------|---------------|
| Short answer | qwen2.5:3b | 2-5 seconds |
| Short answer | qwen2.5:7b | 5-10 seconds |
| Code generation | qwen2.5:7b | 10-30 seconds |
| Long explanation | qwen2.5:7b | 15-45 seconds |

### Tips for Better Performance

1. **Use the smaller model** for simple questions
2. **Keep prompts concise** - shorter input = faster response
3. **One task at a time** - don't run multiple queries simultaneously
4. **Be patient** - CPU inference is slow but it works!

## Upgrading in the Future

If you want faster/better models:

| Upgrade | Benefit |
|---------|---------|
| **16GB RAM** | Run 13B models |
| **More vCPUs** | Slightly faster inference |
| **GPU (RTX 3060+)** | 10-50x faster, run 30B+ models |

Cloud GPU options:
- RunPod
- Vast.ai
- Lambda Labs

## Model Comparison Cheat Sheet

| Model | Strengths | Weaknesses |
|-------|-----------|------------|
| **Qwen 2.5** | Coding, math, multilingual | Larger size |
| **Llama 3.2** | General knowledge, chat | Less good at coding |
| **Phi-3** | Reasoning, efficiency | Smaller knowledge base |
| **Gemma 2** | Fast, efficient | Less capable overall |

## Embeddings Model (for RAG)

The `nomic-embed-text` model converts text into numbers (vectors) for:
- Semantic search
- RAG (Retrieval Augmented Generation)
- Finding similar documents

This is used by n8n and Flowise for the AI agent workflows that search through documents.

## Useful Commands Reference

```bash
# SSH into VPS
ssh cbass

# Enter Ollama container
docker exec -it ollama bash

# Check Ollama logs
docker logs ollama --tail 50

# Check memory usage
free -h

# Check if Ollama is responding
curl http://localhost:11434/api/tags
```

## Resources

- [Ollama Model Library](https://ollama.com/library) - Browse available models
- [Open WebUI Docs](https://docs.openwebui.com/) - Chat interface documentation
- [n8n AI Nodes](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.lmollama/) - Using Ollama in workflows

---

*Created for the CBass AI learning project - January 2026*
