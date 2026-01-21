# Neo4j - Graph Database

**URL**: https://neo4j.cbass.space | **Container**: neo4j | **Port**: 7474 (Browser), 7687 (Bolt)

## Overview

Neo4j is a graph database for storing and querying connected data. Use it for knowledge graphs, relationship mapping, and network analysis - ideal for modeling biological pathways and taxonomies.

## Quick Access

| Environment | URL | Protocol |
|-------------|-----|----------|
| Production | https://neo4j.cbass.space | Browser |
| Local Browser | http://localhost:7474 | Browser |
| Bolt | bolt://neo4j:7687 | Cypher queries |

## First-Time Setup

1. Navigate to Neo4j Browser URL
2. Connect with credentials from `.env`:
   - Connect URL: `neo4j://localhost:7687` (local) or `neo4j://neo4j:7687` (container)
   - Username: `neo4j`
   - Password: From `NEO4J_AUTH` (format: `neo4j/password`)

## Common Tasks

### Create Nodes

```cypher
// Create a gene node
CREATE (g:Gene {name: "BRCA1", chromosome: 17})

// Create a protein node
CREATE (p:Protein {name: "BRCA1 protein", function: "DNA repair"})
```

### Create Relationships

```cypher
// Gene encodes protein
MATCH (g:Gene {name: "BRCA1"})
MATCH (p:Protein {name: "BRCA1 protein"})
CREATE (g)-[:ENCODES]->(p)
```

### Query Relationships

```cypher
// Find all proteins encoded by a gene
MATCH (g:Gene)-[:ENCODES]->(p:Protein)
RETURN g.name, p.name

// Find path between nodes
MATCH path = shortestPath((a:Gene)-[*]-(b:Gene))
WHERE a.name = "BRCA1" AND b.name = "TP53"
RETURN path
```

### Delete Data

```cypher
// Delete specific node and relationships
MATCH (n:Gene {name: "BRCA1"})
DETACH DELETE n

// Clear entire database (careful!)
MATCH (n) DETACH DELETE n
```

## Integration with Other Services

| Service | Configuration |
|---------|---------------|
| n8n | Neo4j credential: Host `neo4j`, Port `7687` |
| Flowise | Neo4j node: URL `bolt://neo4j:7687` |
| Python | `neo4j://neo4j:7687` with driver |

## Cypher Query Language

Basic syntax:

```cypher
// Pattern matching
MATCH (n:Label {property: "value"})

// Create
CREATE (n:Label {property: "value"})

// Relationships
(a)-[:RELATIONSHIP_TYPE]->(b)

// Return results
RETURN n.property

// Filter
WHERE n.property > 10

// Aggregate
RETURN count(n), avg(n.value)
```

## Troubleshooting

### Problem: Authentication failed
**Solution**:
- Check `NEO4J_AUTH` format: `neo4j/yourpassword`
- Restart container after changing password
- Try default: `neo4j/neo4j` (will prompt to change)

### Problem: Connection refused
**Solution**:
- Use `neo4j` hostname from containers
- Use `localhost` from host machine
- Verify container is running

### Problem: Browser shows "Server not available"
**Solution**:
- Wait 30-60 seconds for Neo4j to initialize
- Check logs: `docker compose -p localai logs neo4j`

## Biology Applications

| Use Case | Data Model |
|----------|------------|
| Metabolic pathways | (Metabolite)-[:CONVERTED_TO]->(Metabolite) |
| Gene interactions | (Gene)-[:REGULATES]->(Gene) |
| Taxonomy | (Species)-[:BELONGS_TO]->(Genus) |
| Protein interactions | (Protein)-[:BINDS]->(Protein) |
| Disease networks | (Gene)-[:ASSOCIATED_WITH]->(Disease) |

### Example: Gene Ontology Graph

```cypher
// Create GO terms
CREATE (bp:GOTerm {id: "GO:0006915", name: "apoptotic process", type: "biological_process"})
CREATE (mf:GOTerm {id: "GO:0005515", name: "protein binding", type: "molecular_function"})

// Link gene to GO terms
MATCH (g:Gene {name: "BRCA1"})
MATCH (bp:GOTerm {id: "GO:0006915"})
CREATE (g)-[:INVOLVED_IN]->(bp)
```

## Data Import

### CSV Import

```cypher
// Load genes from CSV
LOAD CSV WITH HEADERS FROM 'file:///genes.csv' AS row
CREATE (g:Gene {name: row.name, chromosome: toInteger(row.chr)})
```

Place CSV files in `neo4j/import/` directory.

### APOC Procedures

Neo4j includes APOC library for advanced operations:

```cypher
// Check APOC is available
RETURN apoc.version()

// JSON import
CALL apoc.load.json('https://api.example.com/data')
YIELD value
CREATE (n:Item) SET n = value
```

## Backup

```bash
# Stop Neo4j first
docker compose -p localai stop neo4j

# Copy data directory
cp -r neo4j/data neo4j-backup-$(date +%Y%m%d)

# Restart
docker compose -p localai start neo4j
```

## Data Storage

Data persists in local directory:
- `neo4j/data/` - Database files
- `neo4j/logs/` - Log files
- `neo4j/import/` - Files for LOAD CSV

## Resources

- [Neo4j Documentation](https://neo4j.com/docs/)
- [Cypher Manual](https://neo4j.com/docs/cypher-manual/)
- [Neo4j Browser Guide](https://neo4j.com/developer/neo4j-browser/)
- [APOC Library](https://neo4j.com/labs/apoc/)
