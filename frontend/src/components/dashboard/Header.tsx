"use client"

import React from 'react'
import { Bell, Search } from 'lucide-react'

export function Header() {
  return (
    <header className="h-16 border-b border-border/30 px-8 flex items-center justify-between sticky top-0 bg-background/80 backdrop-blur-md z-40">
      <div className="flex items-center gap-4 bg-white/5 px-4 py-2 rounded-full border border-border/20 w-96">
        <Search className="w-4 h-4 text-foreground/40" />
        <input 
          type="text" 
          placeholder="Search for threats or logs..." 
          className="bg-transparent border-none outline-none text-sm w-full placeholder:text-foreground/30"
        />
      </div>

      <div className="flex items-center gap-4">
        <button className="p-2 rounded-full hover:bg-white/5 text-foreground/60 relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border-2 border-background"></span>
        </button>
        <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-accent to-secondary border border-border/50"></div>
      </div>
    </header>
  )
}
