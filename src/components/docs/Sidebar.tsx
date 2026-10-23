"use client";

import { useState } from "react";
import { ChevronRight, BookOpen, Layers, BookMarked, Hash } from "lucide-react";
import navJson from "@/data/nav.json";
import type { Route } from "@/lib/docs/router";

interface NavData {
  sections: { id: string; title: string; pages: { slug: string; title: string; description: string }[] }[];
  reference: {
    domains: { id: string; title: string; globals: string[] }[];
    types: string[];
  };
}

export const nav = navJson as unknown as NavData;

export const SECTION_TITLES: Record<string, string> = Object.fromEntries(
  nav.sections.map((s) => [s.id, s.title]),
);

export const PAGE_SECTION: Record<string, string> = Object.fromEntries(
  nav.sections.flatMap((s) => s.pages.map((p) => [p.slug, s.id])),
);

function NavLink({
  href,
  active,
  onClick,
  children,
  className = "",
  title,
}: {
  href: string;
  active: boolean;
  onClick?: () => void;
  children: React.ReactNode;
  className?: string;
  title?: string;
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
    route.kind === "wiki"
      ? `#/wiki/${route.slug}`
      : route.kind === "ref"
        ? `#/ref/${route.name}`
        : route.kind === "refmember"
          ? `#/ref/${route.name}/${route.member}`
          : route.kind === "reference"
            ? "#/ref"
            : "#/";

  const activeSection =
    route.kind === "wiki" ? PAGE_SECTION[route.slug] : undefined;

  return (
    <nav className="space-y-3 pb-16" aria-label="Documentation">
      <Section title="Start" icon={<Hash className="size-3" />} defaultOpen={false} active={current === "#/"}>
        <NavLink href="#/" active={current === "#/"} onClick={onNavigate}>
          Overview
        </NavLink>
      </Section>

      {nav.sections.map((section, si) => (
        <Section
          key={section.id}
          title={section.title}
          icon={
            section.id === "guides" ? (
              <BookOpen className="size-3" />
            ) : section.id === "cookbook" || section.id === "appendix" ? (
              <BookMarked className="size-3" />
            ) : (
              <Layers className="size-3" />
            )
          }
          defaultOpen={activeSection === section.id || (si === 0 && !activeSection)}
          active={activeSection === section.id}
        >
          {section.pages.map((p) => (
            <NavLink
              key={p.slug}
              href={`#/wiki/${p.slug}`}
              active={current === `#/wiki/${p.slug}`}
              onClick={onNavigate}
              title={p.description}
            >
              {p.title}
            </NavLink>
          ))}
        </Section>
      ))}

      <Section
        title="API reference"
        icon={<BookMarked className="size-3" />}
        defaultOpen={route.kind === "reference" || route.kind === "ref" || route.kind === "refmember"}
        active={route.kind === "reference" || route.kind === "ref" || route.kind === "refmember"}
      >
        <NavLink href="#/ref" active={current === "#/ref"} onClick={onNavigate}>
          Overview
        </NavLink>
        <div className="mt-1 border-l border-zinc-200 pl-2 dark:border-zinc-800">
          {nav.reference.domains.map((group) => (
            <details
              key={group.id}
              open={group.globals.some(
                (g) =>
                  current === `#/ref/${g}` || current.startsWith(`#/ref/${g}/`),
              )}
              className="group"
            >
              <summary className="flex cursor-pointer select-none items-center gap-1.5 rounded-md px-2.5 py-[5px] text-[13px] font-medium text-zinc-700 transition-colors hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800/70 [&::-webkit-details-marker]:hidden">
                <ChevronRight className="size-3 shrink-0 text-zinc-400 transition-transform group-open:rotate-90" />
                <span className="truncate">{group.title}</span>
                <span className="ml-auto text-[11px] text-zinc-400 dark:text-zinc-500">
                  {group.globals.length}
                </span>
              </summary>
              <div className="mt-0.5 space-y-px pl-1">
                {group.globals.map((g) => (
                  <NavLink
                    key={g}
                    href={`#/ref/${g}`}
                    active={current === `#/ref/${g}` || current.startsWith(`#/ref/${g}/`)}
                    onClick={onNavigate}
                    className="font-mono !text-[13px]"
                  >
                    {g}
                  </NavLink>
                ))}
              </div>
            </details>
          ))}
          <details
            open={
              current !== "#/ref" &&
              !nav.reference.domains.some((d) =>
                d.globals.some(
                  (g) => current === `#/ref/${g}` || current.startsWith(`#/ref/${g}/`),
                ),
              ) &&
              current.startsWith("#/ref")
            }
            className="group"
          >
            <summary className="flex cursor-pointer select-none items-center gap-1.5 rounded-md px-2.5 py-[5px] text-[13px] font-medium text-zinc-700 transition-colors hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800/70 [&::-webkit-details-marker]:hidden">
              <ChevronRight className="size-3 shrink-0 text-zinc-400 transition-transform group-open:rotate-90" />
              <span>Types A–Z</span>
              <span className="ml-auto text-[11px] text-zinc-400 dark:text-zinc-500">
                {nav.reference.types.length}
              </span>
            </summary>
            <div className="mt-0.5 max-h-96 space-y-px overflow-y-auto pl-1">
              {nav.reference.types.map((n) => (
                <NavLink
                  key={n}
                  href={`#/ref/${n}`}
                  active={current === `#/ref/${n}` || current.startsWith(`#/ref/${n}/`)}
                  onClick={onNavigate}
                  className="font-mono !text-[13px]"
                >
                  {n}
                </NavLink>
              ))}
            </div>
          </details>
        </div>
      </Section>
    </nav>
  );
}
