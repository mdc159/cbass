# CBass Dashboard - Technical Reference

> **Last Updated:** 2026-01-12
> **Location on VPS:** `/opt/cbass/dashboard/`
> **Live URL:** https://cbass.space

---

## Overview

The CBass Dashboard is a **Next.js 16.1.1** application built with **React 19** that serves as the central hub ("AI Command Center") for accessing all self-hosted AI services. It provides authentication, service status monitoring, and one-click container updates.

---

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 16.1.1 | React framework with App Router |
| React | 19.2.3 | UI library |
| TypeScript | 5.x | Type safety |
| Tailwind CSS | 4.x | Utility-first styling |
| Supabase SSR | 0.8.0 | Server-side auth |
| Supabase JS | 2.90.1 | Client-side auth |
| shadcn/ui | - | UI components (Radix primitives) |
| next-themes | 0.4.6 | Dark/light mode switching |
| lucide-react | 0.562.0 | Icons |

---

## Directory Structure

```
/opt/cbass/dashboard/
├── app/
│   ├── layout.tsx              # Root layout with ThemeProvider
│   ├── page.tsx                # Login page (/)
│   ├── globals.css             # Global Tailwind styles
│   ├── favicon.ico
│   ├── dashboard/
│   │   └── page.tsx            # Main dashboard (/dashboard)
│   └── api/
│       ├── health/
│       │   └── route.ts        # GET - Service health checks
│       └── update/
│           └── route.ts        # POST - Container updates
├── components/
│   ├── theme-provider.tsx      # next-themes wrapper
│   ├── service-card.tsx        # Clickable service card
│   └── ui/                     # shadcn/ui components
│       ├── badge.tsx
│       ├── button.tsx
│       ├── card.tsx
│       ├── input.tsx
│       └── label.tsx
├── lib/
│   ├── supabase.ts             # Supabase browser client factory
│   └── utils.ts                # cn() Tailwind merge utility
├── public/                     # Static assets
├── .env.local                  # Environment variables
├── .dockerignore
├── .gitignore
├── Dockerfile                  # Multi-stage production build
├── next.config.ts              # Next.js config (standalone output)
├── package.json
├── package-lock.json
├── postcss.config.mjs
├── eslint.config.mjs
├── components.json             # shadcn/ui config
└── tsconfig.json
```

---

## Pages & Routes

### Login Page (`/`)

**File:** `app/page.tsx`

The landing page with authentication options:

- Email/password form
- GitHub OAuth button
- Google OAuth button
- Sign-up link
- Error display
- Gradient background (slate-900 → purple-900 → slate-900)

**Key code:**
```typescript
const supabase = createClient()

// Email/password login
await supabase.auth.signInWithPassword({ email, password })

// OAuth login
await supabase.auth.signInWithOAuth({
  provider: 'github',  // or 'google'
  options: { redirectTo: `${window.location.origin}/dashboard` }
})
```

### Dashboard (`/dashboard`)

**File:** `app/dashboard/page.tsx`

The main control panel showing all services:

**Features:**
- Header with logo, user email, theme toggle, logout
- 9 service cards in responsive grid (4 cols desktop, 2 tablet, 1 mobile)
- Auto-refresh status every 30 seconds
- "Update Services" section with one-click container updates
- System status footer

**Services monitored:**

| Service | Description | URL | Icon |
|---------|-------------|-----|------|
| n8n | Workflow Automation | https://n8n.cbass.space | 🤖 |
| Open WebUI | AI Chat Interface | https://openwebui.cbass.space | 💬 |
| Flowise | Visual AI Builder | https://flowise.cbass.space | 🔄 |
| OpenCode | AI Code Assistant | https://opencode.cbass.space | 🧠 |
| Supabase | Database & Backend | https://supabase.cbass.space | 🗄️ |
| Langfuse | LLM Observability | https://langfuse.cbass.space | 📊 |
| SearXNG | Meta Search Engine | https://searxng.cbass.space | 🔍 |
| Neo4j | Knowledge Graph | https://neo4j.cbass.space | 🕸️ |
| Kali | Security Lab | https://kali.cbass.space | 🐉 |

**Updatable containers:**
- Open WebUI (`open-webui`)
- n8n (`n8n`)
- Flowise (`flowise`)
- Langfuse (`langfuse-web`)

---

## API Routes

### Health Check - `GET /api/health`

**File:** `app/api/health/route.ts`

Checks all 9 services with HEAD requests (5 second timeout).

**Response:**
```json
{
  "services": [
    { "name": "n8n", "status": "online" },
    { "name": "Open WebUI", "status": "online" },
    { "name": "Flowise", "status": "offline" }
  ]
}
```

**Status logic:**
- `online` - HTTP 200, 401, or 403 (service responding)
- `offline` - Timeout or error

### Container Update - `POST /api/update`

**File:** `app/api/update/route.ts`

Triggers container updates via internal webhook service.

**Request:**
```json
{ "container": "open-webui" }
```

**Valid containers:** `open-webui`, `n8n`, `flowise`, `langfuse-web`

**Response:**
```json
{
  "success": true,
  "message": "Update triggered for open-webui",
  "output": "..."
}
```

**Authentication:** Requires Supabase auth cookie.

**Internal call:**
```
POST http://updater:9000/hooks/update-container?container={name}&token={token}
```

---

## Components

### ServiceCard (`components/service-card.tsx`)

Clickable card displaying service info and status.

**Props:**
```typescript
interface ServiceCardProps {
  name: string
  description: string
  url: string
  icon: string
  status: "online" | "offline" | "pending"
}
```

**Features:**
- Click to open service in new tab
- Status indicator dot (green/yellow/red)
- Status badge (Ready/Starting/Offline)
- Hover animations (lift, glow, external link icon)

### ThemeProvider (`components/theme-provider.tsx`)

Wrapper for next-themes dark/light mode.

```typescript
<ThemeProvider
  attribute="class"
  defaultTheme="system"
  enableSystem
  disableTransitionOnChange
>
  {children}
</ThemeProvider>
```

---

## Lib Utilities

### Supabase Client (`lib/supabase.ts`)

```typescript
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

### Tailwind Merge (`lib/utils.ts`)

```typescript
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

---

## Environment Variables

**File:** `.env.local`

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL (e.g., `https://supabase.cbass.space`) |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anonymous key for client-side auth |

---

## Authentication Flow

```
1. User visits cbass.space
   ↓
2. Login page shown (app/page.tsx)
   ↓
3. User authenticates:
   - Email/password → supabase.auth.signInWithPassword()
   - GitHub → supabase.auth.signInWithOAuth({ provider: 'github' })
   - Google → supabase.auth.signInWithOAuth({ provider: 'google' })
   ↓
4. On success → router.push("/dashboard")
   ↓
5. Dashboard loads (app/dashboard/page.tsx)
   ↓
6. useEffect checks auth: supabase.auth.getUser()
   - If no user → router.push("/")
   - If user exists → Show dashboard
   ↓
7. Logout: supabase.auth.signOut() → router.push("/")
```

---

## Deployment

### Docker Container

| Property | Value |
|----------|-------|
| Container name | `dashboard` |
| Image | `localai-dashboard` |
| Internal port | 3000 |
| Network | `localai_default` |

### Dockerfile

Multi-stage build for optimized production image:

```dockerfile
FROM node:20-alpine AS base

# Stage 1: Install dependencies
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

# Stage 2: Build application
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Production runner
FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

### Next.js Config

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',  // Optimized for Docker deployment
};

export default nextConfig;
```

### Caddy Reverse Proxy

**File:** `/opt/cbass/Caddyfile`

```
cbass.space {
    reverse_proxy dashboard:3000
}

www.cbass.space {
    redir https://cbass.space{uri} permanent
}
```

---

## Making Changes

### Option 1: Direct Edit on VPS

```bash
# SSH into VPS
ssh cbass

# Navigate to project
cd /opt/cbass/dashboard

# Edit files
nano app/page.tsx

# Rebuild container
docker compose -p localai build dashboard

# Restart container
docker compose -p localai up -d dashboard
```

### Option 2: Via Dashboard Update Button

The dashboard has built-in "Update Services" buttons that call `/api/update` to trigger container rebuilds.

### Option 3: Full Redeploy

```bash
# From local machine - copy updated files
scp -r ./dashboard cbass:/opt/cbass/

# SSH and rebuild
ssh cbass "cd /opt/cbass && docker compose -p localai build dashboard && docker compose -p localai up -d dashboard"
```

---

## Styling

### Color Scheme

**Light mode:**
- Background: `bg-gradient-to-br from-slate-50 to-slate-100`
- Cards: White with shadow

**Dark mode:**
- Background: `bg-gradient-to-br from-slate-950 to-slate-900`
- Cards: `slate-900` with border

**Accent colors:**
- Primary gradient: `from-purple-600 to-pink-600`
- Status online: `bg-green-500`
- Status pending: `bg-yellow-500`
- Status offline: `bg-red-500`

### Fonts

- Sans: Geist Sans (`--font-geist-sans`)
- Mono: Geist Mono (`--font-geist-mono`)

---

## Dependencies

**Production:**
```json
{
  "@radix-ui/react-label": "^2.1.8",
  "@radix-ui/react-slot": "^1.2.4",
  "@supabase/ssr": "^0.8.0",
  "@supabase/supabase-js": "^2.90.1",
  "class-variance-authority": "^0.7.1",
  "clsx": "^2.1.1",
  "lucide-react": "^0.562.0",
  "next": "16.1.1",
  "next-themes": "^0.4.6",
  "react": "19.2.3",
  "react-dom": "19.2.3",
  "tailwind-merge": "^3.4.0"
}
```

**Development:**
```json
{
  "@tailwindcss/postcss": "^4",
  "@types/node": "^20",
  "@types/react": "^19",
  "@types/react-dom": "^19",
  "eslint": "^9",
  "eslint-config-next": "16.1.1",
  "tailwindcss": "^4",
  "tw-animate-css": "^1.4.0",
  "typescript": "^5"
}
```

---

## Related Documentation

- [Architecture Diagram](./cbass-architecture-diagram.md) - Visual system overview
- [Dashboard Plan](./cbass-dashboard-plan.md) - Original build plan
- [OAuth Setup Guide](./OAUTH_SETUP_GUIDE.md) - GitHub/Google OAuth configuration
- [Deployment Guide](./DEPLOYMENT_GUIDE.md) - Full deployment instructions

---

## Troubleshooting

### Dashboard not loading

1. Check container status: `docker ps | grep dashboard`
2. Check logs: `docker logs dashboard`
3. Verify Caddy routing: `docker logs caddy`

### Auth not working

1. Check `.env.local` has correct Supabase URL and key
2. Verify Supabase is running: `docker ps | grep supabase`
3. Check OAuth redirect URLs in Supabase dashboard

### Services showing offline

1. Check if service container is running
2. Verify Caddy has routes for subdomain
3. Check SSL certificate status

### Container update fails

1. Verify `updater` service is running
2. Check webhook token matches
3. Review updater logs: `docker logs updater`
