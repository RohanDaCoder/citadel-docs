#!/usr/bin/env python3
"""audit_parity.py — page-by-page parity audit: official llms-full.txt vs
dataset.json (the HTML extraction).

WHY (decided 2026-10-30, after live-verifying both sources):
  * official llms.txt/llms-full.txt cover ONLY the 55 prose pages (52 docs +
    3 example pages). Zero /reference/ URLs, no Parameters/Returns blocks.
    The reference layer (178 parents / 682 members, ~92% of the site) exists
    only as rendered HTML -> the crawl is the ONLY complete source.
  * BUT the official markdown is a *second, independent, zero-heuristic*
    rendering of the same 55 pages. Diffing it against our HTML extraction
    is the strongest available proof that the extractor invents nothing
    and loses nothing. It also catches drift the other way: if minefort
    edits prose, llms-full.txt moves before anyone re-crawls.

What it does:
  1. fence-aware parse of llms-full.txt into H1 sections / H2 pages (code
     fences often contain `# comment` lines — a naive header scan lies);
  2. map every official page to its dataset entry (doc first, guide
     fallback — the three Examples pages are doc slugs on the site);
  3. word-level diff per page (SequenceMatcher over lowercased word
     tokens) plus a missing/extra token set for the worst pages;
  4. report: which dataset pages llms-full.txt does NOT cover (expected:
     4 guides + reference index + reference layer), and every covered
     page's similarity ratio.

Known, benign divergences (verified, not drift):
  * lead paragraphs: the site renders the page lead as p.t-lead OUTSIDE
    the prose div; the extractor captures it as its own 'lead' field
    (2026-10-30 fix — before that it was silently dropped entirely).
    The audit joins lead + markdown; entries without the field fall
    back to stripping the official lead.
  * heading levels: official uses ### where the site uses ## (the page
    title is the H1) -> normalised away in the token stream.

Exit codes: 0 = every covered page >= threshold; 1 = drift found (pages
below threshold are printed for `sync_official.py --doc-pages <slugs>`).

Usage:
  python3 scripts/audit_parity.py            # full report
  python3 scripts/audit_parity.py --min 0.90 # tighten the threshold
"""
import argparse
import difflib
import json
import re
import sys

ROOT = "/home/z/my-project"
LLMS_FULL = f"{ROOT}/scripts/official_llms/minefort-llms-full.txt"
DS_PATH = f"{ROOT}/scripts/dataset.json"

# The three llms 'Examples' entries link to the DOC routes on the site
# (verified: https://minefort.com/docs/citadel/your-first-pack et al.), so
# they are compared against dataset['docs'], not dataset['guides'].
SECTION_NOT_PAGES = ("Citadel 0.1.0 pack API",)  # preamble H1, not a page


def parse_llms_full(path: str) -> dict[str, str]:
    """Fence-aware split of llms-full.txt into {page title: body}.

    H1 lines name sections (Examples, Basics, ...); H2 lines name pages.
    Only lines outside ``` fences are structural; inside a fence a `#` is
    a code comment (e.g. `# citadel.yml`), never a heading.
    """
    pages: dict[str, str] = {}
    title = None
    buf: list[str] = []
    in_fence = False

    def flush():
        if title is not None:
            pages[title] = "\n".join(buf).strip()

    for line in open(path, encoding="utf-8"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            if title is not None:
                buf.append(stripped)
            continue
        if not in_fence and (stripped.startswith("# ")
                             or stripped.startswith("## ")):
            if stripped.startswith("## "):
                flush()
                title = stripped[3:].strip()
                buf = []
            else:  # section H1: close the previous page
                flush()
                title = None
                buf = []
            continue
        if title is not None:
            buf.append(stripped)
    flush()
    return pages


def slugify(title: str) -> str:
    t = title.lower().strip()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t


TOKEN = re.compile(r"[a-z0-9_']+")


def tokens(md: str) -> list[str]:
    """Lowercased word tokens over the whole markdown. Code lines are
    word-split too (fences and headings normalised away), so the ratio
    measures CONTENT parity — missing calls, changed prose — not spacing
    or formatting (```lua vs ```luau, '|' vs '|', '--' vs '#'). The live
    site renders typographic apostrophes, the official file ASCII ones;
    both are normalised so punctuation is not 'drift'."""
    words = []
    for line in md.splitlines():
        s = line.strip().replace("’", "'")
        if s.startswith("```"):
            continue          # fence markers (```lua vs ```luau) are formatting
        words.extend(TOKEN.findall(s.lower()))
    return words


def strip_lead(body: str) -> str:
    """Drop the first paragraph (the page lead). Fallback used only when a
    dataset entry predates lead capture — the official body opens with the
    same lead the site renders as p.t-lead."""
    parts = body.split("\n\n", 1)
    return parts[1] if len(parts) == 2 else body


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=float, default=0.85,
                    help="similarity threshold (default 0.85)")
    ap.add_argument("--show", type=int, default=10,
                    help="extra/missing token samples for drifted pages")
    args = ap.parse_args()

    pages = parse_llms_full(LLMS_FULL)
    ds = json.load(open(DS_PATH))
    docs = ds["docs"]
    guides = ds["guides"]

    covered, drift, unmapped = [], [], []
    for title, body in pages.items():
        if title in SECTION_NOT_PAGES:
            continue
        slug = slugify(title)
        if slug in docs:
            entry = docs[slug]
        elif slug in guides:
            entry = guides[slug]
        else:
            unmapped.append((title, slug))
            continue
        ours = entry["markdown"]
        lead = entry.get("lead", "")
        if lead:
            # the official body opens with the same lead the site renders
            # as p.t-lead; ours captures it as its own field
            ours = lead + "\n\n" + ours
        else:
            body = strip_lead(body)   # pre-lead-capture dataset entry

        a = tokens(body)           # official
        b = tokens(ours)           # ours (HTML extraction)
        ratio = difflib.SequenceMatcher(None, a, b).ratio()
        if ratio < args.min:
            amissing = sorted(set(a) - set(b))   # official says, ours lacks
            bextra = sorted(set(b) - set(a))     # ours says, official lacks
            drift.append((title, slug, ratio, len(a), len(b),
                          amissing[:args.show], bextra[:args.show]))
        else:
            covered.append((title, slug, ratio, len(a)))

    # dataset pages the official files do not cover (expected surplus):
    theirs = {slugify(t) for t in pages} - set(SECTION_NOT_PAGES)
    ours_all = set(docs) | set(guides)
    surplus = sorted(ours_all - theirs)

    print("=== parity audit: official llms-full.txt vs dataset.json ===")
    print(f"official pages parsed: {len(pages)} "
          f"({len(covered) + len(drift) + len(unmapped)} mappable)")
    print(f"dataset docs={len(docs)} guides={len(guides)}")
    print()
    print(f"--- covered ({len(covered)}) ---")
    for title, slug, ratio, n in sorted(covered, key=lambda x: x[2]):
        print(f"  {ratio:6.1%}  {slug}  ({n} tokens)")
    print()
    print("--- DRIFT (below threshold) ---")
    if drift:
        for title, slug, ratio, na, nb, miss, extra in sorted(drift,
                                                              key=lambda x: -x[2]):
            print(f"  {ratio:6.1%}  {slug}  official={na} ours={nb} tokens")
            if miss:
                print(f"         official-only: {', '.join(miss)}")
            if extra:
                print(f"         ours-only:     {', '.join(extra)}")
        print()
        print(f"-> {len(drift)} drifted page(s). Refresh candidates:")
        slugs = ",".join(s for _, s, *_ in drift if s in docs)
        print(f"   python3 scripts/sync_official.py --doc-pages {slugs}")
        print("   (reference parents/members: --sections <ns>)")
    else:
        print("  none — every covered page matches the official markdown")
    if unmapped:
        print()
        print("--- UNMAPPED official pages ---")
        for title, slug in unmapped:
            print(f"  {title!r} -> {slug!r} not in dataset docs/guides")
    print()
    print(f"--- dataset pages NOT in llms-full.txt ({len(surplus)}) ---")
    for s in surplus:
        kind = "doc" if s in docs else "guide"
        print(f"  {kind:5}  {s}")
    ref_extra = (len(ds["reference_parents"]) + len(ds["reference_members"]))
    print(f"  plus the reference layer: {len(ds['reference_parents'])} "
          f"parents / {len(ds['reference_members'])} member pages "
          f"({ref_extra} pages) — absent from the official llms files")

    return 1 if (drift or unmapped) else 0


if __name__ == "__main__":
    sys.exit(main())
