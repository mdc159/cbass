# CBass Setup Session - January 12, 2026

## Overview

This document captures the setup and troubleshooting session for the CBass AI stack deployed on Hostinger VPS.

## Infrastructure

- **Domain**: cbass.space (managed at Amazon Route 53)
- **VPS**: Hostinger (IP: 191.101.0.164, hostname: sebastian)
- **SSH Access**: `ssh cbass` (key: `~/.ssh/cbass_vps`)
- **Deployment Path**: `/opt/cbass`

## Services Deployed

| Service | URL | Status |
|---------|-----|--------|
| Dashboard | https://cbass.space | Running |
| n8n | https://n8n.cbass.space | Running |
| Open WebUI | https://openwebui.cbass.space | Running |
| Flowise | https://flowise.cbass.space | Running |
| Supabase | https://supabase.cbass.space | Running |
| Langfuse | https://langfuse.cbass.space | Running |
| Neo4j | https://neo4j.cbass.space | Running |
| SearXNG | https://searxng.cbass.space | Running |

## Issues Resolved

### 1. SSL Certificates Not Provisioning

**Problem**: Several services showed SSL errors because Let's Encrypt certificates failed to provision.

**Cause**: DNS records hadn't fully propagated when Caddy first started.

**Solution**: Restarted Caddy to retry certificate provisioning:
```bash
ssh cbass "docker restart caddy"
```

### 2. Missing Services in Caddyfile

**Problem**: SearXNG and www redirect weren't configured.

**Solution**: Updated `/opt/cbass/Caddyfile` to add:
```
# SearXNG
{$SEARXNG_HOSTNAME} {
    reverse_proxy searxng:8080
}

# WWW redirect
www.cbass.space {
    redir https://cbass.space{uri} permanent
}
```

Then reloaded Caddy:
```bash
ssh cbass "docker exec caddy caddy reload --config /etc/caddy/Caddyfile"
```

### 3. Dashboard Admin User Creation

**Problem**: No users existed in the dashboard's Supabase auth.

**Solution**: Created admin user via Supabase Admin API:
```bash
ssh cbass 'SERVICE_KEY=$(grep SERVICE_ROLE_KEY /opt/cbass/.env | cut -d= -f2) && \
curl -X POST "https://supabase.cbass.space/auth/v1/admin/users" \
  -H "Authorization: Bearer $SERVICE_KEY" \
  -H "apikey: $SERVICE_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"admin@cbass.space\", \"password\": \"[FROM_ENV]\", \"email_confirm\": true}"'
```

### 4. Dashboard Service Cards Showing Static Status

**Problem**: Service status indicators were hardcoded (not reflecting actual service health).

**Solution**: Implemented dynamic health checks:

1. Created `/opt/cbass/dashboard/app/api/health/route.ts` - API endpoint that pings each service
2. Updated `/opt/cbass/dashboard/app/dashboard/page.tsx` - Fetches status on load + polls every 30 seconds
3. Rebuilt dashboard: `docker compose -p localai build dashboard`
4. Restarted: `docker compose -p localai up -d dashboard`

### 5. Google Safe Browsing "Dangerous Site" Warning

**Problem**: Chrome displayed "Dangerous site" warning for n8n.cbass.space.

**Cause**: Likely the Hostinger VPS IP (191.101.0.164) had bad reputation from previous tenant, or Google's automated systems flagged n8n's login page as potentially deceptive.

**Steps Taken**:

1. Submitted false positive report at: https://safebrowsing.google.com/safebrowsing/report_error/

2. Set up Google Search Console for n8n.cbass.space:
   - Added TXT record in Route 53 for domain verification:
     ```
     n8n.cbass.space  TXT  "google-site-verification=OU_KgZRYAn8JCKClg051r0kqs8WS56vtIz6-qR529H0"
     ```
   - Verified ownership

3. Requested security review in Search Console with explanation that it's a legitimate self-hosted n8n instance

**Status**: Awaiting Google review (typically 24-72 hours)

## Credentials Reference

| Service | Username/Email | Notes |
|---------|---------------|-------|
| CBass Dashboard | admin@cbass.space | Password in .env (DASHBOARD_PASSWORD) |
| Neo4j | neo4j | Password in .env (NEO4J_AUTH) |
| Supabase Postgres | postgres | Password in .env (POSTGRES_PASSWORD) |
| n8n | (create on first visit) | First user becomes owner |
| Open WebUI | (create on first visit) | First user becomes admin |
| Langfuse | (create on first visit) | First user becomes admin |
| Flowise | (no auth) | Currently open |

## Useful Commands

```bash
# SSH into VPS
ssh cbass

# Check all container status
docker ps --format "table {{.Names}}\t{{.Status}}"

# View logs for a service
docker logs [container-name] --tail 50

# Restart a service
docker compose -p localai restart [service-name]

# Rebuild and restart dashboard after code changes
cd /opt/cbass && docker compose -p localai build dashboard && docker compose -p localai up -d dashboard

# Check health API
curl https://cbass.space/api/health | jq .
```

## Files Modified

- `/opt/cbass/Caddyfile` - Added SearXNG and www redirect
- `/opt/cbass/dashboard/app/api/health/route.ts` - Created health check API
- `/opt/cbass/dashboard/app/dashboard/page.tsx` - Dynamic status fetching
- Route 53: Added TXT record for Google Search Console verification

## Next Steps

- [ ] Wait for Google Safe Browsing review to complete
- [ ] Create accounts on n8n, Open WebUI, and Langfuse
- [ ] Consider requesting new IP from Hostinger if Safe Browsing issues persist
- [ ] Optionally enable authentication on Flowise
