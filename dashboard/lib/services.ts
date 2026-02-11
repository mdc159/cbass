export interface Service {
  name: string
  description: string
  icon: string
  url: string
}

export const services: Service[] = [
  { name: "n8n", description: "Workflow Automation", icon: "\u{1F916}", url: process.env.NEXT_PUBLIC_N8N_URL || "https://n8n.cbass.space" },
  { name: "Open WebUI", description: "AI Chat Interface", icon: "\u{1F4AC}", url: process.env.NEXT_PUBLIC_OPENWEBUI_URL || "https://openwebui.cbass.space" },
  { name: "Flowise", description: "Visual AI Builder", icon: "\u{1F504}", url: process.env.NEXT_PUBLIC_FLOWISE_URL || "https://flowise.cbass.space" },
  { name: "Supabase", description: "Database & Backend", icon: "\u{1F5C4}\u{FE0F}", url: process.env.NEXT_PUBLIC_SUPABASE_STUDIO_URL || "https://supabase.cbass.space" },
  { name: "Langfuse", description: "LLM Observability", icon: "\u{1F4CA}", url: process.env.NEXT_PUBLIC_LANGFUSE_URL || "https://langfuse.cbass.space" },
  { name: "SearXNG", description: "Meta Search Engine", icon: "\u{1F50D}", url: process.env.NEXT_PUBLIC_SEARXNG_URL || "https://searxng.cbass.space" },
  { name: "Neo4j", description: "Knowledge Graph", icon: "\u{1F578}\u{FE0F}", url: process.env.NEXT_PUBLIC_NEO4J_URL || "https://neo4j.cbass.space" },
  { name: "Kali", description: "Security Lab", icon: "\u{1F409}", url: process.env.NEXT_PUBLIC_KALI_URL || "https://kali.cbass.space" },
]

export const updatableServices = [
  { name: "Open WebUI", container: "open-webui", icon: "\u{1F4AC}" },
  { name: "n8n", container: "n8n", icon: "\u{1F916}" },
  { name: "Flowise", container: "flowise", icon: "\u{1F504}" },
  { name: "Langfuse", container: "langfuse-web", icon: "\u{1F4CA}" },
]

/**
 * Rewrite localhost URLs to host.docker.internal for server-side health checks.
 * The health API route runs inside Docker where localhost != the host machine.
 */
export function toHealthCheckUrl(url: string): string {
  return url.replace(/\/\/localhost(:\d+)/, "//host.docker.internal$1")
}
