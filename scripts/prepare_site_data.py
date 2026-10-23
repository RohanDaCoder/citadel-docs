#!/usr/bin/env python3
"""Prepare all data files for the Citadel docs site.

Generates:
- src/data/nav.json        navigation tree (guides / docs topics / reference groups + types)
- src/data/pages/*.json    one file per page (lazy-loaded)
- src/data/search.json     compact search index
"""
import os
import re
import json
import unicodedata

SCRIPTS = "/home/z/my-project/scripts"
SITE_DATA = "/home/z/my-project/src/data"
PAGES_DIR = os.path.join(SITE_DATA, "pages")
os.makedirs(PAGES_DIR, exist_ok=True)

with open(os.path.join(SCRIPTS, "dataset.json")) as f:
    ds = json.load(f)
with open(os.path.join(SCRIPTS, "docs_hierarchy.json")) as f:
    docs_hierarchy = json.load(f)
with open(os.path.join(SCRIPTS, "reference_nav.json")) as f:
    reference_nav = json.load(f)

def slugify(text):
    """Slugify heading text to an anchor id."""
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text).strip("-")
    return text or "section"

def parse_toc(markdown):
    """Extract h2/h3 headings from markdown for the page TOC.

    The dedup counter runs over ALL heading levels (h1-h6) so that it matches
    the JS renderer's id assignment exactly.
    """
    toc = []
    used = {}
    for line in markdown.split("\n"):
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            label = re.sub(r"[*`]", "", text)
            sid = slugify(label)
            if sid in used:
                used[sid] += 1
                sid = f"{sid}-{used[sid]}"
            else:
                used[sid] = 0
            if level in (2, 3):
                toc.append({"id": sid, "text": label, "level": level})
    return toc

def extract_headings_text(markdown):
    lines = []
    for line in markdown.split("\n"):
        m = re.match(r"^#{2,4}\s+(.*)$", line)
        if m:
            lines.append(re.sub(r"[*`]", "", m.group(1)).strip())
    return lines

# ---------------- 1. Guides ----------------
GUIDE_ORDER = [
    ("your-first-pack", "Your first pack",
     "Build a small lobby while learning how a Citadel pack works: the two files, solid ground, a welcome, and a /spawn command."),
    ("coin-rush", "Coin rush",
     "Turn a pack into a game: gold coins on a round arena, 60 seconds, a score sidebar, and each player's best score saved."),
    ("parkour-a-room-each", "Parkour, a room each",
     "Give every player a world of their own: /play builds a parkour course in a room that belongs to one player."),
    ("build-a-cottage", "Build a cottage",
     "Build something that looks made by hand: a cottage with a steep roof, thick walls, a chimney, and a garden."),
    ("a-dungeon-dimension", "A dungeon dimension",
     "Add a world of your own beside the main one: a dungeon under a castle with its own type, terrain, and folder."),
]

guides_nav = []
for slug, title, desc in GUIDE_ORDER:
    g = ds["guides"].get(slug)
    if not g:
        continue
    toc = parse_toc(g["markdown"])
    page = {
        "type": "guide",
        "slug": slug,
        "title": title,
        "description": desc,
        "markdown": g["markdown"],
        "toc": toc,
    }
    with open(os.path.join(PAGES_DIR, f"guide-{slug}.json"), "w") as f:
        json.dump(page, f)
    guides_nav.append({"slug": slug, "title": title, "description": desc})

# ---------------- 2. Docs (9 topics, 55 pages) ----------------
docs_nav = []
topic_descriptions = {
    "Examples": "Whole packs that run: read one to see how the calls fit together.",
    "Basics": "What a pack is, how a server runs it, and the rules every call follows.",
    "World": "The ground players stand on: terrain, blocks, builds, time, and the game version's own data.",
    "Players": "Who is here, how they move and see, what they type and click, and what they may do.",
    "Interface": "What a player reads: titles, bars, the HUD, menus, and pictures on walls.",
    "Sound and effects": "What a player hears and sees in the air: sounds, particles, lasers and light.",
    "Entities": "Things in the world: displays, models, NPCs, entities, items, and the zones that notice them.",
    "Game logic": "How a game runs: rooms, the rules a room simulates, events, and code split into modules.",
    "Data": "What survives a restart, what the whole experience shares, and the limits a pack runs in.",
}
for topic in docs_hierarchy:
    topic_title = re.sub(r"\s*\d+$", "", topic["title"]).strip()
    pages_nav = []
    for p in topic["pages"]:
        slug = p["href"].replace("/docs/citadel/", "")
        d = ds["docs"].get(slug)
        if not d:
            continue
        toc = parse_toc(d["markdown"])
        page = {
            "type": "doc",
            "slug": slug,
            "title": p["title"],
            "topic": topic_title,
            "markdown": d["markdown"],
            "toc": toc,
        }
        with open(os.path.join(PAGES_DIR, f"doc-{slug}.json"), "w") as f:
            json.dump(page, f)
        pages_nav.append({"slug": slug, "title": p["title"]})
    docs_nav.append({
        "topic": topic_title,
        "description": topic_descriptions.get(topic_title, ""),
        "pages": pages_nav,
    })

# ---------------- 3. Reference ----------------
# Canonical globals (29, lowercase, from sidebar)
globals_by_topic = []
global_names = set()
for group in reference_nav:
    entries = []
    for e in group["entries"]:
        global_names.add(e["name"].lower())
        entries.append({"name": e["name"], "count": e["count"]})
    globals_by_topic.append({"topic": group["title"], "globals": entries})

# Canonicalize parents.
# Case-variant URLs on the original site can be:
#   (a) the SAME page (server is case-insensitive): world/World -> keep one, under the sidebar-global name
#   (b) DIFFERENT pages (a lowercase global and a Capitalized type): camera/Camera -> keep both
# Member pages attach by exact raw URL key first, then to the group's only canonical.
parents = ds["reference_parents"]
members = ds["reference_members"]

sidebar_global_names = [e["name"] for group in reference_nav for e in group["entries"]]
global_names = {g.lower() for g in sidebar_global_names}

# group parents by lowercase key
groups = {}
for name, data in parents.items():
    groups.setdefault(name.lower(), []).append({"name": name, "data": data})

def content_sig(d):
    return (d.get("title", ""), d.get("lead", ""), len(d.get("members", [])))

canonical = []  # [{name, data}]
for key, variants in groups.items():
    sidebar_name = next((g for g in sidebar_global_names if g.lower() == key), None)
    # dedupe content-identical variants; prefer the exact sidebar global name
    uniq = {}
    for v in variants:
        sig = content_sig(v["data"])
        if sig in uniq:
            existing = uniq[sig]
            # on a tie, prefer the variant matching the sidebar global name
            if sidebar_name and v["name"] == sidebar_name and existing["name"] != sidebar_name:
                uniq[sig] = v
            continue
        uniq[sig] = v
    kept = list(uniq.values())
    if sidebar_name and len(kept) > 1:
        # put the sidebar global first so it keeps the lowercase name
        exact = next((v for v in kept if v["name"] == sidebar_name), None)
        if exact:
            kept = [exact] + [v for v in kept if v is not exact]
    canonical.extend(kept)

# map raw member-page keys -> canonical page
canon_by_name = {c["name"]: c for c in canonical}
members_for = {c["name"]: {} for c in canonical}
for raw_key, mems in members.items():
    if raw_key in canon_by_name:
        members_for[raw_key].update(mems)
        continue
    group_canon = [c for c in canonical if c["name"].lower() == raw_key.lower()]
    if len(group_canon) == 1:
        members_for[group_canon[0]["name"]].update(mems)
    else:
        print(f"WARNING: ambiguous member key {raw_key!r} -> {len(group_canon)} canonicals; skipped")

ref_pages = {}   # canonical name -> page json
ref_nav_types = []
types_by_letter = {}
for entry in sorted(canonical, key=lambda c: c["name"].lower()):
    name = entry["name"]
    data = entry["data"]
    key = name.lower()
    is_global = key in global_names and name in sidebar_global_names
    # parse kind from title: "world global · type World" / "Player type"
    kind = "global" if is_global else "type"
    assoc_type = ""
    m = re.search(r"·\s*type\s+(\S+)", data.get("title", ""))
    if m:
        assoc_type = m.group(1)
    mems = members_for.get(name, {})

    # member list from parent page's own listing
    listing = []
    for mem in data.get("members", []):
        mname = mem["name"]
        detail = mems.get(mname)
        listing.append({
            "name": mname,
            "section": mem.get("section", ""),
            "signature": mem.get("signature", ""),
            "description": mem.get("description", ""),
            "hasPage": detail is not None,
        })
    # member detail pages not present in listing (e.g. task-less parents)
    listed = {m["name"] for m in listing}
    for mname, detail in mems.items():
        if mname not in listed:
            listing.append({
                "name": mname,
                "section": "functions",
                "signature": detail.get("signature", ""),
                "description": detail.get("lead", ""),
                "hasPage": True,
            })
    # split sections
    functions = [m for m in listing if m["section"] != "fields"]
    fields = [m for m in listing if m["section"] == "fields"]

    # topic from reference_nav
    topic = ""
    for group in reference_nav:
        for e in group["entries"]:
            if e["name"].lower() == key:
                topic = group["title"]
                break

    page = {
        "type": "ref",
        "name": name,
        "kind": kind,
        "assocType": assoc_type,
        "topic": topic,
        "lead": data.get("lead", ""),
        "typedef": data.get("typedef", ""),
        "docsLink": data.get("docs_link"),
        "functions": functions,
        "fields": fields,
    }
    ref_pages[name] = page
    with open(os.path.join(PAGES_DIR, f"ref-{name}.json"), "w") as f:
        json.dump(page, f)

    # member detail pages
    for mname, detail in mems.items():
        mpage = {
            "type": "refmember",
            "parent": name,
            "name": mname,
            "title": detail.get("title") or f"{name}.{mname}",
            "kind": detail.get("kind", ""),
            "lead": detail.get("lead", ""),
            "signature": detail.get("signature", ""),
            "params": detail.get("params", []),
            "returns": detail.get("returns", []),
            "usedIn": detail.get("used_in", []),
        }
        with open(os.path.join(PAGES_DIR, f"refm-{name}-{mname}.json"), "w") as f:
            json.dump(mpage, f)

    if not is_global:
        letter = name[0].upper()
        types_by_letter.setdefault(letter, []).append(name)

# types nav (alphabetical)
types_nav = []
for letter in sorted(types_by_letter.keys()):
    types_nav.append({"letter": letter, "names": sorted(types_by_letter[letter])})

reference_nav_out = {
    "globalsByTopic": globals_by_topic,
    "types": types_nav,
}

# ---------------- 4. site nav.json ----------------
nav = {
    "guides": guides_nav,
    "docs": docs_nav,
    "reference": reference_nav_out,
}
with open(os.path.join(SITE_DATA, "nav.json"), "w") as f:
    json.dump(nav, f, indent=1)

# ---------------- 5. search index ----------------
search = []
for g in guides_nav:
    d = ds["guides"][g["slug"]]
    search.append({
        "t": g["title"],
        "u": f"/guides/{g['slug']}",
        "k": "Guide",
        "s": "Guide",
        "x": " ".join(extract_headings_text(d["markdown"]))[:400],
    })
for topic in docs_nav:
    for p in topic["pages"]:
        d = ds["docs"][p["slug"]]
        search.append({
            "t": p["title"],
            "u": f"/docs/{p['slug']}",
            "k": "Docs",
            "s": topic["topic"],
            "x": " ".join(extract_headings_text(d["markdown"]))[:400],
        })
for name, page in ref_pages.items():
    search.append({
        "t": name,
        "u": f"/reference/{name}",
        "k": "Global" if page["kind"] == "global" else "Type",
        "s": page["topic"],
        "x": (page["lead"] + " " + " ".join(m["signature"] for m in page["functions"][:20]))[:400],
    })
    for m in page["functions"] + page["fields"]:
        if m["hasPage"]:
            mem = members_for.get(name, {}).get(m["name"])
            if mem:
                search.append({
                    "t": m["signature"] or m["name"],
                    "u": f"/reference/{name}/{m['name']}",
                    "k": "API",
                    "s": name,
                    "x": mem.get("lead", "")[:300],
                })

with open(os.path.join(SITE_DATA, "search.json"), "w") as f:
    json.dump(search, f)

# ---------------- summary ----------------
n_pages = len(os.listdir(PAGES_DIR))
print(f"Pages generated: {n_pages}")
print(f"Guides: {len(guides_nav)}")
print(f"Doc topics: {len(docs_nav)} ({sum(len(t['pages']) for t in docs_nav)} pages)")
print(f"Reference pages: {len(ref_pages)} ({sum(1 for p in ref_pages.values() if p['kind']=='global')} globals, {sum(1 for p in ref_pages.values() if p['kind']=='type')} types)")
print(f"Member pages: {sum(len(v) for v in members_for.values())}")
print(f"Search entries: {len(search)}")
print(f"nav.json size: {os.path.getsize(os.path.join(SITE_DATA, 'nav.json'))/1024:.0f} KB")
print(f"search.json size: {os.path.getsize(os.path.join(SITE_DATA, 'search.json'))/1024:.0f} KB")
