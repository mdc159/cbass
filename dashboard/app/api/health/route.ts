import { NextResponse } from "next/server"

const services = [
  { name: "n8n", url: "https://n8n.cbass.space" },
  { name: "Open WebUI", url: "https://openwebui.cbass.space" },
  { name: "Flowise", url: "https://flowise.cbass.space" },
  { name: "OpenCode", url: "https://opencode.cbass.space" },
  { name: "Supabase", url: "https://supabase.cbass.space" },
  { name: "Langfuse", url: "https://langfuse.cbass.space" },
  { name: "SearXNG", url: "https://searxng.cbass.space" },
  { name: "Neo4j", url: "https://neo4j.cbass.space" },
  { name: "Kali", url: "https://kali.cbass.space" },
]

async function checkService(url: string): Promise<"online" | "offline"> {
  try {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 5000)
    
    const response = await fetch(url, {
      method: "HEAD",
      signal: controller.signal,
    })
    
    clearTimeout(timeoutId)
    return response.ok || response.status === 401 || response.status === 403 ? "online" : "offline"
  } catch {
    return "offline"
  }
}

export async function GET() {
  const results = await Promise.all(
    services.map(async (service) => ({
      name: service.name,
      status: await checkService(service.url),
    }))
  )

  return NextResponse.json({ services: results })
}
