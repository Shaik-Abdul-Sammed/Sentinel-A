"use client"

import React from 'react'
import { Settings as SettingsIcon, Shield, Sliders, Database, Bell } from 'lucide-react'

export default function SettingsPage() {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold text-accent">Platform Settings</h1>
        <p className="text-foreground/50 mt-1">Configure your AI Cyber Shield parameters.</p>
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
             <Bell className="w-5 h-5 text-accent" /> Alert Protocols
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
