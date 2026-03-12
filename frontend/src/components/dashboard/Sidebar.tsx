"use client"

import React from 'react'
import { Shield, LayoutDashboard, Search, Settings, User, AlertTriangle } from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'

const navItems = [
  { name: 'Overview', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Threat Scanner', href: '/dashboard/scan', icon: Search },
  { name: 'Alerts', href: '/dashboard/alerts', icon: AlertTriangle },
  { name: 'Settings', href: '/dashboard/settings', icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <div className="w-64 h-screen glass border-r border-border/50 flex flex-col p-4 fixed left-0 top-0 z-50">
      <div className="flex items-center gap-2 mb-10 px-2">
        <div className="p-2 bg-accent rounded-lg">
          <Shield className="w-6 h-6 text-primary" />
        </div>
        <span className="text-xl font-bold tracking-tight text-accent">SENTINEL-A</span>
      </div>

      <nav className="flex-1 space-y-2">
        {navItems.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group",
                isActive 
                  ? "bg-accent text-primary font-medium cyber-glow" 
                  : "text-foreground/70 hover:bg-white/5 hover:text-accent"
              )}
            >
              <item.icon className={cn("w-5 h-5", isActive ? "text-primary" : "group-hover:text-accent")} />
              {item.name}
            </Link>
          )
        })}
      </nav>

      <div className="mt-auto pt-4 border-t border-border/30">
        <button className="flex items-center gap-3 px-4 py-3 w-full rounded-xl text-foreground/70 hover:bg-white/5 hover:text-accent transition-all">
          <User className="w-5 h-5" />
          <span>Abdul Sammed</span>
        </button>
      </div>
    </div>
  )
}
