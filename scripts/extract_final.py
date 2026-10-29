#!/usr/bin/env python3
"""extract_final.py — turn the crawled SSR HTML into scripts/dataset.json.

BeautifulSoup extraction of every page in scripts/crawl_html/ into one
structured dataset:

  guides:             { slug: {title, markdown} }
  docs:               { slug: {title, markdown} }
  reference_parents:  { Name: {title, url, lead, typedef, docs_link,
                               members[], sections[]} }
  reference_members:  { Parent: { member: {title, url, kind, lead,
                                           signature, params[], returns[],
                                           used_in[]} } }

Page classification (by URL):
  /docs/citadel                      -> skipped (landing page)
  /docs/citadel/guides/<slug>        -> guides
  /docs/citadel/<slug>               -> docs       (incl. /reference listing)
  /docs/citadel/reference/<Name>     -> reference_parents
  /docs/citadel/reference/<P>/<m>    -> reference_members
  pages without an <article>          -> skipped    (e.g. the /guides listing)

DOM notes (minefort.com is a Next.js SSR app; all of this is stable markup):
  * every page:      <article> with breadcrumb nav, <header>, h1,
                     p.t-lead, then content.
  * doc/guide pages: content in <div class="prose ..."> - h2/h3/p/pre/ul/
                     table blocks; the lead paragraph sits OUTSIDE prose and
                     is deliberately excluded from the markdown.
  * code fences:     <pre><code class="language-<lang>">...</code></pre>
  * parent pages:    <section> per Functions/Fields group; member cards are
                     <a id=...><code>signature</code><p class="t-body">desc</p>
  * member pages:    signature <pre>, then <section>s: Parameters (rows with
                     <code>name</code><code>type</code><span class="t-meta">
                     required|optional</span>), Returns (<code> per value) and
                     Used in (<li><a href><span class="min-w-0"><code>quote</code>
                     <span>source</span></span></a>).
  * the kind (function/method/field) comes from the member-page header label
    ("Function of World" / "Method of ..." / "Field of ...").

Signature cleanup (clean_sig) reproduces the raw-docs spacing:
  'string?'      -> 'string ?'    (space before ? after a word char)
  'Vec3 , block' -> 'Vec3, block' (no space before commas)

Usage:
  python3 scripts/extract_final.py                     # scripts/crawl_html -> scripts/dataset.json
  python3 scripts/extract_final.py --dir X --out Y   # verify a partial crawl
"""
import argparse
import json
import os
import re
from bs4 import BeautifulSoup, NavigableString

ROOT = "/home/z/my-project"
SKIP_P_CLASSES = ("t-lead", "t-body", "mono")   # non-content paragraphs


# ---------------------------------------------------------------- inline md
def inline_md(el) -> str:
    """Render an inline fragment to markdown, keeping source line breaks."""
    parts = []
    for node in el.children:
        if isinstance(node, NavigableString):
            parts.append(str(node))
        elif node.name == "code":
            parts.append("`" + node.get_text().strip() + "`")
        elif node.name == "strong":
            parts.append("**" + inline_md(node).strip() + "**")
        elif node.name == "em":
            parts.append("*" + inline_md(node).strip() + "*")
        elif node.name == "br":
            parts.append("\n")
        elif node.name == "a":
            parts.append(inline_md(node))       # keep the label, drop the href
        else:
            parts.append(inline_md(node))
    return "".join(parts).replace("\xa0", " ")


def heading_text(el) -> str:
    """Heading text with a single space between wrapped nodes ('Types 148')."""
    return re.sub(r" {2,}", " ", " ".join(el.stripped_strings)).strip()


def clean_sig(s: str) -> str:
    """Raw-signature spacing cleanup."""
    s = re.sub(r"([A-Za-z0-9_])\?", r"\1 ?", s)   # string?  -> string ?
    s = re.sub(r"\s+,", ",", s)                   # 'Vec3 ,' -> 'Vec3,'
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


# -------------------------------------------------- api-list blocks (prose pages)
# Some prose pages (input, version-info, mobs-and-drops, dimensions, storage,
# layouts, titles-and-bars, packs...) embed a mini reference card list:
#   div.api-list > div.api-row > code.api-sig + (dl.api-subs dt/dd) + div.api-doc
# The 2026-10-30 parity audit against the official llms-full.txt found the
# old walk silently dropped every api-list (titles-and-bars extracted to 0
# chars). They are emitted as ONE fenced block per list, mirroring the
# shape minefort's own llms-full.txt uses for the same DOM: a signature
# line per row ('sig  -- doc'), dt/dd pairs as '-- dt  dd' comment lines.
# Links keep only their labels, so nothing is invented, nothing lost.
YAML_KEY = re.compile(r"^\s*[A-Za-z_][\w-]*\s*:")


def api_list_md(al) -> str:
    def flat_text(el):
        # text nodes meet element text with original spacing; collapse all
        # whitespace runs to single spaces (multi-space alignment in the
        # DOM is styling, not content)
        return re.sub(r"\s+", " ", el.get_text()).strip()

    rows = al.find_all("div", class_="api-row", recursive=False) or [al]
    sigs, metas = [], []
    for row in rows:
        sig = row.find("code", class_="api-sig", recursive=False)
        doc = row.find("div", class_="api-doc", recursive=False)
        dl = row.find("dl", class_="api-subs", recursive=False)
        sigs.append(flat_text(sig) if sig is not None else None)
        metas.append((doc, dl))
    have = [s for s in sigs if s]
    fence = "yaml" if have and all(YAML_KEY.match(s) for s in have) else "luau"
    mark = "#" if fence == "yaml" else "--"
    out = []
    for sig, (doc, dl) in zip(sigs, metas):
        if sig:
            line = sig
            if doc is not None:
                dtxt = inline_md(doc).strip()
                if dtxt:
                    line += f"    {mark} {dtxt}"
            out.append(line)
        if dl is not None:
            for dt in dl.find_all("dt", recursive=False):
                dd = dt.find_next_sibling("dd")
                line = f"{mark}   " + flat_text(dt)
                if dd is not None:
                    line += "   " + inline_md(dd).strip()
                out.append(line)
    return f"```{fence}\n" + "\n".join(out) + "\n```"


def block_fence(el) -> list:
    """A <pre> (or a multi-line <code>) as a fenced block."""
    code = el if el.name == "code" else el.find("code")
    lang = ""
    for c in (el.get("class") or []) + \
             ((code.get("class") or []) if code is not None else []):
        if c.startswith("language-"):
            lang = c[len("language-"):]
    lang = {"lua": "luau"}.get(lang, lang)
    return [f"```{lang}", el.get_text().rstrip(), "```"]


# ------------------------------------------------------------- article -> md
def article_markdown(article) -> str:
    """Doc/guide pages: content blocks, single-newline joined.

    Content root is the div.prose wrapper when present; otherwise the article
    itself (the /reference listing has no prose div and yields just its h2).
    Classed paragraphs (t-lead, t-body card text, the mono search box) are
    never content.
    """
    root = article.find("div", class_="prose") or article
    had_prose = root is not article
    api_lists = root.find_all("div", class_="api-list")
    api_list_ids = {id(x) for x in api_lists}
    emitted_api = set()

    def enclosing_api_list(el):
        p = el
        while p is not None:
            if id(p) in api_list_ids:
                return p
            p = p.parent
        return None

    def is_skipped(el):
        if el.parent is None:                # detached (nested ul extracted)
            return True
        if el.name == "p" and any(c in (el.get("class") or [])
                                   for c in SKIP_P_CLASSES):
            return True
        for anc in el.parents:
            if anc.name in ("header", "nav", "li") or \
               (anc.get("class") and "card" in anc.get("class")):
                return True
        return False

    lines = []

    def emit(block):
        lines.append(block)

    for el in root.find_all(["h2", "h3", "p", "pre", "ul", "ol", "table",
                             "blockquote", "dl", "code"], recursive=True):
        al = enclosing_api_list(el)
        if al is not None:
            # inside an api-list: the whole list is one block, emitted at
            # the position of its first descendant the walk touches.
            if id(al) not in emitted_api:
                emit(api_list_md(al))
                emitted_api.add(id(al))
            continue
        if is_skipped(el):
            continue
        name = el.name
        if name == "h2":
            emit("## " + heading_text(el))
        elif name == "h3":
            emit("### " + heading_text(el))
        elif name == "p":
            emit(inline_md(el).strip())
        elif name == "pre":
            code = el.find("code")
            lang = ""
            if code:
                for c in code.get("class") or []:
                    if c.startswith("language-"):
                        lang = c[len("language-"):]
            # the site classes Luau code as 'language-lua'; a bare <code> (no
            # class) is a plain fence; 'text'/'sh'/'yaml' pass through
            lang = {"lua": "luau"}.get(lang, lang)
            emit(f"```{lang}\n{el.get_text().rstrip()}\n```")
        elif name == "ul":
            if el.parent is None or el.find_parent("li") or \
                    el.find_parent("header"):
                continue                     # handled inside its parent li
            for line in ul_md(el):
                emit(line)
        elif name == "ol":
            if el.find_parent("li"):
                continue
            for i, li in enumerate(el.find_all("li", recursive=False), 1):
                emit(f"{i}. " + inline_md(li).strip())
        elif name == "table":
            for line in table_md(el):
                emit(line)
        elif name == "blockquote":
            emit("> " + inline_md(el).strip())
    md = "\n".join(lines)
    if had_prose and lines:
        md += "\n"                 # prose pages keep one trailing newline
    return md


def ul_md(ul, indent=""):
    """Bullet list; nested <ul> inside an <li> is indented by two spaces.
    A <pre> or a multi-line <code> inside an <li> becomes a fenced block
    emitted right after the item — the top-level walk skips pre-in-li,
    so this is the only path that renders them (parity audit finding:
    text-formatting's animation examples were silently dropped)."""
    out = []
    for li in ul.find_all("li", recursive=False):
        nested, blocks = [], []
        for sub in li.find_all(["ul", "pre"], recursive=False):
            (nested if sub.name == "ul" else blocks).append(sub.extract())
        for code in li.find_all("code", recursive=False):
            if "\n" in code.get_text():
                blocks.append(code.extract())
        out.append(indent + "- " + inline_md(li).strip())
        for sub in nested:
            out.extend(ul_md(sub, indent + "  "))
        for b in blocks:
            out.extend(block_fence(b))
    return out


def table_md(table) -> list:
    rows = []
    for tr in table.find_all("tr"):
        cells = tr.find_all(["th", "td"])
        rows.append("|" + "|".join(" " + inline_md(c).strip() + " "
                                   for c in cells) + "|")
    if len(rows) >= 2:
        ncol = table.find("tr").find_all(["th", "td"]).__len__()
        rows.insert(1, "|" + "|".join([" --- "] * ncol) + "|")
    return rows


# ------------------------------------------------------------ reference pages
def extract_parent(article, url):
    h1 = article.find("h1")
    lead = article.find("p", class_="t-lead")
    pres = article.find_all("pre")
    entry = {
        "title": h1.get_text().strip(),
        "url": url,
        "lead": inline_md(lead).strip() if lead else "",
        "typedef": pres[0].get_text().strip() if pres else "",
        "docs_link": None,
        "members": [],
        "sections": [],
    }
    for a in article.find_all("a", href=True):
        if a.get_text(strip=True).startswith("Docs: "):
            entry["docs_link"] = {
                "title": a.get_text(strip=True)[len("Docs: "):].strip(),
                "href": a["href"],
            }
            break
    for section in article.find_all("section"):
        h2 = section.find("h2")
        if not h2:
            continue
        label = heading_text(h2)               # 'Functions 39' / 'Fields 1'
        if not label.lower().startswith(("functions", "fields")):
            continue
        stype = label.split()[0].lower()
        entry["sections"].append({"title": label, "type": stype})
        for a in section.find_all("a", id=True):
            p = a.find("p", class_="t-body")
            entry["members"].append({
                "name": a["id"],
                "section": stype,
                "signature": clean_sig(a.find("code").get_text())
                if a.find("code") else "",
                "description": inline_md(p).strip() if p else "",
                "href": a["href"],
            })
    return entry


def extract_member(article, url):
    h1 = article.find("h1")
    lead = article.find("p", class_="t-lead")
    pre = article.find("pre")
    header = article.find("header")

    kind = ""
    htext = header.get_text(" ", strip=True) if header else ""
    for k, marker in (("method", "Method of"), ("field", "Field of"),
                      ("function", "Function of")):
        if marker in htext:
            kind = k
            break

    entry = {
        "title": h1.get_text().strip(),
        "url": url,
        "kind": kind,
        "lead": inline_md(lead).strip() if lead else "",
        "signature": clean_sig(pre.get_text()) if pre else "",
        "params": [],
        "returns": [],
        "used_in": [],
    }

    for section in article.find_all("section"):
        h2 = section.find("h2")
        label = h2.get_text(strip=True) if h2 else ""
        if label == "Parameters":
            card = section.find("div", class_="card")
            if not card:
                continue
            for row in card.find_all("div", recursive=False):
                codes = row.find_all("code", recursive=False)
                meta = row.find("span", class_="t-meta")
                if len(codes) < 2 or meta is None:
                    continue
                entry["params"].append({
                    "name": codes[0].get_text().strip(),
                    "type": clean_sig(codes[1].get_text()),
                    "required": meta.get_text(strip=True) == "required",
                })
        elif label == "Returns":
            for code in section.find_all("code", recursive=False):
                entry["returns"].append(clean_sig(code.get_text()))
        elif label == "Used in":
            for li in section.find_all("li"):
                a = li.find("a", href=True)
                if not a:
                    continue
                wrapper = a.find("span", class_="min-w-0")
                if not wrapper:
                    continue
                quote = wrapper.find("code")
                spans = wrapper.find_all("span", recursive=False)
                source = spans[-1].get_text(strip=True) if spans else ""
                entry["used_in"].append({
                    "quote": quote.get_text() if quote else "",
                    "source": source,
                    "href": a["href"],
                })
    return entry


def article_lead(article) -> str:
    """The p.t-lead headline that sits OUTSIDE the prose div ('' if none).
    Captured as its own field (2026-10-30 parity fix) so the page lead is
    no longer lost — the official llms-full.txt includes it, and the old
    policy of dropping it left the dataset without a word of it."""
    lead = article.find("p", class_="t-lead")
    return inline_md(lead).strip() if lead else ""


# --------------------------------------------------------------------- main
def url_from_manifest_or_name(crawl_dir, fname, manifest):
    for url, f in manifest.items():
        if f == fname:
            return url
    stem = fname[:-len(".html")] if fname.endswith(".html") else fname
    if stem == "index":
        return "/docs/citadel"
    return "/docs/citadel/" + stem.replace("__", "/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=f"{ROOT}/scripts/crawl_html",
                    help="directory with crawled .html files")
    ap.add_argument("--out", default=f"{ROOT}/scripts/dataset.json",
                    help="output dataset path")
    args = ap.parse_args()

    manifest_path = os.path.join(args.dir, "manifest.json")
    manifest = {}
    if os.path.exists(manifest_path):
        manifest = json.load(open(manifest_path))

    data = {"guides": {}, "docs": {}, "reference_parents": {},
            "reference_members": {}}
    skipped = []

    for fname in sorted(os.listdir(args.dir)):
        if not fname.endswith(".html"):
            continue
        url = url_from_manifest_or_name(args.dir, fname, manifest)
        soup = BeautifulSoup(open(os.path.join(args.dir, fname)).read(),
                             "html.parser")
        article = soup.find("article")
        if article is None:                       # listing pages (e.g. /guides)
            skipped.append(url)
            continue
        if url == "/docs/citadel":
            skipped.append(url)                   # landing page: no content
            continue

        if url.startswith("/docs/citadel/guides/"):
            slug = url[len("/docs/citadel/guides/"):]
            data["guides"][slug] = {
                "title": article.find("h1").get_text().strip(),
                "lead": article_lead(article),
                "markdown": article_markdown(article),
            }
        elif url.startswith("/docs/citadel/reference/"):
            parts = url[len("/docs/citadel/reference/"):].split("/")
            if len(parts) == 2 and parts[1]:
                parent, member = parts
                data["reference_members"].setdefault(parent, {})[member] = \
                    extract_member(article, url)
            else:
                parent = parts[0]
                data["reference_parents"][parent] = extract_parent(article, url)
        else:
            slug = url[len("/docs/citadel/"):]
            data["docs"][slug] = {
                "title": article.find("h1").get_text().strip(),
                "lead": article_lead(article),
                "markdown": article_markdown(article),
            }

    # deterministic ordering: alphabetical by key, members inside a parent too
    data["guides"] = dict(sorted(data["guides"].items()))
    data["docs"] = dict(sorted(data["docs"].items()))
    data["reference_parents"] = dict(sorted(data["reference_parents"].items()))
    data["reference_members"] = {
        p: dict(sorted(m.items()))
        for p, m in sorted(data["reference_members"].items())
    }

    with open(args.out, "w") as f:
        json.dump(data, f, indent=1)

    n_members = sum(len(v) for v in data["reference_members"].values())
    print(f"guides {len(data['guides'])} | docs {len(data['docs'])} | "
          f"parents {len(data['reference_parents'])} | "
          f"members {n_members} -> {args.out}")
    if skipped:
        print("skipped (no article / landing):", ", ".join(sorted(skipped)))


if __name__ == "__main__":
    main()
