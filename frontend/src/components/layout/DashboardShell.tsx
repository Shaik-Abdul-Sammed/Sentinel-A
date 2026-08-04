"use client"

import React, { useEffect, useState } from 'react'
import { Sidebar } from "@/components/dashboard/Sidebar";
import { Header } from "@/components/dashboard/Header";
import { ThemeToggle } from "@/components/layout/ThemeToggle";
import { usePathname, useRouter } from "next/navigation";
import { ACCESS_TOKEN_STORAGE_KEY } from "@/lib/api";

export function DashboardShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const isPublicPage = pathname === "/" || pathname === "/login";
  const [ready, setReady] = useState(isPublicPage);

  useEffect(() => {
    if (isPublicPage) {
      setReady(true);
      return;
    }

    const token = window.localStorage.getItem(ACCESS_TOKEN_STORAGE_KEY);
    if (!token && pathname.startsWith("/dashboard")) {
      router.replace("/login");
      return;
    }

    setReady(true);
  }, [isPublicPage, pathname, router]);

  if (!ready) {
    return (
      <main id="main-content" className="flex min-h-screen w-full items-center justify-center text-sm text-foreground/50" role="main" aria-busy="true" aria-live="polite">
        Preparing secure session...
      </main>
    );
  }

  if (isPublicPage) {
    return (
      <div className="min-h-screen w-full">
        <div className="fixed right-4 top-4 z-[80]">
          <ThemeToggle />
        </div>
        <main id="main-content" className="min-h-screen w-full" role="main">{children}</main>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <Sidebar />
      <div className="md:pl-64 flex flex-col min-h-screen">
        <Header />
        <main id="main-content" className="flex-1 p-8" role="main">
          {children}
        </main>
      </div>
    </div>
  );
}
