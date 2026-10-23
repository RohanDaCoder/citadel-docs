import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { ThemeProvider } from "next-themes";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "Citadel Wiki — Minefort Citadel developer documentation",
    template: "%s · Citadel Wiki",
  },
  description:
    "The developer wiki for Minefort Citadel — a Luau scripting engine for Minecraft servers. 60 structured articles, 5 guides, a cookbook, and a complete API reference: 29 globals, 141 types, 674 documented members.",
  keywords: ["Citadel", "Minefort", "Minecraft", "Luau", "game development", "wiki", "docs", "API reference"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-background text-foreground`}
      >
        <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={false}>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
