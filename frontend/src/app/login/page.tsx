"use client"

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Shield, Lock, User, ArrowRight, Loader2 } from 'lucide-react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [loading, setLoading] = useState(false)
  const [username, setUsername] = useState('abdul')
  const [password, setPassword] = useState('')
  const router = useRouter()

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    // Mock login delay
    setTimeout(() => {
      setLoading(false)
      router.push('/')
    }, 1500)
  }

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-[#03001C]">
      {/* Background Glows */}
      <div className="absolute top-[-10%] left-[-10%] w-1/2 h-1/2 bg-primary/20 rounded-full blur-[120px]" />
      <div className="absolute bottom-[-10%] right-[-10%] w-1/2 h-1/2 bg-secondary/20 rounded-full blur-[120px]" />

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass w-full max-w-md p-10 z-10 border-white/5"
      >
        <div className="flex flex-col items-center mb-10">
          <div className="p-4 bg-accent rounded-2xl mb-4 cyber-glow">
            <Shield className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-3xl font-black text-accent tracking-tighter">SENTINEL-A</h1>
          <p className="text-foreground/50 text-sm mt-1">Autonomous Agent Cyber Shield</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-6">
          <div className="space-y-2">
            <label className="text-xs font-bold text-foreground/40 uppercase ml-1">Identity</label>
            <div className="relative">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground/30" />
              <input 
                type="text" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username" 
                className="w-full bg-white/5 border border-border/30 rounded-xl py-3.5 pl-12 pr-4 outline-none focus:border-accent/50 transition-all text-sm"
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-foreground/40 uppercase ml-1">Access Code</label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground/30" />
              <input 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••" 
                className="w-full bg-white/5 border border-border/30 rounded-xl py-3.5 pl-12 pr-4 outline-none focus:border-accent/50 transition-all text-sm font-mono"
              />
            </div>
          </div>

          <button 
            disabled={loading}
            className="w-full bg-accent text-primary font-black py-4 rounded-xl flex items-center justify-center gap-2 hover:scale-[1.02] active:scale-[0.98] transition-all cyber-glow disabled:opacity-50"
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : (
              <>
                AUTHENTICATE <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
        </form>

        <div className="mt-8 pt-8 border-t border-white/5 text-center">
          <p className="text-xs text-foreground/30">
            Powered by Autonomous Threat Intelligence Mesh
          </p>
        </div>
      </motion.div>
    </div>
  )
}
