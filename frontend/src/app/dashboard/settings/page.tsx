"use client"

import React, { useState, useEffect } from 'react'
import { Shield, Bell, Smartphone, Check, RotateCcw } from 'lucide-react'
import { getApiBaseUrl } from '@/lib/api'

export default function SettingsPage() {
  const [apiUrl, setApiUrl] = useState('http://localhost:8000')
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => {
      setApiUrl(getApiBaseUrl())
    }, 0)
    return () => clearTimeout(timer)
  }, [])

  const handleSaveUrl = () => {
    if (typeof window !== 'undefined') {
      window.localStorage.setItem('sentinel_api_url', apiUrl.trim())
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    }
  }

  const handleResetUrl = () => {
    if (typeof window !== 'undefined') {
      window.localStorage.removeItem('sentinel_api_url')
      setApiUrl(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000')
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    }
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold text-accent">Platform Settings</h1>
        <p className="text-foreground/50 mt-1">Configure your AI Cyber Shield and mobile web-app parameters.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="glass p-8 space-y-6">
           <h2 className="text-lg font-bold flex items-center gap-2">
             <Shield className="w-5 h-5 text-accent" /> AI Core Configuration
           </h2>
           <div className="space-y-4">
              <div className="flex justify-between items-center bg-white/5 p-4 rounded-xl">
                 <span className="text-sm">Autonomous Mode</span>
                 <div className="w-10 h-6 bg-accent rounded-full relative p-1 cursor-pointer">
                    <div className="w-4 h-4 bg-primary rounded-full ml-auto" />
                 </div>
              </div>
              <div className="flex justify-between items-center bg-white/5 p-4 rounded-xl">
                 <span className="text-sm">Sensitivity Level</span>
                 <span className="px-3 py-1 bg-accent/20 text-accent rounded text-xs font-bold uppercase">Enhanced</span>
              </div>
           </div>
        </div>

        <div className="glass p-8 space-y-6">
           <h2 className="text-lg font-bold flex items-center gap-2">
             <Smartphone className="w-5 h-5 text-accent" /> Capacitor & Web-App Gateway
           </h2>
           <div className="space-y-4">
              <div>
                 <label htmlFor="api-url-input" className="block text-xs font-bold uppercase tracking-wider text-foreground/60 mb-2">
                   Backend API URL (Mobile / Web)
                 </label>
                 <input
                   id="api-url-input"
                   type="text"
                   value={apiUrl}
                   onChange={(e) => setApiUrl(e.target.value)}
                   placeholder="http://localhost:8000 or http://10.0.2.2:8000"
                   className="w-full bg-white/5 border border-border/30 rounded-xl py-3 px-4 outline-none focus:border-accent/50 text-sm font-mono text-accent"
                 />
                 <p className="text-xs text-foreground/40 mt-1.5">
                   Default is localhost:8000. For Android emulator, use 10.0.2.2:8000.
                 </p>
              </div>
              <div className="flex gap-3">
                 <button
                   onClick={handleSaveUrl}
                   className="flex-1 py-3 bg-accent text-primary rounded-xl text-sm font-bold hover:opacity-90 flex items-center justify-center gap-2 transition-opacity"
                 >
                   {saved ? <Check className="w-4 h-4" /> : null}
                   {saved ? "Saved!" : "Save Endpoint"}
                 </button>
                 <button
                   onClick={handleResetUrl}
                   title="Reset to default"
                   className="px-4 py-3 border border-border/40 text-foreground/70 rounded-xl text-sm hover:bg-white/5 flex items-center justify-center transition-colors"
                 >
                   <RotateCcw className="w-4 h-4" />
                 </button>
              </div>
           </div>
        </div>

        <div className="glass p-8 space-y-6 md:col-span-2">
           <h2 className="text-lg font-bold flex items-center gap-2">
             <Bell className="w-5 h-5 text-accent" /> Alert Protocols & Safety Controls
           </h2>
           <div className="space-y-4">
              <div className="flex justify-between items-center bg-white/5 p-4 rounded-xl">
                 <span className="text-sm">Emergency Lockdown</span>
                 <span className="text-xs text-foreground/30">Manual Confirmation Required</span>
              </div>
              <button className="w-full py-3 border border-red-500/30 text-red-500 rounded-xl text-sm font-bold hover:bg-red-500 hover:text-white transition-all">
                FLUSH THREAT LOGS
              </button>
           </div>
        </div>
      </div>
    </div>
  )
}
