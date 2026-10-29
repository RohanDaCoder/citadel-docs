"use client";

import { ArrowRight, BookOpen, Layers, Boxes, Users, Palette, Server, Wrench, ChefHat, GraduationCap, BookMarked, Search } from "lucide-react";
import { nav } from "./Sidebar";

const SECTION_ICONS: Record<string, React.ReactNode> = {
  "getting-started": <GraduationCap className="size-4" />,
  concepts: <Layers className="size-4" />,
  world: <Boxes className="size-4" />,
  entities: <Users className="size-4" />,
  players: <Users className="size-4" />,
  ui: <Palette className="size-4" />,
  systems: <Server className="size-4" />,
  guides: <BookOpen className="size-4" />,
  cookbook: <ChefHat className="size-4" />,
  appendix: <BookMarked className="size-4" />,
};

const SECTION_BLURBS: Record<string, string> = {
  "getting-started": "What Citadel is, a first pack in five minutes, tooling and the Luau primer.",
  concepts: "The machine model — architecture, manifests, the runtime, events, conventions, rooms and dimensions.",
  world: "Terrain generation, block names and states, builds and schematics, custom blocks, registries, world state.",
  entities: "Custom entities with think loops, entity handles, mob spawning, NPCs.",
  players: "Lifecycle, movement and cameras, inventory, visibility, health, permissions.",
  ui: "Titles and chat, screens, canvases, menus, dialogs, displays and models, particles, sound.",
  systems: "Commands, storage, shared stores, network, HTTP, the Gem shop, the hub, server settings, limits.",
  guides: "Five complete walkthroughs, from a first lobby to a dungeon dimension.",
  cookbook: "Small, complete patterns — cooldowns, leaderboards, teleport pads, kits, teams, minigame loops, save/load.",
  appendix: "The event catalog, client feature matrix, limits table, FAQ.",
};

const TYPE_COUNT = nav.reference.types.length;

export function HomePage({ onSearch }: { onSearch: () => void }) {
  return (
    <div className="mx-auto max-w-[1080px] px-5 pb-24 pt-10 sm:px-8">
      {/* Hero */}
      <div className="relative overflow-hidden rounded-2xl border border-zinc-200 bg-gradient-to-b from-amber-50/80 to-transparent px-6 py-10 sm:px-10 sm:py-14 dark:border-zinc-800 dark:from-amber-950/20">
        <div className="max-w-3xl">
          <div className="mb-4 flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-amber-100 px-3 py-1 text-[11px] font-semibold uppercase tracking-wider text-amber-800 dark:bg-amber-500/15 dark:text-amber-300">
              Developer wiki
            </span>
            <span className="rounded-full border border-zinc-200 px-3 py-1 text-[11px] font-medium text-zinc-500 dark:border-zinc-700 dark:text-zinc-400">
              Engine v0.1.0 · Java clients 1.8–26.x
            </span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight text-zinc-900 sm:text-5xl dark:text-zinc-50">
            Minefort Citadel
          </h1>
          <p className="mt-4 max-w-2xl text-lg leading-8 text-zinc-600 dark:text-zinc-400">
            The complete reference for scripting Minecraft servers in Luau —
            rewritten from the official docs as a structured wiki for
            developers. One pack runs on every Java client from 1.8 to 26.x,
            as the whole game or as a plugin over survival.
          </p>
          <div className="mt-8 flex flex-wrap items-center gap-3">
            <a
              href="#/wiki/what-is-citadel"
              onClick={(e) => {
                e.preventDefault();
                window.location.hash = "#/wiki/what-is-citadel";
                window.scrollTo({ top: 0 });
              }}
              className="inline-flex items-center gap-2 rounded-lg bg-amber-500 px-5 py-2.5 text-sm font-semibold text-white shadow-sm shadow-amber-500/30 transition-colors hover:bg-amber-600"
            >
              What is Citadel?
              <ArrowRight className="size-4" />
            </a>
            <a
              href="#/wiki/quick-start"
              onClick={(e) => {
                e.preventDefault();
                window.location.hash = "#/wiki/quick-start";
                window.scrollTo({ top: 0 });
              }}
              className="inline-flex items-center gap-2 rounded-lg border border-zinc-300 bg-white px-5 py-2.5 text-sm font-semibold text-zinc-700 transition-colors hover:border-amber-300 hover:text-amber-700 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-300 dark:hover:border-amber-500/50 dark:hover:text-amber-300"
            >
              Quick start
            </a>
            <button
              onClick={onSearch}
              className="inline-flex items-center gap-2 rounded-lg px-3 py-2.5 text-sm font-medium text-zinc-500 transition-colors hover:text-zinc-800 dark:text-zinc-400 dark:hover:text-zinc-200"
            >
              <Search className="size-4" />
              Search everything
              <kbd className="rounded border border-zinc-200 bg-white px-1.5 py-0.5 font-mono text-[10px] dark:border-zinc-700 dark:bg-zinc-800">
                ⌘K
              </kbd>
            </button>
          </div>
        </div>
      </div>

      {/* Stat strip */}
      <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
        {[
          { n: `${nav.sections.reduce((a, s) => a + s.pages.length, 0)}`, l: "wiki articles" },
          { n: "29", l: "API globals" },
          { n: `${TYPE_COUNT}`, l: "types documented" },
          { n: "674", l: "API members" },
        ].map((s) => (
          <div
            key={s.l}
            className="rounded-xl border border-zinc-200 bg-zinc-50/60 px-4 py-3.5 text-center dark:border-zinc-800 dark:bg-zinc-900/40"
          >
            <div className="font-mono text-xl font-bold text-amber-600 dark:text-amber-400">{s.n}</div>
            <div className="mt-0.5 text-[12px] font-medium text-zinc-500 dark:text-zinc-400">{s.l}</div>
          </div>
        ))}
      </div>

      {/* Sections */}
      <div className="mt-12">
        <h2 className="text-sm font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">
          The wiki
        </h2>
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {nav.sections.map((section) => (
            <a
              key={section.id}
              href={`#/wiki/${section.pages[0]?.slug ?? ""}`}
              onClick={(e) => {
                e.preventDefault();
                window.location.hash = `#/wiki/${section.pages[0]?.slug ?? ""}`;
                window.scrollTo({ top: 0 });
              }}
              className="group rounded-xl border border-zinc-200 p-5 transition-all hover:border-amber-300 hover:shadow-sm dark:border-zinc-800 dark:hover:border-amber-500/40"
            >
              <div className="flex items-center gap-2.5">
                <span className="flex size-8 items-center justify-center rounded-lg bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300">
                  {SECTION_ICONS[section.id] ?? <Layers className="size-4" />}
                </span>
                <span className="font-semibold text-zinc-900 dark:text-zinc-100">{section.title}</span>
                <span className="ml-auto font-mono text-[11px] text-zinc-400 dark:text-zinc-500">
                  {section.pages.length}
                </span>
              </div>
              <p className="mt-2.5 text-[13.5px] leading-6 text-zinc-500 dark:text-zinc-400">
                {SECTION_BLURBS[section.id] ?? ""}
              </p>
              <div className="mt-3 flex items-center gap-1 text-[12.5px] font-medium text-amber-700 opacity-0 transition-opacity group-hover:opacity-100 dark:text-amber-400">
                Open section
                <ArrowRight className="size-3" />
              </div>
            </a>
          ))}
        </div>
      </div>

      {/* API reference banner */}
      <a
        href="#/ref"
        onClick={(e) => {
          e.preventDefault();
          window.location.hash = "#/ref";
          window.scrollTo({ top: 0 });
        }}
        className="group mt-6 flex items-center gap-4 rounded-2xl border border-zinc-200 bg-gradient-to-r from-zinc-50 to-transparent p-6 transition-colors hover:border-amber-300 dark:border-zinc-800 dark:from-zinc-900/60 dark:hover:border-amber-500/40"
      >
        <span className="flex size-11 shrink-0 items-center justify-center rounded-xl bg-zinc-900 text-amber-400 dark:bg-amber-500/15 dark:text-amber-300">
          <Wrench className="size-5" />
        </span>
        <div className="min-w-0">
          <div className="font-semibold text-zinc-900 dark:text-zinc-100">API reference</div>
          <p className="mt-0.5 text-[13.5px] leading-6 text-zinc-500 dark:text-zinc-400">
            Every global, type and member — signatures, parameters, returns and
            usage examples, cross-linked from every article.
          </p>
        </div>
        <ArrowRight className="ml-auto size-5 shrink-0 text-zinc-300 transition-transform group-hover:translate-x-0.5 group-hover:text-amber-500 dark:text-zinc-600" />
      </a>

      {/* Popular paths */}
      <div className="mt-12">
        <h2 className="text-sm font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">
          Common paths
        </h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          {[
            {
              title: "I'm new here",
              pages: [
                ["What is Citadel?", "what-is-citadel"],
                ["Quick start", "quick-start"],
                ["Luau primer", "luau-primer"],
              ],
            },
            {
              title: "I'm building a game",
              pages: [
                ["Terrain generation", "terrain-generation"],
                ["A minigame loop", "cookbook-minigame-loop"],
                ["Guide: Coin rush", "guide-coin-rush"],
              ],
            },
            {
              title: "I need the exact API",
              pages: [
                ["Event catalog", "event-catalog"],
                ["API reference", "@ref"],
                ["Limits", "limits-table"],
              ],
            },
          ].map((path) => (
            <div
              key={path.title}
              className="rounded-xl border border-zinc-200 p-4 dark:border-zinc-800"
            >
              <div className="text-[13px] font-semibold text-zinc-800 dark:text-zinc-200">{path.title}</div>
              <div className="mt-2.5 space-y-1.5">
                {path.pages.map(([label, slug]) => (
                  <a
                    key={slug}
                    href={slug === "@ref" ? "#/ref" : `#/wiki/${slug}`}
                    onClick={(e) => {
                      e.preventDefault();
                      window.location.hash = slug === "@ref" ? "#/ref" : `#/wiki/${slug}`;
                      window.scrollTo({ top: 0 });
                    }}
                    className="block text-[13px] text-zinc-500 transition-colors hover:text-amber-700 dark:text-zinc-400 dark:hover:text-amber-300"
                  >
                    {label}
                  </a>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
