# Qdrant - Vector Database

**URL**: Internal only | **Container**: qdrant | **Port**: 6333 (REST), 6334 (gRPC)

## Overview

Qdrant is a high-performance vector database optimized for similarity search. Use it for RAG applications, semantic search, and recommendation systems.

## Quick Access

| Environment | URL |
|-------------|-----|
| REST API | http://qdrant:6333 |
| gRPC API | qdrant:6334 |
| Local (dev) | http://localhost:6333 |

Qdrant has a built-in dashboard at the REST endpoint.

## First-Time Setup

Qdrant requires no initial configuration - it's ready to use on startup.

## Common Tasks

### Create a Collection

```bash
curl -X PUT "http://localhost:6333/collections/biology_papers" \
  -H "Content-Type: application/json" \
  -d '{
    "vectors": {
      "size": 1536,
      "distance": "Cosine"
    }
  }'
```

### Insert Vectors

```bash
curl -X PUT "http://localhost:6333/collections/biology_papers/points" \
  -H "Content-Type: application/json" \
  -d '{
    "points": [
      {
        "id": 1,
        "vector": [0.1, 0.2, ...],
        "payload": {"title": "DNA Structure", "author": "Watson"}
      }
    ]
  }'
```

### Search Similar Vectors

```bash
curl -X POST "http://localhost:6333/collections/biology_papers/points/search" \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [0.1, 0.2, ...],
    "limit": 5
  }'
```

### List Collections

```bash
curl "http://localhost:6333/collections"
```

## Integration with Other Services

| Service | Configuration |
|---------|---------------|
| n8n | Qdrant credential: URL `http://qdrant:6333` |
| Flowise | Qdrant node: URL `http://qdrant:6333` |
| LangChain | `QdrantClient(host="qdrant", port=6333)` |

## Vector Dimensions

Common embedding dimensions:

| Model | Dimensions |
|-------|------------|
| OpenAI text-embedding-3-small | 1536 |
| OpenAI text-embedding-3-large | 3072 |
| nomic-embed-text (Ollama) | 768 |
| all-MiniLM-L6-v2 | 384 |

**Important**: Collection vector size must match your embedding model.

## Troubleshooting

### Problem: Collection not found
**Solution**:
- Check collection exists: `curl http://localhost:6333/collections`
- Create collection first before inserting

### Problem: Dimension mismatch
**Solution**:
- Verify embedding model output size
- Recreate collection with correct dimensions
- Check embedding generation is working

### Problem: Connection refused
**Solution**:
- Use container name `qdrant` from other containers
- Use `localhost` only from host machine
- Verify container is running

## Biology Applications

| Use Case | Implementation |
|----------|----------------|
| Paper search | Index research papers, find similar studies |
| Concept lookup | Find related biology concepts by meaning |
| Study material | Semantic search over textbook content |
| Species similarity | Vector similarity for taxonomy |

## RAG Pipeline Example

1. **Index documents**: Split text, generate embeddings, store in Qdrant
2. **Query**: Embed user question, search similar chunks
3. **Generate**: Pass retrieved context to LLM

```python
# Pseudo-code
embedding = ollama.embed(user_question)
results = qdrant.search(embedding, limit=5)
context = "\n".join([r.payload['text'] for r in results])
response = llm.generate(f"Context: {context}\n\nQuestion: {user_question}")
```

## Dashboard

Access built-in dashboard at `http://localhost:6333/dashboard`:
- View collections
- Browse points
- Run test queries

## Data Storage

Data persists in Docker volume:

```bash
docker volume inspect localai_qdrant
```

## Backup

```bash
# Create snapshot
curl -X POST "http://localhost:6333/collections/biology_papers/snapshots"

# List snapshots
curl "http://localhost:6333/collections/biology_papers/snapshots"
```

## Resources

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Qdrant REST API](https://qdrant.github.io/qdrant/redoc/index.html)
- [Qdrant GitHub](https://github.com/qdrant/qdrant)
