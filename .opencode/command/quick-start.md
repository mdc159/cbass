---
description: Quick start guide for first-time setup
agent: build
---

Guide the user through first-time setup of CBass:

1. Check prerequisites:
   - Python installed (python --version)
   - Docker installed and running (docker --version)
   - Git installed (git --version)
2. Check if .env exists:
   - If not, guide to copy from env.example
   - List critical variables that MUST be set
3. Explain profile options:
   - cpu: For systems without GPU
   - gpu-nvidia: For NVIDIA GPUs
   - gpu-amd: For AMD GPUs (Linux only)
   - none: For Mac users running Ollama locally
4. Provide the startup command:
   - `python start_services.py --profile <chosen-profile>`
5. Explain what happens on first run:
   - Supabase repo clones automatically
   - Ollama pulls default models
   - All services start in sequence
6. Provide next steps:
   - Access n8n at http://localhost:5678
   - Access Open WebUI at http://localhost:3000
   - Set up credentials in n8n
