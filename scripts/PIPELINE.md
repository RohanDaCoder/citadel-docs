# Citadel Wiki — Pipeline Documentation

Everything in this project is generated from verified sources: the official
docs at `https://minefort.com/docs/citadel` were crawled once, structured into
`scripts/dataset.json`, and every downstream artifact (Starlight site, llms
files, `citadel.d.ts`) is regenerated from that dataset by the scripts below.
Nothing is hand-typed from memory; nothing is hallucinated.

```
                 minefort.com/docs/citadel  (Next.js SSR - no JS needed)
                        │
        ┌───────────────┴────────────────┐
        │ 1. discover_all.py            │ BFS over SSR <a href> links
        │ 2. crawl_citadel.py           │ download HTML + manifest.json
        └───────────────┬────────────────┘
                        ▼
              scripts/crawl_html/*.html
                        │
        │ 3. extract_final.py            │ BeautifulSoup -> structured JSON
        └───────────────┬────────────────┘
                        ▼
              scripts/dataset.json  (1.0 MB — the verified ground truth)
                        │
     ┌──────────────────┼─────────────────────────────┐
     ▼                  ▼                             ▼
 wiki_src/*.md      4. gen_starlight.py          6. gen_citadel_dts.py
 (hand-authored     → src/content/docs/**       → citadel-ts/types/citadel.d.ts
  synthesis from    → scripts/generated/            │
  the same crawl)     starlight-manifest.json       ▼
     │              → 906 md pages + sidebar   citadel-ts/ (TSTL project:
     └────────────► 5. npm run build              TS -> Luau transpile setup)
                     + check_dist_links.py
                     ▼
                   dist/  (static site)
                        │
        │ 7. gen_llms_full.py → public/llms.txt + llms-full.txt
        └────────────────────────────────────────────────────────┘
```

---

## Stage 1 — Discovery: `scripts/discover_all.py`

The minefort docs are a Next.js app with **server-side rendering**: every page's
HTML already contains the full sidebar/navigation as plain `<a href>` links.
No headless browser or JS execution is needed — a BFS crawl over the SSR HTML
reaches every page:

1. fetch `/docs/citadel` (curl with a full browser UA — Cloudflare rejects
   short UAs with a challenge page),
2. collect every href matching `/docs/citadel/...`,
3. queue new URLs, repeat until the queue empties (~2–3 levels deep: the
   reference index alone lists all 177 type/global parents).

Two details matter:
- **URLs are never case-normalised.** The site links both `world` and `World`,
  `camera` and `Camera`, etc. For 7 pairs the server serves the *same* page
  (case-insensitive); for 5 pairs (`camera/Camera`, `color/Color`,
  `noise/Noise`, `tween/Tween`, `vec3/Vec3`) they are genuinely different pages.
  Both variants are kept and reconciled later, in the site generation.
- `/docs/citadel/llms.txt` and `/docs/citadel/llms-full.txt` are linked but
  404 on the original site — they are skipped.

Run: `python3 scripts/discover_all.py` (writes `scripts/crawl_html/urls.txt`,
~916 URLs; `--limit N` stops early for a test).

## Stage 2 — Download: `scripts/crawl_citadel.py`

Reads `urls.txt` and saves each page as `scripts/crawl_html/<flattened>.html`
(`/` → `__`, so `reference/World/set_block` → `reference_World_set_block.html`)
plus `manifest.json` mapping url → filename (pages carry no canonical/og:url
tag, so the manifest is the extractor's source of truth). Resume-safe
(existing files are skipped), 0.25 s politeness delay, 3 retries with back-off,
and Cloudflare challenge pages are detected and never written.

Run: `python3 scripts/crawl_citadel.py` (~215 MB for the full 916-page crawl).

## Stage 3 — Extraction: `scripts/extract_final.py` → `scripts/dataset.json`

BeautifulSoup turns the HTML into one structured JSON file with four sections:

| key | entries | shape |
|---|---|---|
| `guides` | 5 | `{slug: {title, markdown}}` |
| `docs` | 56 | `{slug: {title, markdown}}` (incl. the `/reference` listing) |
| `reference_parents` | 177 | `{Name: {title, url, lead, typedef, docs_link, members[], sections[]}}` |
| `reference_members` | 674 | `{Parent: {member: {title, url, kind, lead, signature, params[], returns[], used_in[]}}}` |

The DOM rules the extractor relies on (all verified against the live markup):

- **doc/guide pages**: content lives in `article div.prose` — h2/h3, paragraphs,
  `<pre><code class="language-X">` fences (`language-lua` is emitted as
  `luau`, bare `<code>` as a plain fence), bullet lists, pipe tables. The
  `p.t-lead` sits *outside* the prose div and is excluded from the markdown.
  Pages without an `<article>` (the `/guides` card listing) are skipped.
- **reference parents**: h1 (raw text keeps the `global · type X` suffix),
  `p.t-lead`, an optional typedef `<pre>`, a `Docs: X` cross-link chip, and
  per-section member cards `<a id=…><code>signature</code><p class=t-body>…`.
- **reference members**: the kind comes from the header label
  (`Function of` / `Method of` / `Field of`), the signature from the first
  `<pre>`, parameters from card rows (`<code>name</code><code>type</code>
  <span class="t-meta">required|optional</span>`), returns from `<code>` lines
  in the Returns section, and `used_in` quotes from the Used-in list cards.
- **signature cleanup** reproduces the documented spacing exactly:
  `string?` → `string ?`, `Vec3 ,` → `Vec3,`.

**Verification**: `scripts/diff_smoke.py` re-extracts the 14 pages kept in
`scripts/crawl_html_smoke/` (a fixture — HTML + manifest + a fresh
`dataset_smoke.json`) and compares them against the original `dataset.json`:
**12/12 entries byte-identical**, covering every page type plus the
`world`/`World` case-twin. Run it: `python3 scripts/diff_smoke.py`.

## Stage 4 — The wiki itself: `scripts/wiki_src/`

The dataset is the *raw material*; `wiki_src/` is the *authored* synthesis
layer that restructures the paragraph-wall originals into a reference-style
wiki (the "not a port" requirement):

- `_sources/` — every crawled doc page as markdown (`doc-*.md`, `guide-*.md`)
  plus `reference-full.txt` (the complete reference text), all derived from the
  crawl; the authoring ground truth.
- 61 wiki pages across 10 sections (`getting-started`, `concepts`, `world`,
  `entities`, `players`, `ui`, `systems`, `guides`, `cookbook`, `appendix`),
  each with frontmatter (`title/section/order/description/tags`), `In short`
  openers, tables, callouts and cross-links.
- `STYLE.md` (authoring contract), `OUTLINE.md` (information architecture),
  `SLUGS.md` (definitive cross-link slug map).

Every page was written *from* `_sources/` + `reference-full.txt`; API facts
were cross-checked against the reference dataset, so no signature is invented.

## Stage 5 — Starlight generation: `scripts/gen_starlight.py`

One 903-line pass that turns `wiki_src/` + `dataset.json` into the site:

- `wiki_src/*.md` → `src/content/docs/<section>/<slug>.md`: frontmatter →
  Starlight `title`/`description`, leading H1 stripped, `> **Type:**`
  callouts → `:::note`/`:::tip`/`:::caution` admonitions, `/wiki/…` and
  `/ref/…` links rewritten to final routes (case-twins canonicalised:
  the 7 identical lowercase/PascalCase pairs emit one page).
- generated appendices: `appendix/event-catalog.md` (every `on_*` event) and
  `appendix/limits-table.md`.
- API reference from the dataset: 170 parent pages
  (`ref/<Name>/index.md`: lead, linked typedef, functions/fields tables) +
  674 member pages (`ref/<Parent>/<member>.md`: signature, parameters with
  linked types, returns, used-in quotes).
- `scripts/generated/starlight-manifest.json`: the full sidebar + **913
  redirects** preserving every original `minefort.com/docs/citadel` URL.
- self-validates before build: all 3,225 internal links + anchors checked.

Then `npm run build` (907 pages) and `scripts/check_dist_links.py` sweep every
link in the built HTML (217,327 links, 0 broken).

## Stage 6 — Agent files: `scripts/gen_llms_full.py`

Regenerable pipeline stage over `src/content/docs/`: orders all 906 pages
(landing first, then sidebar order), emits each as a `## <title>` section with
an `<a id>` anchor and `<!-- /route/ -->` marker, converts 3,476 internal
links to in-file anchors (two-pass, github-slugger-compatible) and 127 `:::`
admonitions to labelled blockquotes. Output: `public/llms.txt` (28 KB index)
and `public/llms-full.txt` (946 KB, all wiki + reference content inline).
Self-validates: 0 unconverted routes, 0 dangling anchors.

## Stage 7 — TypeScript declarations: `scripts/gen_citadel_dts.py`

Generates `citadel-ts/types/citadel.d.ts` (112 KB) **strictly from
`dataset.json`** — 674 members, 27 globals, 80 interfaces, 57 aliases:

- Luau type strings → TS (unions, arrays `{T}`, records, fn types, literal
  unions, `?` optionality from the raw signatures);
- calling conventions verified from the docs: methods → colon-style interface
  methods, global functions → `this: void` dot calls, spec tables
  (`BlockSpec`/`EntitySpec`/…) → optional callback **properties**;
- gap-fills the reference lacks (`task.*`, `camera.path`, Vec3/Color shapes,
  `player.ui`) cite their wiki source inline; 7 undocumented types stay
  opaque; everything unspecified is `unknown` — nothing guessed.

`citadel-ts/` is the `typescript-to-lua` (TSTL 1.37.1) consumer project:
`tsconfig.json` (`luaTarget: "Luau"`, `.luau` extension,
`luaLibImport: require-minimal`, `noImplicitGlobalVariables`,
`@typescript-to-lua/language-extensions`), an example pack in `src/main.ts`,
and `npm run build` → `dist/main.luau` **is** a Citadel pack folder. The
emitted Luau was checked against the documented dot/colon conventions,
multi-returns and spec literals.

---

## Regeneration cookbook

```sh
# full rebuild from the live site (crawl ~215 MB):
python3 scripts/discover_all.py
python3 scripts/crawl_citadel.py
python3 scripts/extract_final.py            # -> scripts/dataset.json

# rebuild site content + llms files from the existing dataset:
python3 scripts/gen_starlight.py            # -> src/content/docs/**
python3 scripts/gen_llms_full.py            # -> public/llms*.txt
npm install && npm run build                # -> dist/ (907 pages)
python3 scripts/check_dist_links.py         # sweep built HTML

# rebuild the TS declarations + verify the transpile chain:
python3 scripts/gen_citadel_dts.py          # -> citadel-ts/types/citadel.d.ts
cd citadel-ts && npm install && npm run build && npm run check

# verify the extractor against the original dataset (no network needed):
python3 scripts/extract_final.py --dir scripts/crawl_html_smoke \
        --out scripts/crawl_html_smoke/dataset_smoke.json
python3 scripts/diff_smoke.py               # 12/12 byte-identical
```

## Script inventory & provenance

| file | role | provenance |
|---|---|---|
| `scripts/discover_all.py` | BFS URL discovery | **reconstructed** from the original crawler (deleted in the Starlight cleanup), verified against the live site |
| `scripts/crawl_citadel.py` | concurrent downloader + manifest | reconstructed, verified end-to-end |
| `scripts/extract_final.py` | HTML → `dataset.json` | reconstructed; **12/12 entries byte-identical** vs the original dataset (`diff_smoke.py`) |
| `scripts/inspect_dataset.py` | print the dataset schema | original (Task 7) |
| `scripts/diff_smoke.py` | extractor verification harness | original (Task 7) |
| `scripts/crawl_html_smoke/` | 14-page verification fixture | original (Task 7) |
| `scripts/dataset.json` | structured crawl (1.0 MB) | original (Task 1) |
| `scripts/wiki_src/**` | authored wiki sources + `_sources/` raw crawl | original (Tasks 1–2) |
| `scripts/gen_starlight.py` | wiki + dataset → Starlight site | original (Task 3) |
| `scripts/gen_llms_full.py` | site content → llms.txt / llms-full.txt | original (Task 5) |
| `scripts/gen_citadel_dts.py` | dataset → citadel.d.ts | original (Task 6) |
| `scripts/check_dist_links.py` | built-HTML link sweep | original (Task 3) |
| `citadel-ts/**` | TSTL transpile project | original (Task 6) |
