"use client";

import { useMemo, useState } from "react";
import { ChevronRight, FunctionSquare, Variable, BookOpen, ArrowRight } from "lucide-react";
import type { RefPageData } from "@/lib/docs/loader";
import { docsUrlToHash } from "@/lib/docs/router";

function MemberRow({ m, parentName }: { m: RefPageData["functions"][number]; parentName: string }) {
  const href = m.hasPage ? `#/reference/${parentName}/${m.name}` : null;
  const isField = m.section === "fields";
  const Wrapper = href ? "a" : "div";
  return (
    <Wrapper
      {...(href ? { href } : {})}
      className={`group block border-b border-zinc-100 px-4 py-3.5 last:border-0 dark:border-zinc-800/70 ${
        href ? "transition-colors hover:bg-zinc-50 dark:hover:bg-zinc-800/40" : ""
      }`}
      {...(href
        ? {
            onClick: (e: React.MouseEvent) => {
              e.preventDefault();
              window.location.hash = href;
              window.scrollTo({ top: 0 });
            },
          }
        : {})}
    >
      <code className="block break-words font-mono text-[13px] leading-6 text-zinc-800 dark:text-zinc-200">
        {m.signature || `${parentName}.${m.name}`}
      </code>
      {m.description && (
        <p className="mt-1 line-clamp-2 text-[13px] leading-6 text-zinc-500 dark:text-zinc-400">
          {m.description}
        </p>
      )}
    </Wrapper>
  );
}

export function RefPage({ data }: { data: RefPageData }) {
  const [filter, setFilter] = useState("");
  const [tab, setTab] = useState<"functions" | "fields">(
    data.functions.length > 0 ? "functions" : "fields",
  );

  const filtered = useMemo(() => {
    const q = filter.trim().toLowerCase();
    const src = tab === "functions" ? data.functions : data.fields;
    if (!q) return src;
    return src.filter(
      (m) => m.name.toLowerCase().includes(q) || m.signature.toLowerCase().includes(q),
    );
  }, [filter, tab, data]);

  const docsHash = data.docsLink ? docsUrlToHash(data.docsLink.href) : null;

  return (
    <div className="mx-auto max-w-[820px] px-5 pb-24 pt-8 sm:px-8">
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
        <span className="font-mono text-zinc-600 dark:text-zinc-300">{data.name}</span>
      </nav>

      {/* Header */}
      <header className="mt-5 border-b border-zinc-200 pb-7 dark:border-zinc-800">
        <div className="flex flex-wrap items-center gap-2">
          <span
            className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-[11px] font-semibold uppercase tracking-wide ${
              data.kind === "global"
                ? "bg-amber-100 text-amber-800 dark:bg-amber-500/15 dark:text-amber-300"
                : "bg-violet-100 text-violet-800 dark:bg-violet-500/15 dark:text-violet-300"
            }`}
          >
            {data.kind === "global" ? (
              <Variable className="size-3" />
            ) : (
              <FunctionSquare className="size-3" />
            )}
            {data.kind}
          </span>
          {data.assocType && data.assocType.toLowerCase() !== data.name.toLowerCase() && (
            <span className="text-[13px] text-zinc-400 dark:text-zinc-500">
              type{" "}
              <a href={`#/reference/${data.assocType}`} className="font-mono text-violet-700 hover:underline dark:text-violet-300">
                {data.assocType}
              </a>
            </span>
          )}
          {data.topic && (
            <span className="rounded-full bg-zinc-100 px-2.5 py-0.5 text-[11px] font-medium text-zinc-500 dark:bg-zinc-800 dark:text-zinc-400">
              {data.topic}
            </span>
          )}
        </div>
        <h1 className="mt-3 font-mono text-[32px] font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
          {data.name}
        </h1>
        {data.lead && (
          <p className="mt-3 max-w-2xl text-[15px] leading-7 text-zinc-500 dark:text-zinc-400">{data.lead}</p>
        )}
        {data.typedef && (
          <pre className="mt-4 overflow-x-auto rounded-xl border border-zinc-200 bg-zinc-50 p-4 font-mono text-[12.5px] leading-6 text-zinc-700 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-300">
            {data.typedef}
          </pre>
        )}
        {docsHash && (
          <a
            href={docsHash}
            onClick={(e) => {
              e.preventDefault();
              window.location.hash = docsHash;
              window.scrollTo({ top: 0 });
            }}
            className="mt-4 inline-flex items-center gap-1.5 text-sm font-medium text-amber-700 hover:text-amber-800 dark:text-amber-400 dark:hover:text-amber-300"
          >
            <BookOpen className="size-4" />
            Read the guide: {data.docsLink?.title}
            <ArrowRight className="size-3.5" />
          </a>
        )}
      </header>

      {/* Filter + tabs */}
      <div className="sticky top-[57px] z-10 -mx-1 mt-6 flex flex-wrap items-center gap-2 bg-white/95 px-1 py-2 backdrop-blur dark:bg-zinc-950/95">
        {data.functions.length > 0 && data.fields.length > 0 ? (
          <div className="flex rounded-lg border border-zinc-200 p-0.5 dark:border-zinc-700">
            <button
              onClick={() => setTab("functions")}
              className={`rounded-md px-3 py-1 text-[13px] font-medium transition-colors ${
                tab === "functions"
                  ? "bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900"
                  : "text-zinc-500 hover:text-zinc-800 dark:text-zinc-400 dark:hover:text-zinc-200"
              }`}
            >
              Functions {data.functions.length}
            </button>
            <button
              onClick={() => setTab("fields")}
              className={`rounded-md px-3 py-1 text-[13px] font-medium transition-colors ${
                tab === "fields"
                  ? "bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900"
                  : "text-zinc-500 hover:text-zinc-800 dark:text-zinc-400 dark:hover:text-zinc-200"
              }`}
            >
              Fields {data.fields.length}
            </button>
          </div>
        ) : (
          <span className="text-[13px] font-semibold text-zinc-500 dark:text-zinc-400">
            {tab === "functions" ? `Functions ${data.functions.length}` : `Fields ${data.fields.length}`}
          </span>
        )}
        <input
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder={`Filter ${tab}…`}
          className="ml-auto w-44 rounded-lg border border-zinc-200 bg-white px-3 py-1.5 text-[13px] text-zinc-800 outline-none transition-colors placeholder:text-zinc-400 focus:border-amber-400 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-200 dark:focus:border-amber-500"
        />
      </div>

      {/* Member list */}
      {(tab === "functions" ? data.functions : data.fields).length === 0 ? (
        <div className="mt-6 rounded-2xl border border-dashed border-zinc-300 p-10 text-center text-sm text-zinc-400 dark:border-zinc-700 dark:text-zinc-500">
          {filter
            ? `No ${tab} match “${filter}”.`
            : tab === "fields"
              ? "This global has no fields."
              : "This page documents the type itself — see its typedef above and the docs for how to use it."}
        </div>
      ) : (
        <div className="mt-3 overflow-hidden rounded-2xl border border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900">
          {filtered.map((m) => (
            <MemberRow key={m.name + m.section} m={m} parentName={data.name} />
          ))}
          {filtered.length === 0 && (
            <div className="px-4 py-10 text-center text-sm text-zinc-400 dark:text-zinc-500">
              No {tab} match “{filter}”.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
