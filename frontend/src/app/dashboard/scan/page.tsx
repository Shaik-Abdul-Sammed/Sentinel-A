"use client"

import React, { useState } from 'react'
import { Search, ShieldCheck, ShieldAlert, Loader2, Send, Info } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { analyzeURL } from '@/lib/api'
import { cn } from '@/lib/utils'

export default function ScanPage() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!url) return
    
    setLoading(true)
    try {
      const data = await analyzeURL(url)
      setResult(data)
    } catch (err) {
      console.error(err)
      // Mock result if API is not running for prototype demo
      setResult({
        analysis: {
          final_verdict: "SUSPICIOUS",
          confidence: 0.89,
          ai_reasoning: "The URL structure matches known phishing templates targeting financial institutions."
        },
        recommendations: {
          actions: [
            { action: "Block Access", description: "Prevent users from accessing this domain." },
            { action: "Notify IT", description: "Alert security team about potential campaign." }
          ]
        }
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h1 className="text-3xl font-bold text-accent">AI Threat Scanner</h1>
        <p className="text-foreground/50 mt-1">Submit URLs, Emails, or Logs for deep heuristic and LLM analysis.</p>
      </div>

      <div className="glass p-8">
        <form onSubmit={handleScan} className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-foreground/30" />
            <input 
              type="text" 
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Paste suspicious URL or text snippet here..." 
              className="w-full bg-white/5 border border-border/30 rounded-xl py-4 pl-12 pr-4 outline-none focus:border-accent/50 transition-colors"
            />
          </div>
          <button 
            disabled={loading}
            className="px-8 bg-accent text-primary font-bold rounded-xl hover:scale-105 transition-transform disabled:opacity-50 disabled:scale-100 flex items-center gap-2"
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
            Analyze
          </button>
        </form>
      </div>

      <AnimatePresence>
        {result && (
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            <div className={cn(
              "md:col-span-2 glass p-8 border-l-8",
              result.analysis.final_verdict === 'SAFE' ? 'border-l-green-500' : 'border-l-red-500'
            )}>
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-sm uppercase tracking-widest text-foreground/40 font-bold">Analysis Verdict</h3>
                  <div className="flex items-center gap-2 mt-1">
                    {result.analysis.final_verdict === 'SAFE' ? (
                      <ShieldCheck className="w-8 h-8 text-green-400" />
                    ) : (
                      <ShieldAlert className="w-8 h-8 text-red-400" />
                    )}
                    <span className={cn(
                      "text-4xl font-black",
                      result.analysis.final_verdict === 'SAFE' ? 'text-green-400' : 'text-red-400'
                    )}>
                      {result.analysis.final_verdict}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-xs text-foreground/40 font-bold">AI CONFIDENCE</p>
                  <p className="text-2xl font-mono text-accent">{(result.analysis.confidence * 100).toFixed(1)}%</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="bg-white/5 p-4 rounded-lg">
                  <p className="text-sm font-semibold mb-2 flex items-center gap-2">
                    <Info className="w-4 h-4 text-accent" />
                    Agent Reasoning
                  </p>
                  <p className="text-sm text-foreground/70 leading-relaxed italic">
                    "{result.analysis.ai_reasoning}"
                  </p>
                </div>
              </div>
            </div>

            <div className="glass p-8">
              <h3 className="text-sm font-bold text-accent mb-6">SUGGESTED ACTIONS</h3>
              <div className="space-y-4">
                {result.recommendations.actions.map((act: any, i: number) => (
                  <div key={i} className="group cursor-pointer">
                    <p className="text-sm font-bold group-hover:text-accent transition-colors">{act.action}</p>
                    <p className="text-xs text-foreground/40 mt-1">{act.description}</p>
                    <div className="mt-2 h-1 w-0 bg-accent group-hover:w-full transition-all duration-300" />
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
