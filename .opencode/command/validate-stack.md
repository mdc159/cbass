---
description: Validate Docker Compose stack configuration
agent: build
---

Validate the Docker Compose stack:

1. Check docker-compose.yml syntax: `docker compose -p localai -f docker-compose.yml config`
2. Verify all service images are pullable
3. Check for port conflicts between services
4. Validate environment variable references in docker-compose.yml match env.example
5. Ensure volume mount paths are valid
6. Check Caddyfile syntax
7. Verify POSTGRES_PASSWORD in env.example has no @ symbol
8. Check that all *_HOSTNAME variables are properly formatted
9. Report any issues found with specific file:line references
