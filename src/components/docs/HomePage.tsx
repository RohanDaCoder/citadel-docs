"use client";

import { ChevronRight, BookOpen, Layers, BookMarked, Search, ArrowRight } from "lucide-react";
import { nav } from "./Sidebar";

export function HomePage({ onSearch }: { onSearch: () => void }) {
  return (
    <div className="mx-auto max-w-4xl px-5 pb-24 pt-10 sm:px-8">
      {/* Hero */}
      <div className="relative overflow-hidden rounded-3xl border border-zinc-200 bg-gradient-to-br from-amber-50 via-white to-white p-8 sm:p-12 dark:border-zinc-800 dark:from-zinc-900 dark:via-zinc-950 dark:to-zinc-950">
        <div className="absolute -right-16 -top-16 select-none font-mono text-[200px] font-black leading-none text-amber-100 dark:text-zinc-800/60">
          C
        </div>
        <div className="relative">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-amber-200 bg-amber-50 px-3 py-1 text-xs font-medium text-amber-800 dark:border-amber-500/30 dark:bg-amber-500/10 dark:text-amber-300">
            <span className="inline-block size-1.5 rounded-full bg-amber-500" />
            Citadel v0.1.0 · Community docs rebuild
          </div>
          <h1 className="text-4xl font-bold tracking-tight text-zinc-900 sm:text-5xl dark:text-zinc-50">
            Build a Minecraft game{" "}
            <span className="bg-gradient-to-r from-amber-600 to-amber-400 bg-clip-text text-transparent dark:from-amber-400 dark:to-amber-300">
              in Luau.
            </span>
          </h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-zinc-600 dark:text-zinc-300">
            Citadel is a platform for building Minecraft games in Luau. Learn it in the{" "}
            <strong className="font-semibold text-zinc-800 dark:text-zinc-100">guide</strong>, read how each part
            works in the <strong className="font-semibold text-zinc-800 dark:text-zinc-100">docs</strong>, and check
            the exact call in the <strong className="font-semibold text-zinc-800 dark:text-zinc-100">reference</strong>.
          </p>
          <button
            onClick={onSearch}
            className="mt-7 inline-flex items-center gap-2.5 rounded-xl border border-zinc-200 bg-white px-4 py-2.5 text-sm text-zinc-500 shadow-sm transition-all hover:border-zinc-300 hover:text-zinc-800 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-400 dark:hover:border-zinc-600 dark:hover:text-zinc-200"
          >
            <Search className="size-4" />
            Search everything…
            <kbd className="rounded border border-zinc-200 bg-zinc-50 px-1.5 py-0.5 font-mono text-[10px] dark:border-zinc-700 dark:bg-zinc-800">
              ⌘K
            </kbd>
          </button>
        </div>
      </div>

      {/* Three pillars */}
      <div className="mt-8 grid gap-5 md:grid-cols-3">
        <div className="group rounded-2xl border border-zinc-200 bg-white p-6 transition-all hover:-translate-y-0.5 hover:border-emerald-300 hover:shadow-lg dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-emerald-500/40">
          <div className="flex items-center gap-2.5">
            <div className="flex size-9 items-center justify-center rounded-lg bg-emerald-100 text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-400">
              <BookOpen className="size-4.5" />
            </div>
            <div className="font-semibold text-zinc-900 dark:text-zinc-50">Guide</div>
            <a
              href="#/guides/your-first-pack"
              className="ml-auto text-xs font-medium text-zinc-400 transition-colors hover:text-emerald-700 dark:text-zinc-500 dark:hover:text-emerald-400"
            >
              5 games →
            </a>
          </div>
          <p className="mt-3 text-sm leading-6 text-zinc-500 dark:text-zinc-400">
            Learn by building: each guide makes a whole game that runs.
          </p>
          <div className="mt-4 space-y-1.5">
            {nav.guides.map((g, i) => (
              <div key={g.slug} className="flex items-baseline gap-2 text-[13px]">
                <span className="font-mono text-[11px] text-zinc-300 dark:text-zinc-600">{i + 1}</span>
                <a
                  href={`#/guides/${g.slug}`}
                  className="truncate text-zinc-600 transition-colors hover:text-emerald-700 dark:text-zinc-400 dark:hover:text-emerald-400"
                >
                  {g.title}
                </a>
              </div>
            ))}
          </div>
        </div>

        <div className="group rounded-2xl border border-zinc-200 bg-white p-6 transition-all hover:-translate-y-0.5 hover:border-sky-300 hover:shadow-lg dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-sky-500/40">
          <div className="flex items-center gap-2.5">
            <div className="flex size-9 items-center justify-center rounded-lg bg-sky-100 text-sky-700 dark:bg-sky-500/15 dark:text-sky-400">
              <Layers className="size-4.5" />
            </div>
            <div className="font-semibold text-zinc-900 dark:text-zinc-50">Docs</div>
            <a
              href="#/docs/packs"
              className="ml-auto text-xs font-medium text-zinc-400 transition-colors hover:text-sky-700 dark:text-zinc-500 dark:hover:text-sky-400"
            >
              9 topics · 55 pages →
            </a>
          </div>
          <p className="mt-3 text-sm leading-6 text-zinc-500 dark:text-zinc-400">
            How each part of the engine works, one topic at a time.
          </p>
          <div className="mt-4 space-y-1.5">
            {nav.docs.map((t) => (
              <div key={t.topic} className="flex items-baseline justify-between gap-2 text-[13px]">
                <a
                  href={`#/docs/${t.pages[0]?.slug ?? ""}`}
                  className="truncate text-zinc-600 transition-colors hover:text-sky-700 dark:text-zinc-400 dark:hover:text-sky-400"
                >
                  {t.topic}
                </a>
                <span className="font-mono text-[11px] text-zinc-300 dark:text-zinc-600">{t.pages.length}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="group rounded-2xl border border-zinc-200 bg-white p-6 transition-all hover:-translate-y-0.5 hover:border-amber-300 hover:shadow-lg dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-amber-500/40">
          <div className="flex items-center gap-2.5">
            <div className="flex size-9 items-center justify-center rounded-lg bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-400">
              <BookMarked className="size-4.5" />
            </div>
            <div className="font-semibold text-zinc-900 dark:text-zinc-50">Reference</div>
            <a
              href="#/reference"
              className="ml-auto text-xs font-medium text-zinc-400 transition-colors hover:text-amber-700 dark:text-zinc-500 dark:hover:text-amber-400"
            >
              {nav.reference.globalsByTopic.reduce((a, g) => a + g.globals.length, 0)} globals ·{" "}
              {nav.reference.types.reduce((a, t) => a + t.names.length, 0)} types →
            </a>
          </div>
          <p className="mt-3 text-sm leading-6 text-zinc-500 dark:text-zinc-400">
            Every global and type, with its exact signature.
          </p>
          <div className="mt-4 flex flex-wrap gap-1.5">
            {nav.reference.globalsByTopic
              .flatMap((g) => g.globals.map((x) => x.name))
              .slice(0, 20)
              .map((name) => (
                <a
                  key={name}
                  href={`#/reference/${name}`}
                  className="rounded-md bg-zinc-100 px-2 py-0.5 font-mono text-[12px] text-zinc-600 transition-colors hover:bg-amber-100 hover:text-amber-800 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-amber-500/20 dark:hover:text-amber-300"
                >
                  {name}
                </a>
              ))}
          </div>
        </div>
      </div>

      {/* Stats strip */}
      <div className="mt-8 grid grid-cols-2 gap-px overflow-hidden rounded-2xl border border-zinc-200 bg-zinc-200 sm:grid-cols-4 dark:border-zinc-800 dark:bg-zinc-800">
        {[
          { n: "5", l: "step-by-step games" },
          { n: "55", l: "concept pages" },
          { n: "29", l: "engine globals" },
          { n: "674", l: "documented calls" },
        ].map((s) => (
          <div key={s.l} className="bg-white px-6 py-5 text-center dark:bg-zinc-900">
            <div className="font-mono text-2xl font-bold text-zinc-900 dark:text-zinc-50">{s.n}</div>
            <div className="mt-1 text-xs text-zinc-500 dark:text-zinc-400">{s.l}</div>
          </div>
        ))}
      </div>

      {/* Getting started */}
      <div className="mt-8 rounded-2xl border border-zinc-200 dark:border-zinc-800">
        <button
          onClick={() => (window.location.hash = "#/guides/your-first-pack")}
          className="group flex w-full items-center gap-4 rounded-2xl bg-white px-6 py-5 text-left transition-colors hover:bg-amber-50/50 dark:bg-zinc-900 dark:hover:bg-amber-950/20"
        >
          <div className="flex size-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-amber-400 to-amber-600 font-mono text-lg font-bold text-white shadow-md shadow-amber-500/25">
            1
          </div>
          <div className="min-w-0 flex-1">
            <div className="font-semibold text-zinc-900 dark:text-zinc-50">Start with “Your first pack”</div>
            <div className="mt-0.5 truncate text-sm text-zinc-500 dark:text-zinc-400">
              Create the pack&apos;s two files, give players solid ground, welcome them when they join, and add a
              /spawn command.
            </div>
          </div>
          <ArrowRight className="size-5 shrink-0 text-zinc-300 transition-transform group-hover:translate-x-1 group-hover:text-amber-500 dark:text-zinc-600" />
        </button>
      </div>

      <p className="mt-10 text-center text-xs leading-5 text-zinc-400 dark:text-zinc-600">
        Unofficial community reorganization of the official Minefort Citadel documentation.
        <br />
        Content © Minefort — source: minefort.com/docs/citadel
      </p>
    </div>
  );
}
