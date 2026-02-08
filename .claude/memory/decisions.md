# Decisions

## Decisions

### DEC-001: Named volumes for Flowise
- **Date**: 2026-02-07
- **Context**: Flowise UI import was failing silently due to bind mount UID/GID mismatch
- **Decision**: Switched from `~/.flowise:/root/.flowise` to Docker named volume `flowise:/root/.flowise`
- **Alternatives**: Fix host permissions, run as non-root

### DEC-002: Educational biology focus
- **Date**: 2026-02-07
- **Context**: Needed a purpose for the platform beyond personal use
- **Decision**: Frame as educational tutorial platform; interweave AI tool learning with biology applications
- **Alternatives**: General-purpose AI playground, team collaboration focus
