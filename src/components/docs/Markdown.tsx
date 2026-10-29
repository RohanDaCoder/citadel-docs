"use client";

import { useMemo } from "react";
import { Link2, Info, AlertTriangle, Lightbulb, Zap, BookOpen } from "lucide-react";
import { parseMarkdown, type Block, type Inline } from "@/lib/docs/markdown";
import { CodeBlock } from "./CodeBlock";
import { linkToHash, scrollToAnchor } from "@/lib/docs/router";

function InlineRun({ nodes }: { nodes: Inline[] }) {
  return (
    <>
      {nodes.map((n, i) => {
        switch (n.t) {
          case "text":
            return <span key={i}>{n.v}</span>;
          case "code":
            return (
              <code
                key={i}
                className="rounded-[5px] border border-zinc-200 bg-zinc-100 px-1.5 py-px font-mono text-[0.85em] text-zinc-800 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-200"
              >
                {n.v}
              </code>
            );
          case "bold":
            return (
              <strong key={i} className="font-semibold text-zinc-900 dark:text-zinc-50">
                <InlineRun nodes={n.v} />
              </strong>
            );
          case "italic":
            return (
              <em key={i}>
                <InlineRun nodes={n.v} />
              </em>
            );
          case "link": {
            const hash = linkToHash(n.href);
            if (hash !== null) {
              const isAnchor = hash.startsWith("#") && !hash.startsWith("#/");
              return (
                <a
                  key={i}
                  href={hash}
                  onClick={(e) => {
                    e.preventDefault();
                    if (isAnchor) {
                      scrollToAnchor(hash.slice(1));
                    } else {
                      window.location.hash = hash;
                      window.scrollTo({ top: 0 });
                    }
                  }}
                  className="font-medium text-amber-700 underline decoration-amber-300 underline-offset-2 transition-colors hover:text-amber-800 dark:text-amber-400 dark:decoration-amber-500/50 dark:hover:text-amber-300"
                >
                  <InlineRun nodes={n.v} />
                </a>
              );
            }
            return (
              <a
                key={i}
                href={n.href}
                target="_blank"
                rel="noopener noreferrer"
                className="font-medium text-amber-700 underline decoration-amber-300 underline-offset-2 transition-colors hover:text-amber-800 dark:text-amber-400 dark:decoration-amber-500/50 dark:hover:text-amber-300"
              >
                <InlineRun nodes={n.v} />
              </a>
            );
          }
          default:
            return null;
        }
      })}
    </>
  );
}

function HeadingAnchor({ id }: { id: string }) {
  return (
    <button
      aria-label="Link to section"
      onClick={() => scrollToAnchor(id)}
      className="absolute -left-5 top-1/2 hidden -translate-y-1/2 rounded p-1 text-zinc-300 opacity-0 transition-opacity group-hover:opacity-100 hover:text-amber-600 lg:block dark:text-zinc-600 dark:hover:text-amber-400"
    >
      <Link2 className="size-3.5" />
    </button>
  );
}

function Callout({ kind, children }: { kind: string; children: React.ReactNode }) {
  const config: Record<string, { icon: React.ReactNode; label: string; cls: string }> = {
    "In short": {
      icon: <BookOpen className="size-4 shrink-0" />,
      label: "In short",
      cls: "border-amber-400/70 bg-amber-50/80 dark:border-amber-500/60 dark:bg-amber-950/25",
    },
    Note: {
      icon: <Info className="size-4 shrink-0" />,
      label: "Note",
      cls: "border-sky-300 bg-sky-50/70 dark:border-sky-700 dark:bg-sky-950/25",
    },
    Gotcha: {
      icon: <AlertTriangle className="size-4 shrink-0" />,
      label: "Gotcha",
      cls: "border-orange-300 bg-orange-50/70 dark:border-orange-700/80 dark:bg-orange-950/25",
    },
    Tip: {
      icon: <Lightbulb className="size-4 shrink-0" />,
      label: "Tip",
      cls: "border-emerald-300 bg-emerald-50/70 dark:border-emerald-700 dark:bg-emerald-950/25",
    },
    Warning: {
      icon: <Zap className="size-4 shrink-0" />,
      label: "Warning",
      cls: "border-red-300 bg-red-50/70 dark:border-red-800 dark:bg-red-950/25",
    },
  };
  const c = config[kind] ?? config.Note;
  return (
    <div className={`my-5 rounded-xl border-l-4 px-4 py-3 ${c.cls}`}>
      <div className="flex items-center gap-2 pb-1 text-[11px] font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
        {c.icon}
        {c.label}
      </div>
      <div className="text-[15px] leading-7 text-zinc-700 dark:text-zinc-300">{children}</div>
    </div>
  );
}

function renderBlock(block: Block, key: number): React.ReactNode {
  switch (block.t) {
    case "heading": {
      const level = block.level <= 1 ? 2 : block.level;
      const Tag = `h${level}` as "h2" | "h3" | "h4" | "h5" | "h6";
      const cls =
        level === 2
          ? "group relative mt-10 mb-4 scroll-mt-24 border-b border-zinc-200 pb-2 text-2xl font-semibold tracking-tight text-zinc-900 first:mt-0 dark:border-zinc-800 dark:text-zinc-50"
          : level === 3
            ? "group relative mt-8 mb-3 scroll-mt-24 text-lg font-semibold text-zinc-900 dark:text-zinc-100"
            : "group relative mt-6 mb-2 scroll-mt-24 text-base font-semibold text-zinc-800 dark:text-zinc-200";
      return (
        <Tag key={key} id={block.id} className={cls}>
          <InlineRun nodes={block.inlines} />
          <HeadingAnchor id={block.id} />
        </Tag>
      );
    }
    case "paragraph":
      return (
        <p key={key} className="my-4 text-[15px] leading-7 text-zinc-700 dark:text-zinc-300">
          <InlineRun nodes={block.inlines} />
        </p>
      );
    case "code":
      return <CodeBlock key={key} code={block.code} lang={block.lang} />;
    case "list": {
      const ListTag = block.ordered ? "ol" : "ul";
      return (
        <ListTag
          key={key}
          className={
            block.ordered
              ? "my-4 list-decimal space-y-2 pl-6 text-[15px] leading-7 text-zinc-700 dark:text-zinc-300"
              : "my-4 list-disc space-y-2 pl-6 text-[15px] leading-7 text-zinc-700 dark:text-zinc-300"
          }
        >
          {block.items.map((item, idx) => (
            <li key={idx}>
              <InlineRun nodes={item.inlines} />
              {item.children.map((child, ci) => renderBlock(child, ci))}
            </li>
          ))}
        </ListTag>
      );
    }
    case "table":
      return (
        <div key={key} className="my-5 overflow-x-auto rounded-xl border border-zinc-200 dark:border-zinc-800">
          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="border-b border-zinc-200 bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900">
                {block.header.map((cell, ci) => (
                  <th
                    key={ci}
                    className="px-4 py-2.5 text-left font-semibold text-zinc-800 dark:text-zinc-100"
                  >
                    <InlineRun nodes={cell} />
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {block.rows.map((row, ri) => (
                <tr
                  key={ri}
                  className="border-b border-zinc-100 last:border-0 odd:bg-zinc-50/50 dark:border-zinc-800/60 dark:odd:bg-zinc-900/30"
                >
                  {row.map((cell, ci) => (
                    <td key={ci} className="px-4 py-2.5 align-top text-zinc-700 dark:text-zinc-300">
                      <InlineRun nodes={cell} />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    case "quote": {
      if (block.callout) {
        return (
          <Callout key={key} kind={block.callout}>
            <InlineRun nodes={block.inlines} />
          </Callout>
        );
      }
      return (
        <blockquote
          key={key}
          className="my-5 border-l-4 border-zinc-300 pl-4 text-[15px] italic leading-7 text-zinc-600 dark:border-zinc-700 dark:text-zinc-400"
        >
          <InlineRun nodes={block.inlines} />
        </blockquote>
      );
    }
    default:
      return null;
  }
}

export function Markdown({ source }: { source: string }) {
  const blocks = useMemo(() => parseMarkdown(source), [source]);
  return <div>{blocks.map((b, i) => renderBlock(b, i))}</div>;
}
