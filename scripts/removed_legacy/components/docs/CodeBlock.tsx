"use client";

import { useState, useMemo } from "react";
import { Check, Copy } from "lucide-react";
import { tokenizeCode } from "@/lib/docs/highlight";

const TOKEN_CLASS: Record<string, string> = {
  plain: "",
  comment: "text-zinc-500 italic",
  string: "text-emerald-700 dark:text-emerald-300",
  number: "text-orange-600 dark:text-orange-300",
  keyword: "text-rose-600 dark:text-rose-400 font-medium",
  boolean: "text-purple-600 dark:text-purple-300",
  nil: "text-purple-600 dark:text-purple-300",
  fn: "text-amber-700 dark:text-amber-300",
  api: "text-sky-700 dark:text-sky-300 font-medium",
  operator: "text-zinc-500 dark:text-zinc-400",
  property: "text-teal-700 dark:text-teal-300",
  "yaml-key": "text-amber-700 dark:text-amber-300",
  "sh-cmd": "text-sky-700 dark:text-sky-300 font-medium",
};

const LANG_LABEL: Record<string, string> = {
  luau: "Luau",
  lua: "Luau",
  yaml: "YAML",
  yml: "YAML",
  sh: "Shell",
  bash: "Shell",
  shell: "Shell",
  text: "Text",
  "": "Text",
};

export function CodeBlock({ code, lang }: { code: string; lang: string }) {
  const [copied, setCopied] = useState(false);
  const tokens = useMemo(() => tokenizeCode(code, lang), [code, lang]);

  const onCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
    } catch {
      const ta = document.createElement("textarea");
      ta.value = code;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 1600);
  };

  return (
    <div className="group/code my-5 overflow-hidden rounded-xl border border-zinc-200 bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900">
      <div className="flex items-center justify-between border-b border-zinc-200 px-4 py-1.5 dark:border-zinc-800">
        <span className="font-mono text-[11px] font-medium uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
          {LANG_LABEL[lang] ?? lang}
        </span>
        <button
          onClick={onCopy}
          aria-label="Copy code"
          className="flex items-center gap-1 rounded-md px-1.5 py-1 text-[11px] text-zinc-500 transition-colors hover:bg-zinc-200 hover:text-zinc-800 dark:text-zinc-400 dark:hover:bg-zinc-800 dark:hover:text-zinc-200"
        >
          {copied ? <Check className="size-3.5" /> : <Copy className="size-3.5" />}
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <pre className="overflow-x-auto p-4 text-[13px] leading-relaxed">
        <code className="font-mono">
          {tokens.map((tok, idx) => (
            <span key={idx} className={TOKEN_CLASS[tok.type] ?? ""}>
              {tok.v}
            </span>
          ))}
        </code>
      </pre>
    </div>
  );
}
