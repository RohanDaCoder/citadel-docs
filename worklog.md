# Worklog

---
Task ID: 1
Agent: main (Z.ai)
Task: Crawl https://minefort.com/docs/citadel and build a properly structured docs site

Work Log:
- Fetched https://minefort.com/docs/citadel via WebFetch; discovered the docs are a Next.js SPA with SSR (curl with browser UA works).
- Extracted URL structure from raw HTML: /docs/citadel/guides/*, /docs/citadel/<topic-pages>, /docs/citadel/reference/<Name>[/<member>].
- Wrote crawler (scripts/crawl_citadel.py + discover_all.py): discovered and downloaded 916 pages to scripts/crawl_html/ (5 guides, 55 doc pages + index, 851 reference pages incl. member pages).
- Noted the site's own llms.txt/llms-full.txt links are broken (404) — part of the original site's problems.
- Analyzed HTML structure of each page type: guides/docs articles (h1/h2/p/pre/ul/table), reference parent pages (sections with function/field listing cards), reference member pages (lead, signature pre, Parameters card, Returns, Used in).
- Wrote extractor (scripts/extract_final.py): BeautifulSoup -> structured dataset.json (1.0 MB) with markdown for guides/docs and structured data (signature, params with required flags, returns, used_in cross-references) for reference pages. Fixed parameter required-flag bug (span.t-meta selector) and signature spacing cleanup.
- Deduplicated case-variant reference URLs: 7 pairs identical (server case-insensitive: world/World, players/Players, ui/Ui, game/Game, sound/Sound, commands/Commands, fx/Fx), 5 pairs genuinely different pages (camera/Camera, color/Color, noise/Noise, tween/Tween, vec3/Vec3).
- Built docs site data (scripts/prepare_site_data.py): nav.json (navigation tree: 5 guides / 9 topics x 55 pages / 29 globals by topic + types A-Z), 904 per-page JSON files in src/data/pages/, search.json (899 searchable entries incl. all 674 API members), page-loaders.generated.ts (lazy per-page dynamic imports).
- Built Next.js 16 docs app (single `/` route, hash-based SPA router):
  - src/lib/docs/router.ts (useSyncExternalStore hash router, SSR-safe)
  - src/lib/docs/markdown.ts (custom markdown parser: headings w/ slug ids, code fences, nested lists, tables, inline code/bold/links)
  - src/lib/docs/highlight.ts (custom Luau/YAML/shell tokenizer)
  - src/components/docs/: DocsApp (shell: sticky header, sidebar, TOC, mobile drawer), Sidebar (collapsible Guide/Docs/Reference tree), SearchDialog (cmdk, Cmd+K, scored fuzzy search), Markdown renderer, CodeBlock (lang label + copy button + syntax colors), HomePage, ArticlePage (breadcrumbs, prev/next), RefIndexPage, RefPage (functions/fields tabs + filter), RefMemberPage (signature, parameters table, returns, used-in cross links), Toc (scroll-spy).
- Theme: next-themes dark/light, amber/gold accent on zinc palette (no indigo/blue).
- Fixed during verification: nested <a> hydration error (HomePage cards), invalid heading element type (number vs string) in Markdown renderer, TOC id dedup desync between Python and JS, case-variant canonicalization bug (Camera/noise overwriting globals), SSR hydration mismatch (hash router via useSyncExternalStore), setState-in-effect lint errors.
- Verified with agent-browser: all 20+ route types render (home, guides, docs, reference index, globals, types, members, case-variant pages), search dialog (query, filter, keyboard nav, navigation), mobile drawer (390px), light/dark themes, code block copy. VLM QA: 9/10 polish, consistent design, no broken elements.
- Lint passes clean. Dev server healthy (GET / 200).

Stage Summary:
- Deliverable: fully functional, restructured Citadel docs site at `/` (Next.js dev server, port 3000).
- Content: 5 game guides, 9 doc topics (55 pages), reference with 29 globals + 141 unique types + 674 documented API calls — all 904 pages lazy-loaded, all searchable via Cmd+K.
- Key artifacts: scripts/crawl_html/ (916 raw pages), scripts/dataset.json (structured extraction), src/data/ (site data), src/components/docs/ + src/lib/docs/ (app code).
- The new structure replaces the original paragraph-wall format with: hierarchical sidebar navigation, breadcrumbs, per-page TOC, prev/next flow, filterable API listings, parameter tables, cross-references, and full-text search.
