"use client";

import { ChevronRight } from "lucide-react";
import type { GuidePageData, DocPageData } from "@/lib/docs/loader";
import { Markdown } from "./Markdown";
import { getNeighbors, getTopicOfDoc } from "./nav-utils";
import type { Route } from "@/lib/docs/router";

export function PrevNext({ route }: { route: Route }) {
  const { prev, next } = getNeighbors(route);
  if (!prev && !next) return null;
  return (
    <div className="mt-14 grid gap-3 border-t border-zinc-200 pt-6 sm:grid-cols-2 dark:border-zinc-800">
      {prev ? (
        <a
          href={prev.href}
          onClick={(e) => {
            e.preventDefault();
            window.location.hash = prev.href;
            window.scrollTo({ top: 0 });
          }}
          className="group rounded-xl border border-zinc-200 p-4 transition-colors hover:border-amber-300 hover:bg-amber-50/40 dark:border-zinc-800 dark:hover:border-amber-500/40 dark:hover:bg-amber-950/20"
        >
          <div className="text-[11px] font-medium uppercase tracking-wider text-zinc-400">Previous</div>
          <div className="mt-1 flex items-center gap-1 text-sm font-medium text-zinc-800 dark:text-zinc-100">
            <ChevronRight className="size-3.5 rotate-180 text-zinc-400" />
            {prev.title}
          </div>
        </a>
      ) : (
        <div />
      )}
      {next ? (
        <a
          href={next.href}
          onClick={(e) => {
            e.preventDefault();
            window.location.hash = next.href;
            window.scrollTo({ top: 0 });
          }}
          className="group rounded-xl border border-zinc-200 p-4 text-right transition-colors hover:border-amber-300 hover:bg-amber-50/40 dark:border-zinc-800 dark:hover:border-amber-500/40 dark:hover:bg-amber-950/20"
        >
          <div className="text-[11px] font-medium uppercase tracking-wider text-zinc-400">Next</div>
          <div className="mt-1 flex items-center justify-end gap-1 text-sm font-medium text-zinc-800 dark:text-zinc-100">
            {next.title}
            <ChevronRight className="size-3.5 text-zinc-400" />
          </div>
        </a>
      ) : null}
    </div>
  );
}

export function ArticlePage({
  data,
  route,
}: {
  data: GuidePageData | DocPageData;
  route: Route;
}) {
  const isGuide = data.type === "guide";
  const topic = isGuide ? "Guide" : (data as DocPageData).topic || getTopicOfDoc((data as DocPageData).slug) || "Docs";
  const guideIndex = isGuide
    ? ["your-first-pack", "coin-rush", "parkour-a-room-each", "build-a-cottage", "a-dungeon-dimension"].indexOf(
        (data as GuidePageData).slug,
      ) + 1
    : null;

  return (
    <article className="mx-auto max-w-[760px] px-5 pb-24 pt-8 sm:px-8">
      {/* Breadcrumbs */}
      <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-[13px] text-zinc-400 dark:text-zinc-500">
        <a href="#/" className="transition-colors hover:text-zinc-700 dark:hover:text-zinc-300">
          Citadel
        </a>
        <ChevronRight className="size-3" />
        <a
          href={isGuide ? "#/guides/your-first-pack" : "#/docs/packs"}
          className="transition-colors hover:text-zinc-700 dark:hover:text-zinc-300"
        >
          {isGuide ? "Guide" : "Docs"}
        </a>
        {!isGuide && (
          <>
            <ChevronRight className="size-3" />
            <span className="text-zinc-600 dark:text-zinc-300">{topic}</span>
          </>
        )}
      </nav>

      {/* Title */}
      <header className="mt-5 border-b border-zinc-200 pb-7 dark:border-zinc-800">
        <div className="mb-3 flex items-center gap-2">
          <span className="rounded-full bg-zinc-100 px-2.5 py-0.5 text-[11px] font-semibold uppercase tracking-wide text-zinc-500 dark:bg-zinc-800 dark:text-zinc-400">
            {topic}
          </span>
          {guideIndex != null && guideIndex > 0 && (
            <span className="flex size-5 items-center justify-center rounded-full bg-amber-100 font-mono text-[11px] font-bold text-amber-800 dark:bg-amber-500/20 dark:text-amber-300">
              {guideIndex}
            </span>
          )}
        </div>
        <h1 className="text-[34px] font-bold leading-tight tracking-tight text-zinc-900 dark:text-zinc-50">
          {data.title}
        </h1>
        {isGuide && (
          <p className="mt-3 text-[15px] leading-7 text-zinc-500 dark:text-zinc-400">
            {(data as GuidePageData).description}
          </p>
        )}
      </header>

      {/* Content */}
      <div className="mt-2">
        <Markdown source={data.markdown} />
      </div>

      <PrevNext route={route} />
    </article>
  );
}
