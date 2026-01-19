import { NextResponse } from "next/server"
import { cookies } from "next/headers"

const VALID_CONTAINERS = ["open-webui", "n8n", "flowise", "langfuse-web"]
const UPDATE_TOKEN = "cbass-update-secret-2026"

export async function POST(request: Request) {
  // Simple auth check - verify there's a supabase auth cookie
  const cookieStore = await cookies()
  const authCookie = cookieStore.getAll().find(c => c.name.includes('auth-token'))

  if (!authCookie) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  }

  const { container } = await request.json()

  if (!VALID_CONTAINERS.includes(container)) {
    return NextResponse.json({ error: "Invalid container" }, { status: 400 })
  }

  try {
    // Call the webhook service
    const response = await fetch(
      `http://updater:9000/hooks/update-container?container=${container}&token=${UPDATE_TOKEN}`,
      { method: "POST" }
    )

    const text = await response.text()

    return NextResponse.json({
      success: true,
      message: `Update triggered for ${container}`,
      output: text
    })
  } catch (error) {
    return NextResponse.json({
      error: "Failed to trigger update",
      details: String(error)
    }, { status: 500 })
  }
}
