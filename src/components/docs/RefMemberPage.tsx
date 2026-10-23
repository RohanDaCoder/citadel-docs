"use client";

import { ChevronRight, CornerUpLeft, Quote } from "lucide-react";
import type { RefMemberPageData } from "@/lib/docs/loader";
import { docsUrlToHash } from "@/lib/docs/router";

/** Colorize a type string: highlight known type names as links later. */
function TypeCode({ src }: { src: string }) {
  return <span className="font-mono text-[12.5px] leading-6">{src}</span>;
}

export function RefMemberPage({ data }: { data: RefMemberPageData }) {
  const parentHash = `#/reference/${data.parent}`;
  const hasParams = data.params.length > 0;
  const hasReturns = data.returns.length > 0;
  const hasUsedIn = data.usedIn.length > 0;

  return (
    <div className="mx-auto max-w-[760px] px-5 pb-24 pt-8 sm:px-8">
      {/* Breadcrumbs */}
      <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-[13px] text-zinc-400 dark:text-zinc-500">
        <a href="#/" className="transition-colors hover:text-zinc-700 dark:hover:text-zinc-300">
          Citadel
        </a>
        <ChevronRight className="size-3" />
        <a href="#/reference" className="transition-colors hover:text-zinc-700 dark:hover:text-zinc-300">
          Reference
        </a>
        <ChevronRight className="size-3" />
        <a href={parentHash} className="font-mono transition-colors hover:text-zinc-700 dark:hover:text-zinc-300">
          {data.parent}
        </a>
        <ChevronRight className="size-3" />
        <span className="font-mono text-zinc-600 dark:text-zinc-300">{data.name}</span>
      </nav>

      {/* Header */}
      <header className="mt-5 border-b border-zinc-200 pb-7 dark:border-zinc-800">
        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-full bg-rose-100 px-2.5 py-0.5 text-[11px] font-semibold uppercase tracking-wide text-rose-800 dark:bg-rose-500/15 dark:text-rose-300">
            {data.kind || "member"}
          </span>
          <span className="text-[13px] text-zinc-400 dark:text-zinc-500">
            of{" "}
            <a href={parentHash} className="font-mono font-medium text-zinc-700 hover:underline dark:text-zinc-300">
              {data.parent}
            </a>
          </span>
        </div>
        <h1 className="mt-3 font-mono text-[30px] font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
          {data.title || `${data.parent}.${data.name}`}
        </h1>
        {data.lead && (
          <p className="mt-3 max-w-2xl text-[15px] leading-7 text-zinc-500 dark:text-zinc-400">{data.lead}</p>
        )}
        {data.signature && (
          <pre className="mt-5 overflow-x-auto rounded-xl border border-amber-200/60 bg-amber-50 p-4 font-mono text-[13.5px] leading-7 text-zinc-800 dark:border-amber-500/25 dark:bg-amber-950/30 dark:text-zinc-200">
            {data.signature}
          </pre>
        )}
      </header>

      {/* Parameters */}
      {hasParams && (
        <section className="mt-8">
          <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Parameters</h2>
          <div className="mt-3 overflow-hidden rounded-2xl border border-zinc-200 dark:border-zinc-800">
            {data.params.map((p, i) => (
              <div
                key={i}
                className="grid gap-x-6 gap-y-1 border-b border-zinc-100 px-4 py-3 last:border-0 sm:grid-cols-[minmax(0,10rem)_minmax(0,1fr)_auto] dark:border-zinc-800/70"
              >
                <code className="font-mono text-[13px] font-semibold text-zinc-900 dark:text-zinc-100">
                  {p.name}
                </code>
                <div className="text-zinc-500 dark:text-zinc-400">
                  <TypeCode src={p.type} />
                </div>
                <span
                  className={`justify-self-start rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide sm:justify-self-end ${
                    p.required
                      ? "bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300"
                      : "bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-300"
                  }`}
                >
                  {p.required ? "required" : "optional"}
                </span>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Returns */}
      {hasReturns && (
        <section className="mt-8">
          <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Returns</h2>
          <div className="mt-3 space-y-2">
            {data.returns.map((r, i) => (
              <code
                key={i}
                className="block rounded-xl border border-zinc-200 bg-zinc-50 px-4 py-2.5 font-mono text-[13px] text-zinc-700 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-300"
              >
                {r}
              </code>
            ))}
          </div>
        </section>
      )}

      {/* Used in */}
      {hasUsedIn && (
        <section className="mt-8">
          <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Used in</h2>
          <div className="mt-3 space-y-2">
            {data.usedIn.map((u, i) => {
              const hash = docsUrlToHash(u.href);
              return (
                <a
                  key={i}
                  href={hash ?? "#/"}
                  onClick={(e) => {
                    e.preventDefault();
                    if (hash) {
                      window.location.hash = hash;
                      window.scrollTo({ top: 0 });
                    }
                  }}
                  className="group flex items-start gap-3 rounded-xl border border-zinc-200 bg-white px-4 py-3 transition-colors hover:border-amber-300 hover:bg-amber-50/40 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-amber-500/40 dark:hover:bg-amber-950/20"
                >
                  <Quote className="mt-0.5 size-3.5 shrink-0 text-zinc-300 dark:text-zinc-600" />
                  <div className="min-w-0 flex-1">
                    {u.quote && (
                      <code className="block break-words font-mono text-[12.5px] leading-6 text-zinc-600 dark:text-zinc-300">
                        {u.quote}
                      </code>
                    )}
                    <span className="mt-0.5 block text-[11px] font-medium uppercase tracking-wide text-zinc-400 group-hover:text-amber-600 dark:text-zinc-500">
                      {u.source}
                    </span>
                  </div>
                </a>
              );
            })}
          </div>
        </section>
      )}

      {/* Back to parent */}
      <div className="mt-12 border-t border-zinc-200 pt-6 dark:border-zinc-800">
        <a
          href={parentHash}
          onClick={(e) => {
            e.preventDefault();
            window.location.hash = parentHash;
            window.scrollTo({ top: 0 });
          }}
          className="inline-flex items-center gap-1.5 text-sm font-medium text-amber-700 hover:text-amber-800 dark:text-amber-400 dark:hover:text-amber-300"
        >
          <CornerUpLeft className="size-4" />
          All members of <span className="font-mono">{data.parent}</span>
        </a>
      </div>
    </div>
  );
}
