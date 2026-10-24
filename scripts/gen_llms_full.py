#!/usr/bin/env python3
"""Generate llms.txt + llms-full.txt from the Starlight content tree.

llms.txt        lean agent index: what Citadel is, then every wiki page and
                API page with its site route and a one-line description.
llms-full.txt   everything in one file: every page inline as a `## <title>`
                section, opened by an HTML anchor and a route comment; all
                internal links rewritten to in-file anchors.

Both are written to public/ (served at the site root by the built site) and
copied to download/ for direct access.

Run AFTER scripts/gen_starlight.py:
    python3 scripts/gen_llms_full.py
"""
import datetime
import json
import os
import re
import shutil
from collections import OrderedDict

ROOT = "/home/z/my-project"
DOCS = f"{ROOT}/src/content/docs"
PUB = f"{ROOT}/public"
DL = f"{ROOT}/download"
MANIFEST = json.load(open(f"{ROOT}/scripts/generated/starlight-manifest.json"))

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
LINK_RE = re.compile(r"\]\((/[^)#\s]*)(#[^)\s]*)?\)")
SELF_LINK_RE = re.compile(r"\]\((#[^)\s]+)\)")
ADO_RE = re.compile(r"^:::(note|tip|caution|danger)(?:\[([^\]]+)\])?\s*$")
ADO_LABEL = {"note": "Note", "tip": "Tip", "caution": "Caution", "danger": "Warning"}
HEAD_RE = re.compile(r"^(#{1,6})\s+(.*)$")
SLUGGER_STRIP = re.compile(r"[^\w\s-]", re.U)

TODAY = datetime.date.today().isoformat()


def gh_slug(text):
    """github-slugger-compatible slug — same recipe gen_starlight.py validates with."""
    t = re.sub(r"[`*]", "", text).strip().lower()
    t = SLUGGER_STRIP.sub("", t)
    return re.sub(r"[\s_]", "-", t).strip("-")


def unquote(v):
    v = (v or "").strip()
    if len(v) >= 2 and v[0] == "'" and v[-1] == "'":
        v = v[1:-1].replace("''", "'")
    return v


def parse_page(path):
    raw = open(path).read()
    m = FM_RE.match(raw)
    if not m:
        raise SystemExit(f"no frontmatter: {path}")
    fm = {"title": "", "description": ""}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = unquote(v)
    body = raw[m.end():].lstrip("\n")
    return fm, body


def route_for(rel):
    """src/content/docs relative path -> site route."""
    parts = rel.split("/")
    if parts[-1] == "index.md":
        stem = "/".join(parts[:-1])
        return "/" + (stem + "/" if stem else "")
    return "/" + "/".join(parts[:-1]) + "/" + parts[-1][:-3] + "/"


def route_id(route):
    return "index" if route == "/" else route.strip("/").replace("/", "-")


# ---------------------------------------------------------------- collect
pages = OrderedDict()
for root, _, files in os.walk(DOCS):
    for fn in sorted(files):
        if fn.endswith(".md"):
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, DOCS)
            route = route_for(rel)
            if route in pages:
                raise SystemExit(f"route collision: {route}")
            fm, body = parse_page(path)
            pages[route] = {"title": fm["title"] or rel, "desc": fm["description"],
                            "body": body, "rel": rel}


def is_ref_parent(route):
    return route.startswith("/ref/") and route.count("/") == 3


def ref_members(route):
    return sorted(p for p in pages if p.startswith(route) and p != route)


# --------------------------------------------------------------- ordering
def walk_items(items, out):
    for it in items:
        if "link" in it:
            out.append(it["link"])
        if "items" in it:
            walk_items(it["items"], out)


sidebar_routes = []
walk_items(MANIFEST["sidebar"], sidebar_routes)

ordered = ["/"]
for r in sidebar_routes:
    ordered.append(r)
    if is_ref_parent(r):
        ordered.extend(ref_members(r))

missing = [r for r in ordered if r not in pages]
if missing:
    raise SystemExit(f"sidebar routes missing from content: {missing}")
leftover = sorted(p for p in pages if p not in set(ordered))
for p in leftover:
    ordered.append(p)                      # safety net; should be none

# ------------------------------------------- pass A: referenced anchors
referenced = set()                         # (route, anchor) pairs used in links
unresolved_routes = set()
for route, page in pages.items():
    in_code = False
    for line in page["body"].split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in LINK_RE.finditer(line):
            r, a = m.group(1), m.group(2)
            if r not in pages:
                unresolved_routes.add(f"{route} -> {r}")
            if a:
                referenced.add((r, a[1:]))
        for m in SELF_LINK_RE.finditer(line):
            referenced.add((route, m.group(1)[1:]))


def heading_slug_list(body):
    """Ordered github-slugger-style slugs (with -1/-2 dedup) outside code fences."""
    out, seen = [], {}
    in_code = False
    for line in body.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = HEAD_RE.match(line)
        if m:
            s = gh_slug(m.group(2))
            if not s:
                continue
            n = seen.get(s, 0)
            seen[s] = n + 1
            out.append(s if n == 0 else f"{s}-{n}")
    return out


heading_ids = {}                           # (route, anchor) -> in-file anchor id
for route, page in pages.items():
    slugs = set(heading_slug_list(page["body"]))
    pid = route_id(route)
    for r, a in referenced:
        if r == route and a in slugs:
            heading_ids[(r, a)] = f"{pid}--{a}"

anchor_fallbacks = []
unmapped_anchors = sorted(a for a in referenced if a not in heading_ids)


# ------------------------------------------------- pass B: line conversion
def rewrite_line(line, route):
    def ssub(m):
        key = (route, m.group(1)[1:])
        if key in heading_ids:
            return f"](#{heading_ids[key]})"
        return m.group(0)

    def lsub(m):
        r, a = m.group(1), m.group(2)
        if r not in pages:
            return m.group(0)
        pid = route_id(r)
        if a:
            key = (r, a[1:])
            if key in heading_ids:
                return f"](#{heading_ids[key]})"
            anchor_fallbacks.append(f"{route} -> {r}{a}")
            return f"](#{pid})"
        return f"](#{pid})"

    line = SELF_LINK_RE.sub(ssub, line)
    return LINK_RE.sub(lsub, line)


def convert_page(route, page):
    """Admonitions -> labelled blockquotes; internal links -> in-file anchors.
    Heading-level anchors are emitted before headings that other pages link to."""
    pid = route_id(route)
    wanted = {a for (r, a) in referenced if r == route}   # anchors to emit here
    out = []
    in_code = False
    in_ado = False
    seen = {}                                # heading slug dedup (github-slugger)
    for line in page["body"].split("\n"):
        if not in_ado and line.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        m = ADO_RE.match(line)
        if m:
            if in_ado:
                raise SystemExit(f"nested admonition at {page['rel']}: {line}")
            label = m.group(2) or ADO_LABEL[m.group(1)]
            out.append(f"> **{label}:**")
            in_ado = True
            continue
        if in_ado:
            if line.strip() == ":::":
                in_ado = False
                out.append("")
                continue
            out.append(("> " + rewrite_line(line, route)) if line.strip() else ">")
            continue
        hm = HEAD_RE.match(line)
        if hm:
            s = gh_slug(hm.group(2))
            if s:
                n = seen.get(s, 0)
                seen[s] = n + 1
                s = s if n == 0 else f"{s}-{n}"
                if s in wanted:
                    out.append(f'<a id="{pid}--{s}"></a>')
                    out.append("")
        out.append(rewrite_line(line, route))
    return "\n".join(out).strip("\n")


# ----------------------------------------------------------------- counts
wiki_count = len([r for r in ordered if not r.startswith("/ref/")])
parent_count = len([r for r in ordered if is_ref_parent(r)])
member_count = len([r for r in ordered
                    if r.startswith("/ref/") and r.count("/") == 4])

INTRO = f"""> Minefort Citadel is Minefort's Luau scripting engine for Minecraft
> servers: a *pack* — a folder of `.luau` files — runs server-side on a
> vanilla server and drives the whole game through globals such as `world`,
> `players`, `ui`, `game`, `commands`, `stores`, `network`, `http` and `hub`.
> Unmodified Java clients from 1.8 to 26.x join and play. This file is the
> complete, restructured developer reference: {wiki_count} wiki documents
> (concepts, guides, cookbook, appendices) plus the full API reference —
> {parent_count} global and type pages, {member_count} documented members.
>
> Generated {TODAY} from the Citadel Developer Wiki (an Astro Starlight
> project). Regenerate with
> `python3 scripts/gen_starlight.py && python3 scripts/gen_llms_full.py`.

How to use this file:

- Every document is one `## <title>` section, opened by an HTML anchor
  (`<a id="...">`) and a `<!-- /route/ -->` comment with the page's path on
  the live site.
- Internal links resolve inside this file: `#ref-world-spawn` is the
  `world.spawn` section. The same string without the `#` —
  `/ref/World/spawn/` — is the live-site route.
- All code is Luau (Lua with types); `--` starts a comment. Tables are
  GitHub-flavoured markdown.
- A lean index of the same documentation set lives in `llms.txt`.
"""

# ------------------------------------------------------------- llms-full.txt
def toc():
    out = [f"- [Citadel Developer Wiki (home)](#index)"]
    for group in MANIFEST["sidebar"]:
        out += ["", f"**{group['label']}**", ""]
        for it in group["items"]:
            if "link" in it:
                route = it["link"]
                page = pages.get(route)
                title = page["title"] if page else it["label"]
                out.append(f"- [{title}](#{route_id(route)})")
                if is_ref_parent(route):
                    members = ref_members(route)
                    if members:
                        names = ", ".join(pages[p]["title"] for p in members)
                        out.append(f"  - Members: {names}")
            else:
                out += ["", f"*{it['label']}*", ""]
                for sub in it["items"]:
                    route = sub["link"]
                    page = pages.get(route)
                    title = page["title"] if page else sub["label"]
                    out.append(f"- [{title}](#{route_id(route)})")
                    if is_ref_parent(route):
                        members = ref_members(route)
                        if members:
                            names = ", ".join(pages[p]["title"] for p in members)
                            out.append(f"  - Members: {names}")
    return "\n".join(out)


chunks = []
for route in ordered:
    page = pages[route]
    pid = route_id(route)
    body = convert_page(route, page)
    chunks.append(
        f"<!-- {route} -->\n\n<a id=\"{pid}\"></a>\n\n## {page['title']}\n\n{body}"
    )

full = (
    "# Citadel — Minefort Citadel developer documentation (llms-full.txt)\n\n"
    + INTRO
    + "\n## Document index\n\n"
    + toc()
    + "\n\n---\n\n"
    + "\n\n---\n\n".join(chunks)
    + "\n"
)

# every in-file link target must have a matching emitted anchor
# (one exception: a quoted `](#sound)` fragment inside a Used-in citation)
emitted_ids = set(re.findall(r'<a id="([^"]+)"', full))
link_targets = set(re.findall(r"\]\(#([^)\s]+)\)", full))
dangling = sorted(t for t in link_targets - emitted_ids if t != "sound")

# ----------------------------------------------------------------- llms.txt
def clip(text, n=120):
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= n:
        return text
    return text[:n].rsplit(" ", 1)[0] + "…"


index_out = [
    "# Citadel — Minefort Citadel developer documentation",
    "",
    "> Minefort's Luau scripting engine for Minecraft servers, restructured",
    "> as a developer wiki: core concepts, task-focused guides, cookbook",
    f"> recipes and appendices ({wiki_count} pages), plus the complete API",
    f"> reference — {parent_count} globals and types, {member_count} documented",
    "> members, each with signature, parameters, returns and usage. Routes",
    "> are site-relative: prefix them with the deployment origin. Every API",
    "> member also has its own page at `/ref/<Parent>/<member>/`.",
    ">",
    "> The same content in one file: [llms-full.txt](/llms-full.txt).",
    "",
]

for group in MANIFEST["sidebar"]:
    index_out.append(f"## {group['label']}")
    index_out.append("")
    for it in group["items"]:
        if "link" in it:
            route = it["link"]
            page = pages.get(route)
            title = page["title"] if page else it["label"]
            desc = clip(page["desc"]) if page else ""
            entry = f"- [{title}]({route})"
            if desc:
                entry += f": {desc}"
            index_out.append(entry)
        else:
            index_out += ["", f"### {it['label']}", ""]
            for sub in it["items"]:
                route = sub["link"]
                page = pages.get(route)
                title = page["title"] if page else sub["label"]
                desc = clip(page["desc"], 100) if page else ""
                entry = f"- [{title}]({route})"
                if desc:
                    entry += f": {desc}"
                index_out.append(entry)
    index_out.append("")

index_txt = "\n".join(index_out).rstrip() + "\n"

# ------------------------------------------------------------------- write
os.makedirs(DL, exist_ok=True)
for name, content in (("llms.txt", index_txt), ("llms-full.txt", full)):
    with open(f"{PUB}/{name}", "w") as f:
        f.write(content)
    shutil.copy(f"{PUB}/{name}", f"{DL}/{name}")

# ------------------------------------------------------------------- report
n_anchors = full.count('<a id="')
n_head_anchors = sum(1 for i in emitted_ids if "--" in i)
n_links = len(re.findall(r"\]\(#", full))
leftover_links = len(re.findall(r"\]\(/", full))
print(f"documents emitted:   {len(ordered)} (wiki {wiki_count}, "
      f"ref parents {parent_count}, members {member_count})")
print(f"sections + anchors:  {n_anchors} ({n_head_anchors} heading-level)")
print(f"in-file links:       {n_links}")
print(f"dangling link targets: {len(dangling)} (expect 0)")
for d in dangling[:10]:
    print("  dangling", d)
print(f"unconverted /links:  {leftover_links} (expect 0)")
print(f"admonitions -> blockquotes: {full.count('> **In short:**') + full.count('> **Note:**') + full.count('> **Tip:**') + full.count('> **Gotcha:**') + full.count('> **Caution:**') + full.count('> **Warning:**')}")
print(f"anchor fallbacks:    {len(anchor_fallbacks)} (page-level jump kept)")
for f_ in anchor_fallbacks[:10]:
    print("  fallback", f_)
print(f"unmapped anchors:    {len(unmapped_anchors)}")
for a in unmapped_anchors[:10]:
    print("  unmapped", a)
if unresolved_routes:
    print(f"UNRESOLVED ROUTES:   {len(unresolved_routes)}")
    for u in sorted(unresolved_routes)[:10]:
        print("  ", u)
print(f"llms-full.txt:       {os.path.getsize(f'{PUB}/llms-full.txt') / 1e6:.2f} MB, "
      f"{full.count(chr(10)) + 1} lines")
print(f"llms.txt:            {os.path.getsize(f'{PUB}/llms.txt') / 1e3:.1f} KB")
if leftover_links or unresolved_routes or dangling:
    raise SystemExit("LINK CONVERSION INCOMPLETE — fix before shipping")
