# Architecture Diagrams

Visual representations of CBass architecture. Each diagram is also available as an editable FigJam board (links below).

## 1. System Overview

**[Open in FigJam](https://www.figma.com/online-whiteboard/create-diagram/abb94d8c-9106-4f76-9cab-8aaabfc378c6?utm_source=other&utm_content=edit_in_figjam)**

All services grouped by purpose: AI/Chat, Automation/Observability, Data, and Infrastructure.

```mermaid
graph LR
    subgraph Internet["Internet"]
        User["User Browser"]
    end

    subgraph VPS["VPS: sebastian (191.101.0.164)"]
        subgraph Proxy["Reverse Proxy"]
            Caddy["Caddy :80/:443 Auto-TLS"]
        end

        subgraph AI["AI & Chat"]
            OpenWebUI["Open WebUI :8080"]
            Ollama["Ollama :11434"]
            Flowise["Flowise :3001"]
        end

        subgraph Automation["Automation & Observability"]
            N8N["n8n :5678"]
            Langfuse["Langfuse :3000"]
            SearXNG["SearXNG :8081"]
        end

        subgraph Data["Data Layer"]
            Supabase["Supabase (Postgres + pgvector) :8000"]
            Qdrant["Qdrant :6333"]
            Neo4j["Neo4j :7474"]
            ClickHouse["ClickHouse"]
            MinIO["MinIO (S3) :9000"]
            Redis["Redis"]
        end

        subgraph Infra["Infrastructure"]
            Dashboard["Dashboard :3002"]
            Updater["Updater Webhook :9000"]
            Kali["Kali Desktop :6901"]
        end
    end

    User -->|"*.cbass.space"| Caddy
    Caddy --> OpenWebUI
    Caddy --> N8N
    Caddy --> Flowise
    Caddy --> Dashboard
    Caddy --> Langfuse
    Caddy --> Supabase
    Caddy --> Neo4j
    Caddy --> SearXNG
    Caddy --> Kali

    OpenWebUI --> Ollama
    N8N --> Ollama
    Flowise --> Ollama
    N8N --> Supabase
    N8N --> Qdrant
    Langfuse --> ClickHouse
    Langfuse --> MinIO
    Langfuse --> Redis
```

## 2. Network and Routing

**[Open in FigJam](https://www.figma.com/online-whiteboard/create-diagram/94d4e52b-cd6c-4bc3-8b53-ff454169d240?utm_source=other&utm_content=edit_in_figjam)**

Public mode routes through Caddy with auto-TLS. Private mode binds directly to localhost ports.

```mermaid
graph LR
    subgraph Public["Public Mode (VPS)"]
        DNS["*.cbass.space DNS"]
        CaddyPub["Caddy :80/:443"]
        DNS -->|"HTTPS"| CaddyPub
        CaddyPub -->|"cbass.space"| Dash1["Dashboard :3000"]
        CaddyPub -->|"n8n.cbass.space"| N8N1["n8n :5678"]
        CaddyPub -->|"openwebui.cbass.space"| OW1["Open WebUI :8080"]
        CaddyPub -->|"flowise.cbass.space"| FL1["Flowise :3001"]
        CaddyPub -->|"supabase.cbass.space"| SB1["Kong :8000"]
        CaddyPub -->|"langfuse.cbass.space"| LF1["Langfuse :3000"]
        CaddyPub -->|"neo4j.cbass.space"| NJ1["Neo4j :7474"]
        CaddyPub -->|"searxng.cbass.space"| SX1["SearXNG :8080"]
        CaddyPub -->|"kali.cbass.space"| KL1["Kali :6901"]
    end

    subgraph Private["Private Mode (macOS)"]
        Browser["localhost"]
        Browser -->|":3002"| Dash2["Dashboard"]
        Browser -->|":5678"| N8N2["n8n"]
        Browser -->|":8080"| OW2["Open WebUI"]
        Browser -->|":3001"| FL2["Flowise"]
        Browser -->|":8000"| SB2["Supabase"]
        Browser -->|":3000"| LF2["Langfuse"]
        Browser -->|":7474"| NJ2["Neo4j"]
        Browser -->|":8081"| SX2["SearXNG"]
    end
```

### Subdomain Routing Table

| Subdomain | Container | Internal Port |
|-----------|-----------|---------------|
| `cbass.space` | dashboard | :3000 |
| `n8n.cbass.space` | n8n | :5678 |
| `openwebui.cbass.space` | open-webui | :8080 |
| `flowise.cbass.space` | flowise | :3001 |
| `supabase.cbass.space` | kong | :8000 |
| `langfuse.cbass.space` | langfuse-web | :3000 |
| `neo4j.cbass.space` | neo4j | :7474 |
| `searxng.cbass.space` | searxng | :8080 |
| `kali.cbass.space` | kali | :6901 |

## 3. Data and Storage Layer

**[Open in FigJam](https://www.figma.com/online-whiteboard/create-diagram/040aa88a-f9b6-46ab-9c50-2b943ccd8993?utm_source=other&utm_content=edit_in_figjam)**

All persistent data stores, which services use them, and their Docker volume mappings.

```mermaid
graph LR
    subgraph Services["Services"]
        N8N["n8n"]
        OW["Open WebUI"]
        FL["Flowise"]
        LF["Langfuse"]
    end

    subgraph Databases["Databases"]
        PG["Supabase Postgres + pgvector"]
        Neo["Neo4j Graph DB"]
        CH["ClickHouse Analytics"]
    end

    subgraph VectorStores["Vector Stores"]
        QD["Qdrant"]
        PGV["pgvector (in Postgres)"]
    end

    subgraph ObjectStorage["Object Storage (S3)"]
        MIO["MinIO"]
    end

    subgraph Cache["Cache"]
        RD["Redis / Valkey"]
    end

    N8N -->|"workflows, credentials"| PG
    N8N -->|"RAG embeddings"| QD
    N8N -->|"RAG embeddings"| PGV
    OW -->|"chat history"| PG
    FL -->|"chatflows"| PG
    LF -->|"traces, events"| CH
    LF -->|"media, exports"| MIO
    LF -->|"sessions"| RD
```

### Docker Named Volumes

| Volume | Container | Mount Path | Purpose |
|--------|-----------|------------|---------|
| `n8n_storage` | n8n | `/home/node/.n8n` | Workflows, credentials, execution data |
| `ollama_storage` | ollama | `/root/.ollama` | Downloaded model weights |
| `qdrant_storage` | qdrant | `/qdrant/storage` | Vector embeddings and indexes |
| `open-webui` | open-webui | app data | Chat history, user settings |
| `flowise` | flowise | `/root/.flowise` | Chatflow definitions, uploads |
| `langfuse_postgres_data` | langfuse-db | `/var/lib/postgresql/data` | Langfuse traces and metadata |
| `langfuse_clickhouse_data` | clickhouse | `/var/lib/clickhouse` | Analytics events |
| `langfuse_minio_data` | minio | `/data` | S3-compatible object storage (media, exports) |
| `caddy-data` | caddy | `/data` | TLS certificates |
| `caddy-config` | caddy | `/config` | Caddy config state |
| `valkey-data` | redis | data | Session cache |
| `kali-data` | kali | `/home/kasm-user` | Kali user home directory |
| `kali-tools` | kali | tools | Installed security tools |

## 4. AI Request Flow (RAG Pipeline)

**[Open in FigJam](https://www.figma.com/online-whiteboard/create-diagram/fbfa2642-2f77-46d3-8e9a-fe6c35659bfd?utm_source=other&utm_content=edit_in_figjam)**

The path of a user question through the RAG pipeline.

```mermaid
sequenceDiagram
    participant U as User Browser
    participant OW as Open WebUI
    participant Pipe as n8n_pipe.py
    participant N8N as n8n Workflow
    participant EMB as Embedding Model
    participant VS as Vector Store (Qdrant/pgvector)
    participant LLM as LLM (Ollama/OpenAI)

    U->>OW: Ask question
    OW->>Pipe: Forward via pipe function
    Pipe->>N8N: POST webhook with question
    N8N->>EMB: Generate embedding for query
    EMB-->>N8N: Query vector
    N8N->>VS: Similarity search
    VS-->>N8N: Relevant context chunks
    N8N->>LLM: Prompt + context + question
    LLM-->>N8N: Generated answer
    N8N-->>Pipe: Response
    Pipe-->>OW: Display answer
    OW-->>U: Show response with sources
```

### Ollama Configuration (Apple Silicon)

On macOS, Ollama runs natively via Homebrew (not in Docker) for Metal GPU access:

| Setting | Value | Purpose |
|---------|-------|---------|
| Flash attention | On | Faster inference |
| KV cache | q8_0 | Halves memory vs fp16 |
| Context window | 8192 | Default context length |
| Max loaded models | 2 | Concurrent model limit |
| Model storage | `/Volumes/Storage` | External SSD |

Services reach Ollama via `host.docker.internal:11434` (macOS) or `ollama:11434` (Docker/VPS).

## 5. Update and Deploy Pipeline

**[Open in FigJam](https://www.figma.com/online-whiteboard/create-diagram/22db788a-33fa-495f-84c7-4a22320f3bba?utm_source=other&utm_content=edit_in_figjam)**

Two deployment paths: dashboard buttons for container updates, git for code changes.

```mermaid
graph LR
    subgraph DashUpdate["Dashboard Update Flow"]
        Click["Click Update Button"]
        API["Next.js /api/update"]
        Auth["Check Supabase Auth Cookie"]
        Webhook["Updater Webhook :9000"]
        Script["update-container.sh"]
        Pull["docker compose pull"]
        Up["docker compose up -d"]
        Prune["docker image prune"]

        Click -->|"POST {container}"| API
        API --> Auth
        Auth -->|"+ token"| Webhook
        Webhook -->|"$1 = container"| Script
        Script --> Pull
        Pull --> Up
        Up --> Prune
    end

    subgraph GitDeploy["Git Deploy Flow (VPS)"]
        Dev["Local Dev"]
        Push["git push origin master"]
        SSH["ssh cbass"]
        GPull["git pull"]
        Build["docker compose build"]
        Deploy["docker compose up -d"]

        Dev --> Push
        Push --> SSH
        SSH --> GPull
        GPull --> Build
        Build --> Deploy
    end
```

### Updatable Services

| Service | Container Name | Triggered By |
|---------|---------------|--------------|
| Open WebUI | `open-webui` | Dashboard button |
| n8n | `n8n` | Dashboard button |
| Flowise | `flowise` | Dashboard button |
| Langfuse | `langfuse-web` | Dashboard button |

The updater runs a custom Docker image (`scripts/Dockerfile`) with `bash`, `docker-cli`, and `docker-cli-compose`. The `COMPOSE_FILE` env var ensures recreated containers use the correct override file for their environment (private or public).

## Supabase Internal Architecture

```mermaid
flowchart TB
    subgraph "Supabase Stack"
        Kong[Kong :8000] --> Auth[GoTrue :9999]
        Kong --> Rest[PostgREST :3000]
        Kong --> Realtime[Realtime :4000]
        Kong --> Storage[Storage :5000]
        Kong --> Studio[Studio :3000]

        Auth --> DB[(PostgreSQL :5432)]
        Rest --> DB
        Realtime --> DB
        Storage --> DB

        Pooler[Supavisor :6543] --> DB
    end
```
