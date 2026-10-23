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
    default: "Citadel Docs — Build a Minecraft game in Luau",
    template: "%s · Citadel Docs",
  },
  description:
    "Structured, searchable documentation for Minefort Citadel: 5 hands-on game guides, 9 concept topics (55 pages), and a full API reference with 29 globals and 136 types.",
  keywords: ["Citadel", "Minefort", "Minecraft", "Luau", "game development", "docs", "API reference"],
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
