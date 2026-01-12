---
description: Check status of all services in the stack
agent: build
---

Check the status of all services in the localai stack:

1. Run `docker compose -p localai ps` to list all containers
2. Check health status of each container
3. Identify any containers that are:
   - Not running
   - Unhealthy
   - Restarting repeatedly
4. For problematic containers, show last 20 lines of logs
5. Check if required ports are accessible:
   - n8n: 5678
   - Open WebUI: 8080 (internal)
   - Flowise: 3001
   - Ollama: 11434
   - Supabase Kong: 8000
   - SearXNG: 8080
   - Langfuse: 3000
   - Neo4j: 7474
6. Summarize overall stack health with service count and status
