import Link from "next/link"
import { ArrowRight, Shield, Radar, Lock, Sparkles, Waves } from "lucide-react"

const highlights = [
  { title: "Live telemetry", description: "Streaming alerts, status, and timeline events from the backend pipeline.", icon: Radar },
  { title: "Protected console", description: "Authentication-gated dashboard with live websocket updates.", icon: Lock },
  { title: "Demo-ready", description: "Built-in simulation paths for phishing and insider scenarios.", icon: Sparkles },
]

export default function HomePage() {
  return (
    <div className="min-h-screen overflow-hidden bg-background text-foreground">
      <div aria-hidden="true" className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(182,234,218,0.22),transparent_30%),radial-gradient(circle_at_bottom_right,rgba(0,194,255,0.18),transparent_30%),linear-gradient(135deg,rgba(255,255,255,0.03),transparent_45%)]" />
      <div aria-hidden="true" className="absolute inset-0 cyber-grid opacity-30" />

      <section className="relative mx-auto flex min-h-screen w-full max-w-7xl flex-col justify-center px-6 py-16 lg:px-10" aria-labelledby="home-title">
        <div className="grid items-center gap-14 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="space-y-8">
            <div className="inline-flex items-center gap-3 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.3em] text-foreground/60 backdrop-blur">
              <Waves className="h-3.5 w-3.5 text-accent" aria-hidden="true" />
              Sentinel-A Cyber Defense Platform
            </div>

            <div className="space-y-5">
              <h1 id="home-title" className="max-w-3xl text-5xl font-black tracking-tight text-accent sm:text-6xl lg:text-7xl">
                Real-time AI defense for live security operations.
              </h1>
              <p className="max-w-2xl text-base leading-7 text-foreground/85 sm:text-lg">
                Sentinel-A combines telemetry ingestion, agent orchestration, anomaly detection, and phishing analysis into a demo-ready cyber shield with a working login flow and protected SOC console.
              </p>
            </div>

            <div className="flex flex-col gap-4 sm:flex-row">
              <Link href="/login" className="inline-flex items-center justify-center gap-2 rounded-xl bg-accent px-6 py-4 font-black text-primary transition-transform hover:scale-[1.02] cyber-glow">
                Enter the console
                <ArrowRight className="h-5 w-5" aria-hidden="true" />
              </Link>
              <Link href="/dashboard" className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-6 py-4 font-semibold text-foreground backdrop-blur transition-colors hover:bg-white/10">
                Open dashboard preview
              </Link>
            </div>

            <div className="grid gap-4 pt-4 sm:grid-cols-3">
              {highlights.map((item) => (
                <div key={item.title} className="glass rounded-2xl border border-white/5 p-4">
                  <item.icon className="mb-3 h-5 w-5 text-accent" aria-hidden="true" />
                  <h2 className="text-sm font-bold text-foreground">{item.title}</h2>
                  <p className="mt-2 text-xs leading-5 text-foreground/60">{item.description}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="relative">
            <div aria-hidden="true" className="absolute -inset-6 rounded-[2rem] bg-accent/10 blur-3xl" />
            <div className="glass relative overflow-hidden rounded-[2rem] border border-white/10 p-8 shadow-2xl shadow-black/30" aria-label="System readiness panel">
              <div className="flex items-center justify-between border-b border-white/10 pb-5">
                <div>
                  <p className="text-xs uppercase tracking-[0.3em] text-foreground/40">System Status</p>
                  <h2 className="mt-2 text-2xl font-black text-foreground">Operations online</h2>
                </div>
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-accent text-primary cyber-glow">
                  <Shield className="h-6 w-6" aria-hidden="true" />
                </div>
              </div>

              <div className="grid gap-4 py-6 sm:grid-cols-2">
                {[
                  ["Threat pipeline", "Streaming"],
                  ["Auth flow", "Backend-backed"],
                  ["Demo roles", "SOC / Admin"],
                  ["Websocket", "Protected"],
                ].map(([label, value]) => (
                  <div key={label} className="rounded-2xl border border-white/8 bg-white/5 p-4">
                    <p className="text-xs uppercase tracking-[0.2em] text-foreground/40">{label}</p>
                    <p className="mt-2 text-lg font-bold text-foreground">{value}</p>
                  </div>
                ))}
              </div>

              <div className="rounded-2xl border border-accent/20 bg-accent/10 p-5 text-sm text-foreground/80">
                Demo credentials: <span className="font-mono text-accent">soc / soc2026</span>
                <br />
                Admin demo: <span className="font-mono text-accent">abdul / sentinela2026</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
