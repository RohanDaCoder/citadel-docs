"use client";

import { useState, useEffect } from "react";
import { ChevronRight, BookOpen, Layers, BookMarked, Hash } from "lucide-react";
import navJson from "@/data/nav.json";
import type { Route } from "@/lib/docs/router";

interface NavData {
  guides: { slug: string; title: string; description: string }[];
  docs: { topic: string; description: string; pages: { slug: string; title: string }[] }[];
  reference: {
    globalsByTopic: { topic: string; globals: { name: string; count: number | null }[] }[];
    types: { letter: string; names: string[] }[];
  };
}

export const nav = navJson as unknown as NavData;

function NavLink({
  href,
  active,
  onClick,
  children,
  className = "",
}: {
  href: string;
  active: boolean;
  onClick?: () => void;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <a
      href={href}
      onClick={(e) => {
        e.preventDefault();
        window.location.hash = href;
        window.scrollTo({ top: 0 });
        onClick?.();
      }}
      className={`block truncate rounded-md px-2.5 py-[5px] text-[13.5px] leading-snug transition-colors ${
        active
          ? "bg-amber-100 font-medium text-amber-900 dark:bg-amber-500/15 dark:text-amber-300"
          : "text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-800/70 dark:hover:text-zinc-100"
      } ${className}`}
    >
      {children}
    </a>
  );
}

function Section({
  title,
  icon,
  defaultOpen,
  active,
  children,
}: {
  title: string;
  icon?: React.ReactNode;
  defaultOpen: boolean;
  active: boolean;
  children: React.ReactNode;
}) {
  const [manual, setManual] = useState<boolean | null>(null);
  const open = manual ?? (defaultOpen || active);
  return (
    <div className="mt-1">
      <button
        onClick={() => setManual(!open)}
        className="flex w-full items-center gap-1.5 rounded-md px-2 py-1.5 text-[11px] font-semibold uppercase tracking-wider text-zinc-400 transition-colors hover:text-zinc-600 dark:text-zinc-500 dark:hover:text-zinc-300"
        aria-expanded={open}
      >
        <ChevronRight
          className={`size-3 shrink-0 transition-transform ${open ? "rotate-90" : ""}`}
        />
        {icon}
        <span className="truncate">{title}</span>
      </button>
      {open && <div className="mt-0.5 space-y-px pl-[3px]">{children}</div>}
    </div>
  );
}

export function Sidebar({
  route,
  onNavigate,
}: {
  route: Route;
  onNavigate?: () => void;
}) {
  const current =
    route.kind === "guide"
      ? `#/guides/${route.slug}`
      : route.kind === "doc"
        ? `#/docs/${route.slug}`
        : route.kind === "ref"
          ? `#/reference/${route.name}`
          : route.kind === "refmember"
            ? `#/reference/${route.name}/${route.member}`
            : route.kind === "reference"
              ? "#/reference"
              : "#/";

  return (
    <nav className="space-y-3 pb-16" aria-label="Documentation">
      <Section title="Home" icon={<Hash className="size-3" />} defaultOpen={false} active={current === "#/"}>
        <NavLink href="#/" active={current === "#/"} onClick={onNavigate}>
          Overview
        </NavLink>
      </Section>

      <Section
        title="Guide · 5 games"
        icon={<BookOpen className="size-3" />}
        defaultOpen={route.kind === "guide"}
        active={route.kind === "guide"}
      >
        {nav.guides.map((g, i) => (
          <NavLink
            key={g.slug}
            href={`#/guides/${g.slug}`}
            active={current === `#/guides/${g.slug}`}
            onClick={onNavigate}
          >
            {i + 1}. {g.title}
          </NavLink>
        ))}
      </Section>

      <Section
        title="Docs · 9 topics"
        icon={<Layers className="size-3" />}
        defaultOpen={route.kind === "doc"}
        active={route.kind === "doc"}
      >
        {nav.docs.map((topic) => (
          <details
            key={topic.topic}
            open={topic.pages.some((p) => current === `#/docs/${p.slug}`)}
            className="group"
          >
            <summary className="flex cursor-pointer select-none items-center gap-1.5 rounded-md px-2.5 py-[5px] text-[13.5px] font-medium text-zinc-700 transition-colors hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800/70 [&::-webkit-details-marker]:hidden">
              <ChevronRight className="size-3 shrink-0 text-zinc-400 transition-transform group-open:rotate-90" />
              <span className="truncate">{topic.topic}</span>
              <span className="ml-auto text-[11px] text-zinc-400 dark:text-zinc-500">
                {topic.pages.length}
              </span>
            </summary>
            <div className="mt-0.5 space-y-px border-l border-zinc-200 pl-2 dark:border-zinc-800">
              {topic.pages.map((p) => (
                <NavLink
                  key={p.slug}
                  href={`#/docs/${p.slug}`}
                  active={current === `#/docs/${p.slug}`}
                  onClick={onNavigate}
                >
                  {p.title}
                </NavLink>
              ))}
            </div>
          </details>
        ))}
      </Section>

      <Section
        title="Reference"
        icon={<BookMarked className="size-3" />}
        defaultOpen={route.kind === "reference" || route.kind === "ref" || route.kind === "refmember"}
        active={route.kind === "reference" || route.kind === "ref" || route.kind === "refmember"}
      >
        <NavLink href="#/reference" active={current === "#/reference"} onClick={onNavigate}>
          Overview
        </NavLink>
        <div className="mt-1 border-l border-zinc-200 pl-2 dark:border-zinc-800">
          <div className="px-2.5 py-1 text-[11px] font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">
            Globals
          </div>
          {nav.reference.globalsByTopic.map((group) => (
            <details
              key={group.topic}
              open={group.globals.some(
                (g) => current === `#/reference/${g.name}` || current.startsWith(`#/reference/${g.name}/`),
              )}
              className="group"
            >
              <summary className="flex cursor-pointer select-none items-center gap-1.5 rounded-md px-2.5 py-[5px] text-[13px] font-medium text-zinc-700 transition-colors hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800/70 [&::-webkit-details-marker]:hidden">
                <ChevronRight className="size-3 shrink-0 text-zinc-400 transition-transform group-open:rotate-90" />
                <span className="truncate">{group.topic}</span>
              </summary>
              <div className="mt-0.5 space-y-px pl-1">
                {group.globals.map((g) => (
                  <NavLink
                    key={g.name}
                    href={`#/reference/${g.name}`}
                    active={
                      current === `#/reference/${g.name}` || current.startsWith(`#/reference/${g.name}/`)
                    }
                    onClick={onNavigate}
                    className="font-mono !text-[13px]"
                  >
                    {g.name}
                    {g.count != null && (
                      <span className="ml-1.5 font-sans text-[11px] text-zinc-400 dark:text-zinc-500">
                        {g.count}
                      </span>
                    )}
                  </NavLink>
                ))}
              </div>
            </details>
          ))}
          <details
            open={
              current !== "#/reference" &&
              nav.reference.types.some((t) =>
                t.names.some(
                  (n) =>
                    current === `#/reference/${n}` || current.startsWith(`#/reference/${n}/`),
                ),
              )
            }
            className="group"
          >
            <summary className="flex cursor-pointer select-none items-center gap-1.5 rounded-md px-2.5 py-[5px] text-[13px] font-medium text-zinc-700 transition-colors hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800/70 [&::-webkit-details-marker]:hidden">
              <ChevronRight className="size-3 shrink-0 text-zinc-400 transition-transform group-open:rotate-90" />
              <span>Types A–Z</span>
              <span className="ml-auto text-[11px] text-zinc-400 dark:text-zinc-500">
                {nav.reference.types.reduce((a, t) => a + t.names.length, 0)}
              </span>
            </summary>
            <div className="mt-0.5 max-h-96 space-y-px overflow-y-auto pl-1">
              {nav.reference.types.map((t) => (
                <div key={t.letter}>
                  <div className="px-2.5 pb-0.5 pt-2 font-mono text-[10px] font-bold text-zinc-400 dark:text-zinc-600">
                    {t.letter}
                  </div>
                  {t.names.map((n) => (
                    <NavLink
                      key={n}
                      href={`#/reference/${n}`}
                      active={current === `#/reference/${n}` || current.startsWith(`#/reference/${n}/`)}
                      onClick={onNavigate}
                      className="font-mono !text-[13px]"
                    >
                      {n}
                    </NavLink>
                  ))}
                </div>
              ))}
            </div>
          </details>
        </div>
      </Section>
    </nav>
  );
}
