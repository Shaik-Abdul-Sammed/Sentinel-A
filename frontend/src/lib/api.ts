import axios from "axios"

export function getApiBaseUrl(): string {
  if (typeof window !== "undefined") {
    const customUrl = window.localStorage.getItem("sentinel_api_url")
    if (customUrl) return customUrl
  }
  return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
}

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  timeout: 15000,
})

api.interceptors.request.use((config) => {
  config.baseURL = getApiBaseUrl()
  return config
})

export const ACCESS_TOKEN_STORAGE_KEY = "sentinel_access_token"

let socToken: string | null = null
let socTokenExpMs: number | null = null

type JwtPayload = {
  exp?: number
  role?: string
  sub?: string
}

function decodeJwtPayload(token: string) {
  try {
    const body = token.split(".")[1]
    if (!body) {
      return null
    }
    const normalized = body.replace(/-/g, "+").replace(/_/g, "/")
    const padded = normalized + "=".repeat((4 - (normalized.length % 4)) % 4)
    return JSON.parse(atob(padded))
  } catch {
    return null
  }
}

function getStoredAccessToken() {
  if (typeof window === "undefined") {
    return null
  }
  return window.localStorage.getItem(ACCESS_TOKEN_STORAGE_KEY)
}

function storeAccessToken(token: string) {
  if (typeof window === "undefined") {
    return
  }
  window.localStorage.setItem(ACCESS_TOKEN_STORAGE_KEY, token)
}

function clearAccessToken() {
  if (typeof window === "undefined") {
    return
  }
  window.localStorage.removeItem(ACCESS_TOKEN_STORAGE_KEY)
}

function isTokenFresh(payload: JwtPayload | null) {
  if (!payload?.exp) {
    return true
  }
  return payload.exp * 1000 - Date.now() > 60_000
}

export function getAccessTokenPayload(token?: string | null) {
  if (!token) {
    return null
  }
  return decodeJwtPayload(token) as JwtPayload | null
}

export async function loginWithCredentials(username: string, password: string) {
  const params = new URLSearchParams()
  params.set("username", username)
  params.set("password", password)
  const response = await api.post("/auth/login", params, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  })
  const token = response.data.access_token as string
  storeAccessToken(token)
  return {
    access_token: token,
    token_type: response.data.token_type as string,
    payload: decodeJwtPayload(token) as JwtPayload | null,
  }
}

export function logout() {
  clearAccessToken()
}

async function getActiveAccessToken() {
  const storedToken = getStoredAccessToken()
  if (storedToken) {
    const payload = decodeJwtPayload(storedToken) as JwtPayload | null
    if (isTokenFresh(payload)) {
      return storedToken
    }
    clearAccessToken()
  }
  return ensureSocToken()
}

async function refreshSocToken() {
  socToken = null
  socTokenExpMs = null
  return ensureSocToken(true)
}

async function ensureSocToken(forceRefresh = false) {
  const now = Date.now()
  if (!forceRefresh && socToken && socTokenExpMs && socTokenExpMs - now > 60_000) {
    return socToken
  }
  const params = new URLSearchParams()
  params.set("username", "soc")
  params.set("password", "soc2026")
  const response = await api.post("/auth/login", params, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  })
  socToken = response.data.access_token as string
  const payload = decodeJwtPayload(socToken)
  socTokenExpMs = payload?.exp ? payload.exp * 1000 : now + 15 * 60 * 1000
  return socToken
}

async function authHeaders() {
  const token = await getActiveAccessToken()
  return {
    Authorization: `Bearer ${token}`,
  }
}

export type AlertItem = {
  alert_id: string
  title: string
  threat_type: string
  risk_score: number
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
  decision: "ALLOW" | "ALERT" | "ESCALATE" | "BLOCK"
  actor_id: string
  source: string
  status: string
  created_at: string
  actions: string[]
}

export type TimelineItem = {
  time: string
  event: string
  message: string
  risk_score: number
}

export type SystemStatus = {
  shield_status: string
  events_processed: number
  alerts_total: number
  alerts_open: number
  auto_blocked: number
  escalations: number
  average_risk_score: number
  last_updated: string
}

export type ConsoleScenario = {
  scenario_id: string
  title: string
  industry: string
  impact: string
  logs: string[]
}

export type ConsoleFinding = {
  error_type: string
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
  line_number: number
  log_excerpt: string
  root_cause: string
  how_to_solve: string[]
  preventive_control: string
  confidence: number
}

export type ConsoleAnalysisResult = {
  scenario_id?: string | null
  summary: {
    total_lines: number
    detected_errors: number
    unclassified_lines: number
    overall_risk: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
  }
  detected_errors: ConsoleFinding[]
  unknown_lines: Array<{ line_number: number; log_excerpt: string }>
  triage_priority: Array<{ order: number; error_type: string; why_first: string }>
  efficiency_advantage: {
    auto_grouping: string
    root_cause_mapping: string
    time_saved_estimate: string
  }
}

export type RuntimeConsoleEvent = {
  event_id: string
  source: string
  level: string
  url?: string
  stack?: string
  user_agent?: string
  message: string
  occurred_at: string
}

export type RuntimeConsoleIngestPayload = {
  message: string
  source?: string
  level?: string
  stack?: string
  url?: string
  user_agent?: string
  timestamp?: string
}

export async function analyzeURL(content: string) {
  const response = await api.post("/telemetry/phishing-scan", { content })
  const data = response.data
  return {
    analysis: {
      final_verdict: data.analysis.final_verdict,
      confidence: data.analysis.confidence,
      ai_reasoning: data.analysis.ai_reasoning,
    },
    recommendations: {
      actions: (data.decision.actions || []).map((action: string) => ({
        action,
        description: "Generated by Sentinel-A policy orchestrator.",
      })),
    },
  }
}

export async function getSystemStatus(): Promise<SystemStatus> {
  const response = await api.get("/telemetry/status")
  return response.data
}

export async function getAlerts(limit = 25): Promise<AlertItem[]> {
  const response = await api.get("/telemetry/alerts", {
    params: { limit },
    headers: await authHeaders(),
  })
  return response.data.items || []
}

export async function getTimeline(limit = 25): Promise<TimelineItem[]> {
  const response = await api.get("/telemetry/timeline", {
    params: { limit },
    headers: await authHeaders(),
  })
  return response.data.items || []
}

export async function simulateScenario(scenario: "phishing" | "insider") {
  const response = await api.post(`/telemetry/simulate/${scenario}`, null, {
    headers: await authHeaders(),
  })
  return response.data
}

export async function getConsoleScenarios(): Promise<ConsoleScenario[]> {
  const response = await api.get("/advanced/console/scenarios", {
    headers: await authHeaders(),
  })
  return response.data.scenarios || []
}

export async function analyzeConsoleLogs(logs: string[], scenarioId?: string): Promise<ConsoleAnalysisResult> {
  const response = await api.post(
    "/advanced/console/analyze",
    {
      logs,
      scenario_id: scenarioId,
    },
    {
      headers: await authHeaders(),
    },
  )
  return response.data
}

export async function ingestRuntimeConsoleEvent(payload: RuntimeConsoleIngestPayload) {
  const response = await api.post("/advanced/console/runtime/ingest", payload, {
    headers: await authHeaders(),
  })
  return response.data
}

export async function getRuntimeConsoleEvents(limit = 200): Promise<RuntimeConsoleEvent[]> {
  const response = await api.get("/advanced/console/runtime/events", {
    params: { limit },
    headers: await authHeaders(),
  })
  return response.data.items || []
}

export async function clearRuntimeConsoleEvents() {
  const response = await api.delete("/advanced/console/runtime/events", {
    headers: await authHeaders(),
  })
  return response.data
}

export async function analyzeRuntimeConsoleEvents(limit = 250): Promise<ConsoleAnalysisResult> {
  const response = await api.post(
    "/advanced/console/runtime/analyze",
    null,
    {
      params: { limit },
      headers: await authHeaders(),
    },
  )
  return response.data
}

export type TelemetryWsMessage = {
  type?: string
  status?: SystemStatus
  event?: Record<string, unknown>
  alert?: AlertItem
  [key: string]: unknown
}

export function subscribeTelemetry(onMessage: (message: TelemetryWsMessage) => void) {
  const apiUrl = getApiBaseUrl()
  let ws: WebSocket | null = null
  let pingId: ReturnType<typeof setInterval> | null = null
  let reconnectId: ReturnType<typeof setTimeout> | null = null
  let closed = false
  let reconnectAttempts = 0

  const connect = async () => {
    const token = await getActiveAccessToken()
    if (closed) {
      return
    }
    const wsUrl = `${apiUrl.replace("http://", "ws://").replace("https://", "wss://")}/telemetry/ws?token=${encodeURIComponent(token)}`
    ws = new WebSocket(wsUrl)

    ws.onopen = () => {
      reconnectAttempts = 0
      if (reconnectId) {
        clearTimeout(reconnectId)
        reconnectId = null
      }
      pingId = setInterval(() => {
        if (ws?.readyState === WebSocket.OPEN) {
          ws.send("ping")
        }
      }, 15000)
    }

    ws.onmessage = (event) => {
      try {
        onMessage(JSON.parse(event.data))
      } catch (error) {
        console.error("Invalid websocket payload", error)
      }
    }

    ws.onclose = async (event) => {
      if (pingId) {
        clearInterval(pingId)
        pingId = null
      }
      if (closed) {
        return
      }

      const tokenExpired = event.code === 1008 || event.code === 4001 || (socTokenExpMs !== null && socTokenExpMs <= Date.now())
      if (tokenExpired) {
        await refreshSocToken()
      }

      reconnectAttempts += 1
      const delay = Math.min(30_000, 1000 * 2 ** Math.min(reconnectAttempts, 5))
      reconnectId = setTimeout(() => {
        void connect().catch((error) => console.error("Websocket reconnect failed", error))
      }, delay)
    }
  }

  connect().catch((error) => {
    console.error("Failed to initialize websocket auth", error)
  })

  return () => {
    closed = true
    if (pingId) {
      clearInterval(pingId)
    }
    if (reconnectId) {
      clearTimeout(reconnectId)
    }
    ws?.close()
  }
}
