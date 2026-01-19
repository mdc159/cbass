"use client"

import { useEffect, useState, useCallback } from "react"
import { ServiceCard } from "@/components/service-card"
import { Button } from "@/components/ui/button"
import { createClient } from "@/lib/supabase"
import { useRouter } from "next/navigation"
import { LogOut, Moon, Sun, RefreshCw, Download, Loader2 } from "lucide-react"
import { useTheme } from "next-themes"

const services = [
  { name: "n8n", description: "Workflow Automation", url: "https://n8n.cbass.space", icon: "🤖" },
  { name: "Open WebUI", description: "AI Chat Interface", url: "https://openwebui.cbass.space", icon: "💬" },
  { name: "Flowise", description: "Visual AI Builder", url: "https://flowise.cbass.space", icon: "🔄" },
  { name: "Supabase", description: "Database & Backend", url: "https://supabase.cbass.space", icon: "🗄️" },
  { name: "Langfuse", description: "LLM Observability", url: "https://langfuse.cbass.space", icon: "📊" },
  { name: "SearXNG", description: "Meta Search Engine", url: "https://searxng.cbass.space", icon: "🔍" },
  { name: "Neo4j", description: "Knowledge Graph", url: "https://neo4j.cbass.space", icon: "🕸️" },
  { name: "Kali", description: "Security Lab", url: "https://kali.cbass.space", icon: "🐉" }
]

const updatableServices = [
  { name: "Open WebUI", container: "open-webui", icon: "💬" },
  { name: "n8n", container: "n8n", icon: "🤖" },
  { name: "Flowise", container: "flowise", icon: "🔄" },
  { name: "Langfuse", container: "langfuse-web", icon: "📊" },
]

type ServiceStatus = "online" | "offline" | "pending"

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null)
  const [statuses, setStatuses] = useState<Record<string, ServiceStatus>>({})
  const [checking, setChecking] = useState(true)
  const [updating, setUpdating] = useState<string | null>(null)
  const [updateMessage, setUpdateMessage] = useState<string | null>(null)
  const router = useRouter()
  const supabase = createClient()
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  const fetchStatuses = useCallback(async () => {
    try {
      const response = await fetch("/api/health")
      const data = await response.json()
      const statusMap: Record<string, ServiceStatus> = {}
      data.services.forEach((s: { name: string; status: ServiceStatus }) => {
        statusMap[s.name] = s.status
      })
      setStatuses(statusMap)
    } catch (error) {
      console.error("Failed to fetch service statuses:", error)
    } finally {
      setChecking(false)
    }
  }, [])

  useEffect(() => {
    setMounted(true)
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) { router.push("/") } else { setUser(user) }
    }
    getUser()
  }, [router, supabase.auth])

  useEffect(() => {
    fetchStatuses()
    const interval = setInterval(fetchStatuses, 30000)
    return () => clearInterval(interval)
  }, [fetchStatuses])

  const handleLogout = async () => {
    await supabase.auth.signOut()
    router.push("/")
  }

  const handleRefresh = () => {
    setChecking(true)
    fetchStatuses()
  }

  const handleUpdate = async (container: string, name: string) => {
    setUpdating(container)
    setUpdateMessage(null)
    try {
      const response = await fetch("/api/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ container })
      })
      const data = await response.json()
      if (data.success) {
        setUpdateMessage(`✅ ${name} update triggered! Container will restart.`)
        setTimeout(() => { fetchStatuses(); setUpdateMessage(null) }, 10000)
      } else {
        setUpdateMessage(`❌ Update failed: ${data.error}`)
      }
    } catch (error) {
      setUpdateMessage(`❌ Update failed: ${error}`)
    } finally {
      setUpdating(null)
    }
  }

  if (!user || !mounted) {
    return (<div className="min-h-screen flex items-center justify-center"><div className="text-2xl">Loading...</div></div>)
  }

  const onlineCount = Object.values(statuses).filter(s => s === "online").length

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900">
      <header className="border-b bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="text-3xl">🎯</div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">CBass</h1>
              <p className="text-sm text-muted-foreground">AI Command Center</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-sm text-muted-foreground hidden sm:block">{user.email}</div>
            <Button variant="ghost" size="icon" onClick={handleRefresh} disabled={checking} title="Refresh status">
              <RefreshCw className={`h-5 w-5 ${checking ? "animate-spin" : ""}`} />
            </Button>
            <Button variant="ghost" size="icon" onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
              {theme === "dark" ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </Button>
            <Button variant="outline" onClick={handleLogout} className="gap-2">
              <LogOut className="h-4 w-4" /><span className="hidden sm:inline">Logout</span>
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">Welcome back!</h2>
          <p className="text-muted-foreground">Access your AI services and tools</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {services.map((service) => (
            <ServiceCard key={service.name} {...service} status={statuses[service.name] || "pending"} />
          ))}
        </div>

        <div className="mt-12 border-t pt-8">
          <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Download className="h-5 w-5" /> Update Services
          </h3>
          <p className="text-sm text-muted-foreground mb-4">
            Pull latest images and restart containers. Services will be briefly unavailable during update.
          </p>
          {updateMessage && (
            <div className="mb-4 p-3 rounded-lg bg-slate-100 dark:bg-slate-800 text-sm">{updateMessage}</div>
          )}
          <div className="flex flex-wrap gap-3">
            {updatableServices.map((service) => (
              <Button key={service.container} variant="outline" onClick={() => handleUpdate(service.container, service.name)} disabled={updating !== null} className="gap-2">
                {updating === service.container ? <Loader2 className="h-4 w-4 animate-spin" /> : <span>{service.icon}</span>}
                Update {service.name}
              </Button>
            ))}
          </div>
        </div>

        <div className="mt-12 text-center text-sm text-muted-foreground">
          <p>
            <span className={`inline-block w-2 h-2 rounded-full mr-2 ${onlineCount > 0 ? "bg-green-500 animate-pulse" : "bg-yellow-500"}`}></span>
            {checking ? "Checking services..." : `System operational • ${onlineCount} of ${services.length} services ready`}
          </p>
        </div>
      </main>
    </div>
  )
}
