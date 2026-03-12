"use client"

import React from 'react'
import { ShieldAlert, Zap, Globe, Lock, CheckCircle, ExternalLink } from 'lucide-react'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

const stats = [
  { label: 'Shield Status', value: 'ACTIVE', icon: Lock, color: 'text-green-400' },
  { label: 'AI Agents', value: '12', icon: Zap, color: 'text-yellow-400' },
  { label: 'Threats Blocked', value: '1,284', icon: ShieldAlert, color: 'text-red-400' },
  { label: 'Uptime', value: '99.98%', icon: Globe, color: 'text-blue-400' },
]

const recentThreats = [
  { id: 1, type: 'Phishing', target: 'hr@example.com', level: 'HIGH', agent: 'Agent-X Detect', status: 'Blocked' },
  { id: 2, type: 'Insider Risk', target: 'user_082', level: 'MEDIUM', agent: 'Behavioral-1', status: 'Monitoring' },
  { id: 3, type: 'Fraud Attempt', target: 'Fin-Node-4', level: 'CRITICAL', agent: 'Fraud Shield', status: 'Isolated' },
]

export default function Dashboard() {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-accent">Cyber Shield Overview</h1>
          <p className="text-foreground/50 mt-1">Real-time autonomous defense monitoring.</p>
        </div>
        <div className="flex gap-4">
          <button className="px-6 py-2 glass hover:bg-white/10 transition-all text-sm font-medium">Download Report</button>
          <button className="px-6 py-2 bg-accent text-primary rounded-lg font-bold hover:scale-105 transition-transform text-sm cyber-glow">
            Deploy New Agent
          </button>
        </div>
      </div>

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
          <h2 className="text-xl font-bold mb-6">Autonomous Threat Intelligence</h2>
          <div className="h-64 flex items-center justify-center border-y border-border/20 relative">
             {/* Mock Map Background */}
             <div className="absolute inset-0 opacity-10 flex items-center justify-center">
                <div className="w-full h-full border-[20px] border-accent/20 rounded-full blur-3xl animate-pulse" />
             </div>
             <div className="text-center relative z-10">
                <div className="text-6xl font-black text-accent drop-shadow-[0_0_20px_rgba(182,234,218,0.5)]">14%</div>
                <div className="text-foreground/60 uppercase tracking-widest text-sm mt-2">National Risk Level</div>
             </div>
          </div>
          <div className="mt-6 flex justify-between items-center text-sm">
            <div className="flex gap-6">
               <div className="flex items-center gap-2">
                 <div className="w-3 h-3 bg-red-500 rounded-full" /> 
                 <span>Active Attacks (2)</span>
               </div>
               <div className="flex items-center gap-2 text-foreground/50">
                 <div className="w-3 h-3 bg-yellow-500 rounded-full" /> 
                 <span>Potential Risks (5)</span>
               </div>
            </div>
            <button className="text-accent flex items-center gap-1 hover:underline">
               Detailed Map <ExternalLink className="w-3 h-3" />
            </button>
          </div>
        </div>

        {/* AI Agent Activity */}
        <div className="glass p-8 flex flex-col">
          <h2 className="text-xl font-bold mb-6">AI Agent Suggestions</h2>
          <div className="space-y-4 flex-1">
             <div className="p-4 bg-white/5 border border-l-4 border-l-red-500 rounded-r-lg">
                <p className="text-xs text-red-400 font-bold mb-1">CRITICAL SUGGESTION</p>
                <p className="text-sm font-medium">Isolate endpoint ID-094</p>
                <p className="text-xs text-foreground/40 mt-1">Found 85% match for lateral movement patterns.</p>
                <button className="mt-3 w-full py-1.5 bg-red-500/20 text-red-500 rounded text-xs font-bold hover:bg-red-500 hover:text-white transition-colors">
                  EXECUTE MITIGATION
                </button>
             </div>
             <div className="p-4 bg-white/5 border border-l-4 border-l-yellow-500 rounded-r-lg">
                <p className="text-xs text-yellow-400 font-bold mb-1">HIGH RISK ALERT</p>
                <p className="text-sm font-medium">Enforce MFA for user 'shaik.sammed'</p>
                <p className="text-xs text-foreground/40 mt-1">Unusual login geolocation detected.</p>
                <button className="mt-3 w-full py-1.5 bg-yellow-500/20 text-yellow-500 rounded text-xs font-bold hover:bg-yellow-500 hover:text-white transition-colors">
                  ACCEPT
                </button>
             </div>
          </div>
        </div>
      </div>

      {/* Recent Threats Table */}
      <div className="glass p-8">
         <h2 className="text-xl font-bold mb-6">Real-time Analysis Log</h2>
         <div className="overflow-x-auto">
           <table className="w-full text-left">
             <thead>
               <tr className="border-b border-border/30 text-foreground/40 text-sm">
                 <th className="pb-4 font-medium">Threat Type</th>
                 <th className="pb-4 font-medium">Source / Target</th>
                 <th className="pb-4 font-medium">Level</th>
                 <th className="pb-4 font-medium">AI Agent</th>
                 <th className="pb-4 font-medium">Status</th>
                 <th className="pb-4"></th>
               </tr>
             </thead>
             <tbody className="text-sm">
               {recentThreats.map((threat, idx) => (
                 <motion.tr 
                   initial={{ opacity: 0, x: -20 }}
                   animate={{ opacity: 1, x: 0 }}
                   transition={{ delay: 0.5 + (idx * 0.1) }}
                   key={threat.id} 
                   className="border-b border-border/20 last:border-none group hover:bg-white/5 transition-all"
                 >
                   <td className="py-4 font-semibold">{threat.type}</td>
                   <td className="py-4 text-foreground/60">{threat.target}</td>
                   <td className="py-4">
                      <span className={cn(
                        "px-2 py-1 rounded text-[10px] font-black tracking-tight",
                        threat.level === 'CRITICAL' ? "bg-red-500 text-white shadow-[0_0_10px_rgba(239,68,68,0.4)]" :
                        threat.level === 'HIGH' ? "bg-orange-500 text-white" : "bg-yellow-500 text-black"
                      )}>
                        {threat.level}
                      </span>
                   </td>
                   <td className="py-4 flex items-center gap-2">
                     <div className="w-2 h-2 rounded-full bg-accent animate-pulse shadow-[0_0_8px_#B6EADA]" />
                     {threat.agent}
                   </td>
                   <td className="py-4">
                      <div className="flex items-center gap-2">
                         <CheckCircle className="w-4 h-4 text-green-400" />
                         <span>{threat.status}</span>
                      </div>
                   </td>
                   <td className="py-4 text-right">
                      <button className="text-foreground/30 hover:text-accent opacity-0 group-hover:opacity-100 transition-opacity">
                         <ExternalLink className="w-4 h-4" />
                      </button>
                   </td>
                 </motion.tr>
               ))}
             </tbody>
           </table>
         </div>
      </div>
    </div>
  )
}
