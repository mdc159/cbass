# CBass IP-Only Deployment (No Domain Required)

## Quick Start - Deploy Now, Add Domains Later

This guide deploys CBass using IP addresses and ports. When your domain is ready, you can easily switch to HTTPS with domains.

---

## Step 1: SSH into VPS

bash
ssh root@191.101.0.164


---

## Step 2: Install Prerequisites

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

# Configure firewall (open all service ports for IP access)
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8001/tcp
ufw allow 8002/tcp
ufw allow 8003/tcp
ufw allow 8004/tcp
ufw allow 8005/tcp
ufw allow 8006/tcp
ufw allow 8007/tcp
ufw allow 8008/tcp
ufw --force enable


---

## Step 3: Clone Repository

bash
cd /opt
git clone https://github.com/mdc159/cbass.git
cd cbass


---

## Step 4: Generate Supabase Keys

bash
docker run --rm supabase/gotrue:latest gotrue generate keys --jwt-secret a8f812ef858eff8389154e1d524f43eec97208f1f8e48867ec651e3158616ff7


**COPY THE OUTPUT**:

anon key: eyJhbGc...
service_role key: eyJhbGc...


---

## Step 5: Create .env File

bash
nano /opt/cbass/.env


**Paste this content** (replace ANON_KEY and SERVICE_ROLE_KEY with your generated keys):

env
# CBass Production Environment Configuration
# IP-ONLY DEPLOYMENT (No domains - use ports)
# VPS: 191.101.0.164

############
# [required] n8n credentials
############
N8N_ENCRYPTION_KEY=2b4e41aba3c014d03e2b57d9965b0f553551f772538ba3ad5f9aa03192c5ad62
N8N_USER_MANAGEMENT_JWT_SECRET=b8183a57cd9d9ecbfdc568904810ff38b7bf8bffec9227a8f3989ec5425f85c1

############
# [required] Supabase Secrets
############
POSTGRES_PASSWORD=CRYSu0R8cY5mk817PxCy3E3R8zwUH0PcK75kmAb_5Jg
JWT_SECRET=a8f812ef858eff8389154e1d524f43eec97208f1f8e48867ec651e3158616ff7
ANON_KEY=REPLACE_WITH_GENERATED_ANON_KEY
SERVICE_ROLE_KEY=REPLACE_WITH_GENERATED_SERVICE_ROLE_KEY
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=HCLsR1NUJeqrsV-8dApBPA
POOLER_TENANT_ID=5a70b689-37c3-4d60-963a-ad0d812e7fad

############
# [required] Neo4j
############
NEO4J_AUTH=neo4j/r5po9iSJqxMk3IlGYEj9OQ

############
# [required] Langfuse credentials
############
CLICKHOUSE_PASSWORD=2d550ccb260f22f982fc114dac7781f0
MINIO_ROOT_PASSWORD=114cbd9f584e19ec56cd5c72bc4c830d
LANGFUSE_SALT=1036f0f9fd48f7d1fbdd77d0c0baa3cb
NEXTAUTH_SECRET=827f4737d1edb5a68d3221be7dabe26f44a81683787ec8f0b2dab27b5e4f7710
ENCRYPTION_KEY=26f913afd60520c80960cf06cd391308064a8a53e370b331404a27f5d8089880

############
# [IP-ONLY] Caddy Config - ALL COMMENTED OUT
############
# N8N_HOSTNAME=n8n.cbass.space
# WEBUI_HOSTNAME=openwebui.cbass.space
# FLOWISE_HOSTNAME=flowise.cbass.space
# SUPABASE_HOSTNAME=supabase.cbass.space
# LANGFUSE_HOSTNAME=langfuse.cbass.space
# NEO4J_HOSTNAME=neo4j.cbass.space
# SEARXNG_HOSTNAME=searxng.cbass.space
# LETSENCRYPT_EMAIL=admin@cbass.space

############
# Database defaults
############
POSTGRES_HOST=db
POSTGRES_DB=postgres
POSTGRES_PORT=5432
POSTGRES_USER=postgres

############
# Supavisor
############
POOLER_PROXY_PORT_TRANSACTION=6543
POOLER_DEFAULT_POOL_SIZE=20
POOLER_MAX_CLIENT_CONN=100
SECRET_KEY_BASE=UpNVntn3cDxHJpq99YMc1T1AQgQpc8kfYTuRgBiYa15BLrx8etQoXz3gZv1/u2oq
VAULT_ENC_KEY=your-32-character-encryption-key
POOLER_DB_POOL_SIZE=5

############
# API Proxy
############
KONG_HTTP_PORT=8000
KONG_HTTPS_PORT=8443

############
# API
############
PGRST_DB_SCHEMAS=public,storage,graphql_public

############
# Auth
############
SITE_URL=http://localhost:3000
ADDITIONAL_REDIRECT_URLS=
JWT_EXPIRY=3600
DISABLE_SIGNUP=false
API_EXTERNAL_URL=http://localhost:8000

MAILER_URLPATHS_CONFIRMATION="/auth/v1/verify"
MAILER_URLPATHS_INVITE="/auth/v1/verify"
MAILER_URLPATHS_RECOVERY="/auth/v1/verify"
MAILER_URLPATHS_EMAIL_CHANGE="/auth/v1/verify"

ENABLE_EMAIL_SIGNUP=true
ENABLE_EMAIL_AUTOCONFIRM=true
SMTP_ADMIN_EMAIL=admin@example.com
SMTP_HOST=supabase-mail
SMTP_PORT=2500
SMTP_USER=fake_mail_user
SMTP_PASS=fake_mail_password
SMTP_SENDER_NAME=CBass
ENABLE_ANONYMOUS_USERS=false

ENABLE_PHONE_SIGNUP=true
ENABLE_PHONE_AUTOCONFIRM=true

############
# Studio
############
STUDIO_DEFAULT_ORGANIZATION=CBass Organization
STUDIO_DEFAULT_PROJECT=CBass Project
STUDIO_PORT=3000
SUPABASE_PUBLIC_URL=http://localhost:8000
IMGPROXY_ENABLE_WEBP_DETECTION=true

############
# Functions
############
FUNCTIONS_VERIFY_JWT=false

############
# Logs
############
LOGFLARE_PUBLIC_ACCESS_TOKEN=your-super-secret-and-long-logflare-key-public
LOGFLARE_PRIVATE_ACCESS_TOKEN=your-super-secret-and-long-logflare-key-private
DOCKER_SOCKET_LOCATION=/var/run/docker.sock


**Save**: Ctrl+X, then Y, then Enter

---

## Step 6: Deploy with Private Environment

Since we're using IP addresses, use --environment private to expose ports:

bash
python3 start_services.py --profile cpu --environment private


**This takes 10-15 minutes on first run.**

---

## Step 7: Monitor Deployment

bash
# Watch logs
docker compose -p localai logs -f

# Or check specific service
docker compose -p localai logs -f n8n


---

## Step 8: Verify Services

bash
docker compose -p localai ps


All services should show "Up".

---

## Access Your Services (via IP and Ports)

**No HTTPS yet - using HTTP with ports:**

- **n8n**: http://191.101.0.164:8001
- **Open WebUI**: http://191.101.0.164:8002
- **Flowise**: http://191.101.0.164:8003
- **Ollama**: http://191.101.0.164:8004
- **Supabase**: http://191.101.0.164:8005
  - Username: admin
  - Password: HCLsR1NUJeqrsV-8dApBPA
- **SearXNG**: http://191.101.0.164:8006
- **Langfuse**: http://191.101.0.164:8007
- **Neo4j**: http://191.101.0.164:8008

---

## When Domain is Ready: Switch to HTTPS

Once cbass.space DNS is configured:

1. **Update .env file**:
   bash
   nano /opt/cbass/.env
   

   Uncomment the Caddy hostname lines:
   env
   N8N_HOSTNAME=n8n.cbass.space
   WEBUI_HOSTNAME=openwebui.cbass.space
   FLOWISE_HOSTNAME=flowise.cbass.space
   SUPABASE_HOSTNAME=supabase.cbass.space
   LANGFUSE_HOSTNAME=langfuse.cbass.space
   NEO4J_HOSTNAME=neo4j.cbass.space
   SEARXNG_HOSTNAME=searxng.cbass.space
   LETSENCRYPT_EMAIL=admin@cbass.space
   

2. **Redeploy with public environment**:
   bash
   docker compose -p localai down
   python3 start_services.py --profile cpu --environment public
   

3. **Access via HTTPS**:
   - https://n8n.cbass.space
   - https://openwebui.cbass.space
   - etc.

---

## Troubleshooting

### Check logs
bash
docker compose -p localai logs -f [service-name]


### Restart services
bash
docker compose -p localai down
python3 start_services.py --profile cpu --environment private


### Can't access services?
Check firewall:
bash
ufw status


Make sure ports 8001-8008 are allowed.

---

## Summary

**Deploy command**: python3 start_services.py --profile cpu --environment private

**Access services**: http://191.101.0.164:800X (where X = 1-8)

**When domain ready**: Update .env, redeploy with --environment public

