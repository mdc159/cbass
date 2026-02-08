# SearXNG - Meta Search Engine

**URL**: https://searxng.cbass.space | **Container**: searxng | **Port**: 8080

## Overview

SearXNG is a privacy-respecting meta search engine that aggregates results from multiple search providers. Use it for research without tracking, or integrate with AI workflows for web search capabilities.

## Quick Access

| Environment | URL |
|-------------|-----|
| Production | https://searxng.cbass.space |
| Local | http://localhost:8081 |

## First-Time Setup

SearXNG works out of the box. No account needed.

## Common Tasks

### Web Search

1. Navigate to SearXNG URL
2. Enter search query
3. Filter by categories (general, images, news, science, etc.)

### Configure Search Engines

1. Click Preferences (gear icon)
2. Select Engines tab
3. Enable/disable search providers
4. Save preferences

### API Search (JSON)

```bash
curl "http://localhost:8081/search?q=photosynthesis&format=json"
```

## Integration with Other Services

### n8n Integration

Use HTTP Request node:

```json
{
  "url": "http://searxng:8080/search",
  "method": "GET",
  "qs": {
    "q": "{{ $json.query }}",
    "format": "json",
    "categories": "science"
  }
}
```

### Flowise Integration

Use SearXNG as a tool in agents for web search capability.

## Search Categories

| Category | Content |
|----------|---------|
| general | Web pages |
| images | Image search |
| news | News articles |
| science | Academic/scientific |
| files | File downloads |
| videos | Video content |
| social media | Social posts |

## Academic Search Engines

Enable these for biology research:

| Engine | Content |
|--------|---------|
| Google Scholar | Academic papers |
| PubMed | Biomedical literature |
| Semantic Scholar | AI-powered academic |
| BASE | Bielefeld Academic Search |
| arXiv | Preprints (physics, bio, CS) |

## Troubleshooting

### Problem: Container restarting
**Solution**:
```bash
chmod 755 searxng
docker compose -p localai restart searxng
```

### Problem: No search results
**Solution**:
- Check internet connectivity
- Some engines may be rate-limited
- Try different search engines
- Check SearXNG logs

### Problem: Slow searches
**Solution**:
- Reduce number of enabled engines
- Increase timeout in settings
- Use specific category filters

## Biology Applications

| Use Case | How To |
|----------|--------|
| Literature search | Use science category, enable Google Scholar |
| Image references | Search images for diagrams, specimens |
| News monitoring | Track biology news without tracking |
| Multi-source research | Compare results across engines |

## Configuration

SearXNG config is auto-generated in `searxng/` directory on first run.

Key settings in `searxng/settings.yml`:

```yaml
general:
  instance_name: "CBass Search"

search:
  default_lang: "en"

server:
  secret_key: auto-generated
```

## API Response Format

```json
{
  "query": "photosynthesis",
  "results": [
    {
      "title": "Photosynthesis - Wikipedia",
      "url": "https://en.wikipedia.org/wiki/Photosynthesis",
      "content": "Description text...",
      "engine": "google"
    }
  ],
  "suggestions": ["chlorophyll", "light reaction"]
}
```

## Privacy Features

- No tracking cookies
- No search history stored
- No IP logging
- Results from multiple sources
- Self-hosted = full control

## Environment Variables

```bash
# In .env
SEARXNG_HOSTNAME=searxng.cbass.space
SEARXNG_UWSGI_WORKERS=4
SEARXNG_UWSGI_THREADS=4
```

## Resources

- [SearXNG Documentation](https://docs.searxng.org/)
- [SearXNG GitHub](https://github.com/searxng/searxng)
- [Available Engines](https://docs.searxng.org/user/configured_engines.html)
