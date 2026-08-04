"use client"

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Shield, Lock, User, ArrowRight, Loader2, AlertCircle } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { getAccessTokenPayload, loginWithCredentials } from '@/lib/api'

const demoAccounts = [
  { label: 'SOC Analyst', username: 'soc', password: 'soc2026' },
  { label: 'Admin', username: 'abdul', password: 'sentinela2026' },
  { label: 'Sensor', username: 'sensor', password: 'sensor2026' },
]

export default function LoginPage() {
  const [loading, setLoading] = useState(false)
  const [username, setUsername] = useState('soc')
  const [password, setPassword] = useState('soc2026')
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const result = await loginWithCredentials(username, password)
      const role = getAccessTokenPayload(result.access_token)?.role
      if (!role) {
        throw new Error('Login succeeded but no role was returned.')
      }
      setLoading(false)
      router.replace('/dashboard')
    } catch (loginError) {
      setLoading(false)
      setError(loginError instanceof Error ? loginError.message : 'Authentication failed.')
    }
  }

  const quickDemoLogin = async (demoUsername: string, demoPassword: string) => {
    setUsername(demoUsername)
    setPassword(demoPassword)
    setLoading(true)
    setError(null)

    try {
      const result = await loginWithCredentials(demoUsername, demoPassword)
      const role = getAccessTokenPayload(result.access_token)?.role
      if (!role) {
        throw new Error('Login succeeded but no role was returned.')
      }
      setLoading(false)
      router.replace('/dashboard')
    } catch (loginError) {
      setLoading(false)
      setError(loginError instanceof Error ? loginError.message : 'Authentication failed.')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-background text-foreground px-4 py-10">
      {/* Background Glows */}
      <div className="absolute top-[-10%] left-[-10%] w-1/2 h-1/2 bg-primary/25 rounded-full blur-[120px]" aria-hidden="true" />
      <div className="absolute bottom-[-10%] right-[-10%] w-1/2 h-1/2 bg-secondary/25 rounded-full blur-[120px]" aria-hidden="true" />

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass w-full max-w-md p-10 z-10 border-white/10"
        role="region"
        aria-labelledby="login-heading"
      >
        <div className="flex flex-col items-center mb-10">
          <div className="p-4 bg-accent rounded-2xl mb-4 cyber-glow">
            <Shield className="w-10 h-10 text-primary" aria-hidden="true" />
          </div>
          <h1 id="login-heading" className="text-3xl font-black text-accent tracking-tighter">SENTINEL-A</h1>
          <p className="text-foreground/80 text-sm mt-1">Autonomous Agent Cyber Shield</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-6" aria-describedby="login-help-text">
          {error && (
            <div className="flex items-start gap-3 rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200" role="alert" aria-live="assertive">
              <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
              <span>{error}</span>
            </div>
          )}

          <div className="space-y-2">
            <label htmlFor="username" className="text-xs font-bold text-foreground uppercase ml-1">Identity</label>
            <div className="relative">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground/30" aria-hidden="true" />
              <input 
                id="username"
                type="text" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username" 
                autoComplete="username"
                aria-invalid={Boolean(error)}
                className="w-full bg-white/10 border border-border/40 rounded-xl py-3.5 pl-12 pr-4 outline-none focus:border-accent/60 transition-all text-sm text-foreground"
              />
            </div>
          </div>

          <div className="space-y-2">
            <label htmlFor="password" className="text-xs font-bold text-foreground uppercase ml-1">Access Code</label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground/30" aria-hidden="true" />
              <input 
                id="password"
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••" 
                autoComplete="current-password"
                aria-invalid={Boolean(error)}
                className="w-full bg-white/10 border border-border/40 rounded-xl py-3.5 pl-12 pr-4 outline-none focus:border-accent/60 transition-all text-sm font-mono text-foreground"
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-foreground uppercase ml-1">Demo Login</label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
              {demoAccounts.map((account) => (
                <button
                  key={account.username}
                  type="button"
                  disabled={loading}
                  onClick={() => quickDemoLogin(account.username, account.password)}
                  className="rounded-lg border border-border/50 bg-white/10 px-3 py-2 text-xs font-semibold text-foreground transition-colors hover:border-accent/50 hover:text-accent disabled:opacity-50"
                  aria-label={`Login as ${account.label}`}
                >
                  {account.label}
                </button>
              ))}
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

        <div id="login-help-text" className="mt-6 rounded-xl border border-border/50 bg-white/10 px-4 py-3 text-xs text-foreground">
          Demo credentials: <span className="font-mono text-accent">soc / soc2026</span> or <span className="font-mono text-accent">abdul / sentinela2026</span>
        </div>

        <div className="mt-8 pt-8 border-t border-border/40 text-center">
          <p className="text-xs text-foreground">
            Powered by Autonomous Threat Intelligence Mesh
          </p>
        </div>
      </motion.div>
    </div>
  )
}
