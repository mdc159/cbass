# Service: <Service Name>

## Summary

- **Purpose**: <Why this service exists in CBass>
- **Container**: `<container-name>`
- **Internal Port(s)**: `<port>`
- **Public URL**: `<subdomain or localhost>`

## Dependencies

- **Upstream**: <services this depends on>
- **Downstream**: <services that depend on this>

## Configuration

### Environment Variables

```bash
# Required
KEY=

# Optional
OPTIONAL_KEY=
```

### Volumes

- `<volume-name>` → `<path>`

## Operations

### Common Tasks

```bash
# Logs
docker compose -p localai logs -f <service>

# Restart
docker compose -p localai restart <service>
```

### Health Checks

- **URL**: `<health endpoint>`
- **Expected**: `<healthy response>`

## Troubleshooting

- **Symptom**: <what you see>
  - **Cause**: <why it happens>
  - **Fix**: <how to fix it>

## References

- Related docs or external links.
