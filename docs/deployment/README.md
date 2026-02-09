# Deployment Guide

CBass can be deployed locally for development or on a VPS for production.

## Deployment Options

| Mode | Use Case | Guide |
|------|----------|-------|
| **Local Development** | Learning, testing, development | [local-dev.md](./local-dev.md) |
| **VPS Production** | Public-facing deployment | [vps-setup.md](./vps-setup.md) |

## Prerequisites

### All Deployments

- [Python 3.x](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker + Docker Compose
- [Git](https://git-scm.com/)

### VPS Additional Requirements

- Ubuntu Linux server (recommended)
- Domain name with DNS access
- Ports 80 and 443 available

## GPU Profiles

| Profile | Flag | Use Case |
|---------|------|----------|
| `gpu-nvidia` | `--profile gpu-nvidia` | NVIDIA GPU with CUDA |
| `gpu-amd` | `--profile gpu-amd` | AMD GPU with ROCm (Linux) |
| `cpu` | `--profile cpu` | CPU-only inference |
| `none` | `--profile none` | External API only (no Ollama) |

## Environment Modes

| Mode | Flag | Behavior |
|------|------|----------|
| `private` | `--environment private` | All ports exposed locally |
| `public` | `--environment public` | Only 80/443 via Caddy |

## Quick Start Commands

```bash
# Local development (NVIDIA GPU)
python start_services.py --profile gpu-nvidia --environment private --open-dashboard

# Local development (CPU only)
python start_services.py --profile cpu --environment private --open-dashboard

# VPS production
python start_services.py --profile cpu --environment public
```

Optional startup convenience:
- `--open-dashboard` opens the dashboard in your default browser after startup.
- `--dashboard-url` overrides the default dashboard URL (`http://localhost:3002`).

## DNS & SSL

For production deployments, see [dns-ssl.md](./dns-ssl.md) for:
- DNS A record configuration
- Automatic SSL via Caddy/Let's Encrypt
- Subdomain routing setup

## Archived Guides

Previous deployment documentation has been archived for reference:
- [docs/archive/DEPLOYMENT.md](../archive/DEPLOYMENT.md)
- [docs/archive/DEPLOYMENT_GUIDE.md](../archive/DEPLOYMENT_GUIDE.md)
- [docs/archive/DEPLOYMENT_GUIDE_CORRECTED.md](../archive/DEPLOYMENT_GUIDE_CORRECTED.md)
- [docs/archive/DEPLOYMENT_2STAGE.md](../archive/DEPLOYMENT_2STAGE.md)
- [docs/archive/DEPLOYMENT_IP_ONLY.md](../archive/DEPLOYMENT_IP_ONLY.md)
