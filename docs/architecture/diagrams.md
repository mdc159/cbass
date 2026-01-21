# Architecture Diagrams

Visual representations of CBass architecture.

## High-Level Architecture

```mermaid
graph TB
    subgraph Internet
        User[User Browser]
    end

    subgraph "Reverse Proxy"
        Caddy[Caddy :80/:443]
    end

    subgraph "Frontend Layer"
        Dashboard[Dashboard :3000]
        OpenWebUI[Open WebUI :8080]
        Flowise[Flowise :3001]
    end

    subgraph "Workflow & AI Layer"
        N8N[n8n :5678]
        Ollama[Ollama :11434]
        Langfuse[Langfuse :3000]
    end

    subgraph "Data Layer"
        Supabase[Supabase Kong :8000]
        Qdrant[Qdrant :6333]
        Neo4j[Neo4j :7474]
    end

    subgraph Utilities
        SearXNG[SearXNG :8080]
        Kali[Kali :6901]
    end

    User --> Caddy
    Caddy --> Dashboard
    Caddy --> OpenWebUI
    Caddy --> N8N
    Caddy --> Flowise
    Caddy --> Supabase
    Caddy --> Langfuse
    Caddy --> Neo4j
    Caddy --> SearXNG
    Caddy --> Kali

    OpenWebUI --> N8N
    N8N --> Ollama
    N8N --> Supabase
    N8N --> Qdrant
    N8N --> Neo4j
    Flowise --> Ollama
    Flowise --> Supabase
```

## Request Flow

```mermaid
sequenceDiagram
    participant User
    participant Caddy
    participant OpenWebUI
    participant n8n_pipe
    participant n8n
    participant Ollama
    participant Supabase
    participant Qdrant

    User->>Caddy: HTTPS Request
    Caddy->>OpenWebUI: Proxy to :8080
    OpenWebUI->>n8n_pipe: Chat Message
    n8n_pipe->>n8n: POST /webhook
    n8n->>Supabase: Query Context
    n8n->>Qdrant: Vector Search
    n8n->>Ollama: LLM Inference
    Ollama-->>n8n: Response
    n8n-->>n8n_pipe: JSON Response
    n8n_pipe-->>OpenWebUI: Display
    OpenWebUI-->>User: Chat Response
```

## RAG Pipeline

```mermaid
flowchart LR
    subgraph Ingestion
        Doc[Document] --> Chunk[Chunker]
        Chunk --> Embed[Embedder]
        Embed --> Store[(Vector DB)]
    end

    subgraph Query
        Q[Query] --> QEmbed[Embed Query]
        QEmbed --> Search[Vector Search]
        Search --> Store
        Store --> Context[Retrieved Context]
    end

    subgraph Generation
        Context --> Prompt[Prompt Template]
        Q --> Prompt
        Prompt --> LLM[Ollama]
        LLM --> Response[Response]
    end
```

## Network Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Internet                                │
│                         │                                   │
│                    [Firewall]                               │
│                    80, 443 only                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Caddy :80/:443                            │
│              (TLS Termination, Routing)                      │
└─────────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────┐
│              Docker Network: localai_default                 │
│                                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │   n8n    │ │ flowise  │ │ open-    │ │ ollama   │       │
│  │  :5678   │ │  :3001   │ │  webui   │ │  :11434  │       │
│  └──────────┘ └──────────┘ │  :8080   │ └──────────┘       │
│                            └──────────┘                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ supabase │ │  qdrant  │ │  neo4j   │ │ searxng  │       │
│  │   kong   │ │  :6333   │ │  :7474   │ │  :8080   │       │
│  │  :8000   │ └──────────┘ │  :7687   │ └──────────┘       │
│  └──────────┘              └──────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Supabase Architecture

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

## Data Flow Patterns

### Chat with Context (RAG)

```
1. User asks question
2. Question → Embedding model → Vector
3. Vector → Qdrant search → Similar documents
4. Documents + Question → Prompt template
5. Prompt → Ollama → Response
6. Response → User
```

### Knowledge Graph Query

```
1. User asks about relationships
2. Extract entities from question
3. Query Neo4j graph
4. Traverse relationships
5. Combine graph data with LLM response
6. Enriched answer → User
```

### Automated Workflow

```
1. Trigger (webhook, schedule, etc.)
2. n8n executes workflow nodes
3. Nodes interact with:
   - Ollama (AI processing)
   - Supabase (data storage)
   - External APIs
4. Output to destination
```

## Deployment Modes

### Private (Development)

```
localhost:5678 → n8n
localhost:8080 → Open WebUI
localhost:3001 → Flowise
... all ports exposed
```

### Public (Production)

```
*.cbass.space → Caddy :443 → Internal services
                    │
                    ├── n8n.cbass.space → n8n:5678
                    ├── openwebui.cbass.space → open-webui:8080
                    ├── flowise.cbass.space → flowise:3001
                    └── ... etc
```
