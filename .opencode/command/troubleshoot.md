---
description: Troubleshoot common issues with the stack
agent: build
---

Diagnose and provide solutions for common CBass issues:

1. Check for common problems:
   - Supabase pooler restarting (check GitHub issue #30210)
   - SearXNG restarting (check permissions: chmod 755 searxng)
   - @ symbol in POSTGRES_PASSWORD
   - Port conflicts with existing services
   - Docker daemon not running
   - Insufficient disk space
2. For each running container, check:
   - Exit codes if stopped
   - Error messages in logs
   - Resource usage (CPU, memory)
3. Check Docker network:
   - Verify localai network exists
   - Check service connectivity
4. Provide specific solutions based on errors found
5. Reference AGENTS.md NOTES section for known issues
6. Suggest relevant commands to fix issues
