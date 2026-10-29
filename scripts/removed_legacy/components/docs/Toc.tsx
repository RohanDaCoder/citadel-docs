"use client";

import { useEffect, useState } from "react";
import { List } from "lucide-react";
import type { TocEntry } from "@/lib/docs/loader";
import { scrollToAnchor } from "@/lib/docs/router";

export function Toc({ toc }: { toc: TocEntry[] }) {
  const [active, setActive] = useState<string>("");

  useEffect(() => {
    if (toc.length === 0) return;
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setActive(entry.target.id);
          }
        }
      },
      { rootMargin: "-80px 0px -70% 0px" },
    );
    for (const t of toc) {
      const el = document.getElementById(t.id);
      if (el) observer.observe(el);
    }
    return () => observer.disconnect();
  }, [toc]);

  if (toc.length === 0) return null;

  return (
    <div className="sticky top-[72px] hidden max-h-[calc(100vh-100px)] w-56 shrink-0 overflow-y-auto py-8 pr-2 xl:block">
      <div className="mb-3 flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">
        <List className="size-3" />
        On this page
      </div>
      <nav className="space-y-1 border-l border-zinc-200 dark:border-zinc-800">
        {toc.map((t) => (
          <a
            key={t.id}
            href={`#${t.id}`}
            onClick={(e) => {
              e.preventDefault();
              scrollToAnchor(t.id);
            }}
            className={`-ml-px block border-l-2 py-1 text-[13px] leading-snug transition-colors ${
              t.level === 3 ? "pl-6" : "pl-3.5"
            } ${
              active === t.id
                ? "border-amber-500 font-medium text-amber-700 dark:border-amber-400 dark:text-amber-300"
                : "border-transparent text-zinc-500 hover:border-zinc-300 hover:text-zinc-800 dark:text-zinc-400 dark:hover:text-zinc-200"
            }`}
          >
            {t.text}
          </a>
        ))}
      </nav>
    </div>
  );
}
