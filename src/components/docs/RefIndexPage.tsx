"use client";

import { ChevronRight, Search } from "lucide-react";
import { nav } from "./Sidebar";

export function RefIndexPage({ onSearch }: { onSearch: () => void }) {
  const globalCount = nav.reference.globalsByTopic.reduce((a, g) => a + g.globals.length, 0);
  const typeCount = nav.reference.types.reduce((a, t) => a + t.names.length, 0);

  return (
    <div className="mx-auto max-w-4xl px-5 pb-24 pt-8 sm:px-8">
      <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-[13px] text-zinc-400 dark:text-zinc-500">
        <a href="#/" className="transition-colors hover:text-zinc-700 dark:hover:text-zinc-300">
          Citadel
        </a>
        <ChevronRight className="size-3" />
        <span className="text-zinc-600 dark:text-zinc-300">Reference</span>
      </nav>

      <header className="mt-5 border-b border-zinc-200 pb-7 dark:border-zinc-800">
        <h1 className="text-[34px] font-bold tracking-tight text-zinc-900 dark:text-zinc-50">Reference</h1>
        <p className="mt-3 max-w-2xl text-[15px] leading-7 text-zinc-500 dark:text-zinc-400">
          Every global is a slot; the number is how many calls it holds. Types are what calls hand you and take
          back. Together: <strong className="font-semibold text-zinc-700 dark:text-zinc-200">{globalCount} globals</strong>,{" "}
          <strong className="font-semibold text-zinc-700 dark:text-zinc-200">{typeCount} types</strong>, 674
          documented calls.
        </p>
        <button
          onClick={onSearch}
          className="mt-5 inline-flex items-center gap-2.5 rounded-xl border border-zinc-200 bg-white px-4 py-2 text-sm text-zinc-500 shadow-sm transition-all hover:border-zinc-300 hover:text-zinc-800 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-400 dark:hover:border-zinc-600 dark:hover:text-zinc-200"
        >
          <Search className="size-4" />
          Search the reference…
          <kbd className="rounded border border-zinc-200 bg-zinc-50 px-1.5 py-0.5 font-mono text-[10px] dark:border-zinc-700 dark:bg-zinc-800">
            ⌘K
          </kbd>
        </button>
      </header>

      {/* Globals by topic */}
      <section className="mt-9">
        <h2 className="text-xl font-semibold text-zinc-900 dark:text-zinc-50">Globals by topic</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          {nav.reference.globalsByTopic.map((group) => (
            <div
              key={group.topic}
              className="rounded-2xl border border-zinc-200 bg-white p-5 dark:border-zinc-800 dark:bg-zinc-900"
            >
              <div className="flex items-baseline justify-between">
                <h3 className="text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
                  {group.topic}
                </h3>
                <span className="font-mono text-[11px] text-zinc-300 dark:text-zinc-600">
                  {group.globals.length}
                </span>
              </div>
              <div className="mt-3 space-y-1">
                {group.globals.map((g) => (
                  <a
                    key={g.name}
                    href={`#/reference/${g.name}`}
                    className="group flex items-center gap-2.5 rounded-lg px-2.5 py-1.5 transition-colors hover:bg-zinc-50 dark:hover:bg-zinc-800/60"
                  >
                    <code className="font-mono text-[13px] font-medium text-amber-800 group-hover:text-amber-600 dark:text-amber-300 dark:group-hover:text-amber-200">
                      {g.name}
                    </code>
                    {g.count != null && (
                      <span className="ml-auto rounded-full bg-zinc-100 px-2 py-0.5 font-mono text-[10px] text-zinc-400 dark:bg-zinc-800 dark:text-zinc-500">
                        {g.count}
                      </span>
                    )}
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
          {nav.reference.types.map((t) => (
            <div key={t.letter} className="flex gap-4 border-b border-zinc-100 py-2.5 last:border-0 dark:border-zinc-800/60">
              <div className="w-4 shrink-0 pt-0.5 font-mono text-[12px] font-bold text-zinc-300 dark:text-zinc-600">
                {t.letter}
              </div>
              <div className="flex flex-wrap gap-1.5">
                {t.names.map((n) => (
                  <a
                    key={n}
                    href={`#/reference/${n}`}
                    className="rounded-md bg-zinc-50 px-2 py-1 font-mono text-[12px] text-zinc-600 transition-colors hover:bg-amber-100 hover:text-amber-800 dark:bg-zinc-800/70 dark:text-zinc-300 dark:hover:bg-amber-500/20 dark:hover:text-amber-300"
                  >
                    {n}
                  </a>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
