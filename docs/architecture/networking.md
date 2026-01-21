# Networking

Ports, container communication, and network configuration.

## Docker Network

All services run on the `localai_default` Docker network.

### Container DNS

Services communicate using container names as hostnames:

| Container | Internal URL |
|-----------|-------------|
| ollama | http://ollama:11434 |
| n8n | http://n8n:5678 |
| qdrant | http://qdrant:6333 |
| neo4j | bolt://neo4j:7687 |
| db | postgresql://db:5432 |
| flowise | http://flowise:3001 |
| open-webui | http://open-webui:8080 |
| searxng | http://searxng:8080 |
| kong | http://kong:8000 |

## Port Reference

### External Ports (Production)

| Port | Service | Protocol |
|------|---------|----------|
| 80 | Caddy | HTTP (redirects to 443) |
| 443 | Caddy | HTTPS |

### Internal Ports

| Port | Service | Protocol | Purpose |
|------|---------|----------|---------|
| 3000 | Dashboard, Langfuse, Studio | HTTP | Multiple services share |
| 3001 | Flowise | HTTP | AI builder |
| 5432 | PostgreSQL | TCP | Database |
| 5678 | n8n | HTTP | Workflow engine |
| 6333 | Qdrant | HTTP | Vector DB REST |
| 6334 | Qdrant | gRPC | Vector DB gRPC |
| 6379 | Redis | TCP | Cache |
| 6543 | Supavisor | TCP | Connection pooler |
| 6901 | Kali | HTTPS | VNC/noVNC |
| 7474 | Neo4j | HTTP | Browser UI |
| 7687 | Neo4j | Bolt | Graph queries |
| 8000 | Kong | HTTP | Supabase gateway |
| 8080 | Open WebUI, SearXNG | HTTP | Multiple services |
| 8123 | ClickHouse | HTTP | Analytics |
| 9000 | MinIO, Updater, ClickHouse | HTTP | Multiple services |
| 11434 | Ollama | HTTP | LLM API |

### Local Development Ports (Private Mode)

In private mode, services expose ports directly:

| Service | Local URL |
|---------|-----------|
| n8n | http://localhost:5678 |
| Open WebUI | http://localhost:8080 |
| Flowise | http://localhost:3001 |
| Supabase | http://localhost:8000 |
| Neo4j | http://localhost:7474 |
| Langfuse | http://localhost:3000 |
| SearXNG | http://localhost:8081 |
| Qdrant | http://localhost:6333 |
| Ollama | http://localhost:11434 |

## Subdomain Routing (Production)

Caddy routes based on hostname:

| Subdomain | Target | Port |
|-----------|--------|------|
| cbass.space | dashboard | 3000 |
| n8n.cbass.space | n8n | 5678 |
| openwebui.cbass.space | open-webui | 8080 |
| flowise.cbass.space | flowise | 3001 |
| supabase.cbass.space | kong | 8000 |
| langfuse.cbass.space | langfuse-web | 3000 |
| neo4j.cbass.space | neo4j | 7474 |
| searxng.cbass.space | searxng | 8080 |
| kali.cbass.space | kali | 6901 |

## Configuration Examples

### n8n Credentials

When configuring credentials in n8n:

```yaml
# Ollama
Host: ollama
Port: 11434
# Full URL: http://ollama:11434

# PostgreSQL (Supabase)
Host: db
Port: 5432
Database: postgres
User: postgres
Password: <from .env>

# Qdrant
URL: http://qdrant:6333

# Neo4j
Host: neo4j
Port: 7687
Protocol: bolt
```

### Flowise Connections

```yaml
# Ollama
Base URL: http://ollama:11434

# Qdrant
Qdrant URL: http://qdrant:6333

# PostgreSQL
Connection String: postgresql://postgres:PASSWORD@db:5432/postgres
```

## Firewall Configuration

### Production (VPS)

```bash
# UFW configuration
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

### Verify

```bash
ufw status
```

## Troubleshooting

### Container Can't Reach Another

```bash
# Test connectivity
docker exec -it n8n curl http://ollama:11434

# Check DNS resolution
docker exec -it n8n nslookup ollama
```

### Check Network

```bash
# List networks
docker network ls

# Inspect network
docker network inspect localai_default
```

### Port Conflicts

```bash
# Find what's using a port (Windows)
netstat -ano | findstr :5678

# Find what's using a port (Linux/Mac)
lsof -i :5678
```

### Service Not Accessible

1. Check service is running: `docker compose -p localai ps`
2. Check logs: `docker compose -p localai logs <service>`
3. Verify port mapping in docker-compose.yml
4. Check firewall isn't blocking
