# DNS and SSL Configuration

Guide to setting up domain names and automatic HTTPS for CBass.

## Overview

CBass uses Caddy as a reverse proxy, which automatically:
- Provisions SSL certificates from Let's Encrypt
- Redirects HTTP to HTTPS
- Routes subdomains to internal services

## DNS Setup

### Required A Records

Add these A records in your DNS provider (Route 53, Cloudflare, etc.):

| Hostname | Type | Value | TTL |
|----------|------|-------|-----|
| `cbass.space` | A | VPS_IP | 300 |
| `www.cbass.space` | A | VPS_IP | 300 |
| `n8n.cbass.space` | A | VPS_IP | 300 |
| `openwebui.cbass.space` | A | VPS_IP | 300 |
| `flowise.cbass.space` | A | VPS_IP | 300 |
| `supabase.cbass.space` | A | VPS_IP | 300 |
| `langfuse.cbass.space` | A | VPS_IP | 300 |
| `neo4j.cbass.space` | A | VPS_IP | 300 |
| `searxng.cbass.space` | A | VPS_IP | 300 |
| `kali.cbass.space` | A | VPS_IP | 300 |

### Verify DNS Propagation

Wait 5-10 minutes, then verify:

```bash
nslookup n8n.cbass.space
# Should return your VPS IP

dig n8n.cbass.space +short
# Should return your VPS IP
```

## SSL Configuration

### Automatic (Let's Encrypt)

Caddy handles SSL automatically. Just ensure:

1. DNS records point to your VPS
2. Ports 80 and 443 are open
3. `LETSENCRYPT_EMAIL` is set in `.env`

```bash
# .env
LETSENCRYPT_EMAIL=your@email.com
```

### Verify SSL

After deployment, Caddy logs show certificate status:

```bash
docker compose -p localai logs caddy | grep -i "certificate"
```

Test HTTPS:

```bash
curl -I https://n8n.cbass.space
# Should show HTTP/2 200
```

## Subdomain Routing

The `Caddyfile` maps subdomains to services:

| Subdomain | Service | Internal Port |
|-----------|---------|---------------|
| `cbass.space` | dashboard | 3000 |
| `n8n.cbass.space` | n8n | 5678 |
| `openwebui.cbass.space` | open-webui | 8080 |
| `flowise.cbass.space` | flowise | 3001 |
| `supabase.cbass.space` | kong | 8000 |
| `langfuse.cbass.space` | langfuse-web | 3000 |
| `neo4j.cbass.space` | neo4j | 7474 |
| `searxng.cbass.space` | searxng | 8080 |
| `kali.cbass.space` | kali | 6901 |

## Environment Variables

Set these in `.env` for production:

```bash
# === Hostnames (production only) ===
DASHBOARD_HOSTNAME=cbass.space
N8N_HOSTNAME=n8n.cbass.space
WEBUI_HOSTNAME=openwebui.cbass.space
FLOWISE_HOSTNAME=flowise.cbass.space
SUPABASE_HOSTNAME=supabase.cbass.space
LANGFUSE_HOSTNAME=langfuse.cbass.space
NEO4J_HOSTNAME=neo4j.cbass.space
SEARXNG_HOSTNAME=searxng.cbass.space
KALI_HOSTNAME=kali.cbass.space

# === SSL ===
LETSENCRYPT_EMAIL=your@email.com
```

## Adding New Subdomains

To add a new service subdomain:

1. **Add DNS record** pointing to your VPS IP

2. **Add to Caddyfile**:
   ```caddyfile
   {$NEW_SERVICE_HOSTNAME} {
       reverse_proxy new-service:port
   }
   ```

3. **Add to .env**:
   ```bash
   NEW_SERVICE_HOSTNAME=newservice.cbass.space
   ```

4. **Restart Caddy**:
   ```bash
   docker compose -p localai restart caddy
   ```

## Troubleshooting

### Certificate Not Issued

```bash
# Check Caddy logs
docker compose -p localai logs caddy

# Common causes:
# - DNS not propagated (wait longer)
# - Ports 80/443 blocked (check firewall)
# - Rate limited (wait 1 hour)
```

### ERR_SSL_PROTOCOL_ERROR

- DNS not yet propagated
- Caddy hasn't finished provisioning
- Wait 2-3 minutes and retry

### Mixed Content Warnings

Ensure all service URLs use HTTPS in configuration.

### Certificate Renewal

Caddy automatically renews certificates. No action needed.

To force renewal:

```bash
docker compose -p localai restart caddy
```

## Firewall Configuration

Required ports:

```bash
ufw allow 80/tcp    # HTTP (ACME challenge)
ufw allow 443/tcp   # HTTPS
ufw reload
```

## DNS Providers

### Route 53 (AWS)

1. Go to Route 53 > Hosted Zones > your domain
2. Click "Create Record"
3. Enter subdomain, select A record, paste IP

### Cloudflare

1. Go to DNS settings
2. Add A record
3. Set Proxy status to "DNS only" (orange cloud OFF)

### Namecheap

1. Go to Domain List > Manage
2. Advanced DNS > Add New Record
3. Type: A Record, Host: subdomain, Value: IP
