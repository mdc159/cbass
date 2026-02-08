# Your First n8n Workflow

Build a simple AI-powered workflow in 10 minutes.

## Goal

Create a webhook that receives a question, sends it to a local LLM, and returns the answer.

## Prerequisites

- CBass running (`python start_services.py --profile gpu-nvidia`)
- n8n account created (http://localhost:5678)

## Step 1: Create New Workflow

1. Open n8n at http://localhost:5678
2. Click **Add workflow**
3. Name it "My First AI Workflow"

## Step 2: Add Webhook Trigger

1. Click the **+** button to add a node
2. Search for "Webhook"
3. Click **Webhook** node
4. Configure:
   - **HTTP Method**: POST
   - **Path**: `ask-ai`
5. Click **Listen for test event** (we'll test later)

## Step 3: Add AI Model

1. Click the **+** button after Webhook
2. Search for "Chat Model"
3. Select **Ollama Chat Model**
4. Configure:
   - **Model**: `qwen2.5:7b-instruct-q4_K_M` (or any model you have)
   - **Base URL**: `http://ollama:11434`
5. Connect Webhook → Ollama Chat Model

## Step 4: Add AI Agent

1. Click **+** after the chat model
2. Search for "Agent"
3. Select **AI Agent**
4. Configure:
   - **Text**: `{{ $json.body.question }}`
   - (Connect the Ollama model as the chat model)

## Step 5: Add Response

1. Click **+** after AI Agent
2. Search for "Respond to Webhook"
3. Configure:
   - **Response Body**: `{{ $json.output }}`

## Step 6: Test the Workflow

1. Click **Test workflow** in n8n
2. In a terminal or Postman, send:

```bash
curl -X POST http://localhost:5678/webhook-test/ask-ai \
  -H "Content-Type: application/json" \
  -d '{"question": "What is photosynthesis?"}'
```

You should receive an AI-generated response about photosynthesis!

## Step 7: Activate

1. Click the **Active** toggle (top right)
2. Copy the **Production URL** for real use:
   - `http://localhost:5678/webhook/ask-ai`

## Understanding the Workflow

```
Webhook (receives question)
    ↓
Ollama Chat Model (connects to local LLM)
    ↓
AI Agent (processes question with LLM)
    ↓
Respond to Webhook (returns answer)
```

## Key Concepts

### Expression Syntax

n8n uses `{{ }}` for dynamic values:
- `{{ $json.body.question }}` - Get question from webhook body
- `{{ $json.output }}` - Get agent output

### Container Communication

Use container names, not localhost:
- Ollama: `http://ollama:11434`
- Qdrant: `http://qdrant:6333`
- PostgreSQL: `db:5432`

## Try It: Biology Enhancement

Make this workflow biology-focused:

1. Edit the AI Agent's **System Message**:
   ```
   You are a helpful biology tutor. Explain concepts clearly
   and use examples from the natural world. If asked about
   non-biology topics, politely redirect to biology.
   ```

2. Test with biology questions:
   ```bash
   curl -X POST http://localhost:5678/webhook/ask-ai \
     -H "Content-Type: application/json" \
     -d '{"question": "How does DNA replication work?"}'
   ```

## Next Steps

1. Add memory with Supabase or Qdrant
2. Import pre-built RAG workflows from `n8n/backup/workflows/`
3. Connect to Open WebUI using n8n_pipe
4. Explore more [biology project ideas](./biology-projects.md)

## Troubleshooting

### "No response from Ollama"

- Check Ollama is running: `docker compose -p localai ps ollama`
- Verify model exists: `docker exec -it ollama ollama list`

### Expression errors

- Always wrap in `{{ }}`
- Webhook data is in `.body`: `{{ $json.body.field }}`

### Workflow won't activate

- Check all nodes are connected
- Verify credentials are configured
- Look at error messages in node configuration
