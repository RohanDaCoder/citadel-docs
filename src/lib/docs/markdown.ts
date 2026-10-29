/** Minimal markdown parser for the Citadel docs content subset. */

export type Inline =
  | { t: "text"; v: string }
  | { t: "code"; v: string }
  | { t: "bold"; v: Inline[] }
  | { t: "italic"; v: Inline[] }
  | { t: "link"; v: Inline[]; href: string };

export type Block =
  | { t: "heading"; level: number; id: string; text: string; inlines: Inline[] }
  | { t: "paragraph"; inlines: Inline[] }
  | { t: "code"; lang: string; code: string }
  | { t: "list"; ordered: boolean; items: { inlines: Inline[]; children: Block[] }[] }
  | { t: "table"; header: Inline[][]; rows: Inline[][][] }
  | { t: "quote"; lines: string; inlines: Inline[]; callout: string | null };

function slugify(text: string): string {
  const s = text
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/[\s_]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return s || "section";
}

/** Parse inline markdown (code, bold, italic, links). */
export function parseInline(src: string): Inline[] {
  const out: Inline[] = [];
  let buf = "";
  let i = 0;
  const pushText = () => {
    if (buf) out.push({ t: "text", v: buf });
    buf = "";
  };
  while (i < src.length) {
    const ch = src[i];
    if (ch === "`") {
      const end = src.indexOf("`", i + 1);
      if (end > i) {
        pushText();
        out.push({ t: "code", v: src.slice(i + 1, end) });
        i = end + 1;
        continue;
      }
    }
    if (ch === "*" && src[i + 1] === "*") {
      const end = src.indexOf("**", i + 2);
      if (end > i + 1) {
        pushText();
        out.push({ t: "bold", v: parseInline(src.slice(i + 2, end)) });
        i = end + 2;
        continue;
      }
    }
    if (ch === "*" && src[i + 1] !== "*" && src[i + 1] !== " ") {
      const end = src.indexOf("*", i + 1);
      if (end > i + 1) {
        pushText();
        out.push({ t: "italic", v: parseInline(src.slice(i + 1, end)) });
        i = end + 1;
        continue;
      }
    }
    if (ch === "[") {
      const closeBracket = findCloseBracket(src, i);
      if (closeBracket > 0 && src[closeBracket + 1] === "(") {
        const closeParen = src.indexOf(")", closeBracket + 2);
        if (closeParen > closeBracket + 2) {
          pushText();
          const label = src.slice(i + 1, closeBracket);
          const href = src.slice(closeBracket + 2, closeParen);
          out.push({ t: "link", v: parseInline(label), href });
          i = closeParen + 1;
          continue;
        }
      }
    }
    buf += ch;
    i += 1;
  }
  pushText();
  return out;
}

function findCloseBracket(src: string, start: number): number {
  let depth = 0;
  for (let i = start; i < src.length; i++) {
    if (src[i] === "\\") continue;
    if (src[i] === "[") depth++;
    else if (src[i] === "]") {
      depth--;
      if (depth === 0) return i;
    }
  }
  return -1;
}

/** Parse a markdown document into blocks, assigning heading ids. */
export function parseMarkdown(src: string): Block[] {
  const lines = src.split("\n");
  const blocks: Block[] = [];
  const usedIds = new Map<string, number>();
  let i = 0;

  const nextId = (text: string) => {
    const base = slugify(text);
    const n = usedIds.get(base) ?? 0;
    usedIds.set(base, n + 1);
    return n === 0 ? base : `${base}-${n}`;
  };

  while (i < lines.length) {
    const line = lines[i];

    // blank
    if (!line.trim()) {
      i++;
      continue;
    }

    // fenced code
    if (line.startsWith("```")) {
      const lang = line.slice(3).trim();
      const codeLines: string[] = [];
      i++;
      while (i < lines.length && !lines[i].startsWith("```")) {
        codeLines.push(lines[i]);
        i++;
      }
      i++; // closing fence
      blocks.push({ t: "code", lang, code: codeLines.join("\n") });
      continue;
    }

    // heading
    const h = /^(#{1,6})\s+(.*)$/.exec(line);
    if (h) {
      const level = h[1].length;
      const text = h[2].trim();
      const label = text.replace(/[*`]/g, "");
      blocks.push({
        t: "heading",
        level,
        id: nextId(label),
        text: label,
        inlines: parseInline(text),
      });
      i++;
      continue;
    }

    // table
    if (line.trim().startsWith("|")) {
      const tableLines: string[] = [];
      while (i < lines.length && lines[i].trim().startsWith("|")) {
        tableLines.push(lines[i]);
        i++;
      }
      const rows = tableLines
        .filter((l) => !/^\s*\|[\s:|-]+\|\s*$/.test(l))
        .map((l) =>
          l
            .trim()
            .replace(/^\||\|$/g, "")
            .split("|")
            .map((c) => parseInline(c.trim())),
        );
      if (rows.length > 0) {
        blocks.push({ t: "table", header: rows[0], rows: rows.slice(1) });
      }
      continue;
    }

    // list
    const isUl = /^\s*-\s+/.test(line);
    const isOl = /^\s*\d+\.\s+/.test(line);
    if (isUl || isOl) {
      const ordered = isOl;
      const items: { inlines: Inline[]; children: Block[] }[] = [];
      while (i < lines.length) {
        const l = lines[i];
        const m = /^(\s*)(?:-|\d+\.)\s+(.*)$/.exec(l);
        if (!m) {
          // continuation line belonging to previous item
          if (items.length > 0 && l.trim() && /^\s{2,}\S/.test(l)) {
            const prev = items[items.length - 1];
            prev.inlines = prev.inlines.concat(parseInline(" " + l.trim()));
            i++;
            continue;
          }
          break;
        }
        const indent = m[1].length;
        if (indent >= 2 && items.length > 0) {
          // nested under previous item — collect its raw block
          const nestedLines: string[] = [];
          while (i < lines.length) {
            const nm = /^(\s*)(?:-|\d+\.)\s+/.exec(lines[i]);
            if (nm && nm[1].length >= 2) {
              nestedLines.push(lines[i].replace(/^\s{2}/, ""));
              i++;
            } else if (lines[i].trim() && nestedLines.length > 0 && !/^\s*(?:-|\d+\.)\s+/.test(lines[i])) {
              nestedLines.push(lines[i].replace(/^\s{2}/, ""));
              i++;
            } else {
              break;
            }
          }
          const prev = items[items.length - 1];
          prev.children = parseMarkdown(nestedLines.join("\n")).filter(
            (b) => b.t === "list",
          ) as { t: "list"; ordered: boolean; items: { inlines: Inline[]; children: Block[] }[] }[];
          continue;
        }
        items.push({ inlines: parseInline(m[2].trim()), children: [] });
        i++;
      }
      blocks.push({ t: "list", ordered, items });
      continue;
    }

    // blockquote
    if (line.startsWith(">")) {
      const quoteLines: string[] = [];
      while (i < lines.length && lines[i].startsWith(">")) {
        quoteLines.push(lines[i].replace(/^>\s?/, ""));
        i++;
      }
      const joined = quoteLines.join(" ").trim();
      const cm = /^\*\*(In short|Note|Gotcha|Tip|Warning|Caution):?\*\*\s*/.exec(joined);
      let callout: string | null = null;
      let body = joined;
      if (cm) {
        callout = cm[1] === "Caution" ? "Warning" : cm[1];
        body = joined.slice(cm[0].length);
      }
      blocks.push({ t: "quote", lines: joined, inlines: parseInline(body), callout });
      continue;
    }

    // paragraph: accumulate until blank line or new block marker
    const paraLines: string[] = [];
    while (
      i < lines.length &&
      lines[i].trim() &&
      !lines[i].startsWith("```") &&
      !lines[i].startsWith("#") &&
      !lines[i].startsWith(">") &&
      !lines[i].trim().startsWith("|") &&
      !/^\s*-\s+/.test(lines[i]) &&
      !/^\s*\d+\.\s+/.test(lines[i])
    ) {
      paraLines.push(lines[i]);
      i++;
    }
    if (paraLines.length) {
      blocks.push({ t: "paragraph", inlines: parseInline(paraLines.join(" ").trim()) });
    } else {
      i++; // safety
    }
  }

  return blocks;
}
