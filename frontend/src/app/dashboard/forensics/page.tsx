"use client"

import React, { useEffect, useMemo, useState } from "react"
import { AlertTriangle, CheckCircle2, ClipboardList, Download, Loader2, Radar, Sparkles, TerminalSquare, Trash2 } from "lucide-react"
import {
  analyzeConsoleLogs,
  analyzeRuntimeConsoleEvents,
  clearRuntimeConsoleEvents,
  getConsoleScenarios,
  getRuntimeConsoleEvents,
  ingestRuntimeConsoleEvent,
  type ConsoleAnalysisResult,
  type RuntimeConsoleEvent,
  type ConsoleScenario,
} from "@/lib/api"
import { cn } from "@/lib/utils"

const severityStyles: Record<string, string> = {
  LOW: "bg-emerald-500/15 text-emerald-400 border-emerald-500/40",
  MEDIUM: "bg-yellow-500/15 text-yellow-300 border-yellow-500/40",
  HIGH: "bg-orange-500/15 text-orange-300 border-orange-500/40",
  CRITICAL: "bg-red-500/15 text-red-300 border-red-500/40",
}

export default function ForensicsPage() {
  const [scenarios, setScenarios] = useState<ConsoleScenario[]>([])
  const [selectedScenario, setSelectedScenario] = useState<ConsoleScenario | null>(null)
  const [rawLogText, setRawLogText] = useState("")
  const [analysis, setAnalysis] = useState<ConsoleAnalysisResult | null>(null)
  const [runtimeEvents, setRuntimeEvents] = useState<RuntimeConsoleEvent[]>([])
  const [captureLiveRuntime, setCaptureLiveRuntime] = useState(false)
  const [loadingScenarios, setLoadingScenarios] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  const [analyzingRuntime, setAnalyzingRuntime] = useState(false)
  const [clearingRuntime, setClearingRuntime] = useState(false)
  const [exportingPdf, setExportingPdf] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const load = async () => {
      setLoadingScenarios(true)
      setError(null)
      try {
        const items = await getConsoleScenarios()
        setScenarios(items)
        if (items.length > 0) {
          setSelectedScenario(items[0])
          setRawLogText(items[0].logs.join("\n"))
        }
      } catch (fetchError) {
        setError(fetchError instanceof Error ? fetchError.message : "Failed to load scenarios")
      } finally {
        setLoadingScenarios(false)
      }
    }
    load().catch(console.error)
  }, [])

  useEffect(() => {
    const hydrateRuntimeEvents = async () => {
      try {
        const events = await getRuntimeConsoleEvents(120)
        setRuntimeEvents(events)
      } catch {
        // Silent fallback: runtime panel remains empty when backend is unavailable.
      }
    }
    hydrateRuntimeEvents().catch(console.error)
  }, [])

  useEffect(() => {
    if (!captureLiveRuntime) {
      return
    }

    const postRuntimeEvent = async (payload: {
      message: string
      source: string
      level: string
      stack?: string
      url?: string
      timestamp?: string
    }) => {
      try {
        const response = await ingestRuntimeConsoleEvent({
          ...payload,
          user_agent: navigator.userAgent,
        })
        const ingested = response?.event
        if (ingested) {
          setRuntimeEvents((previous) => [...previous, ingested].slice(-120))
        }
      } catch {
        // Ignore transient ingestion failures to avoid recursion from error handlers.
      }
    }

    const onWindowError = (event: ErrorEvent) => {
      const message = event.message || "Unknown window error"
      const stack = event.error?.stack || undefined
      void postRuntimeEvent({
        message,
        source: "window.onerror",
        level: "error",
        stack,
        url: event.filename || window.location.href,
        timestamp: new Date().toISOString(),
      })
    }

    const onUnhandledRejection = (event: PromiseRejectionEvent) => {
      const reason = event.reason
      const message =
        typeof reason === "string"
          ? reason
          : reason?.message || JSON.stringify(reason || "Unhandled promise rejection")
      const stack = reason?.stack || undefined
      void postRuntimeEvent({
        message,
        source: "unhandledrejection",
        level: "error",
        stack,
        url: window.location.href,
        timestamp: new Date().toISOString(),
      })
    }

    window.addEventListener("error", onWindowError)
    window.addEventListener("unhandledrejection", onUnhandledRejection)

    return () => {
      window.removeEventListener("error", onWindowError)
      window.removeEventListener("unhandledrejection", onUnhandledRejection)
    }
  }, [captureLiveRuntime])

  const lineCount = useMemo(() => {
    if (!rawLogText.trim()) {
      return 0
    }
    return rawLogText.split("\n").filter((line) => line.trim().length > 0).length
  }, [rawLogText])

  const chooseScenario = (scenario: ConsoleScenario) => {
    setSelectedScenario(scenario)
    setRawLogText(scenario.logs.join("\n"))
    setAnalysis(null)
  }

  const runAnalysis = async () => {
    const logs = rawLogText
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0)

    if (logs.length === 0) {
      setError("Paste or load at least one console log line before analysis.")
      return
    }

    setError(null)
    setAnalyzing(true)
    try {
      const result = await analyzeConsoleLogs(logs, selectedScenario?.scenario_id)
      setAnalysis(result)
    } catch (analysisError) {
      setError(analysisError instanceof Error ? analysisError.message : "Analysis failed")
    } finally {
      setAnalyzing(false)
    }
  }

  const runRuntimeAnalysis = async () => {
    setError(null)
    setAnalyzingRuntime(true)
    try {
      const result = await analyzeRuntimeConsoleEvents(250)
      setAnalysis(result)
      const lines = runtimeEvents.map((item) => {
        const prefix = `[${(item.level || "error").toUpperCase()}]`
        return `${prefix} ${item.message}`
      })
      if (lines.length > 0) {
        setRawLogText(lines.join("\n"))
      }
    } catch (runtimeError) {
      setError(runtimeError instanceof Error ? runtimeError.message : "Runtime analysis failed")
    } finally {
      setAnalyzingRuntime(false)
    }
  }

  const clearRuntime = async () => {
    setClearingRuntime(true)
    try {
      await clearRuntimeConsoleEvents()
      setRuntimeEvents([])
    } catch (runtimeClearError) {
      setError(runtimeClearError instanceof Error ? runtimeClearError.message : "Failed to clear runtime events")
    } finally {
      setClearingRuntime(false)
    }
  }

  const buildReportPayload = () => {
    const logs = rawLogText
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0)

    return {
      exported_at: new Date().toISOString(),
      source: "Sentinel-A Console Forensics",
      scenario: selectedScenario,
      summary: analysis?.summary || null,
      analysis,
      logs,
      runtime_events: runtimeEvents,
    }
  }

  const exportJsonReport = () => {
    const payload = buildReportPayload()
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement("a")
    anchor.href = url
    anchor.download = `sentinel-forensics-${new Date().toISOString().replace(/[:.]/g, "-")}.json`
    anchor.click()
    URL.revokeObjectURL(url)
  }

  const exportPdfReport = async () => {
    if (!analysis) {
      setError("Run an analysis first before exporting PDF.")
      return
    }

    setExportingPdf(true)
    try {
      const { jsPDF } = await import("jspdf")
      const doc = new jsPDF({ unit: "pt", format: "a4" })
      const pageWidth = doc.internal.pageSize.getWidth()
      const pageHeight = doc.internal.pageSize.getHeight()
      const margin = 48
      const contentWidth = pageWidth - margin * 2
      let y = margin

      const writeBlock = (title: string, value: string) => {
        doc.setFont("helvetica", "bold")
        doc.setFontSize(12)
        doc.text(title, margin, y)
        y += 18
        doc.setFont("helvetica", "normal")
        doc.setFontSize(10)
        const lines = doc.splitTextToSize(value, contentWidth)
        doc.text(lines, margin, y)
        y += lines.length * 14 + 14
        if (y > pageHeight - margin) {
          doc.addPage()
          y = margin
        }
      }

      writeBlock("Sentinel-A Forensic Report", `Generated at ${new Date().toISOString()}`)
      writeBlock("Scenario", selectedScenario?.title || "Manual log input")
      writeBlock(
        "Summary",
        `Detected errors: ${analysis.summary.detected_errors}\nOverall risk: ${analysis.summary.overall_risk}\nUnclassified lines: ${analysis.summary.unclassified_lines}`,
      )

      analysis.detected_errors.forEach((finding, index) => {
        writeBlock(
          `Issue ${index + 1}: ${finding.error_type}`,
          `Severity: ${finding.severity}\nRoot cause: ${finding.root_cause}\nHow to solve: ${finding.how_to_solve.join("; ")}\nPrevention: ${finding.preventive_control}`,
        )
      })

      if (analysis.unknown_lines.length > 0) {
        writeBlock(
          "Unknown Lines",
          analysis.unknown_lines
            .slice(0, 10)
            .map((line) => `line ${line.line_number}: ${line.log_excerpt}`)
            .join("\n"),
        )
      }

      doc.save(`sentinel-forensics-${new Date().toISOString().replace(/[:.]/g, "-")}.pdf`)
    } catch (pdfError) {
      setError(pdfError instanceof Error ? pdfError.message : "Failed to export PDF")
    } finally {
      setExportingPdf(false)
    }
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <header className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-accent flex items-center gap-2">
            <TerminalSquare className="h-7 w-7" />
            Console Forensics Lab
          </h1>
          <p className="text-foreground/70 mt-2 max-w-3xl">
            Load real-world incident scenarios, inspect raw browser console logs, and get root-cause plus remediation guidance instantly.
          </p>
        </div>
        <div className="glass px-4 py-3 text-xs text-foreground/80">
          <p className="font-semibold">Triage acceleration</p>
          <p>Groups duplicates, prioritizes blast radius, and returns fix playbooks in one pass.</p>
        </div>
      </header>

      {error && (
        <div className="rounded-xl border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-200" role="alert">
          {error}
        </div>
      )}

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-[1.1fr_1.4fr]">
        <div className="glass p-6 space-y-4">
          <h2 className="text-lg font-semibold text-accent flex items-center gap-2">
            <Radar className="h-5 w-5" />
            Real-World Scenarios
          </h2>

          {loadingScenarios ? (
            <div className="text-sm text-foreground/70 flex items-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin" />
              Loading scenario library...
            </div>
          ) : (
            <div className="space-y-3">
              {scenarios.map((scenario) => (
                <button
                  key={scenario.scenario_id}
                  type="button"
                  onClick={() => chooseScenario(scenario)}
                  className={cn(
                    "w-full rounded-xl border px-4 py-3 text-left transition-colors",
                    selectedScenario?.scenario_id === scenario.scenario_id
                      ? "border-accent/50 bg-accent/10"
                      : "border-border/50 bg-white/5 hover:border-accent/30",
                  )}
                >
                  <p className="text-sm font-semibold text-foreground">{scenario.title}</p>
                  <p className="mt-1 text-xs text-foreground/70">{scenario.industry} • {scenario.impact}</p>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="glass p-6 space-y-4">
          <div className="flex items-center justify-between gap-3">
            <h2 className="text-lg font-semibold text-accent flex items-center gap-2">
              <ClipboardList className="h-5 w-5" />
              Raw Console Logs
            </h2>
            <span className="text-xs text-foreground/70">{lineCount} lines loaded</span>
          </div>

          <textarea
            value={rawLogText}
            onChange={(event) => setRawLogText(event.target.value)}
            className="h-72 w-full rounded-xl border border-border/50 bg-black/35 p-4 font-mono text-xs text-emerald-200 outline-none focus:border-accent/60"
            placeholder="Paste browser console logs here..."
            aria-label="Raw console logs"
          />

          <button
            type="button"
            onClick={runAnalysis}
            disabled={analyzing}
            className="inline-flex items-center gap-2 rounded-xl bg-accent px-5 py-3 text-sm font-bold text-primary transition-transform hover:scale-[1.01] disabled:opacity-60"
          >
            {analyzing ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
            Analyze Logs
          </button>

          <div className="rounded-xl border border-border/50 bg-white/5 p-4 space-y-3">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <h3 className="text-sm font-semibold text-foreground">Live Runtime Ingestion</h3>
              <span className="text-xs text-foreground/70">{runtimeEvents.length} captured events</span>
            </div>
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                onClick={() => setCaptureLiveRuntime((previous) => !previous)}
                className={cn(
                  "rounded-lg px-3 py-2 text-xs font-semibold border transition-colors",
                  captureLiveRuntime
                    ? "border-emerald-500/50 bg-emerald-500/15 text-emerald-300"
                    : "border-border/50 bg-white/10 text-foreground",
                )}
              >
                {captureLiveRuntime ? "Stop Live Capture" : "Start Live Capture"}
              </button>

              <button
                type="button"
                onClick={runRuntimeAnalysis}
                disabled={analyzingRuntime || runtimeEvents.length === 0}
                className="rounded-lg px-3 py-2 text-xs font-semibold border border-accent/50 bg-accent/10 text-accent disabled:opacity-50"
              >
                {analyzingRuntime ? "Analyzing..." : "Analyze Live Stream"}
              </button>

              <button
                type="button"
                onClick={clearRuntime}
                disabled={clearingRuntime || runtimeEvents.length === 0}
                className="rounded-lg px-3 py-2 text-xs font-semibold border border-red-500/40 bg-red-500/10 text-red-300 disabled:opacity-50 inline-flex items-center gap-1"
              >
                <Trash2 className="h-3.5 w-3.5" />
                {clearingRuntime ? "Clearing..." : "Clear Stream"}
              </button>
            </div>

            {runtimeEvents.length > 0 && (
              <div className="max-h-40 overflow-auto rounded-lg border border-border/40 bg-black/35 p-2 space-y-1">
                {runtimeEvents.slice(-8).map((item) => (
                  <p key={item.event_id} className="font-mono text-[11px] text-emerald-200 whitespace-pre-wrap">
                    [{(item.level || "error").toUpperCase()}] {item.message}
                  </p>
                ))}
              </div>
            )}
          </div>
        </div>
      </section>

      {analysis && (
        <section className="space-y-6">
          <div className="flex flex-wrap gap-2 justify-end">
            <button
              type="button"
              onClick={exportJsonReport}
              className="inline-flex items-center gap-2 rounded-lg border border-border/50 bg-white/10 px-3 py-2 text-xs font-semibold text-foreground hover:bg-white/15"
            >
              <Download className="h-3.5 w-3.5" />
              Export JSON
            </button>
            <button
              type="button"
              onClick={exportPdfReport}
              disabled={exportingPdf}
              className="inline-flex items-center gap-2 rounded-lg border border-accent/50 bg-accent/10 px-3 py-2 text-xs font-semibold text-accent disabled:opacity-60"
            >
              <Download className="h-3.5 w-3.5" />
              {exportingPdf ? "Generating PDF..." : "Export PDF"}
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="glass p-4">
              <p className="text-xs text-foreground/70">Detected Errors</p>
              <p className="text-2xl font-bold text-accent">{analysis.summary.detected_errors}</p>
            </div>
            <div className="glass p-4">
              <p className="text-xs text-foreground/70">Overall Risk</p>
              <p className="text-2xl font-bold text-accent">{analysis.summary.overall_risk}</p>
            </div>
            <div className="glass p-4">
              <p className="text-xs text-foreground/70">Unclassified Lines</p>
              <p className="text-2xl font-bold text-accent">{analysis.summary.unclassified_lines}</p>
            </div>
            <div className="glass p-4">
              <p className="text-xs text-foreground/70">Estimated Speedup</p>
              <p className="text-sm font-semibold text-accent mt-1">{analysis.efficiency_advantage.time_saved_estimate}</p>
            </div>
          </div>

          <div className="glass p-6 space-y-4">
            <h3 className="text-lg font-semibold text-accent">Detected Errors and Fix Strategy</h3>
            {analysis.detected_errors.length === 0 && (
              <div className="rounded-lg border border-emerald-500/40 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-300 flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4" />
                No known high-risk signatures found. Continue monitoring unknown lines.
              </div>
            )}

            {analysis.detected_errors.map((finding, index) => (
              <article key={`${finding.error_type}-${index}`} className="rounded-xl border border-border/50 bg-white/5 p-4 space-y-3">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-sm font-bold text-foreground">{finding.error_type}</span>
                  <span className={cn("rounded-md border px-2 py-1 text-xs font-semibold", severityStyles[finding.severity] || severityStyles.MEDIUM)}>
                    {finding.severity}
                  </span>
                  <span className="text-xs text-foreground/70">line {finding.line_number}</span>
                  <span className="text-xs text-foreground/70">confidence {(finding.confidence * 100).toFixed(0)}%</span>
                </div>

                <pre className="overflow-x-auto rounded-lg bg-black/40 p-3 text-xs text-emerald-200">{finding.log_excerpt}</pre>

                <div>
                  <p className="text-xs font-semibold uppercase tracking-wider text-foreground/70">Likely Root Cause</p>
                  <p className="text-sm text-foreground mt-1">{finding.root_cause}</p>
                </div>

                <div>
                  <p className="text-xs font-semibold uppercase tracking-wider text-foreground/70">How To Solve</p>
                  <ul className="mt-1 space-y-1 text-sm text-foreground">
                    {finding.how_to_solve.map((step, stepIndex) => (
                      <li key={stepIndex} className="flex gap-2">
                        <span className="text-accent">{stepIndex + 1}.</span>
                        <span>{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="rounded-lg border border-accent/35 bg-accent/10 px-3 py-2 text-xs text-foreground/90">
                  Prevention: {finding.preventive_control}
                </div>
              </article>
            ))}
          </div>

          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            <div className="glass p-6">
              <h3 className="text-lg font-semibold text-accent">Triage Priority</h3>
              <div className="mt-3 space-y-2">
                {analysis.triage_priority.map((item) => (
                  <div key={`${item.order}-${item.error_type}`} className="rounded-lg border border-border/40 bg-white/5 px-3 py-2">
                    <p className="text-sm font-semibold text-foreground">{item.order}. {item.error_type}</p>
                    <p className="text-xs text-foreground/70 mt-1">{item.why_first}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="glass p-6">
              <h3 className="text-lg font-semibold text-accent">Operational Advantage</h3>
              <div className="mt-3 space-y-3 text-sm text-foreground">
                <p><span className="text-accent font-semibold">Auto Grouping:</span> {analysis.efficiency_advantage.auto_grouping}</p>
                <p><span className="text-accent font-semibold">Root Cause Mapping:</span> {analysis.efficiency_advantage.root_cause_mapping}</p>
                <p><span className="text-accent font-semibold">Time Saved:</span> {analysis.efficiency_advantage.time_saved_estimate}</p>
              </div>
            </div>
          </div>

          {analysis.unknown_lines.length > 0 && (
            <div className="glass p-6">
              <h3 className="text-lg font-semibold text-accent flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-yellow-300" />
                Unknown Lines Requiring Human Review
              </h3>
              <div className="mt-3 space-y-2">
                {analysis.unknown_lines.slice(0, 8).map((line) => (
                  <div key={`${line.line_number}-${line.log_excerpt}`} className="rounded-lg border border-border/40 bg-white/5 px-3 py-2">
                    <p className="text-xs text-foreground/60">line {line.line_number}</p>
                    <pre className="text-xs text-foreground mt-1 whitespace-pre-wrap">{line.log_excerpt}</pre>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>
      )}
    </div>
  )
}
