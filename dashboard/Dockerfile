FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ARG NEXT_PUBLIC_SUPABASE_URL
ARG NEXT_PUBLIC_SUPABASE_ANON_KEY
ARG NEXT_PUBLIC_N8N_URL
ARG NEXT_PUBLIC_OPENWEBUI_URL
ARG NEXT_PUBLIC_FLOWISE_URL
ARG NEXT_PUBLIC_SUPABASE_STUDIO_URL
ARG NEXT_PUBLIC_LANGFUSE_URL
ARG NEXT_PUBLIC_SEARXNG_URL
ARG NEXT_PUBLIC_NEO4J_URL
ARG NEXT_PUBLIC_KALI_URL
ENV NEXT_PUBLIC_SUPABASE_URL=$NEXT_PUBLIC_SUPABASE_URL
ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=$NEXT_PUBLIC_SUPABASE_ANON_KEY
ENV NEXT_PUBLIC_N8N_URL=$NEXT_PUBLIC_N8N_URL
ENV NEXT_PUBLIC_OPENWEBUI_URL=$NEXT_PUBLIC_OPENWEBUI_URL
ENV NEXT_PUBLIC_FLOWISE_URL=$NEXT_PUBLIC_FLOWISE_URL
ENV NEXT_PUBLIC_SUPABASE_STUDIO_URL=$NEXT_PUBLIC_SUPABASE_STUDIO_URL
ENV NEXT_PUBLIC_LANGFUSE_URL=$NEXT_PUBLIC_LANGFUSE_URL
ENV NEXT_PUBLIC_SEARXNG_URL=$NEXT_PUBLIC_SEARXNG_URL
ENV NEXT_PUBLIC_NEO4J_URL=$NEXT_PUBLIC_NEO4J_URL
ENV NEXT_PUBLIC_KALI_URL=$NEXT_PUBLIC_KALI_URL

# Build the application
RUN npm run build

# Production image, copy all the files and run next
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
