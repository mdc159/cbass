# CBass VPS Deployment Guide

Complete guide for deploying CBass to a cloud VPS.

## Prerequisites

### VPS Requirements
- **OS**: Ubuntu 22.04 LTS (recommended)
- **RAM**: Minimum 8GB (16GB+ recommended for GPU workloads)
- **Storage**: 50GB+ SSD
- **CPU**: 4+ cores recommended
- **GPU**: Optional (NVIDIA or AMD for Ollama acceleration)

### Software Requirements
- Docker & Docker Compose
- Python 3.8+
- Git
- UFW (firewall)

## Quick Deployment

### 1. Provision VPS

Choose a provider:
- **DigitalOcean**: GPU Droplets available
- **Hetzner**: Cost-effective, good performance
- **Linode**: Reliable, good support
- **AWS Lightsail**: Easy to use, AWS ecosystem

### 2. Initial Server Setup

```bash
# SSH into your VPS
ssh root@your-vps-ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose (if not included)
apt install docker-compose-plugin -y

# Install Python and Git
apt install python3 python3-pip git -y

# Configure firewall
ufw allow 22
ufw allow 80
ufw allow 443
ufw enable
```

### 3. Deploy CBass

```bash
# Download and run deployment script
curl -fsSL https://raw.githubusercontent.com/mdc159/cbass/master/deploy.sh -o deploy.sh
chmod +x deploy.sh

# Run deployment (will prompt for configuration)
sudo ./deploy.sh
```

### 4. Configure Environment

Edit `.env` file at `/opt/cbass/.env`:

```bash
cd /opt/cbass
nano .env
```

**Required Variables:**
```bash
# N8N Configuration
N8N_ENCRYPTION_KEY=<generate-random-32-char-string>
N8N_USER_MANAGEMENT_JWT_SECRET=<generate-random-32-char-string>

# Supabase Secrets
POSTGRES_PASSWORD=<strong-password-no-@-symbol>
JWT_SECRET=<generate-random-32-char-string>
ANON_KEY=<generate-from-supabase-docs>
SERVICE_ROLE_KEY=<generate-from-supabase-docs>
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=<strong-password>
POOLER_TENANT_ID=<generate-uuid>

# Neo4j
NEO4J_AUTH=neo4j/<strong-password>

# Langfuse
CLICKHOUSE_PASSWORD=<strong-password>
MINIO_ROOT_PASSWORD=<strong-password>
LANGFUSE_SALT=<generate-random-string>
NEXTAUTH_SECRET=<generate-random-32-char-string>
ENCRYPTION_KEY=<generate-random-32-char-string>
```

**Production Variables (for custom domains):**
```bash
# Caddy Config - Set these for automatic HTTPS
N8N_HOSTNAME=n8n.yourdomain.com
WEBUI_HOSTNAME=openwebui.yourdomain.com
FLOWISE_HOSTNAME=flowise.yourdomain.com
SUPABASE_HOSTNAME=supabase.yourdomain.com
LANGFUSE_HOSTNAME=langfuse.yourdomain.com
NEO4J_HOSTNAME=neo4j.yourdomain.com
LETSENCRYPT_EMAIL=your-email@example.com
```

### 5. Configure DNS

For each hostname above, create an **A record** pointing to your VPS IP:

```
n8n.yourdomain.com        A    your-vps-ip
openwebui.yourdomain.com  A    your-vps-ip
flowise.yourdomain.com    A    your-vps-ip
supabase.yourdomain.com   A    your-vps-ip
langfuse.yourdomain.com   A    your-vps-ip
neo4j.yourdomain.com      A    your-vps-ip
```

### 6. Install OpenCode (Optional but Recommended)

OpenCode provides AI-assisted development and is excellent for learning:

```bash
# Install OpenCode
curl -fsSL https://opencode.ai/install | bash

# Or via npm
npm install -g opencode-ai

# Verify installation
opencode --version
```

**For web access**, add to `.env`:
```bash
OPENCODE_HOSTNAME=opencode.yourdomain.com
```

Uncomment the OpenCode section in `Caddyfile`, then start as systemd service (see OPENCODE_SETUP.md for details).

### 7. Start Services

```bash
cd /opt/cbass

# For GPU (NVIDIA)
sudo python3 start_services.py --profile gpu-nvidia --environment public

# For CPU only
sudo python3 start_services.py --profile cpu --environment public
```

## Profile Options

| Profile | Use Case |
|---------|----------|
| `cpu` | No GPU available |
| `gpu-nvidia` | NVIDIA GPU (requires nvidia-docker) |
| `gpu-amd` | AMD GPU (Linux only) |
| `none` | Ollama running separately |

## Environment Options

| Environment | Ports Exposed | Use Case |
|-------------|---------------|----------|
| `private` | All ports (8001-8008) | Local development, trusted network |
| `public` | Only 80, 443 | Production VPS, internet-facing |

## Post-Deployment

### Access Services

Once DNS propagates and Caddy provisions TLS certificates:

- **n8n**: https://n8n.yourdomain.com
- **Open WebUI**: https://openwebui.yourdomain.com
- **Flowise**: https://flowise.yourdomain.com
- **Supabase**: https://supabase.yourdomain.com
- **Langfuse**: https://langfuse.yourdomain.com
- **Neo4j**: https://neo4j.yourdomain.com

### Initial Setup

1. **n8n** (https://n8n.yourdomain.com):
   - Create admin account
   - Configure credentials:
     - Ollama: `http://ollama:11434`
     - Postgres: Host `db`, credentials from .env
     - Qdrant: `http://qdrant:6333`

2. **Open WebUI** (https://openwebui.yourdomain.com):
   - Create admin account
   - Add n8n integration (paste `n8n_pipe.py` as function)
   - Configure webhook URL from n8n

3. **Supabase** (https://supabase.yourdomain.com):
   - Login with DASHBOARD_USERNAME/DASHBOARD_PASSWORD from .env
   - Create database tables as needed

## Maintenance

### Update Stack

```bash
cd /opt/cbass
sudo ./deploy.sh
```

### View Logs

```bash
# All services
docker compose -p localai logs -f

# Specific service
docker compose -p localai logs -f n8n
docker compose -p localai logs -f ollama
```

### Check Status

```bash
docker compose -p localai ps
```

### Restart Services

```bash
cd /opt/cbass
docker compose -p localai restart
```

### Stop Services

```bash
docker compose -p localai down
```

## Troubleshooting

### Supabase Pooler Restarting

See: https://github.com/supabase/supabase/issues/30210

### SearXNG Restarting

```bash
chmod 755 /opt/cbass/searxng
```

### Check Firewall

```bash
ufw status
```

### Check Docker

```bash
docker ps
docker compose -p localai ps
```

### Disk Space

```bash
df -h
docker system df
```

### Clean Up Docker

```bash
docker system prune -a
```

## Security Checklist

- [ ] Firewall configured (only ports 22, 80, 443)
- [ ] Strong passwords in .env (no @ in POSTGRES_PASSWORD)
- [ ] SSH key-based authentication enabled
- [ ] Root login disabled
- [ ] Automatic security updates enabled
- [ ] Regular backups configured
- [ ] TLS certificates auto-renewing via Caddy
- [ ] All *_HOSTNAME variables set
- [ ] .env file has restricted permissions (600)

## Backup Strategy

### Critical Data

- `/opt/cbass/.env` - Environment configuration
- Docker volumes:
  - `localai_n8n_data`
  - `localai_supabase_db`
  - `localai_ollama_data`

### Backup Command

```bash
# Backup volumes
docker run --rm -v localai_n8n_data:/data -v /backup:/backup alpine tar czf /backup/n8n_data.tar.gz /data
docker run --rm -v localai_supabase_db:/data -v /backup:/backup alpine tar czf /backup/supabase_db.tar.gz /data
docker run --rm -v localai_ollama_data:/data -v /backup:/backup alpine tar czf /backup/ollama_data.tar.gz /data

# Backup .env
cp /opt/cbass/.env /backup/.env.backup
```

## Support

- **GitHub Issues**: https://github.com/mdc159/cbass/issues
- **Original Project**: https://github.com/coleam00/local-ai-packaged
- **n8n Community**: https://community.n8n.io/
- **Supabase Docs**: https://supabase.com/docs
