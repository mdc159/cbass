# Flowise Best Practices Guide

Based on analysis of the [Flowise Masterclass 2025](https://youtu.be/9TaRksXuLWY) examples and official [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise) documentation.

## Table of Contents
- [Architecture Patterns](#architecture-patterns)
- [Node Configuration](#node-configuration)
- [Memory Strategies](#memory-strategies)
- [Tool Integration](#tool-integration)
- [State Management](#state-management)
- [Temperature Guidelines](#temperature-guidelines)
- [Common Patterns by Use Case](#common-patterns-by-use-case)
- [RAG Setup (Official)](#rag-setup-official)
- [Streaming & Sessions (Official)](#streaming--sessions-official)
- [Monitoring & Observability (Official)](#monitoring--observability-official)
- [Security Configuration (Official)](#security-configuration-official)
- [Production Deployment (Official)](#production-deployment-official)
- [Environment Variables Reference (Official)](#environment-variables-reference-official)

---

## Architecture Patterns

### 1. Simple Chat (ChatGPT Clone)
```
ChatOpenAI → ConversationChain ← BufferWindowMemory
```
**Use when:** Building conversational assistants without external tools
**Components:** LLM + Memory + System Prompt

### 2. Tool Agent (Research Agent)
```
ChatOpenAI → Tool Agent ← BufferWindowMemory
                 ↑
         [Tools: SerpAPI, Calculator, Custom]
```
**Use when:** Agent needs to decide when to use external capabilities
**Components:** LLM + Memory + Tools array

### 3. RAG Agent (Customer Support)
```
ChatOpenAI → Tool Agent ← BufferWindowMemory
Document Store → Retriever Tool → Tool Agent
```
**Use when:** Answering questions from a knowledge base
**Components:** Vector Store + Retriever Tool + Agent

### 4. Structured Extraction (Invoice Analyzer)
```
ChatOpenAI → LLMChain ← PromptTemplate
                ↑
    StructuredOutputParser
```
**Use when:** Extracting specific fields from unstructured input
**Components:** LLM + Prompt Template + Output Parser

### 5. Sequential Team (Content Creation)
```
Start → Writer → Condition → Reviewer → Loop back to Writer
                    ↓
              Direct Reply (when done)
```
**Use when:** Iterative refinement with feedback loops
**Key insight:** Use message count conditions to limit iterations

### 6. Supervisor Team (Software Development)
```
         ┌─────────────────┐
         │   Supervisor    │
         └───────┬─────────┘
        ┌────────┼────────┐
        ↓        ↓        ↓
   Developer  Reviewer  Writer
```
**Use when:** Coordinating specialized roles
**Key insight:** All workers report to supervisor, no direct worker-to-worker communication

### 7. Deep Research (Planner + Parallel Execution)
```
Start → Planner → Iteration Block → Subagents (parallel) → Writer → Condition
                                                              ↑        ↓
                                                         Loop back or Reply
```
**Use when:** Multi-perspective research or data gathering
**Key insight:** Planner creates task array, iteration block parallelizes execution

---

## Node Configuration

### Chat Models (ChatOpenAI)
| Parameter | Recommended Value | Notes |
|-----------|-------------------|-------|
| `streaming` | `true` | Better UX for all chat applications |
| `modelName` | `gpt-4o-mini` | Cost-effective default; use `gpt-4o` for complex reasoning |
| `temperature` | See [guidelines](#temperature-guidelines) | Task-dependent |
| `maxTokens` | Leave empty | Let model decide unless you need limits |

### Conversation Chain
| Parameter | Recommended Value | Notes |
|-----------|-------------------|-------|
| `systemMessagePrompt` | Clear role definition | "You are a helpful assistant that..." |
| Memory | Always connect | BufferWindowMemory for most cases |

### Tool Agent
| Parameter | Recommended Value | Notes |
|-----------|-------------------|-------|
| `maxIterations` | 10-20 | Prevents infinite loops |
| `systemMessage` | Include tool usage guidance | Explain when/how to use each tool |

### Retriever Tool
| Parameter | Recommended Value | Notes |
|-----------|-------------------|-------|
| `description` | Detailed and specific | This determines when the agent uses it |
| `returnSourceDocuments` | `true` | For citations and transparency |

---

## Memory Strategies

### BufferWindowMemory (Most Common)
```json
{
  "k": 20,
  "memoryKey": "chat_history"
}
```
- Keeps last K message exchanges
- Good for: General chat, tool agents
- Trade-off: Loses older context

### SQLiteAgentMemory (Persistent)
- Survives across sessions
- Good for: Long-running workflows, content creation teams
- Trade-off: More storage, slower

### Agentflow Memory Options
| Strategy | Use Case |
|----------|----------|
| `allMessages` | Full history needed |
| `windowSize` | Recent context sufficient |
| `conversationSummary` | Long conversations |
| `conversationSummaryBuffer` | Balance of both |

### Best Practice
- **Short interactions:** BufferWindowMemory with k=10-20
- **Long sessions:** Summary-based memory
- **Persistent workflows:** SQLiteAgentMemory

---

## Tool Integration

### Tool Selection Principles
1. **Match tools to agent role** - A researcher needs search tools, a coder needs code execution
2. **Provide clear descriptions** - The agent uses descriptions to decide when to call tools
3. **Limit tool count** - 3-5 tools per agent works best; too many confuses the model

### Common Tool Combinations

| Agent Type | Tools |
|------------|-------|
| Research Agent | SerpAPI, Arxiv, Web Scraper |
| Data Analyst | Calculator, SQL Query, Chart Generator |
| Customer Support | Retriever Tool (FAQ/docs) |
| Content Creator | SerpAPI (research), Custom Tool (formatting) |

### Tool Description Best Practice
```
❌ Bad:  "Search the web"
✅ Good: "Search the web for current information about topics not in your training data. Use for recent news, prices, or facts that may have changed."
```

---

## State Management

### Flow State (Agentflows)
Use for coordinating between nodes:
```javascript
// Initialize in Start node
{
  "subagents": [],
  "findings": ""
}

// Access in other nodes
$flow.state.findings
```

### When to Use State
- Accumulating results across iterations
- Passing structured data between agents
- Tracking workflow progress
- Storing planner outputs for executor nodes

### State Keys Pattern
```javascript
// Planning phase
$flow.state.tasks = [/* planned tasks */]

// Execution phase
$flow.state.results = [/* accumulated results */]

// Synthesis phase
$flow.state.finalReport = "..."
```

---

## Temperature Guidelines

| Task Type | Temperature | Reasoning |
|-----------|-------------|-----------|
| Creative writing | 0.8-0.9 | Diverse, interesting outputs |
| Research/exploration | 0.7-0.9 | Explore different angles |
| General chat | 0.5-0.7 | Balance creativity and coherence |
| Supervisor routing | 0.3-0.5 | Consistent, deterministic decisions |
| Data extraction | 0.1-0.3 | Accurate, predictable outputs |
| Code generation | 0.2-0.4 | Correct syntax, logical code |

### Multi-Agent Temperature Strategy
```
Planner:     0.9  (creative task breakdown)
Researchers: 0.7  (thorough exploration)
Supervisor:  0.5  (reliable routing)
Writer:      0.6  (coherent synthesis)
```

---

## Common Patterns by Use Case

### Biology Learning Assistant
```
Pattern: RAG Agent
Components:
- Document Store with biology textbooks/papers
- Retriever Tool with description: "Search biology knowledge base for concepts, definitions, and explanations"
- Tool Agent with system prompt focused on educational explanations
- BufferWindowMemory for conversation context
```

### Research Paper Analyzer
```
Pattern: Structured Extraction
Components:
- PromptTemplate with fields: title, authors, abstract, methodology, findings, limitations
- StructuredOutputParser enforcing JSON schema
- LLMChain with low temperature (0.2)
```

### Study Group Tutor
```
Pattern: Supervisor Team
Workers:
- Explainer: Breaks down complex concepts
- Quiz Master: Creates practice questions
- Fact Checker: Verifies information accuracy
Supervisor routes based on student needs
```

### Literature Review Assistant
```
Pattern: Deep Research
Components:
- Planner creates search queries for different aspects
- Subagents search Arxiv, PubMed (via SerpAPI), web sources
- Writer synthesizes findings with citations
- Condition checks if more sources needed
```

---

## Anti-Patterns to Avoid

### ❌ Too Many Tools
- Problem: Agent gets confused, makes poor tool choices
- Solution: Limit to 3-5 well-described tools per agent

### ❌ Missing Memory
- Problem: Agent forgets context, repeats itself
- Solution: Always connect appropriate memory node

### ❌ Vague Tool Descriptions
- Problem: Agent uses tools inappropriately
- Solution: Write specific descriptions with usage criteria

### ❌ Hardcoded Iteration Counts
- Problem: Workflow stops too early or runs forever
- Solution: Use conditions based on output quality/completeness

### ❌ Direct Worker-to-Worker Communication
- Problem: Uncoordinated, chaotic workflow
- Solution: Route through supervisor for team patterns

### ❌ Single Temperature for All Agents
- Problem: Creative agents are too rigid, routing is unpredictable
- Solution: Match temperature to task type

---

## Quick Start Templates

### 1. Simple Q&A Bot
```
Nodes: ChatOpenAI → ConversationChain ← BufferWindowMemory
Config: temp=0.7, k=20, streaming=true
```

### 2. Document Q&A
```
Nodes: Document Store → Retriever Tool → Tool Agent ← Memory
Config: returnSourceDocuments=true, temp=0.6
```

### 3. Data Extractor
```
Nodes: PromptTemplate + StructuredOutputParser → LLMChain ← ChatOpenAI
Config: temp=0.2, define JSON schema in parser
```

### 4. Research Team
```
Nodes: Start → Planner → Iteration → Subagents → Writer → Condition
Config: Planner temp=0.9, use flow state for coordination
```

---

## RAG Setup (Official)

### Vector Store Configuration

**Supported Vector Stores:**
- Postgres (pgvector), Supabase, Qdrant, Pinecone, Chroma, Milvus
- Redis, Elasticsearch, OpenSearch, Weaviate, Faiss (in-memory)
- MongoDB Atlas, Couchbase, Zep, and more

### Postgres Vector Store Environment Variables
```bash
POSTGRES_VECTORSTORE_HOST=localhost
POSTGRES_VECTORSTORE_PORT=5432
POSTGRES_VECTORSTORE_USER=postgres
POSTGRES_VECTORSTORE_PASSWORD=password
POSTGRES_VECTORSTORE_DATABASE=flowise
POSTGRES_VECTORSTORE_TABLE_NAME=documents          # default: "documents"
POSTGRES_VECTORSTORE_CONTENT_COLUMN_NAME=pageContent # default: "pageContent"
POSTGRES_VECTORSTORE_SSL=false
```

### Record Manager (Deduplication)

Use a Record Manager to prevent duplicate embeddings during re-indexing:

```bash
POSTGRES_RECORDMANAGER_HOST=localhost
POSTGRES_RECORDMANAGER_PORT=5432
POSTGRES_RECORDMANAGER_USER=postgres
POSTGRES_RECORDMANAGER_PASSWORD=password
POSTGRES_RECORDMANAGER_DATABASE=flowise
POSTGRES_RECORDMANAGER_TABLE_NAME=upsertion_records  # default
POSTGRES_RECORDMANAGER_SSL=false
```

**Key insight:** Always use a Record Manager when documents may be re-processed to avoid storing duplicate vectors.

### Search Types

| Type | Use Case | Parameters |
|------|----------|------------|
| **Similarity** | Standard semantic search | `topK`: number of results (default: 4) |
| **MMR** | Diverse results | `fetchK`: initial fetch (default: 20), `lambda`: diversity 0-1 (default: 0.5) |

**MMR (Maximum Marginal Relevance):**
- `lambda = 0` → Maximum diversity
- `lambda = 1` → Maximum relevance (most similar)
- `lambda = 0.5` → Balanced (recommended starting point)

### File Upload in Chat

From official VectorStoreUtils.ts:
> Uploaded files will be upserted on the fly to the vector store. Files will have metadata updated with chatId, allowing association with the conversation. When querying, metadata filters by chatId to retrieve session-specific files.

**Requirements:**
- Only one vector store can have file upload enabled at a time
- Must connect a Document Loader node (PDF, DOCX, TXT, etc.)

---

## Streaming & Sessions (Official)

### Session Management

**Key parameters:**
- `sessionId`: Unique identifier for conversation session
- `overrideConfig`: Runtime configuration overrides
- `vars`: Variables accessible in prompts

### Using Variables

**Static Variables** (defined in chatflow):
```javascript
$vars.variableName
```

**Runtime Variables** (passed via API):
```json
{
  "question": "Hello",
  "overrideConfig": {
    "vars": {
      "customValue": "data"
    }
  }
}
```

### Streaming SSE Events

When streaming is enabled, the response uses Server-Sent Events:

| Event | Description |
|-------|-------------|
| `start` | Stream initialization |
| `token` | Individual token output |
| `metadata` | Tool calls, sources, reasoning |
| `end` | Stream completion |
| `error` | Error during streaming |

---

## Monitoring & Observability (Official)

### Metrics Collection

Enable via environment variables:
```bash
ENABLE_METRICS=true
METRICS_PROVIDER=prometheus  # or: open_telemetry
METRICS_INCLUDE_NODE_METRICS=true
METRICS_SERVICE_NAME=FlowiseAI
```

### Prometheus Setup

Official Prometheus config (from `metrics/prometheus/prometheus.config.yml`):
```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'FlowiseAI'
    static_configs:
      - targets: ['localhost:3000']
    metrics_path: /api/v1/metrics/
    scheme: http
    authorization:
      type: Bearer
      credentials_file: '/etc/prometheus/api_key.txt'
```

### OpenTelemetry Setup

```bash
METRICS_PROVIDER=open_telemetry
METRICS_OPEN_TELEMETRY_METRIC_ENDPOINT=http://localhost:4318/v1/metrics
METRICS_OPEN_TELEMETRY_PROTOCOL=http  # http | grpc | proto
METRICS_OPEN_TELEMETRY_DEBUG=false
```

### Third-Party Observability

Flowise integrates with Langfuse for LLM observability. Enable via the analytic nodes in your chatflows.

### Logging Configuration

```bash
LOG_PATH=/path/to/logs
LOG_LEVEL=info  # error | warn | info | verbose | debug
DEBUG=true      # Print component-level logs

# Sanitize sensitive data in logs
LOG_SANITIZE_BODY_FIELDS=password,secret,token,apikey,api_key
LOG_SANITIZE_HEADER_FIELDS=authorization,x-api-key,cookie
```

---

## Security Configuration (Official)

### Secret Key Management

**Option 1: Local file (default)**
```bash
SECRETKEY_PATH=/path/to/.flowise
```

**Option 2: Override with specific key**
```bash
FLOWISE_SECRETKEY_OVERWRITE=your-32-char-encryption-key
```

**Option 3: AWS Secrets Manager**
```bash
SECRETKEY_STORAGE_TYPE=aws
SECRETKEY_AWS_ACCESS_KEY=your-access-key
SECRETKEY_AWS_SECRET_KEY=your-secret-key
SECRETKEY_AWS_REGION=us-west-2
SECRETKEY_AWS_NAME=FlowiseEncryptionKey
```

### CORS & Embedding

```bash
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
IFRAME_ORIGINS=https://yourdomain.com  # For chatbot embed
```

### Custom Functions Security

Control what Node.js modules can be used in Custom Tool/Function nodes:

```bash
# Built-in Node.js modules
TOOL_FUNCTION_BUILTIN_DEP=crypto,fs

# External npm packages
TOOL_FUNCTION_EXTERNAL_DEP=moment,lodash

# Allow all project dependencies (not recommended for production)
ALLOW_BUILTIN_DEP=false
```

### MCP (Model Context Protocol) Security

```bash
CUSTOM_MCP_SECURITY_CHECK=true
CUSTOM_MCP_PROTOCOL=sse  # sse | stdio
```

### HTTP Security

```bash
HTTP_DENY_LIST=internal-service.local,192.168.1.0/24
TRUST_PROXY=true  # Enable when behind reverse proxy
```

### Disable Nodes

Hide specific nodes from the UI:
```bash
DISABLED_NODES=bufferMemory,chatOpenAI  # comma-separated list
```

---

## Production Deployment (Official)

### Database Options

| Type | Use Case | Variables |
|------|----------|-----------|
| **SQLite** | Development, single instance | `DATABASE_PATH=/data/.flowise` |
| **PostgreSQL** | Production, multi-instance | See below |
| **MySQL** | Production alternative | Similar to PostgreSQL |

**PostgreSQL Configuration:**
```bash
DATABASE_TYPE=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=flowise
DATABASE_PASSWORD=password
DATABASE_NAME=flowise
DATABASE_SSL=true
DATABASE_SSL_KEY_BASE64=<base64-cert>  # For self-signed
```

### Storage Options

| Type | Use Case | Variables |
|------|----------|-----------|
| **Local** | Development | `BLOB_STORAGE_PATH=/data/storage` |
| **S3** | Production (AWS) | See below |
| **GCS** | Production (GCP) | See below |

**S3 Storage:**
```bash
STORAGE_TYPE=s3
S3_STORAGE_BUCKET_NAME=flowise-storage
S3_STORAGE_ACCESS_KEY_ID=your-key
S3_STORAGE_SECRET_ACCESS_KEY=your-secret
S3_STORAGE_REGION=us-west-2
S3_ENDPOINT_URL=https://custom-s3.example.com  # Optional for S3-compatible
S3_FORCE_PATH_STYLE=false
```

**Google Cloud Storage:**
```bash
STORAGE_TYPE=gcs
GOOGLE_CLOUD_STORAGE_PROJ_ID=your-project-id
GOOGLE_CLOUD_STORAGE_CREDENTIAL=/path/to/keyfile.json
GOOGLE_CLOUD_STORAGE_BUCKET_NAME=flowise-storage
GOOGLE_CLOUD_UNIFORM_BUCKET_ACCESS=true
```

### Queue Mode (Horizontal Scaling)

For high-load production deployments, use queue mode with Redis:

**Main Server:**
```bash
MODE=queue
QUEUE_NAME=flowise-queue
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your-password
```

**Worker Configuration:**
```bash
WORKER_PORT=5566
MODE=queue
QUEUE_NAME=flowise-queue
WORKER_CONCURRENCY=100000
REMOVE_ON_AGE=86400        # Remove completed jobs after 24h
REMOVE_ON_COUNT=10000      # Keep max 10k completed jobs
REDIS_HOST=localhost
REDIS_PORT=6379
```

**Queue Architecture:**
1. Main server sends execution ID to Redis queue
2. Available worker retrieves and processes the job
3. Worker notifies main server on completion
4. Scale by adding/removing worker instances

### Docker Deployment

**Data Persistence (Critical):**
```bash
DATABASE_PATH=/root/.flowise
LOG_PATH=/root/.flowise/logs
SECRETKEY_PATH=/root/.flowise
BLOB_STORAGE_PATH=/root/.flowise/storage
```

**Mount these paths as Docker volumes to persist data across container restarts.**

### Production Checklist

- [ ] Switch from SQLite to PostgreSQL/MySQL
- [ ] Configure external storage (S3/GCS) for uploads
- [ ] Set `FLOWISE_SECRETKEY_OVERWRITE` for consistent encryption
- [ ] Configure CORS for your domains
- [ ] Enable SSL (`DATABASE_SSL=true`)
- [ ] Set up monitoring (Prometheus/OpenTelemetry)
- [ ] Use queue mode for horizontal scaling
- [ ] Configure log sanitization for sensitive fields
- [ ] Disable unused nodes (`DISABLED_NODES`)
- [ ] Set appropriate file size limits (`FLOWISE_FILE_SIZE_LIMIT`)

---

## Environment Variables Reference (Official)

### Core Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | HTTP port | `3000` |
| `CORS_ORIGINS` | Allowed CORS origins | `*` |
| `IFRAME_ORIGINS` | Allowed iframe origins | `*` |
| `FLOWISE_FILE_SIZE_LIMIT` | Max upload size | `50mb` |
| `SHOW_COMMUNITY_NODES` | Show community nodes | `true` |
| `DISABLE_FLOWISE_TELEMETRY` | Opt out of telemetry | `false` |
| `DISABLED_NODES` | Comma-separated node names | - |
| `MODEL_LIST_CONFIG_JSON` | Custom model list path | - |

### Database

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_TYPE` | `sqlite`, `mysql`, `postgres` | `sqlite` |
| `DATABASE_PATH` | SQLite file location | `~/.flowise` |
| `DATABASE_HOST` | DB host (non-sqlite) | - |
| `DATABASE_PORT` | DB port | `5432` |
| `DATABASE_USER` | DB username | - |
| `DATABASE_PASSWORD` | DB password | - |
| `DATABASE_NAME` | Database name | - |
| `DATABASE_SSL` | Enable SSL | `false` |

### Security

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRETKEY_PATH` | Encryption key location | `packages/server` |
| `FLOWISE_SECRETKEY_OVERWRITE` | Override encryption key | - |
| `TOOL_FUNCTION_BUILTIN_DEP` | Allowed Node.js modules | - |
| `TOOL_FUNCTION_EXTERNAL_DEP` | Allowed npm packages | - |
| `ALLOW_BUILTIN_DEP` | Allow all project deps | `false` |
| `HTTP_DENY_LIST` | Blocked HTTP destinations | - |
| `CUSTOM_MCP_SECURITY_CHECK` | MCP security validation | `true` |

### Logging

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug logging | `false` |
| `LOG_PATH` | Log file directory | `./logs` |
| `LOG_LEVEL` | `error`, `warn`, `info`, `verbose`, `debug` | `info` |
| `LOG_JSON_SPACES` | JSON log formatting | `2` |

### Storage

| Variable | Description | Default |
|----------|-------------|---------|
| `STORAGE_TYPE` | `local`, `s3`, `gcs` | `local` |
| `BLOB_STORAGE_PATH` | Local storage path | `~/.flowise/storage` |
| `S3_STORAGE_*` | S3 configuration | - |
| `GOOGLE_CLOUD_*` | GCS configuration | - |

### Queue (Scaling)

| Variable | Description | Default |
|----------|-------------|---------|
| `MODE` | `main`, `queue` | `main` |
| `QUEUE_NAME` | Redis queue name | `flowise-queue` |
| `WORKER_PORT` | Worker health check port | - |
| `WORKER_CONCURRENCY` | Jobs per worker | `100000` |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `REDIS_PASSWORD` | Redis password | - |

### Metrics

| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_METRICS` | Enable metrics collection | `false` |
| `METRICS_PROVIDER` | `prometheus`, `open_telemetry` | - |
| `METRICS_INCLUDE_NODE_METRICS` | Per-node metrics | `true` |
| `METRICS_SERVICE_NAME` | Service identifier | `FlowiseAI` |

---

## Import/Export Procedures

### Exporting Workflows

**Single Flow Export** (from canvas menu):
- Downloads raw `{nodes, edges}` JSON
- Does NOT include metadata (name, type, id)
- Cannot be directly imported via "Load Data"
- Use only for sharing flow structure

**Export All** (Settings → Export Data):
- Downloads complete `ExportData.json` with all flows, tools, variables
- Includes full metadata for each item
- Preferred format for backups and migration
- Can be imported via "Load Data"

### Importing Workflows

**Recommended: Settings → Load Data**
```
Settings (gear icon) → Load Data → Select JSON file
```
- Accepts ExportData format (from "Export All" or `wrap_flowise.ps1`)
- Persists to database immediately
- Shows import errors clearly
- Handles all types: ChatFlows, AgentFlows, Tools, Variables

**Not Recommended: Canvas → Load Chatflow**
- Only loads flow into visual canvas (doesn't save to database)
- Errors fail silently (check browser DevTools console)
- Requires raw `{nodes, edges}` format
- Must manually save after loading

### Converting Raw Exports to ExportData Format

Use the CBass `wrap_flowise.ps1` script:

```powershell
# Convert all files in flowise directory
.\wrap_flowise.ps1 -Path "flowise"
# Output: flowise/flowise-import.json

# Convert single file
.\wrap_flowise.ps1 -Path "flowise\MyWorkflow.json"
# Output: flowise/MyWorkflow-exportdata.json

# Then import via: Settings → Load Data
```

The script:
- Auto-detects flow type (AgentFlow vs ChatFlow) from node types
- Generates proper UUIDs for each flow
- Recognizes and includes Tool files
- Creates ExportData format with all 15 required arrays

### ExportData Format Reference

```json
{
  "AgentFlow": [],
  "AgentFlowV2": [
    {
      "id": "uuid-string",
      "name": "Flow Name",
      "flowData": "{\"nodes\":[...],\"edges\":[...]}",
      "type": "AGENTFLOW"
    }
  ],
  "ChatFlow": [...],
  "Tool": [
    {
      "name": "tool_name",
      "description": "Tool description",
      "schema": "[{\"property\":\"input\",\"type\":\"string\"}]",
      "func": "// JavaScript function code"
    }
  ],
  "AssistantFlow": [],
  "AssistantCustom": [],
  "AssistantOpenAI": [],
  "AssistantAzure": [],
  "ChatMessage": [],
  "ChatMessageFeedback": [],
  "CustomTemplate": [],
  "DocumentStore": [],
  "DocumentStoreFileChunk": [],
  "Execution": [],
  "Variable": []
}
```

### Backup Strategy

1. **Regular exports**: Use "Export All" from Settings periodically
2. **Version control**: Store ExportData.json files in git
3. **VPS backup**: Backup Docker volume directly
   ```bash
   # Create backup
   docker cp flowise:/root/.flowise ./flowise-backup-$(date +%Y%m%d)

   # Restore if needed
   docker cp ./flowise-backup-YYYYMMDD/. flowise:/root/.flowise/
   docker compose -p localai restart flowise
   ```

### Troubleshooting Import Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| "Load Chatflow" does nothing | Silent JSON parse error | Check browser DevTools console |
| Flow loads but doesn't save | Using canvas load, not "Load Data" | Use Settings → Load Data instead |
| Import shows error | Invalid format | Convert to ExportData format first |
| Duplicate flows after import | Same flow imported multiple times | Delete duplicates in UI |

---

## Resources

- **Video Tutorial:** [Flowise Masterclass 2025](https://youtu.be/9TaRksXuLWY)
- **Example Flows:** `references/flowise-masterclass/`
- **Live Instance:** https://flowise.cbass.space
- **Official Docs:** https://docs.flowiseai.com
- **Official Repo:** https://github.com/FlowiseAI/Flowise
- **Environment Variables:** https://docs.flowiseai.com/configuration/environment-variables
- **Deployment Guides:** https://docs.flowiseai.com/configuration/deployment

---

*Generated from analysis of leonvanzyl/flowise-masterclass-2025 examples and official FlowiseAI/Flowise repository*
