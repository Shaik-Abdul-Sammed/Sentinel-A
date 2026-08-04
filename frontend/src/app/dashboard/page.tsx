"use client"

import React, { useEffect, useState } from 'react'
import { ShieldAlert, Zap, Globe, Lock, CheckCircle, ExternalLink, Loader2 } from 'lucide-react'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'
import { getAlerts, getSystemStatus, getTimeline, simulateScenario, subscribeTelemetry, type AlertItem, type SystemStatus, type TimelineItem } from '@/lib/api'

export default function Dashboard() {
  const [status, setStatus] = useState<SystemStatus | null>(null)
  const [alerts, setAlerts] = useState<AlertItem[]>([])
  const [timeline, setTimeline] = useState<TimelineItem[]>([])
  const [loadingSim, setLoadingSim] = useState<"phishing" | "insider" | null>(null)

  const loadData = async () => {
    const [statusData, alertsData, timelineData] = await Promise.all([
      getSystemStatus(),
      getAlerts(8),
      getTimeline(6),
    ])
    setStatus(statusData)
    setAlerts(alertsData)
    setTimeline(timelineData)
  }

  useEffect(() => {
    loadData().catch(console.error)
    const unsubscribe = subscribeTelemetry((message) => {
      if (message?.status) {
        setStatus(message.status)
      }
      loadData().catch(console.error)
    })
    return () => unsubscribe()
  }, [])

  const stats = [
    { label: 'Shield Status', value: status?.shield_status || 'BOOTING', icon: Lock, color: 'text-green-400' },
    { label: 'Events Processed', value: String(status?.events_processed || 0), icon: Zap, color: 'text-yellow-400' },
    { label: 'Auto Blocks', value: String(status?.auto_blocked || 0), icon: ShieldAlert, color: 'text-red-400' },
    { label: 'Avg Risk Score', value: `${status?.average_risk_score || 0}`, icon: Globe, color: 'text-blue-400' },
  ]

  const runScenario = async (scenario: "phishing" | "insider") => {
    setLoadingSim(scenario)
    try {
      await simulateScenario(scenario)
      await loadData()
    } catch (error) {
      console.error(error)
    } finally {
      setLoadingSim(null)
    }
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col gap-4 md:flex-row md:justify-between md:items-end">
        <div>
          <h1 className="text-3xl font-bold text-accent">Cyber Shield Overview</h1>
          <p className="text-foreground/50 mt-1">Real-time autonomous defense monitoring with live telemetry.</p>
        </div>
        <div className="flex flex-col sm:flex-row gap-3" role="group" aria-label="Simulation controls">
          <button
            onClick={() => runScenario('phishing')}
            disabled={loadingSim !== null}
            className="px-6 py-2 glass hover:bg-white/10 transition-all text-sm font-medium disabled:opacity-60"
            aria-label="Run phishing simulation"
          >
            {loadingSim === 'phishing' ? <Loader2 className="w-4 h-4 animate-spin inline" /> : 'Simulate Phishing'}
          </button>
          <button
            onClick={() => runScenario('insider')}
            disabled={loadingSim !== null}
            className="px-6 py-2 bg-accent text-primary rounded-lg font-bold hover:scale-105 transition-transform text-sm cyber-glow disabled:opacity-60"
            aria-label="Run insider simulation"
          >
            {loadingSim === 'insider' ? <Loader2 className="w-4 h-4 animate-spin inline" /> : 'Simulate Insider'}
          </button>
        </div>
      </div>

      <p className="sr-only" aria-live="polite">
        {status ? `Shield ${status.shield_status}. ${status.events_processed} events processed.` : 'Loading shield status.'}
      </p>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <motion.div 
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="glass p-6 hover:border-accent/40 transition-colors"
          >
            <div className="flex justify-between items-start mb-4">
              <stat.icon className={cn("w-6 h-6", stat.color)} />
              <div className="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center">
                <div className={cn("w-2 h-2 rounded-full", stat.color.replace('text', 'bg'))} />
              </div>
            </div>
            <p className="text-foreground/40 text-sm">{stat.label}</p>
            <h3 className="text-2xl font-bold mt-1">{stat.value}</h3>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Risk Center */}
        <div className="lg:col-span-2 glass p-8 relative overflow-hidden">
          <h2 className="text-xl font-bold mb-6">Autonomous Threat Intelligence Timeline</h2>
          <div className="h-64 flex items-center justify-center border-y border-border/20 relative">
             {/* Mock Map Background */}
             <div className="absolute inset-0 opacity-10 flex items-center justify-center">
                <div className="w-full h-full border-[20px] border-accent/20 rounded-full blur-3xl animate-pulse" />
             </div>
             <div className="text-center relative z-10">
                <div className="text-6xl font-black text-accent drop-shadow-[0_0_20px_rgba(182,234,218,0.5)]">{status?.average_risk_score || 0}</div>
                <div className="text-foreground/60 uppercase tracking-widest text-sm mt-2">Current Average Risk Score</div>
             </div>
          </div>
          <div className="mt-6 flex justify-between items-center text-sm">
            <div className="flex gap-6">
               <div className="flex items-center gap-2">
                 <div className="w-3 h-3 bg-red-500 rounded-full" /> 
                 <span>Open Alerts ({status?.alerts_open || 0})</span>
               </div>
               <div className="flex items-center gap-2 text-foreground/50">
                 <div className="w-3 h-3 bg-yellow-500 rounded-full" /> 
                 <span>Escalations ({status?.escalations || 0})</span>
               </div>
            </div>
            <span className="text-accent flex items-center gap-1">Live Pipeline <ExternalLink className="w-3 h-3" /></span>
          </div>
        </div>

        {/* AI Agent Activity */}
        <div className="glass p-8 flex flex-col">
          <h2 className="text-xl font-bold mb-6">Recent Decisions</h2>
          <div className="space-y-4 flex-1">
            {timeline.length === 0 && (
              <div className="p-4 bg-white/5 border rounded-r-lg">
                <p className="text-xs text-foreground/50">No events yet. Run a simulation to populate live decisions.</p>
              </div>
            )}
            {timeline.map((item, idx) => (
              <div key={`${item.time}-${idx}`} className="p-4 bg-white/5 border border-l-4 border-l-yellow-500 rounded-r-lg">
                <p className="text-xs text-yellow-400 font-bold mb-1">{item.event}</p>
                <p className="text-sm font-medium">{item.message}</p>
                <p className="text-xs text-foreground/40 mt-1">Risk Score: {item.risk_score}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Threats Table */}
      <div className="glass p-8">
         <h2 className="text-xl font-bold mb-6">Real-time Analysis Log</h2>
         <div className="overflow-x-auto">
           <table className="w-full text-left">
             <caption className="sr-only">Most recent threats analyzed by Sentinel-A policy agents</caption>
             <thead>
               <tr className="border-b border-border/30 text-foreground/40 text-sm">
                 <th scope="col" className="pb-4 font-medium">Threat Type</th>
                 <th scope="col" className="pb-4 font-medium">Source / Target</th>
                 <th scope="col" className="pb-4 font-medium">Level</th>
                 <th scope="col" className="pb-4 font-medium">AI Agent</th>
                 <th scope="col" className="pb-4 font-medium">Status</th>
                 <th scope="col" className="pb-4"><span className="sr-only">Actions</span></th>
               </tr>
             </thead>
             <tbody className="text-sm">
               {alerts.map((threat, idx) => (
                 <motion.tr 
                   initial={{ opacity: 0, x: -20 }}
                   animate={{ opacity: 1, x: 0 }}
                   transition={{ delay: 0.5 + (idx * 0.1) }}
                   key={threat.alert_id}
                   className="border-b border-border/20 last:border-none group hover:bg-white/5 transition-all"
                 >
                   <td className="py-4 font-semibold">{threat.threat_type}</td>
                   <td className="py-4 text-foreground/60">{threat.actor_id} @ {threat.source}</td>
                   <td className="py-4">
                      <span className={cn(
                        "px-2 py-1 rounded text-[10px] font-black tracking-tight",
                        threat.risk_level === 'CRITICAL' ? "bg-red-500 text-white shadow-[0_0_10px_rgba(239,68,68,0.4)]" :
                        threat.risk_level === 'HIGH' ? "bg-orange-500 text-white" : "bg-yellow-500 text-black"
                      )}>
                        {threat.risk_level}
                      </span>
                   </td>
                   <td className="py-4 flex items-center gap-2">
                     <div className="w-2 h-2 rounded-full bg-accent animate-pulse shadow-[0_0_8px_#B6EADA]" />
                     Policy Agent
                   </td>
                   <td className="py-4">
                      <div className="flex items-center gap-2">
                         <CheckCircle className="w-4 h-4 text-green-400" />
                         <span>{threat.decision}</span>
                      </div>
                   </td>
                   <td className="py-4 text-right">
                     <button aria-label={`Open alert ${threat.alert_id}`} className="text-foreground/30 hover:text-accent opacity-0 group-hover:opacity-100 transition-opacity">
                         <ExternalLink className="w-4 h-4" />
                      </button>
                   </td>
                 </motion.tr>
               ))}
               {alerts.length === 0 && (
                 <tr>
                   <td className="py-6 text-foreground/50" colSpan={6}>No alerts yet. Trigger simulation to see detections.</td>
                 </tr>
               )}
             </tbody>
           </table>
         </div>
      </div>
    </div>
  )
}
