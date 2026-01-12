---
description: Comprehensive health check of the entire stack
agent: build
---

Perform a comprehensive health check of the CBass stack:

1. Check if Docker is running
2. Verify docker-compose.yml syntax is valid
3. Check if any containers are running: `docker compose -p localai ps`
4. For each service, check:
   - Container status (running/stopped/restarting)
   - Health check status (if configured)
   - Recent logs for errors (last 50 lines)
   - Port accessibility
5. Check disk space for Docker volumes
6. Verify network connectivity between services
7. Check if Supabase directory exists and is up to date
8. Report overall stack health with recommendations
