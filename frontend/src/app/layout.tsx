import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { DashboardShell } from "@/components/layout/DashboardShell";

const inter = Inter({ subsets: ["latin"] });

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
      <body className={`${inter.className} cyber-grid min-h-screen`}>
        <DashboardShell>
          {children}
        </DashboardShell>
      </body>
    </html>
  );
}
