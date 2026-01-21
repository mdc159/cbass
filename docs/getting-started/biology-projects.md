# Biology + AI Projects

Apply the CBass AI tools to biology learning.

## Beginner Projects

### 1. Biology Study Assistant

**Tools**: Open WebUI + Ollama

**Goal**: Chat with an AI tutor about biology topics

**Steps**:
1. Open http://localhost:8080
2. Start a new chat
3. Ask questions like:
   - "Explain the Krebs cycle step by step"
   - "What's the difference between mitosis and meiosis?"
   - "How do neurons transmit signals?"

**Tips**:
- Ask for analogies: "Explain it like I'm 10 years old"
- Request diagrams: "Describe what a diagram of this would look like"
- Quiz yourself: "Give me 5 practice questions about [topic]"

---

### 2. Flashcard Generator

**Tools**: n8n + Ollama

**Goal**: Auto-generate flashcards from biology text

**Workflow**:
1. Webhook receives biology text
2. AI generates Q&A pairs
3. Returns formatted flashcards

**AI Prompt**:
```
From the following biology text, create 5 flashcards.
Format each as:
Q: [question]
A: [answer]

Text: {{ $json.body.text }}
```

**Test**:
```bash
curl -X POST http://localhost:5678/webhook/flashcards \
  -d '{"text": "Photosynthesis is the process by which plants convert light energy into chemical energy. It occurs in chloroplasts and produces glucose and oxygen from carbon dioxide and water."}'
```

---

### 3. Research Paper Finder

**Tools**: n8n + SearXNG

**Goal**: Search for biology papers on a topic

**Workflow**:
1. Webhook receives search topic
2. SearXNG searches (science category)
3. Returns formatted results

**HTTP Request Configuration**:
```
URL: http://searxng:8080/search
Query: q={{ $json.body.topic }}&format=json&categories=science
```

---

## Intermediate Projects

### 4. Biology PDF Chat (RAG)

**Tools**: n8n + Supabase + Qdrant + Ollama

**Goal**: Upload a biology textbook PDF and ask questions

**Workflow**:
1. Upload PDF
2. Extract and chunk text
3. Generate embeddings (nomic-embed-text)
4. Store in Qdrant
5. Query with questions

**Import**: Use `V2_Local_Supabase_RAG_AI_Agent.json` from `n8n/backup/workflows/`

---

### 5. Species Database

**Tools**: Supabase

**Goal**: Build a searchable database of species

**Schema**:
```sql
CREATE TABLE species (
  id SERIAL PRIMARY KEY,
  scientific_name TEXT NOT NULL,
  common_name TEXT,
  kingdom TEXT,
  phylum TEXT,
  class TEXT,
  order_name TEXT,
  family TEXT,
  genus TEXT,
  description TEXT,
  habitat TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

**Extensions**:
- Add image URLs
- Add vector embeddings for semantic search
- Create API with n8n

---

### 6. Gene Interaction Graph

**Tools**: Neo4j

**Goal**: Model gene regulatory networks

**Cypher Queries**:
```cypher
// Create genes
CREATE (brca1:Gene {name: "BRCA1", chromosome: 17})
CREATE (tp53:Gene {name: "TP53", chromosome: 17})
CREATE (rb1:Gene {name: "RB1", chromosome: 13})

// Create relationships
CREATE (brca1)-[:INTERACTS_WITH]->(tp53)
CREATE (tp53)-[:REGULATES]->(rb1)

// Query: Find all genes TP53 regulates
MATCH (tp53:Gene {name: "TP53"})-[:REGULATES]->(target)
RETURN target.name
```

---

## Advanced Projects

### 7. Literature Monitor

**Tools**: n8n + SearXNG + Email/Slack

**Goal**: Get notified when new papers publish on your topic

**Workflow**:
1. Schedule (daily)
2. Search PubMed/Google Scholar via SearXNG
3. Filter for new results
4. Store seen papers in Supabase
5. Send notification for new ones

---

### 8. Metabolic Pathway Explorer

**Tools**: Neo4j + n8n + Open WebUI

**Goal**: Build and query metabolic pathway graphs

**Data Model**:
```cypher
// Nodes
(:Metabolite {name: "Glucose", formula: "C6H12O6"})
(:Enzyme {name: "Hexokinase", ec_number: "2.7.1.1"})
(:Pathway {name: "Glycolysis"})

// Relationships
(glucose)-[:CONVERTED_TO {enzyme: "Hexokinase"}]->(g6p)
(enzyme)-[:CATALYZES]->(reaction)
(metabolite)-[:PART_OF]->(pathway)
```

**Queries**:
- Find all steps in glycolysis
- What enzyme converts X to Y?
- Shortest path between two metabolites

---

### 9. Biology RAG with Knowledge Graph

**Tools**: n8n + Neo4j + Qdrant + Ollama

**Goal**: Combine vector search with knowledge graph for better answers

**Architecture**:
1. Query → Vector search (Qdrant) → Relevant passages
2. Query → Graph search (Neo4j) → Related concepts
3. Combine context → LLM → Enhanced answer

---

### 10. Lab Notebook Assistant

**Tools**: Flowise + Supabase + Ollama

**Goal**: AI-powered lab notebook that tracks experiments

**Features**:
- Log experiments via chat
- Search past experiments
- Generate reports
- Suggest next steps based on results

---

## Project Ideas by Tool

| Tool | Biology Projects |
|------|------------------|
| **Open WebUI** | Study Q&A, concept explanations, quiz prep |
| **n8n** | Paper monitoring, data pipelines, automated flashcards |
| **Flowise** | Study chatbots, flashcard generators, lab assistants |
| **Supabase** | Species databases, experiment logs, paper metadata |
| **Qdrant** | Semantic paper search, concept similarity, RAG |
| **Neo4j** | Gene networks, metabolic pathways, taxonomies |
| **Langfuse** | Track learning progress, analyze study patterns |
| **SearXNG** | Literature search, multi-source research |

## Learning Path

1. **Week 1**: Open WebUI basics, prompt engineering
2. **Week 2**: First n8n workflow, flashcard generator
3. **Week 3**: Supabase database, species tracker
4. **Week 4**: RAG pipeline, PDF chat
5. **Week 5**: Neo4j graphs, gene networks
6. **Week 6**: Combine tools, literature monitor

## Tips for Biology AI Projects

1. **Be specific**: "Explain photosynthesis" → "Explain the light-dependent reactions in photosynthesis"
2. **Request sources**: Ask the AI to cite concepts (then verify manually)
3. **Use examples**: "Give me examples of [process] in different organisms"
4. **Build gradually**: Start simple, add complexity
5. **Connect tools**: Each tool adds capability

## Resources

- [n8n AI Tutorial](https://docs.n8n.io/advanced-ai/intro-tutorial/)
- [PubMed API](https://www.ncbi.nlm.nih.gov/home/develop/api/)
- [KEGG Pathways](https://www.genome.jp/kegg/pathway.html)
- [UniProt API](https://www.uniprot.org/help/api)
