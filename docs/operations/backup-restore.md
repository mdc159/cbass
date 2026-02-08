# Backup & Restore

Procedures for protecting and recovering CBass data.

## What to Backup

| Component | Location | Priority |
|-----------|----------|----------|
| Environment variables | `.env` | Critical |
| n8n workflows | Docker volume / Export | High |
| Flowise chatflows | Docker volume / Export | High |
| PostgreSQL database | Docker volume | High |
| Qdrant collections | Docker volume | Medium |
| Neo4j graphs | `neo4j/data/` | Medium |
| Ollama models | Docker volume | Low (re-downloadable) |
| User data (Open WebUI) | Docker volume | Medium |

## Docker Volumes

### List Volumes

```bash
docker volume ls | grep localai
```

Typical volumes:
- `localai_n8n_data`
- `localai_postgres_data`
- `localai_qdrant`
- `localai_flowise`
- `localai_ollama`
- `localai_open-webui`

### Backup Volume

```bash
# Generic volume backup
docker run --rm \
  -v localai_n8n_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/n8n-data-$(date +%Y%m%d).tar.gz /data
```

### Restore Volume

```bash
# Stop service first
docker compose -p localai stop n8n

# Restore
docker run --rm \
  -v localai_n8n_data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/n8n-data-20240115.tar.gz -C /

# Restart
docker compose -p localai start n8n
```

## Application-Level Exports

### n8n Workflows

**Export via UI:**
1. Open n8n
2. Open workflow
3. Menu (...) > Export

**Export via API:**
```bash
# Export all workflows
curl -X GET "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-KEY: your-api-key" \
  > workflows-backup.json

# Export credentials (encrypted)
curl -X GET "http://localhost:5678/api/v1/credentials" \
  -H "X-N8N-API-KEY: your-api-key" \
  > credentials-backup.json
```

**Restore:**
```bash
curl -X POST "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d @workflow.json
```

### Flowise Chatflows

**Export:**
1. In Flowise: Settings > Export All
2. Saves ExportData JSON with all chatflows, tools, etc.

**Restore:**
1. In Flowise: Settings > Load Data
2. Select ExportData JSON file

### PostgreSQL (Supabase)

**Full Dump:**
```bash
docker exec -it db pg_dump -U postgres postgres > backup-$(date +%Y%m%d).sql
```

**Specific Tables:**
```bash
docker exec -it db pg_dump -U postgres -t my_table postgres > table-backup.sql
```

**Restore:**
```bash
docker exec -i db psql -U postgres postgres < backup-20240115.sql
```

### Qdrant Collections

**Create Snapshot:**
```bash
curl -X POST "http://localhost:6333/collections/my_collection/snapshots"
```

**List Snapshots:**
```bash
curl "http://localhost:6333/collections/my_collection/snapshots"
```

**Download Snapshot:**
```bash
curl -o snapshot.tar \
  "http://localhost:6333/collections/my_collection/snapshots/my_collection-12345.snapshot"
```

### Neo4j Database

**Stop and Copy:**
```bash
docker compose -p localai stop neo4j
cp -r neo4j/data neo4j-backup-$(date +%Y%m%d)
docker compose -p localai start neo4j
```

**Using neo4j-admin:**
```bash
docker exec -it neo4j neo4j-admin database dump neo4j --to-path=/data
```

## Environment Variables

### Backup .env

```bash
cp .env .env.backup-$(date +%Y%m%d)
```

**Important**: Store .env backup securely (contains secrets).

### Critical Variables to Document

Keep a secure record of:
- `N8N_ENCRYPTION_KEY` - Required to decrypt n8n credentials
- `POSTGRES_PASSWORD` - Database access
- `JWT_SECRET`, `ANON_KEY`, `SERVICE_ROLE_KEY` - Supabase auth
- `NEO4J_AUTH` - Neo4j access

## Automated Backup Script

Create `backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Database
docker exec db pg_dump -U postgres postgres > $BACKUP_DIR/postgres.sql

# n8n workflows
docker run --rm -v localai_n8n_data:/data -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/n8n.tar.gz /data

# Flowise
docker run --rm -v localai_flowise:/data -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/flowise.tar.gz /data

# Neo4j
cp -r /opt/cbass/neo4j/data $BACKUP_DIR/neo4j-data

# Environment
cp /opt/cbass/.env $BACKUP_DIR/.env.backup

# Clean old backups (keep 7 days)
find /opt/backups -mtime +7 -type d -exec rm -rf {} +

echo "Backup completed: $BACKUP_DIR"
```

Schedule with cron:
```bash
0 2 * * * /opt/cbass/backup.sh >> /var/log/cbass-backup.log 2>&1
```

## Disaster Recovery

### Complete Restore Procedure

1. **Fresh server setup:**
   ```bash
   apt update && apt upgrade -y
   curl -fsSL https://get.docker.com | sh
   apt install -y docker-compose-plugin python3 git
   ```

2. **Clone repository:**
   ```bash
   cd /opt
   git clone https://github.com/mdc159/cbass.git
   cd cbass
   ```

3. **Restore .env:**
   ```bash
   cp /path/to/backup/.env.backup .env
   ```

4. **Start services (creates volumes):**
   ```bash
   python3 start_services.py --profile cpu --environment public
   docker compose -p localai down
   ```

5. **Restore data:**
   ```bash
   # Database
   docker exec -i db psql -U postgres postgres < /path/to/backup/postgres.sql

   # n8n
   docker run --rm -v localai_n8n_data:/data -v /path/to/backup:/backup \
     alpine tar xzf /backup/n8n.tar.gz -C /

   # Flowise
   docker run --rm -v localai_flowise:/data -v /path/to/backup:/backup \
     alpine tar xzf /backup/flowise.tar.gz -C /

   # Neo4j
   cp -r /path/to/backup/neo4j-data/* neo4j/data/
   ```

6. **Restart services:**
   ```bash
   python3 start_services.py --profile cpu --environment public
   ```

## VPS Migration

### From Old VPS to New VPS

1. **On old VPS**: Create backups of all data
2. **Transfer**: `scp -r /opt/backups/* user@new-vps:/opt/backups/`
3. **On new VPS**: Follow disaster recovery procedure
4. **Update DNS**: Point domain to new IP
5. **Verify**: Test all services
