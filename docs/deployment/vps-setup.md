# VPS Production Deployment

Complete guide to deploying CBass on a VPS with automatic HTTPS.

## Prerequisites

- Ubuntu Linux server (20.04+ recommended)
- Root or sudo access
- Domain name with DNS access
- Minimum 4GB RAM, 2 CPU cores, 40GB disk

## Step 1: Configure DNS Records

**Do this FIRST before deploying.**

Add A records pointing to your VPS IP:

| Subdomain | Type | Value | TTL |
|-----------|------|-------|-----|
| `cbass.space` | A | YOUR_VPS_IP | 300 |
| `www.cbass.space` | A | YOUR_VPS_IP | 300 |
| `n8n.cbass.space` | A | YOUR_VPS_IP | 300 |
| `openwebui.cbass.space` | A | YOUR_VPS_IP | 300 |
| `flowise.cbass.space` | A | YOUR_VPS_IP | 300 |
| `supabase.cbass.space` | A | YOUR_VPS_IP | 300 |
| `langfuse.cbass.space` | A | YOUR_VPS_IP | 300 |
| `neo4j.cbass.space` | A | YOUR_VPS_IP | 300 |
| `searxng.cbass.space` | A | YOUR_VPS_IP | 300 |
| `kali.cbass.space` | A | YOUR_VPS_IP | 300 |

Wait 5-10 minutes for DNS propagation, then verify:

```bash
nslookup n8n.cbass.space
```

## Step 2: Server Setup

SSH into your VPS:

```bash
ssh root@YOUR_VPS_IP
```

Install prerequisites:

```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

# Install Docker Compose plugin
apt install -y docker-compose-plugin

# Install Python and Git
apt install -y python3 python3-pip git

# Configure firewall
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP (for ACME challenge)
ufw allow 443/tcp  # HTTPS
ufw --force enable
```

## Step 3: Clone Repository

```bash
cd /opt
git clone https://github.com/mdc159/cbass.git
cd cbass
```

## Step 4: Configure Environment

Create `.env` file:

```bash
cp env.example .env
nano .env
```

**Required settings:**

```bash
# === Required Secrets ===
N8N_ENCRYPTION_KEY=           # openssl rand -hex 32
N8N_USER_MANAGEMENT_JWT_SECRET=

POSTGRES_PASSWORD=            # NO '@' character!
JWT_SECRET=
ANON_KEY=
SERVICE_ROLE_KEY=
DASHBOARD_USERNAME=
DASHBOARD_PASSWORD=

NEO4J_AUTH=neo4j/yourpassword

CLICKHOUSE_PASSWORD=
MINIO_ROOT_PASSWORD=
LANGFUSE_SALT=
NEXTAUTH_SECRET=
ENCRYPTION_KEY=

# === Production Hostnames ===
DASHBOARD_HOSTNAME=cbass.space
N8N_HOSTNAME=n8n.cbass.space
WEBUI_HOSTNAME=openwebui.cbass.space
FLOWISE_HOSTNAME=flowise.cbass.space
SUPABASE_HOSTNAME=supabase.cbass.space
LANGFUSE_HOSTNAME=langfuse.cbass.space
NEO4J_HOSTNAME=neo4j.cbass.space
SEARXNG_HOSTNAME=searxng.cbass.space
KALI_HOSTNAME=kali.cbass.space
LETSENCRYPT_EMAIL=your@email.com
```

Save: `Ctrl+X`, `Y`, `Enter`

## Step 5: Deploy

```bash
python3 start_services.py --profile cpu --environment public
```

**What happens:**
1. Clones/updates Supabase repository (sparse checkout)
2. Copies `.env` to `supabase/docker/.env`
3. Generates SearXNG secret key
4. Stops any existing containers
5. Starts Supabase stack (waits 10s for init)
6. Starts AI stack with selected profile
7. Caddy provisions Let's Encrypt certificates

First run takes 10-15 minutes to download images.

## Step 6: Verify Deployment

Check services:

```bash
docker compose -p localai ps
```

Expected output shows all services as "Up":
- n8n, open-webui, flowise, ollama
- kong, db, qdrant, neo4j
- caddy, langfuse-web, searxng, kali

Check Caddy logs for SSL:

```bash
docker compose -p localai logs caddy
```

## Step 7: Initial Service Setup

### n8n (https://n8n.cbass.space)

1. Create admin account (first user becomes owner)
2. Configure credentials for internal services:

| Service | Host | Port |
|---------|------|------|
| Ollama | `ollama` | 11434 |
| PostgreSQL | `db` | 5432 |
| Qdrant | `qdrant` | 6333 |
| Neo4j | `neo4j` | 7687 |

### Open WebUI (https://openwebui.cbass.space)

1. Create admin account
2. Ollama is pre-configured

### Supabase (https://supabase.cbass.space)

Login with credentials from `.env`:
- Username: `DASHBOARD_USERNAME`
- Password: `DASHBOARD_PASSWORD`

## Updating Services

```bash
cd /opt/cbass

# Pull latest code
git pull

# Pull latest images
docker compose -p localai -f docker-compose.yml --profile cpu pull

# Restart
python3 start_services.py --profile cpu --environment public
```

## Monitoring

### View Logs

```bash
# All services
docker compose -p localai logs -f

# Specific service
docker compose -p localai logs -f n8n
docker compose -p localai logs -f caddy
```

### Resource Usage

```bash
docker stats
```

## Troubleshooting

### SSL Certificate Issues

```bash
# Check Caddy logs
docker compose -p localai logs caddy

# Verify DNS
nslookup n8n.cbass.space

# Verify ports open
ufw status
```

### Service Not Starting

```bash
# Check logs
docker compose -p localai logs <service-name>

# Restart service
docker compose -p localai restart <service-name>
```

### Supabase Issues

```bash
# If corrupted, delete and re-clone
rm -rf supabase/
python3 start_services.py --profile cpu --environment public
```

### SearXNG Restarting

```bash
chmod 755 searxng
docker compose -p localai restart searxng
```

### Postgres Connection Errors

Ensure `POSTGRES_PASSWORD` has no `@` character - it breaks URI parsing.

## Backup

### Docker Volumes

```bash
# List volumes
docker volume ls | grep localai

# Backup a volume
docker run --rm -v localai_n8n_data:/data -v $(pwd):/backup alpine tar czf /backup/n8n-backup.tar.gz /data
```

### Database

```bash
# PostgreSQL dump
docker exec -it db pg_dump -U postgres postgres > backup.sql
```

## Security Notes

- All traffic goes through Caddy (HTTPS enforced)
- Internal services communicate on Docker network
- Only ports 80, 443, and 22 exposed
- Keep `.env` secure and never commit it
