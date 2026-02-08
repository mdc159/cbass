# Security Checklist

Security considerations for the CBass stack.

## Production Security

### Essential Checklist

- [ ] **HTTPS enforced** - All traffic through Caddy with auto-TLS
- [ ] **Firewall configured** - Only ports 22, 80, 443 open
- [ ] **Strong passwords** - All services use strong, unique passwords
- [ ] **.env secured** - Never committed to git, restricted file permissions
- [ ] **SSH key auth** - Password auth disabled on VPS
- [ ] **Regular updates** - Docker images and system packages updated

### Firewall Configuration

```bash
# Ubuntu UFW
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP (for ACME)
ufw allow 443/tcp   # HTTPS
ufw enable
```

### SSH Hardening

In `/etc/ssh/sshd_config`:
```
PasswordAuthentication no
PermitRootLogin prohibit-password
PubkeyAuthentication yes
```

Restart: `systemctl restart sshd`

## Secrets Management

### .env File Security

```bash
# Restrict permissions
chmod 600 .env

# Never commit
# .env is in .gitignore
```

### Critical Secrets

| Variable | Purpose | Generation |
|----------|---------|------------|
| `N8N_ENCRYPTION_KEY` | Encrypts n8n credentials | `openssl rand -hex 32` |
| `POSTGRES_PASSWORD` | Database access | Strong random password |
| `JWT_SECRET` | Supabase auth tokens | `openssl rand -hex 32` |
| `ENCRYPTION_KEY` | Langfuse encryption | `openssl rand -hex 32` |
| `VNC_PW` | Kali desktop access | Strong password |

### Password Requirements

- Minimum 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- **Never use `@` in POSTGRES_PASSWORD** (breaks URI parsing)

## Network Security

### Internal Communication

All services communicate on Docker network `localai_default`:
- Not exposed to internet
- Container names used for addressing
- No authentication needed internally

### External Access

Only through Caddy reverse proxy:
- HTTPS enforced
- Auto-redirect HTTP → HTTPS
- Valid SSL certificates

### Service Authentication

| Service | Authentication |
|---------|----------------|
| n8n | User accounts (first user = admin) |
| Open WebUI | User accounts |
| Flowise | Optional username/password |
| Supabase | Dashboard username/password |
| Neo4j | Username/password from NEO4J_AUTH |
| Langfuse | User accounts |
| Kali | VNC password |

## Data Protection

### Sensitive Data Locations

| Data | Location | Protection |
|------|----------|------------|
| Credentials | n8n volume | Encrypted with N8N_ENCRYPTION_KEY |
| User data | PostgreSQL | Database authentication |
| API keys | .env | File permissions |
| Chat history | Open WebUI volume | User authentication |

### Backup Security

- Store backups securely (encrypted, offsite)
- Include .env in secure backup (not in regular backup)
- Test restore procedures regularly

## Service-Specific Security

### n8n

- First user becomes admin
- Use webhook authentication where possible
- Don't expose internal credentials in workflows
- Review workflows for data leakage

### Supabase

- Change default credentials
- Use row-level security (RLS) for tables
- Don't expose SERVICE_ROLE_KEY to clients
- Use ANON_KEY for client-side access

### Ollama

- Internal only (no direct external access)
- Consider request rate limiting
- Be cautious with model capabilities

### Kali

- Strong VNC password required
- Only use for authorized testing
- Don't expose to public without authentication
- Keep container updated

## Monitoring

### Log Monitoring

```bash
# Watch for errors
docker compose -p localai logs -f | grep -i error

# Check Caddy access logs
docker compose -p localai logs caddy
```

### Resource Monitoring

```bash
# Container resources
docker stats

# System resources
htop
df -h
```

### Failed Login Attempts

Check service logs for authentication failures.

## Updates

### Keep Systems Updated

```bash
# System packages
apt update && apt upgrade -y

# Docker images
docker compose -p localai pull
python3 start_services.py --profile <profile> --environment public
```

### Security Patches

- Subscribe to security advisories for:
  - Docker
  - Individual services (n8n, Supabase, etc.)
  - Ubuntu/Linux

## Incident Response

### If Compromised

1. **Isolate**: Disconnect from network
2. **Preserve**: Don't delete logs
3. **Investigate**: Check access logs, running processes
4. **Recover**: Restore from clean backup
5. **Harden**: Fix vulnerability, rotate all credentials

### Credential Rotation

If credentials may be compromised:

1. Generate new secrets
2. Update .env
3. Restart affected services
4. Update any external integrations

## Development vs Production

### Development (Private Mode)

- Ports exposed locally for debugging
- OK for trusted local network
- Don't expose to internet

### Production (Public Mode)

- Only 80/443 through Caddy
- All authentication enabled
- Strong passwords required
- Regular security updates

## Security Resources

- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [n8n Security Docs](https://docs.n8n.io/hosting/security/)
- [Supabase Security](https://supabase.com/docs/guides/auth/row-level-security)
