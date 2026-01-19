"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ExternalLink } from "lucide-react"

interface ServiceCardProps {
  name: string
  description: string
  url: string
  icon: string
  status: "online" | "offline" | "pending"
}

export function ServiceCard({ name, description, url, icon, status }: ServiceCardProps) {
  const statusColors = {
    online: "bg-green-500",
    offline: "bg-red-500",
    pending: "bg-yellow-500"
  }

  return (
    <Card 
      className="group cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-1 border-2 hover:border-primary/50"
      onClick={() => window.open(url, '_blank')}
    >
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="text-4xl mb-2">{icon}</div>
          <div className={`w-3 h-3 rounded-full ${statusColors[status]} animate-pulse`} />
        </div>
        <CardTitle className="flex items-center gap-2 group-hover:text-primary transition-colors">
          {name}
          <ExternalLink className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
        </CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        <Badge variant={status === "online" ? "default" : status === "pending" ? "secondary" : "destructive"}>
          {status === "online" ? "Ready" : status === "pending" ? "Starting" : "Offline"}
        </Badge>
      </CardContent>
    </Card>
  )
}
