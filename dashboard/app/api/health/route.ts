import { NextResponse } from "next/server"
import { services, toHealthCheckUrl } from "@/lib/services"

async function checkService(url: string): Promise<"online" | "offline"> {
  try {
    const healthUrl = toHealthCheckUrl(url)
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 5000)

    const response = await fetch(healthUrl, {
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
