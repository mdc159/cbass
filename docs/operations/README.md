# Operations Guide

Day-to-day operations for managing the CBass stack.

## Guides

| Guide | Content |
|-------|---------|
| [Common Tasks](./common-tasks.md) | Start, stop, restart, logs |
| [Backup & Restore](./backup-restore.md) | Data protection procedures |
| [Troubleshooting](./troubleshooting.md) | Known issues and fixes |
| [Security](./security.md) | Security checklist |

## Quick Reference

### Essential Commands

```bash
# Check status
docker compose -p localai ps

# View logs
docker compose -p localai logs -f <service-name>

# Restart service
docker compose -p localai restart <service-name>

# Stop all
docker compose -p localai down

# Start services
python start_services.py --profile gpu-nvidia --environment private --open-dashboard
```

### Service Health

| Symptom | Check | Fix |
|---------|-------|-----|
| Service not accessible | `docker compose -p localai ps` | Restart service |
| Slow responses | `docker stats` | Check resources |
| SSL errors | Caddy logs | Verify DNS, wait for cert |
| Database errors | Service logs | Check credentials |

### Log Locations

| Service | Command |
|---------|---------|
| All services | `docker compose -p localai logs -f` |
| Specific | `docker compose -p localai logs -f <service>` |
| Caddy SSL | `docker compose -p localai logs caddy \| grep -i cert` |
