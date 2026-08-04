import type { Metadata } from "next";
import { Space_Grotesk, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";
import { DashboardShell } from "@/components/layout/DashboardShell";

const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-ui",
  display: "swap",
});

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  weight: ["400", "600"],
  display: "swap",
});

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
      <body className={`${spaceGrotesk.variable} ${ibmPlexMono.variable} cyber-grid min-h-screen`}>
        <a href="#main-content" className="skip-link">Skip to main content</a>
        <DashboardShell>
          {children}
        </DashboardShell>
      </body>
    </html>
  );
}
