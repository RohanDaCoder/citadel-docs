"use client";

import { useEffect, useMemo, useState, useCallback } from "react";
import { Command } from "cmdk";
import { Search, FileText, BookOpen, Box, Globe, Braces, CornerDownLeft } from "lucide-react";
import searchJson from "@/data/search.json";

interface SearchEntry {
  t: "page" | "ref" | "refmember";
  title: string;
  section: string;
  route: string;
  text: string;
  keywords: string;
}

const entries = searchJson as unknown as SearchEntry[];

function kindOf(e: SearchEntry): string {
  if (e.t === "ref") return e.section === "API" ? "Global" : "Type";
  if (e.t === "refmember") return "API";
  return e.section === "guides" ? "Guide" : "Wiki";
}

const KIND_ICON: Record<string, React.ReactNode> = {
  Guide: <BookOpen className="size-3.5 shrink-0 text-emerald-600 dark:text-emerald-400" />,
  Wiki: <FileText className="size-3.5 shrink-0 text-sky-600 dark:text-sky-400" />,
  Global: <Globe className="size-3.5 shrink-0 text-amber-600 dark:text-amber-400" />,
  Type: <Box className="size-3.5 shrink-0 text-violet-600 dark:text-violet-400" />,
  API: <Braces className="size-3.5 shrink-0 text-rose-600 dark:text-rose-400" />,
};

const KIND_BADGE: Record<string, string> = {
  Guide: "bg-emerald-100 text-emerald-800 dark:bg-emerald-500/15 dark:text-emerald-300",
  Wiki: "bg-sky-100 text-sky-800 dark:bg-sky-500/15 dark:text-sky-300",
  Global: "bg-amber-100 text-amber-800 dark:bg-amber-500/15 dark:text-amber-300",
  Type: "bg-violet-100 text-violet-800 dark:bg-violet-500/15 dark:text-violet-300",
  API: "bg-rose-100 text-rose-800 dark:bg-rose-500/15 dark:text-rose-300",
};

export function SearchDialog({ open, onOpenChange }: { open: boolean; onOpenChange: (v: boolean) => void }) {
  const [query, setQuery] = useState("");

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.key === "k" || e.key === "K") && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        onOpenChange(!open);
      }
      if (e.key === "/" && !open) {
        const target = e.target as HTMLElement;
        if (target.tagName !== "INPUT" && target.tagName !== "TEXTAREA") {
          e.preventDefault();
          onOpenChange(true);
        }
      }
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open, onOpenChange]);

  const go = useCallback(
    (url: string) => {
      onOpenChange(false);
      setQuery("");
      window.location.hash = url;
      window.scrollTo({ top: 0 });
    },
    [onOpenChange],
  );

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return entries.slice(0, 40);
    const terms = q.split(/\s+/);
    const scored: { e: SearchEntry; score: number }[] = [];
    for (const e of entries) {
      const title = e.title.toLowerCase();
      const hay = (e.title + " " + e.section + " " + e.text + " " + e.keywords).toLowerCase();
      let score = -1;
      if (title.startsWith(q)) score = 100;
      else if (title.includes(q)) score = 60;
      else if (terms.every((t) => hay.includes(t))) score = 20;
      else if (hay.includes(q)) score = 10;
      if (score > 0) {
        // boost exact name match for API entries
        if (e.t !== "page" && title.split("(")[0].trim() === q) score += 50;
        scored.push({ e, score });
      }
    }
    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, 50).map((s) => s.e);
  }, [query]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center bg-zinc-950/50 px-4 pt-[12vh] backdrop-blur-sm"
      onClick={() => onOpenChange(false)}
    >
      <Command
        loop
        className="w-full max-w-xl overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-2xl dark:border-zinc-700 dark:bg-zinc-900"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center gap-2.5 border-b border-zinc-200 px-4 dark:border-zinc-700">
          <Search className="size-4 shrink-0 text-zinc-400" />
          <Command.Input
            autoFocus
            value={query}
            onValueChange={setQuery}
            placeholder="Search articles, guides, globals, types, and API calls…"
            className="h-12 w-full bg-transparent text-[15px] text-zinc-900 outline-none placeholder:text-zinc-400 dark:text-zinc-100"
          />
          <kbd className="hidden shrink-0 rounded border border-zinc-200 bg-zinc-50 px-1.5 py-0.5 text-[10px] font-medium text-zinc-400 sm:block dark:border-zinc-700 dark:bg-zinc-800">
            ESC
          </kbd>
        </div>
        <Command.List className="max-h-[46vh] overflow-y-auto p-2">
          <Command.Empty className="px-4 py-10 text-center text-sm text-zinc-400">
            No results for “{query}”
          </Command.Empty>
          {filtered.map((e) => {
            const k = kindOf(e);
            return (
            <Command.Item
              key={e.route + e.title}
              value={e.title + " " + e.section + " " + e.text}
              onSelect={() => go(e.route)}
              className="group flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-700 data-[selected=true]:bg-zinc-100 dark:text-zinc-300 dark:data-[selected=true]:bg-zinc-800"
            >
              {KIND_ICON[k]}
              <div className="min-w-0 flex-1">
                <div className={`truncate ${e.t === "page" ? "font-sans" : "font-mono"} text-[13px] text-zinc-900 dark:text-zinc-100`}>
                  {e.title}
                </div>
                <div className="truncate text-[11px] text-zinc-400 dark:text-zinc-500">{e.section}</div>
              </div>
              <span
                className={`shrink-0 rounded-full px-2 py-0.5 text-[10px] font-semibold ${KIND_BADGE[k]}`}
              >
                {k}
              </span>
              <CornerDownLeft className="size-3.5 shrink-0 text-zinc-300 opacity-0 group-data-[selected=true]:opacity-100 dark:text-zinc-600" />
            </Command.Item>
            );
          })}
        </Command.List>
        <div className="flex items-center justify-between border-t border-zinc-200 px-4 py-2 text-[11px] text-zinc-400 dark:border-zinc-700 dark:text-zinc-500">
          <span>{filtered.length} results</span>
          <span className="flex items-center gap-3">
            <span>↑↓ navigate</span>
            <span>↵ open</span>
          </span>
        </div>
      </Command>
    </div>
  );
}
