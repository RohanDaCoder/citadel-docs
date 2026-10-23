"use client";

import { useMemo, useState } from "react";
import { ChevronRight, Search } from "lucide-react";
import { nav } from "./Sidebar";

export function RefIndexPage({ onSearch }: { onSearch: () => void }) {
  const globalCount = nav.reference.domains.reduce((a, g) => a + g.globals.length, 0);
  const typeCount = nav.reference.types.length;
  const [filter, setFilter] = useState("");

  const filteredTypes = useMemo(() => {
    if (!filter.trim()) return nav.reference.types;
    const q = filter.trim().toLowerCase();
    return nav.reference.types.filter((t) => t.toLowerCase().includes(q));
  }, [filter]);

  return (
    <div className="mx-auto max-w-4xl px-5 pb-24 pt-8 sm:px-8">
      <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-[13px] text-zinc-400 dark:text-zinc-500">
        <a href="#/" className="transition-colors hover:text-zinc-700 dark:hover:text-zinc-300">
          Citadel
        </a>
        <ChevronRight className="size-3" />
        <span className="text-zinc-600 dark:text-zinc-300">API reference</span>
      </nav>

      <header className="mt-5 border-b border-zinc-200 pb-7 dark:border-zinc-800">
        <h1 className="text-[34px] font-bold tracking-tight text-zinc-900 dark:text-zinc-50">API reference</h1>
        <p className="mt-3 max-w-2xl text-[15px] leading-7 text-zinc-500 dark:text-zinc-400">
          The complete Citadel API:{" "}
          <strong className="font-semibold text-zinc-700 dark:text-zinc-200">{globalCount} globals</strong>,{" "}
          <strong className="font-semibold text-zinc-700 dark:text-zinc-200">{typeCount} types</strong> and{" "}
          <strong className="font-semibold text-zinc-700 dark:text-zinc-200">674 documented members</strong>{" "}
          with signatures, parameters, returns and usage examples. Every entry
          is cross-linked from the wiki articles, and every usage example
          links back to where it appeared in the docs.
        </p>
        <div className="mt-5 flex flex-wrap gap-3">
          <button
            onClick={onSearch}
            className="inline-flex items-center gap-2.5 rounded-xl border border-zinc-200 bg-white px-4 py-2 text-sm text-zinc-500 shadow-sm transition-all hover:border-zinc-300 hover:text-zinc-800 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-400 dark:hover:border-zinc-600 dark:hover:text-zinc-200"
          >
            <Search className="size-4" />
            Search the reference…
            <kbd className="rounded border border-zinc-200 bg-zinc-50 px-1.5 py-0.5 font-mono text-[10px] dark:border-zinc-700 dark:bg-zinc-800">
              ⌘K
            </kbd>
          </button>
          <input
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Filter types…"
            className="w-44 rounded-xl border border-zinc-200 bg-white px-3.5 py-2 text-sm text-zinc-800 shadow-sm outline-none transition-colors placeholder:text-zinc-400 focus:border-amber-400 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-200 dark:focus:border-amber-500/60"
          />
        </div>
      </header>

      {/* Globals by domain */}
      <section className="mt-9">
        <h2 className="text-xl font-semibold text-zinc-900 dark:text-zinc-50">Globals by domain</h2>
        <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
          The tables a script reaches for. The first six belong to the main
          room; <code className="rounded bg-zinc-100 px-1 py-0.5 font-mono text-[12px] dark:bg-zinc-800">rooms.create{}</code>{" "}
          gives another room its own.
        </p>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          {nav.reference.domains.map((group) => (
            <div
              key={group.id}
              className="rounded-2xl border border-zinc-200 bg-white p-5 dark:border-zinc-800 dark:bg-zinc-900"
            >
              <div className="flex items-baseline justify-between">
                <h3 className="text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
                  {group.title}
                </h3>
                <span className="font-mono text-[11px] text-zinc-300 dark:text-zinc-600">
                  {group.globals.length}
                </span>
              </div>
              <div className="mt-3 space-y-1">
                {group.globals.map((g) => (
                  <a
                    key={g}
                    href={`#/ref/${g}`}
                    className="group flex items-center gap-2.5 rounded-lg px-2.5 py-1.5 transition-colors hover:bg-zinc-50 dark:hover:bg-zinc-800/60"
                  >
                    <code className="font-mono text-[13px] font-medium text-amber-800 group-hover:text-amber-600 dark:text-amber-300 dark:group-hover:text-amber-200">
                      {g}
                    </code>
                  </a>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Types A-Z */}
      <section className="mt-10">
        <h2 className="text-xl font-semibold text-zinc-900 dark:text-zinc-50">Types A–Z</h2>
        <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
          What calls hand you and take back: handles, specs, option tables, unions.
        </p>
        <div className="mt-4 rounded-2xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
          {filteredTypes.length === 0 && (
            <p className="py-6 text-center text-sm text-zinc-400">No type matches “{filter}”.</p>
          )}
          {filteredTypes.length > 0 && (
            <div className="flex flex-wrap gap-1.5">
              {filteredTypes.map((n) => (
                <a
                  key={n}
                  href={`#/ref/${n}`}
                  className="rounded-md bg-zinc-50 px-2 py-1 font-mono text-[12px] text-zinc-600 transition-colors hover:bg-amber-100 hover:text-amber-800 dark:bg-zinc-800/70 dark:text-zinc-300 dark:hover:bg-amber-500/20 dark:hover:text-amber-300"
                >
                  {n}
                </a>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
