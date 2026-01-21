# Troubleshooting Guide

Solutions for common issues in the CBass stack.

## General Diagnostics

### Check Service Status

```bash
docker compose -p localai ps
```

All services should show "Up". If a service shows "Restarting" or "Exit", check its logs.

### View Service Logs

```bash
docker compose -p localai logs -f <service-name>
```

### Check Resource Usage

```bash
docker stats
```

High CPU/memory may indicate resource exhaustion.

## Service-Specific Issues

### n8n

#### Webhook Not Responding

**Symptoms**: External requests to webhook URL fail

**Solutions**:
1. Verify workflow is activated (check toggle)
2. Use Production URL (not Test URL)
3. Check n8n logs: `docker compose -p localai logs -f n8n`
4. Verify Caddy is routing correctly

#### Credential Connection Failed

**Symptoms**: Cannot connect to Ollama, Postgres, etc.

**Solutions**:
1. Use container names, not localhost:
   - Ollama: `http://ollama:11434`
   - PostgreSQL: `db` (not localhost)
   - Qdrant: `http://qdrant:6333`
2. Verify target service is running
3. Test connectivity: `docker exec -it n8n curl http://ollama:11434`

#### Execution Stuck

**Solutions**:
1. Check execution history in n8n
2. Review error details
3. Verify external services are available
4. Check for rate limits

---

### Flowise

#### Import Fails Silently

**Symptoms**: File upload appears to work but nothing imports

**Solutions**:
1. Use Settings > Load Data (not "Load Chatflow" button)
2. Verify JSON is valid ExportData format
3. Use wrapper script: `.\wrap_flowise.ps1 -Path "file.json"`
4. Check browser console for errors

#### Model Not Found

**Symptoms**: "Model not found" errors

**Solutions**:
1. Verify Ollama has the model: `docker exec -it ollama ollama list`
2. Check model name spelling exactly
3. Invalid names: `gpt-4.1-mini` → Use `gpt-4o-mini`

#### UI Upload Fails

**Symptoms**: File uploads error or timeout

**Solutions**:
File size limit or volume permissions. Verify:
1. `FLOWISE_FILE_SIZE_LIMIT=50mb` in .env
2. Caddy body limit in Caddyfile
3. Named volume in docker-compose.yml

---

### Ollama

#### Model Download Stuck

**Solutions**:
1. Check disk space: `df -h`
2. Restart download: `docker exec -it ollama ollama pull <model>`
3. Check network connectivity

#### Out of Memory

**Symptoms**: OOM errors, slow performance

**Solutions**:
1. Use smaller models (3B instead of 7B)
2. Use quantized models (q4_K_M)
3. Increase Docker memory allocation
4. Close other applications

#### Slow Inference

**Solutions**:
1. Verify GPU is being used (if available)
2. Use correct profile: `--profile gpu-nvidia`
3. Check `docker stats` for resource usage
4. Try smaller models

---

### Supabase

#### Pooler Restarting

**Symptoms**: `supavisor` container keeps restarting

**Status**: Known issue - [GitHub #30210](https://github.com/supabase/supabase/issues/30210)

**Impact**: Services still work without pooler. Can be ignored.

#### Analytics Startup Failure

**Symptoms**: Analytics container fails after password change

**Solution**:
```bash
rm -rf supabase/docker/volumes/db/data
python3 start_services.py --profile cpu
```

#### Service Unavailable

**Solutions**:
1. Verify no `@` in POSTGRES_PASSWORD (breaks URI parsing)
2. Check Kong logs: `docker compose -p localai logs kong`
3. Wait for all Supabase containers to initialize (~30s)

#### Files Not Found

**Solution**: Delete and re-clone:
```bash
rm -rf supabase/
python3 start_services.py --profile cpu
```

---

### SearXNG

#### Container Restarting

**Symptoms**: SearXNG keeps restarting

**Solution**:
```bash
chmod 755 searxng
docker compose -p localai restart searxng
```

#### No Search Results

**Solutions**:
1. Check internet connectivity
2. Some engines may be rate-limited
3. Try different search engines in preferences

---

### Caddy / SSL

#### Certificate Not Issued

**Symptoms**: HTTPS not working, certificate errors

**Solutions**:
1. Verify DNS propagation: `nslookup n8n.cbass.space`
2. Check ports open: `ufw status` (80 and 443 needed)
3. Check Caddy logs: `docker compose -p localai logs caddy`
4. May be rate-limited - wait 1 hour

#### 502 Bad Gateway

**Symptoms**: Caddy returns 502 error

**Solutions**:
1. Target service not running
2. Check service: `docker compose -p localai ps`
3. Check Caddyfile routing

#### ERR_SSL_PROTOCOL_ERROR

**Solutions**:
1. DNS not yet propagated - wait
2. Caddy hasn't finished provisioning - wait 2-3 minutes
3. Clear browser cache

---

### Neo4j

#### Authentication Failed

**Solutions**:
1. Check `NEO4J_AUTH` format: `neo4j/yourpassword`
2. Restart container after password change
3. Default is `neo4j/neo4j` (prompts to change)

#### Browser Shows "Server not available"

**Solutions**:
1. Wait 30-60 seconds for Neo4j to initialize
2. Check logs: `docker compose -p localai logs neo4j`

---

### Docker / General

#### Port Already in Use

**Solutions**:
```bash
# Find what's using the port (Windows)
netstat -ano | findstr :5678

# Find what's using the port (Linux/Mac)
lsof -i :5678

# Kill the process or change CBass port
```

#### Out of Disk Space

**Solutions**:
```bash
# Check disk usage
df -h

# Clean Docker resources
docker system prune -a
```

#### Container Won't Start

**Solutions**:
1. Check logs: `docker compose -p localai logs <service>`
2. Check resources: `docker stats`
3. Remove and recreate: `docker compose -p localai up -d --force-recreate <service>`

## Network Issues

### Container Can't Reach Another

```bash
# Test from inside container
docker exec -it n8n curl http://ollama:11434

# Check network
docker network inspect localai_default
```

### External Access Blocked

1. Check firewall: `ufw status`
2. Verify ports 80, 443 are open
3. Check Caddy configuration

## Data Issues

### Lost Data After Update

Docker volumes persist by default. If data is lost:
1. Check volume exists: `docker volume ls | grep localai`
2. Check volume wasn't accidentally removed
3. Restore from backup

### Corrupted Data

1. Stop service
2. Restore from backup
3. If no backup, may need to delete volume and start fresh

## Getting Help

If none of the above helps:

1. **Collect information**:
   - Service logs
   - Docker status
   - Error messages

2. **Check documentation**:
   - Service-specific docs in `docs/services/`
   - Original project documentation

3. **Report issue**:
   - GitHub issues with reproduction steps
   - Include relevant logs and configuration
