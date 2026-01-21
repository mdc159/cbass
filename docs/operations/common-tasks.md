# Common Tasks

Frequently used operations for managing CBass.

## Starting Services

### Local Development

```bash
# NVIDIA GPU
python start_services.py --profile gpu-nvidia --environment private

# AMD GPU (Linux)
python start_services.py --profile gpu-amd --environment private

# CPU only
python start_services.py --profile cpu --environment private

# No local LLM
python start_services.py --profile none --environment private
```

### Production (VPS)

```bash
python3 start_services.py --profile cpu --environment public
```

## Stopping Services

```bash
# Stop all containers (preserves data)
docker compose -p localai down

# Stop and remove volumes (DATA LOSS)
docker compose -p localai down -v
```

## Checking Status

### All Services

```bash
docker compose -p localai ps
```

Expected output shows all services as "Up".

### Resource Usage

```bash
docker stats
```

Shows CPU, memory, network for each container.

### Specific Service Health

```bash
# Check if service responds
curl http://localhost:5678/healthz  # n8n
curl http://localhost:6333/health   # Qdrant
```

## Viewing Logs

### All Services

```bash
docker compose -p localai logs -f
```

### Specific Service

```bash
docker compose -p localai logs -f n8n
docker compose -p localai logs -f ollama
docker compose -p localai logs -f caddy
```

### Filter Logs

```bash
# Last 100 lines
docker compose -p localai logs --tail 100 n8n

# Since timestamp
docker compose -p localai logs --since "2024-01-01" n8n

# Errors only
docker compose -p localai logs n8n 2>&1 | grep -i error
```

## Restarting Services

### Single Service

```bash
docker compose -p localai restart n8n
docker compose -p localai restart ollama
```

### All Services

```bash
docker compose -p localai down
python start_services.py --profile <profile> --environment <env>
```

## Updating Services

### Update Containers

```bash
# Stop services
docker compose -p localai down

# Pull latest images
docker compose -p localai -f docker-compose.yml --profile <profile> pull

# Restart
python start_services.py --profile <profile> --environment <env>
```

### Update Code

```bash
cd /path/to/cbass
git pull
python start_services.py --profile <profile> --environment <env>
```

## Managing Ollama Models

### List Models

```bash
docker exec -it ollama ollama list
```

### Pull New Model

```bash
docker exec -it ollama ollama pull llama3.1
docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama pull codellama
```

### Remove Model

```bash
docker exec -it ollama ollama rm <model-name>
```

### Check Model Info

```bash
docker exec -it ollama ollama show llama3.1
```

## Database Operations

### PostgreSQL (Supabase)

```bash
# Connect to database
docker exec -it db psql -U postgres

# Run SQL query
docker exec -it db psql -U postgres -c "SELECT * FROM my_table;"

# Dump database
docker exec -it db pg_dump -U postgres postgres > backup.sql
```

### Neo4j

```bash
# Access via browser
http://localhost:7474

# Connect: bolt://localhost:7687
# Auth: neo4j/password (from NEO4J_AUTH)
```

### Qdrant

```bash
# List collections
curl http://localhost:6333/collections

# Check health
curl http://localhost:6333/health
```

## File Operations

### Access Shared Files (n8n)

Files in `./shared/` are available at `/data/shared` in n8n container.

```bash
# Copy file to shared
cp myfile.txt ./shared/

# Access in n8n
# /data/shared/myfile.txt
```

### Import n8n Workflow

1. Copy JSON to `n8n/backup/workflows/`
2. Or import via UI: n8n > Add workflow > Import from file

### Import Flowise Chatflow

1. Convert to ExportData format: `.\wrap_flowise.ps1 -Path "file.json"`
2. In Flowise: Settings > Load Data > Select file

## Network Diagnostics

### Check Container Connectivity

```bash
# From one container to another
docker exec -it n8n curl http://ollama:11434

# Check DNS resolution
docker exec -it n8n nslookup ollama
```

### List Docker Networks

```bash
docker network ls
docker network inspect localai_default
```

## Clean Up

### Remove Unused Resources

```bash
# Remove unused containers, networks, images
docker system prune

# Include volumes (CAREFUL - removes data)
docker system prune -a --volumes
```

### Clear Logs

```bash
# Truncate container logs
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' <container-id>)
```

## VPS-Specific Operations

### SSH Access

```bash
ssh cbass
# Or
ssh root@191.101.0.164
```

### Check Disk Space

```bash
df -h
```

### Monitor Resources

```bash
htop
# or
docker stats
```

### Restart After Reboot

```bash
cd /opt/cbass
python3 start_services.py --profile cpu --environment public
```
