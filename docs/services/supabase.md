# Supabase - Database & Auth Platform

**URL**: https://supabase.cbass.space | **Container**: kong (gateway) | **Port**: 8000

## Overview

Supabase provides PostgreSQL database with pgvector extension for embeddings, authentication, real-time subscriptions, and file storage. It's the primary data layer for CBass.

## Quick Access

| Environment | URL |
|-------------|-----|
| Production | https://supabase.cbass.space |
| Local | http://localhost:8000 |

## First-Time Setup

1. Navigate to Supabase Studio URL
2. Login with credentials from `.env`:
   - Username: `DASHBOARD_USERNAME`
   - Password: `DASHBOARD_PASSWORD`

## Architecture

Supabase runs as multiple containers:

| Container | Port | Purpose |
|-----------|------|---------|
| kong | 8000, 8443 | API Gateway |
| db | 5432 | PostgreSQL database |
| auth | 9999 | Authentication (GoTrue) |
| rest | 3000 | REST API (PostgREST) |
| realtime | 4000 | WebSocket subscriptions |
| storage | 5000 | File storage |
| studio | 3000 | Dashboard UI |
| pooler | 6543 | Connection pooler |

## Common Tasks

### Access Database

**Via Studio UI:**
1. Go to Table Editor
2. Browse/create tables
3. Run SQL queries

**Via psql:**
```bash
docker exec -it db psql -U postgres
```

### Create Table with Vector Column

```sql
-- Enable pgvector (if not already)
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with embedding column
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding vector(1536)
);

-- Create index for similarity search
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);
```

### Vector Similarity Search

```sql
-- Find similar documents
SELECT content, embedding <=> '[0.1, 0.2, ...]'::vector AS distance
FROM documents
ORDER BY distance
LIMIT 5;
```

## Integration with Other Services

| Service | How to Connect |
|---------|----------------|
| n8n | Postgres credential, host: `db`, port: 5432 |
| Flowise | PostgreSQL connection string |
| Direct | `postgresql://postgres:PASSWORD@db:5432/postgres` |

**Important**: Use container name `db`, not `localhost`.

## Connection String

```
postgresql://postgres:YOUR_POSTGRES_PASSWORD@db:5432/postgres
```

**Warning**: `POSTGRES_PASSWORD` cannot contain `@` character.

## Troubleshooting

### Problem: Pooler restarting
**Solution**:
Known issue. See [GitHub #30210](https://github.com/supabase/supabase/issues/30210).
Pooler is optional - direct connections still work.

### Problem: Analytics startup failure
**Solution**:
After changing Postgres password, delete and reinitialize:
```bash
rm -rf supabase/docker/volumes/db/data
python3 start_services.py --profile cpu
```

### Problem: Service unavailable
**Solution**:
- Verify no `@` in `POSTGRES_PASSWORD`
- Check containers: `docker compose -p localai ps`
- View logs: `docker compose -p localai logs kong`

### Problem: Files not found
**Solution**:
Delete and re-clone supabase:
```bash
rm -rf supabase/
python3 start_services.py --profile cpu
```

## Biology Applications

| Use Case | Implementation |
|----------|----------------|
| Species database | Table with species info, taxonomy |
| Experimental data | Store lab results, measurements |
| Research papers | Store metadata with vector embeddings |
| User auth | Supabase Auth for study app |
| File storage | Store PDFs, images of specimens |

## API Access

### REST API

```bash
# List tables (requires API key)
curl "http://localhost:8000/rest/v1/" \
  -H "apikey: YOUR_ANON_KEY" \
  -H "Authorization: Bearer YOUR_ANON_KEY"
```

### JavaScript Client

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'http://localhost:8000',
  'YOUR_ANON_KEY'
)

const { data } = await supabase
  .from('documents')
  .select('*')
```

## Backup

### Database Dump

```bash
# Full backup
docker exec -it db pg_dump -U postgres postgres > backup.sql

# Restore
docker exec -i db psql -U postgres postgres < backup.sql
```

### Specific Tables

```bash
docker exec -it db pg_dump -U postgres -t tablename postgres > table_backup.sql
```

## Environment Variables

Key Supabase variables in `.env`:

```bash
POSTGRES_PASSWORD=         # Database password (no @)
JWT_SECRET=                # For auth tokens
ANON_KEY=                  # Public API key
SERVICE_ROLE_KEY=          # Admin API key
DASHBOARD_USERNAME=        # Studio login
DASHBOARD_PASSWORD=        # Studio password
```

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [Supabase Self-Hosting](https://supabase.com/docs/guides/self-hosting)
