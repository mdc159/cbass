# CBass 2-Stage Deployment Guide

## Why 2 Stages?

Supabase requires JWT keys (ANON_KEY and SERVICE_ROLE_KEY) that are generated from your JWT_SECRET. The demo keys in env.example won't work with your custom JWT_SECRET.

**Stage 1**: Generate proper Supabase keys
**Stage 2**: Deploy with correct keys

---

## STAGE 1: Generate Supabase Keys

### Step 1: SSH into VPS

bash
ssh root@191.101.0.164


### Step 2: Install Prerequisites

bash
apt update && apt upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt install -y docker-compose-plugin python3 python3-pip git
ufw allow 22/tcp && ufw allow 80/tcp && ufw allow 443/tcp
ufw --force enable


### Step 3: Clone Repository

bash
cd /opt
git clone https://github.com/mdc159/cbass.git
cd cbass


### Step 4: Generate Supabase JWT Keys

Run this Docker command to generate keys from your JWT_SECRET:

bash
docker run --rm supabase/gotrue:latest gotrue generate keys --jwt-secret a8f812ef858eff8389154e1d524f43eec97208f1f8e48867ec651e3158616ff7


**This will output:**

anon key: eyJhbGc...  (long string)
service_role key: eyJhbGc...  (long string)


**COPY THESE KEYS!** You'll need them in the next step.

---

## STAGE 2: Deploy with Correct Keys

### Step 5: Create .env File with Generated Keys

bash
nano /opt/cbass/.env


Paste this content, **replacing ANON_KEY and SERVICE_ROLE_KEY with the keys you just generated**:

env
# CBass Production Environment Configuration
# Domain: cbass.space
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
# [PRODUCTION] Caddy Config
############
N8N_HOSTNAME=n8n.cbass.space
WEBUI_HOSTNAME=openwebui.cbass.space
FLOWISE_HOSTNAME=flowise.cbass.space
SUPABASE_HOSTNAME=supabase.cbass.space
LANGFUSE_HOSTNAME=langfuse.cbass.space
NEO4J_HOSTNAME=neo4j.cbass.space
SEARXNG_HOSTNAME=searxng.cbass.space
LETSENCRYPT_EMAIL=admin@cbass.space

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
SITE_URL=https://supabase.cbass.space
ADDITIONAL_REDIRECT_URLS=
JWT_EXPIRY=3600
DISABLE_SIGNUP=false
API_EXTERNAL_URL=https://supabase.cbass.space

MAILER_URLPATHS_CONFIRMATION="/auth/v1/verify"
MAILER_URLPATHS_INVITE="/auth/v1/verify"
MAILER_URLPATHS_RECOVERY="/auth/v1/verify"
MAILER_URLPATHS_EMAIL_CHANGE="/auth/v1/verify"

ENABLE_EMAIL_SIGNUP=true
ENABLE_EMAIL_AUTOCONFIRM=true
SMTP_ADMIN_EMAIL=admin@cbass.space
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
SUPABASE_PUBLIC_URL=https://supabase.cbass.space
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

### Step 6: Deploy!

bash
python3 start_services.py --profile cpu --environment public


**What happens:**
1. Clones Supabase repo
2. Copies .env to supabase/docker/.env
3. Starts Supabase stack (waits 10s)
4. Starts AI stack (n8n, Ollama, Open WebUI, etc.)
5. Caddy provisions SSL certificates

**First run takes 10-15 minutes** (downloading images).

### Step 7: Monitor

bash
# Watch logs
docker compose -p localai logs -f

# Or specific service
docker compose -p localai logs -f caddy


### Step 8: Verify

bash
docker compose -p localai ps


All services should show "Up".

---

## Access Your Services

- **n8n**: https://n8n.cbass.space
- **Open WebUI**: https://openwebui.cbass.space
- **Flowise**: https://flowise.cbass.space
- **Supabase**: https://supabase.cbass.space (admin / HCLsR1NUJeqrsV-8dApBPA)
- **Langfuse**: https://langfuse.cbass.space
- **Neo4j**: https://neo4j.cbass.space
- **SearXNG**: https://searxng.cbass.space

---

## Troubleshooting

### Supabase not starting?

bash
# Check if keys are correct
docker compose -p localai logs kong
docker compose -p localai logs auth

# If auth errors, regenerate keys and update .env


### Services not accessible?

1. Check DNS: nslookup n8n.cbass.space
2. Check Caddy: docker compose -p localai logs caddy
3. Check firewall: ufw status

### Restart everything

bash
docker compose -p localai down
python3 start_services.py --profile cpu --environment public


---

## Summary

**Your JWT_SECRET**: a8f812ef858eff8389154e1d524f43eec97208f1f8e48867ec651e3158616ff7

**Generate keys with**:
bash
docker run --rm supabase/gotrue:latest gotrue generate keys --jwt-secret a8f812ef858eff8389154e1d524f43eec97208f1f8e48867ec651e3158616ff7


**Then deploy with**:
bash
python3 start_services.py --profile cpu --environment public


