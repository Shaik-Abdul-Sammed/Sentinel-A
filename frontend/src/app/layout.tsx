import type { Metadata } from "next";
import "./globals.css";
import { DashboardShell } from "@/components/layout/DashboardShell";

export const metadata: Metadata = {
  title: "Sentinel-A | Cyber Shield",
  description: "India's AI Agent Cyber Shield",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="cyber-grid min-h-screen font-sans">
        <a href="#main-content" className="skip-link">Skip to main content</a>
        <DashboardShell>
          {children}
        </DashboardShell>
      </body>
    </html>
  );
}

