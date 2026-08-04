"use client"

import React, { useEffect, useState } from "react"
import { Moon, Sun } from "lucide-react"

type Theme = "dark" | "light"

const STORAGE_KEY = "sentinel-theme"

function getPreferredTheme(): Theme {
  if (typeof window === "undefined") {
    return "dark"
  }

  const storedTheme = window.localStorage.getItem(STORAGE_KEY)
  if (storedTheme === "dark" || storedTheme === "light") {
    return storedTheme
  }

  const prefersLight = window.matchMedia("(prefers-color-scheme: light)").matches
  return prefersLight ? "light" : "dark"
}

function applyTheme(theme: Theme) {
  document.documentElement.setAttribute("data-theme", theme)
  document.documentElement.style.colorScheme = theme
  window.localStorage.setItem(STORAGE_KEY, theme)
}

export function ThemeToggle({ className = "" }: { className?: string }) {
  const [theme, setTheme] = useState<Theme>("dark")
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    const preferredTheme = getPreferredTheme()
    setTheme(preferredTheme)
    applyTheme(preferredTheme)
    setMounted(true)
  }, [])

  const toggleTheme = () => {
    const nextTheme: Theme = theme === "dark" ? "light" : "dark"
    setTheme(nextTheme)
    applyTheme(nextTheme)
  }

  if (!mounted) {
    return (
      <button
        type="button"
        aria-label="Theme toggle loading"
        className={`h-10 w-10 rounded-full border border-border/50 bg-white/10 ${className}`.trim()}
      />
    )
  }

  const isLight = theme === "light"

  return (
    <button
      type="button"
      onClick={toggleTheme}
      className={`inline-flex h-10 w-10 items-center justify-center rounded-full border border-border/60 bg-white/10 text-foreground hover:bg-white/20 transition-colors ${className}`.trim()}
      aria-label={isLight ? "Switch to dark theme" : "Switch to light theme"}
      title={isLight ? "Switch to dark theme" : "Switch to light theme"}
    >
      {isLight ? <Moon className="h-4 w-4" aria-hidden="true" /> : <Sun className="h-4 w-4" aria-hidden="true" />}
    </button>
  )
}
