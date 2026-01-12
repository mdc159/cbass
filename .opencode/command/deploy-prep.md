---
description: Prepare project for VPS deployment
agent: deploy
---

Prepare this Docker Compose project for VPS deployment:

1. Verify all required environment variables are documented in env.example
2. Check Caddyfile has correct reverse proxy routes for all services
3. Verify docker-compose.yml has proper health checks
4. Create/update deploy.sh script that handles:
   - Pulling latest code from git
   - Running start_services.py with appropriate profile
   - Verifying all containers are healthy
5. Document any manual DNS setup required (A records for subdomains)
6. Check firewall rules (ports 80, 443 only for public deployment)
7. Verify no @ symbol in POSTGRES_PASSWORD (breaks connection strings)
