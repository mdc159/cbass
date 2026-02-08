# Caddy - Reverse Proxy

**URL**: N/A (infrastructure) | **Container**: caddy | **Port**: 80, 443

## Overview

Caddy is the reverse proxy that routes all external traffic to internal services. It automatically provisions SSL certificates from Let's Encrypt and enforces HTTPS.

## Architecture

```
Internet → :443 (Caddy) → Internal Services
                ↓
         ┌──────┼──────────┬──────────┐
         ↓      ↓          ↓          ↓
       n8n   flowise   open-webui   ...
      :5678   :3001      :8080
```

## How It Works

1. DNS points `*.cbass.space` to VPS IP
2. Caddy receives HTTPS requests on port 443
3. Reads hostname from request
4. Routes to appropriate internal service
5. Auto-provisions SSL via Let's Encrypt ACME

## Configuration

The `Caddyfile` defines routing:

```caddyfile
{$N8N_HOSTNAME} {
    reverse_proxy n8n:5678
}

{$FLOWISE_HOSTNAME} {
    reverse_proxy flowise:3001
    request_body {
        max_size 50MB
    }
}

{$WEBUI_HOSTNAME} {
    reverse_proxy open-webui:8080
}
```

## Adding a New Service

1. **Add DNS record** pointing subdomain to VPS

2. **Add to Caddyfile**:
   ```caddyfile
   {$NEW_SERVICE_HOSTNAME} {
       reverse_proxy service-container:port
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

## Common Tasks

### Check SSL Status

```bash
docker compose -p localai logs caddy | grep -i "certificate"
```

### Force Certificate Renewal

```bash
docker compose -p localai restart caddy
```

### View Access Logs

```bash
docker compose -p localai logs -f caddy
```

### Test Configuration

```bash
docker exec caddy caddy validate --config /etc/caddy/Caddyfile
```

## Troubleshooting

### Problem: SSL certificate not issued
**Causes & Solutions**:
- DNS not propagated → Wait, verify with `nslookup`
- Port 80 blocked → Open firewall: `ufw allow 80`
- Rate limited → Wait 1 hour, check Let's Encrypt status

### Problem: 502 Bad Gateway
**Solution**:
- Target service not running
- Check service: `docker compose -p localai ps`
- Check service logs

### Problem: Connection refused
**Solution**:
- Verify Caddy is running
- Check ports 80/443 are open
- Verify firewall: `ufw status`

### Problem: Mixed content warnings
**Solution**:
- Ensure all internal URLs use HTTPS
- Update application configurations

## Security Features

| Feature | Description |
|---------|-------------|
| Auto-HTTPS | All HTTP redirected to HTTPS |
| ACME | Automatic certificate provisioning |
| HSTS | HTTP Strict Transport Security |
| TLS 1.2+ | Modern TLS only |

## Environment Variables

```bash
# Required for production
LETSENCRYPT_EMAIL=your@email.com

# Service hostnames
DASHBOARD_HOSTNAME=cbass.space
N8N_HOSTNAME=n8n.cbass.space
WEBUI_HOSTNAME=openwebui.cbass.space
FLOWISE_HOSTNAME=flowise.cbass.space
# ... etc
```

## File Upload Limits

Some services need larger upload limits:

```caddyfile
{$FLOWISE_HOSTNAME} {
    reverse_proxy flowise:3001
    request_body {
        max_size 50MB
    }
}
```

## WebSocket Support

Caddy automatically handles WebSocket upgrades for:
- Open WebUI streaming
- n8n real-time updates
- Supabase Realtime

## Local Development

In `private` mode, Caddy is not used - services expose ports directly:
- n8n: http://localhost:5678
- Flowise: http://localhost:3001
- etc.

## Certificate Storage

Certificates stored in Docker volume:

```bash
docker volume inspect localai_caddy_data
# Contains: /data/caddy/certificates/
```

## Caddyfile Syntax

```caddyfile
# Basic reverse proxy
example.com {
    reverse_proxy backend:8080
}

# With options
example.com {
    reverse_proxy backend:8080 {
        header_up X-Forwarded-Proto {scheme}
    }
    encode gzip
    log {
        output file /var/log/caddy/access.log
    }
}

# Redirect
www.example.com {
    redir https://example.com{uri}
}
```

## Resources

- [Caddy Documentation](https://caddyserver.com/docs/)
- [Caddyfile Reference](https://caddyserver.com/docs/caddyfile)
- [Let's Encrypt](https://letsencrypt.org/)
