# Langfuse - LLM Observability

**URL**: https://langfuse.cbass.space | **Container**: langfuse-web | **Port**: 3000

## Overview

Langfuse provides observability and analytics for LLM applications. Track prompts, responses, latency, costs, and user feedback to debug and improve your AI workflows.

## Quick Access

| Environment | URL |
|-------------|-----|
| Production | https://langfuse.cbass.space |
| Local | http://localhost:3000 |

## First-Time Setup

1. Navigate to Langfuse URL
2. Click "Sign up" to create account
3. Create a project
4. Generate API keys in project settings

## Architecture

Langfuse runs as multiple containers:

| Container | Purpose |
|-----------|---------|
| langfuse-web | Web UI and API |
| langfuse-worker | Background processing |
| clickhouse | Analytics database |
| minio | S3-compatible storage |

## Common Tasks

### Create API Keys

1. Go to Settings > API Keys
2. Click "Create API Key"
3. Copy Public Key and Secret Key

### View Traces

1. Go to Traces in sidebar
2. Filter by time, model, user
3. Click trace to see details

### Analyze Costs

1. Go to Analytics > Cost
2. View by model, user, or time
3. Export data as CSV

## Integration with Other Services

### n8n Integration

Use HTTP Request node to send traces:

```json
{
  "url": "https://langfuse.cbass.space/api/public/traces",
  "method": "POST",
  "headers": {
    "Authorization": "Basic base64(publicKey:secretKey)"
  },
  "body": {
    "name": "my-trace",
    "input": "user message",
    "output": "assistant response"
  }
}
```

### Python SDK

```python
from langfuse import Langfuse

langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://langfuse.cbass.space"
)

# Create trace
trace = langfuse.trace(name="biology-qa")

# Log generation
generation = trace.generation(
    name="llm-call",
    model="llama3.1",
    input="What is DNA?",
    output="DNA is..."
)
```

### JavaScript SDK

```javascript
import Langfuse from "langfuse";

const langfuse = new Langfuse({
  publicKey: "pk-...",
  secretKey: "sk-...",
  baseUrl: "https://langfuse.cbass.space"
});

const trace = langfuse.trace({ name: "biology-qa" });
```

## Key Metrics

| Metric | What It Shows |
|--------|---------------|
| Traces | Individual conversations/sessions |
| Generations | LLM calls with input/output |
| Latency | Response time per call |
| Token usage | Input/output tokens per model |
| Cost | Estimated $ per model |
| Scores | User feedback ratings |

## Troubleshooting

### Problem: Traces not appearing
**Solution**:
- Check API keys are correct
- Verify network connectivity
- Check langfuse-worker is running
- Flush SDK: `langfuse.flush()`

### Problem: Dashboard slow
**Solution**:
- ClickHouse needs time to process
- Check ClickHouse container health
- Reduce date range filter

### Problem: Authentication error
**Solution**:
- Regenerate API keys
- Check key format (Public + Secret)
- Verify base URL includes https://

## Biology Applications

| Use Case | What to Track |
|----------|---------------|
| Study assistant | Track questions and answer quality |
| RAG performance | Compare retrieval vs generation quality |
| Prompt engineering | A/B test different prompts |
| Student progress | Track learning interactions |
| Cost monitoring | Monitor API usage for biology projects |

## Scores and Feedback

Add human feedback to traces:

```python
# In Python SDK
trace.score(
    name="accuracy",
    value=0.9,
    comment="Good explanation of photosynthesis"
)
```

Use scores to:
- Train evaluation models
- Identify poor responses
- Compare prompt versions

## Environment Variables

```bash
# Required in .env
CLICKHOUSE_PASSWORD=
MINIO_ROOT_PASSWORD=
LANGFUSE_SALT=
NEXTAUTH_SECRET=
ENCRYPTION_KEY=

# Hostname (production)
LANGFUSE_HOSTNAME=langfuse.cbass.space
```

## Data Storage

| Data | Storage |
|------|---------|
| Traces, spans | ClickHouse |
| Files, exports | MinIO |
| User accounts | PostgreSQL |

## Resources

- [Langfuse Documentation](https://langfuse.com/docs)
- [Langfuse Python SDK](https://langfuse.com/docs/sdk/python)
- [Langfuse Self-Hosting](https://langfuse.com/docs/deployment/self-host)
