# CBass Deployment Guide for cbass.space

## CORRECTED: Use start_services.py (NOT deploy.sh)

---

## Step 1: Configure DNS Records

**IMPORTANT: Do this FIRST before deploying!**

Log into your DNS provider (where you registered cbass.space) and add these A records:

| Subdomain | Type | Value | TTL |
|-----------|------|-------|-----|
| n8n.cbass.space | A | 191.101.0.164 | 300 |
| openwebui.cbass.space | A | 191.101.0.164 | 300 |
| flowise.cbass.space | A | 191.101.0.164 | 300 |
| supabase.cbass.space | A | 191.101.0.164 | 300 |
| langfuse.cbass.space | A | 191.101.0.164 | 300 |
| neo4j.cbass.space | A | 191.101.0.164 | 300 |
| searxng.cbass.space | A | 191.101.0.164 | 300 |

**Wait 5-10 minutes for DNS propagation.**

Check with: nslookup n8n.cbass.space

---

## Step 2: SSH into Your VPS

bash
ssh root@191.101.0.164


---

## Step 3: Install Prerequisites

bash
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
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable


---

## Step 4: Clone Repository

bash
cd /opt
git clone https://github.com/mdc159/cbass.git
cd cbass


---

## Step 5: Create .env File

bash
nano .env


Paste the entire content from your local X:\GitHub\CBass\.env file.

**Save**: Press Ctrl+X, then Y, then Enter

---

## Step 6: Deploy with start_services.py

**IMPORTANT: Use start_services.py, NOT deploy.sh**

bash
# For VPS deployment with CPU profile and public environment
python3 start_services.py --profile cpu --environment public


**What this does:**
1. Clones/updates Supabase repository (sparse checkout)
2. Copies .env to supabase/docker/.env
3. Generates SearXNG secret key
4. Stops existing containers
5. Starts Supabase stack first (waits 10s for init)
6. Starts local AI stack with CPU profile
7. Caddy automatically provisions Let''s Encrypt SSL certificates

**This will take 10-15 minutes on first run** (downloading Docker images).

---

## Step 7: Monitor Deployment

Watch the logs:

bash
# In another terminal, watch logs
docker compose -p localai logs -f


Or check specific services:

bash
docker compose -p localai logs -f caddy
docker compose -p localai logs -f n8n
docker compose -p localai logs -f ollama


---

## Step 8: Verify Deployment

Check all services are running:

bash
docker compose -p localai ps


You should see:
- n8n (Up)
- open-webui (Up)
- flowise (Up)
- ollama (Up)
- kong (Supabase - Up)
- caddy (Up)
- langfuse-web (Up)
- neo4j (Up)
- qdrant (Up)
- postgres (Up)
- redis (Up)

---

## Step 9: Access Your Services

After deployment completes and DNS has propagated:

- **n8n**: https://n8n.cbass.space
- **Open WebUI**: https://openwebui.cbass.space
- **Flowise**: https://flowise.cbass.space
- **Supabase**: https://supabase.cbass.space
- **Langfuse**: https://langfuse.cbass.space
- **Neo4j**: https://neo4j.cbass.space
- **SearXNG**: https://searxng.cbass.space

All will have automatic HTTPS via Let''s Encrypt! 🔒

---

## Step 10: Initial Setup

### n8n (https://n8n.cbass.space)
1. Create admin account (first user becomes admin)
2. Set up credentials:
   - **Ollama**: http://ollama:11434
   - **Postgres** (Supabase): 
     - Host: db
     - Database: postgres
     - User: postgres
     - Password: CRYSu0R8cY5mk817PxCy3E3R8zwUH0PcK75kmAb_5Jg
   - **Qdrant**: http://qdrant:6333

### Open WebUI (https://openwebui.cbass.space)
1. Create admin account
2. Configure Ollama: http://ollama:11434
3. Install n8n_pipe.py function (see README)

### Supabase (https://supabase.cbass.space)
- Username: admin
- Password: HCLsR1NUJeqrsV-8dApBPA

---

## Troubleshooting

### Services not starting?

bash
# Check logs
docker compose -p localai logs -f

# Restart all services
docker compose -p localai down
python3 start_services.py --profile cpu --environment public


### Supabase issues?

bash
# Check if supabase folder was cloned
ls -la supabase/

# If missing or corrupted, delete and restart
rm -rf supabase/
python3 start_services.py --profile cpu --environment public


### SearXNG restarting?

bash
chmod 755 searxng
docker compose -p localai restart searxng


### Caddy not getting SSL certificates?

1. Verify DNS is propagated: nslookup n8n.cbass.space
2. Check Caddy logs: docker compose -p localai logs caddy
3. Ensure ports 80 and 443 are open: ufw status

### Check specific service

bash
docker compose -p localai logs [service-name]
docker compose -p localai restart [service-name]


---

## Updating Services

To update all containers to latest versions:

bash
# Stop services
docker compose -p localai -f docker-compose.yml --profile cpu down

# Pull latest images
docker compose -p localai -f docker-compose.yml --profile cpu pull

# Restart
python3 start_services.py --profile cpu --environment public


---

## Next Steps

1. **Install OpenCode** (see OPENCODE_SETUP.md)
2. **Set up n8n workflows** (pre-built workflows in n8n/backup/workflows/)
3. **Configure Open WebUI + n8n integration** (n8n_pipe.py)
4. **Set up backups** (Docker volumes in /var/lib/docker/volumes/)
5. **Configure monitoring** (Langfuse for LLM observability)

---

## Important Notes

- **First run**: Ollama will automatically pull qwen2.5:7b-instruct-q4_K_M and nomic-embed-text
- **Supabase folder**: Auto-cloned, do NOT commit to git
- **Postgres password**: No @ symbol (breaks connection strings)
- **Project name**: All services use localai project name
- **Profiles**: cpu, gpu-nvidia, gpu-amd, none
- **Environments**: private (exposes ports), public (only 80/443)

