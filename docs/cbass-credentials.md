# CBass Deployment - Access Information

**VPS IP:** 191.101.0.164  
**Domain:** cbass.space  
**SSH Access:** `ssh cbass` (using key at ~/.ssh/cbass_vps)

---

## Service URLs

| Service | URL | Status |
|---------|-----|--------|
| **n8n** | https://n8n.cbass.space | ✅ Working |
| **Open WebUI** | https://openwebui.cbass.space | ⏳ Certificate pending |
| **Flowise** | https://flowise.cbass.space | ⏳ Certificate pending |
| **Supabase Studio** | https://supabase.cbass.space | ⏳ Certificate pending |
| **Langfuse** | https://langfuse.cbass.space | ⏳ Certificate pending |
| **Neo4j Browser** | https://neo4j.cbass.space | ⏳ Certificate pending |
| **SearXNG** | https://searxng.cbass.space | ⏳ Certificate pending |

---

## Credentials

### Supabase Dashboard
- **URL:** https://supabase.cbass.space
- **Username:** `admin`
- **Password:** `HCLsR1NUJeqrsV-8dApBPA`

### Postgres Database (for n8n credentials)
- **Host:** `db` (internal Docker network)
- **Database:** `postgres`
- **Port:** `5432`
- **Username:** `postgres`
- **Password:** `CRYSu0R8cY5mk817PxCy3E3R8zwUH0PcK75kmAb_5Jg`

### Neo4j
- **URL:** https://neo4j.cbass.space (when certificate ready)
- **Auth:** `neo4j/r5po9iSJqxMk3IlGYEj9OQ`
- **Username:** `neo4j`
- **Password:** `r5po9iSJqxMk3IlGYEj9OQ`

### Supabase API Keys
- **ANON_KEY:** `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYW5vbiIsImlzcyI6InN1cGFiYXNlIiwiaWF0IjoxNjQxNzY5MjAwLCJleHAiOjE3OTk1MzU2MDB9.PcIqRO5GhuM9j3MOQBy27G-yYQI1nqPU2xUimzmgeow`
- **SERVICE_ROLE_KEY:** `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoic2VydmljZV9yb2xlIiwiaXNzIjoic3VwYWJhc2UiLCJpYXQiOjE2NDE3NjkyMDAsImV4cCI6MTc5OTUzNTYwMH0.mylxJcByw2KhROteKKXN55O1Dr3Kz850CRFxMKQ0nV4`

---

## n8n Setup (Ready Now)

### 1. Create n8n Account
Visit https://n8n.cbass.space and create your admin account (first-time setup).

### 2. Configure n8n Credentials

After logging in, go to **Settings → Credentials** and add:

#### Ollama Credential
- **Base URL:** `http://ollama:11434`

#### Postgres Credential (Supabase)
- **Host:** `db`
- **Database:** `postgres`
- **User:** `postgres`
- **Password:** `CRYSu0R8cY5mk817PxCy3E3R8zwUH0PcK75kmAb_5Jg`
- **Port:** `5432`

#### Qdrant Credential
- **URL:** `http://qdrant:6333`
- **API Key:** (any value - running locally without auth)

---

## Open WebUI Setup (When Certificate Ready)

### 1. Create Account
Visit https://openwebui.cbass.space and create your account.

### 2. Install n8n Integration
1. Go to **Workspace → Functions → Add Function**
2. Download `n8n_pipe.py` from: https://openwebui.com/f/coleam/n8n_pipe/
3. Or copy from `/opt/cbass/n8n_pipe.py` on the VPS
4. Paste the code and save
5. Click the gear icon and set `n8n_url` to your n8n webhook URL
6. Toggle the function ON

---

## Useful Commands

### Check All Containers
```bash
ssh cbass "docker compose -p localai ps"
```

### Check Caddy SSL Progress
```bash
ssh cbass "docker compose -p localai logs caddy --tail 50"
```

### View Specific Service Logs
```bash
ssh cbass "docker compose -p localai logs -f [service-name]"
```

### Restart Services
```bash
ssh cbass "cd /opt/cbass && python3 start_services.py --profile cpu --environment public"
```

### Restart Just Caddy (to retry SSL)
```bash
ssh cbass "docker compose -p localai restart caddy"
```

---

## Important Notes

- **Project Name:** All docker compose commands use `-p localai`
- **Environment:** `public` (only ports 80/443 exposed)
- **Profile:** `cpu` (no GPU acceleration)
- **Ollama Models:** Auto-downloads `qwen2.5:7b-instruct-q4_K_M` and `nomic-embed-text` on first run
- **Supabase Access:** Goes through Kong gateway (internal port 8000)
- **Full .env file:** Located at `/opt/cbass/.env` on VPS

---

## GitHub Repository
https://github.com/mdc159/cbass

---

## Next Steps

1. ✅ **n8n is ready** - Create account and set up credentials
2. ⏳ **Wait 5-10 minutes** for remaining SSL certificates (Caddy is retrying with ZeroSSL)
3. 🔄 **Check certificate status** with: `ssh cbass "docker compose -p localai logs caddy --tail 50 | grep successfully"`
4. 🚀 **Start building** - Import workflows from `n8n/backup/workflows/` directory

---

**Generated:** 2026-01-12  
**Session:** CBass Deployment to Hostinger VPS
