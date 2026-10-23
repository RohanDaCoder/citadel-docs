#!/usr/bin/env python3
"""Build the Citadel wiki site data from wiki_src/ + dataset.json.

Outputs:
  src/data/nav.json            - navigation tree
  src/data/redirects.json      - original minefort docs URLs -> new hash routes
  src/data/search.json         - search index
  src/data/pages/*.json        - per-page data (wiki, ref, refmember)
  src/data/page-loaders.generated.ts
"""
import json, os, re, sys, hashlib
from collections import OrderedDict

ROOT = "/home/z/my-project"
SRC = f"{ROOT}/scripts/wiki_src"
DATA = f"{ROOT}/src/data"
DATASET = json.load(open(f"{ROOT}/scripts/dataset.json"))

SECTIONS = [
    ("getting-started", "Getting started"),
    ("concepts", "Core concepts"),
    ("world", "World & building"),
    ("entities", "Entities"),
    ("players", "Players"),
    ("ui", "Interface & media"),
    ("systems", "Server systems"),
    ("guides", "Guides"),
    ("cookbook", "Cookbook"),
    ("appendix", "Appendix"),
]

# ---------------------------------------------------------------- frontmatter
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)

def parse_page(path):
    raw = open(path).read()
    m = FM_RE.match(raw)
    if not m:
        raise SystemExit(f"no frontmatter: {path}")
    fm = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip().strip('"') for x in v[1:-1].split(",") if x.strip()]
            fm[k.strip()] = v
    body = raw[m.end():].lstrip("\n")
    return fm, body

def slugify(text):
    s = text.lower().normalize("NFKD") if hasattr(text, "normalize") else text.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s).strip("-")
    return s or "section"

def build_toc(body):
    """Heading TOC matching the JS slugify (deduped)."""
    used = {}
    toc = []
    in_code = False
    for line in body.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{2,3})\s+(.*)$", line)  # only H2/H3 in TOC
        if not m:
            continue
        label = re.sub(r"[*`]", "", m.group(2)).strip()
        base = slugify(label)
        n = used.get(base, 0)
        used[base] = n + 1
        hid = base if n == 0 else f"{base}-{n}"
        toc.append({"id": hid, "text": label, "level": len(m.group(1))})
    return toc

# ---------------------------------------------------------------- wiki pages
os.makedirs(f"{DATA}/pages", exist_ok=True)
for f in os.listdir(f"{DATA}/pages"):
    os.remove(f"{DATA}/pages/{f}")

wiki_pages = OrderedDict()  # slug -> data
for sec_id, _ in SECTIONS:
    secdir = f"{SRC}/{sec_id}"
    if not os.path.isdir(secdir):
        continue
    files = sorted(os.listdir(secdir), key=lambda f: (
        int(re.match(r"^\d+-", f) and 0 or 0), f))
    entries = []
    for fname in files:
        if not fname.endswith(".md"):
            continue
        fm, body = parse_page(f"{secdir}/{fname}")
        slug = fname[:-3]
        entries.append({
            "slug": slug, "title": fm.get("title", slug),
            "description": fm.get("description", ""),
            "order": int(fm.get("order", 99)),
        })
        wiki_pages[slug] = {
            "type": "wiki",
            "slug": slug,
            "section": sec_id,
            "title": fm.get("title", slug),
            "description": fm.get("description", ""),
            "tags": fm.get("tags", []),
            "markdown": body,
            "toc": build_toc(body),
        }
    entries.sort(key=lambda e: e["order"])

# ------------------------------------------------------- generated appendices
def gen_event_catalog():
    rows = []
    seen = set()
    for parent, mems in DATASET["reference_members"].items():
        for name, m in mems.items():
            if not name.startswith("on_"):
                continue
            key = f"{parent}.{name}"
            if key in seen:
                continue
            seen.add(key)
            sig = m.get("signature", "")
            lead = (m.get("lead", "") or "").strip()
            if not lead:
                # fall back to parent member description
                p = DATASET["reference_parents"].get(parent)
                if p:
                    for mm in p.get("members", []):
                        if mm["name"] == name:
                            lead = mm.get("description", "")
                            break
            rows.append({
                "parent": parent, "name": name, "kind": m.get("kind", ""),
                "signature": sig, "description": lead,
            })
    rows.sort(key=lambda r: (r["parent"].lower(), r["name"]))
    lines = [
        "---",
        "title: Event catalog",
        "section: appendix",
        "order: 1",
        'description: Every on_* event in the Citadel API in one table — what fires it, what the handler receives, and where the full treatment lives.',
        "tags: [events, reference, catalog]",
        "---",
        "# Event catalog",
        "",
        "> **In short:** every `on_*` subscription in the API, one row each.",
        "> Subscribe with the call, keep the connection, cancel to stop. The",
        "> model itself — deadlines, asks, ordering — is in",
        "> [The event model](/wiki/events).",
        "",
        f"{len(rows)} events across {len(set(r['parent'] for r in rows))} types.",
        "",
    ]
    # group by parent
    byp = OrderedDict()
    for r in rows:
        byp.setdefault(r["parent"], []).append(r)
    for parent in sorted(byp, key=str.lower):
        lines.append(f"## `{parent}`")
        lines.append("")
        lines.append("| Event | Signature | Fires when |")
        lines.append("| --- | --- | --- |")
        for r in byp[parent]:
            desc = (r["description"] or "").replace("\n", " ").replace("|", "\\|")
            if len(desc) > 160:
                desc = desc[:157] + "..."
            sig = r["signature"].replace("|", "\\|")
            lines.append(f"| [`{r['name']}`](/ref/{parent}/{r['name']}) | `{sig}` | {desc} |")
        lines.append("")
    lines += [
        "## See also",
        "",
        "- [The event model](/wiki/events) — subscriptions, asks, deadlines.",
        "- [Runtime](/wiki/runtime) — the event queue and its 4096 cap.",
        "",
    ]
    return "\n".join(lines)

def gen_limits_table():
    content = """---
title: Limits
section: appendix
order: 4
description: Every numeric limit in Citadel in one table — tick budgets, load times, event queues, stores, blobs, leases, builds and generation.
tags: [limits, reference, budget]
---
# Limits

> **In short:** every number the engine enforces, in one place. Each row
> links to the page that explains what happens at the edge.

| Limit | Value | What it bounds | Details |
| --- | --- | --- | --- |
| Tick budget | 2 ms default (`budget_ms`) | A pack's tick and event callbacks per tick | [Limits](/wiki/limits) |
| Runaway limit | 100 ms | Joins, input events, commands, task threads | [Limits](/wiki/limits) |
| Chunk callback | 2 s | `on_generate` / `on_populate` per chunk | [Terrain generation](/wiki/terrain-generation) |
| Chunk wait | 60 s | The engine's wait for a chunk to be made; then it is air | [Terrain generation](/wiki/terrain-generation) |
| Entry script | 5 s between waits, 30 s total | Pack load; past it the load fails | [Runtime](/wiki/runtime) |
| Event queue | 4096 ordinary events per pack | Overflow drops the oldest and logs | [Limits](/wiki/limits) |
| Ask deadline | 2 ms | `on_break` / `on_place` / `on_damage` answers; miss and the action is denied | [The event model](/wiki/events) |
| `on_slow` | at most once a second | Budget warnings to the script | [Limits](/wiki/limits) |
| Slow-pack log | at most once every 5 s | Server log lines about budget | [Limits](/wiki/limits) |
| Zone re-trigger | 0.5 s | A route trigger block, after a trip | [Rooms and dimensions](/wiki/rooms-and-dimensions) |
| Store facts | 1 MiB each, keys 256 B | `stores` values | [Shared stores](/wiki/shared-stores) |
| Store blobs | 32 MiB each, 1,000 per player | `stores` blobs | [Shared stores](/wiki/shared-stores) |
| Hosted storage | 512 MiB + 1 MiB per Java player ever joined | Per experience | [Shared stores](/wiki/shared-stores) |
| Pending store requests | 32 per pack | Concurrent yielding store calls | [Shared stores](/wiki/shared-stores) |
| Lease tokens | 100,000 issued; leases last up to 1 hour | `stores.lease` | [Shared stores](/wiki/shared-stores) |
| Build size | 4,096 16-block cubes (32 MB) in a 256-million-block box | One `world.build` | [Building](/wiki/building) |
| `max_health` | 1 to 1024 | `player.max_health` writes | [Health](/wiki/health) |
| Player name to `player:connect` | 1 to 128 chars | Server addresses | [Player lifecycle](/wiki/player-lifecycle) |
| Camera moves | 20 per second | Camera positioning | [Movement](/wiki/movement) |
| Client versions | 1.8 to 26.x join every server | Java clients | [Client versions](/appendix/client-versions) |

## See also

- [Limits](/wiki/limits) — the budget system in depth.
- [FAQ](/appendix/faq) — when a limit is why.
"""
    return content

for slug, body in [("event-catalog", gen_event_catalog()),
                   ("limits-table", gen_limits_table())]:
    fm, _ = parse_page.__wrapped__ if False else (None, None)
    # manual frontmatter split since content is known
    m = FM_RE.match(body)
    fmraw = m.group(1)
    fm = {}
    for line in fmraw.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip().strip('"') for x in v[1:-1].split(",") if x.strip()]
            fm[k.strip()] = v
    content = body[m.end():].lstrip("\n")
    wiki_pages[slug] = {
        "type": "wiki", "slug": slug, "section": "appendix",
        "title": fm["title"], "description": fm["description"],
        "tags": fm["tags"], "markdown": content, "toc": build_toc(content),
    }

# ---------------------------------------------------------------- redirects
DOC_TO_WIKI = {
    "your-first-pack": "quick-start",
    "api-basics": "conventions",
    "packs": "pack-anatomy",
    "modules-and-tasks": "runtime",
    "limits-and-reload": "limits",
    "game-events": "events",
    "cancelling-events": "events",
    "rooms": "rooms-and-dimensions",
    "dimensions": "rooms-and-dimensions",
    "a-world-per-player": "rooms-and-dimensions",
    "blocks-and-terrain": "terrain-generation",
    "building-well": "building",
    "named-parts": "building",
    "custom-blocks": "custom-blocks",
    "game-data": "game-data",
    "custom-entities": "custom-entities",
    "mobs-and-drops": "mobs",
    "npcs": "npcs",
    "players": "player-lifecycle",
    "body-and-movement": "movement",
    "cameras": "movement",
    "input": "movement",
    "items": "inventory",
    "armour": "inventory",
    "permissions": "permissions",
    "hud": "ui-basics",
    "titles-and-bars": "ui-basics",
    "text-formatting": "ui-basics",
    "screens": "screens",
    "layouts": "screens",
    "canvases": "canvases",
    "map-pictures": "canvases",
    "menus": "menus",
    "hotbar-menus": "menus",
    "dialogs": "dialogs",
    "displays": "displays",
    "3d-models": "displays",
    "particles-and-lasers": "fx",
    "sound": "sound",
    "commands": "commands",
    "storage": "storage",
    "shared-stores": "shared-stores",
    "network": "network",
    "http": "http",
    "shop": "shop",
    "hub": "hub",
    "server-settings": "server-settings",
    "client-versions": "client-versions",
    "version-info": "tooling",
    "scoreboard-with-a-button": "guide-scoreboard-with-a-button",
    "room-rules": "world-state",
    "time-and-tweens": "world-state",
    "vectors-and-colours": "conventions",
    "lighting": "displays",
    "zones-and-raycasts": "spatial-queries",
    "reference": "",
}

redirects = {}
for slug, target in DOC_TO_WIKI.items():
    redirects[f"/docs/citadel/{slug}"] = f"#/wiki/{target}" if target else "#/ref"
GUIDE_REDIRECTS = {
    "your-first-pack": "#/wiki/quick-start",
}
for g in DATASET["guides"]:
    redirects[f"/docs/citadel/guides/{g}"] = GUIDE_REDIRECTS.get(g, f"#/wiki/guide-{g}")
# reference URLs keep their shape but move to /ref
redirects["/docs/citadel/reference"] = "#/ref"

# ---------------------------------------------------------------- reference
REF_DOMAINS = [
    ("world", "World & game", ["world", "game", "models", "parts", "routes", "noise", "fields", "data"]),
    ("players", "Players", ["players", "camera"]),
    ("interface", "Interface & media", ["ui", "fx", "sound", "message", "tween", "color", "colors"]),
    ("systems", "Systems", ["commands", "time", "task", "rooms", "storage", "stores", "http", "network", "shop", "hub"]),
    ("engine", "Engine", ["citadel", "vec3"]),
]
# enriched module leads (hand-written; fall back to dataset lead)
MODULE_LEADS = {
    "world": "A room's blocks, entities, displays, screens and time — the `world` global, or `room.world`. Start here for terrain, block writes, entities in the world, and world rules.",
    "players": "Everyone in the room: joins and leaves, clicks and chat, inventory, visibility and health — the `players` global, or `room.players`.",
    "ui": "What the players see: titles, chat lines, sidebars, boss bars, screens, menus and dialogs — the `ui` global, or `room.ui`.",
    "game": "The game version's own facts — blocks, items, entity kinds, terrain — and the pack's definitions of its own blocks and entities.",
    "commands": "`commands.add` with typed arguments, tab-completion, permissions and aliases.",
    "time": "Clocks for a pack: a callback every tick, one every few seconds, and the seconds since the pack started.",
    "task": "The scheduler: `spawn`, `delay`, `defer`, `wait` and `cancel`.",
    "storage": "A per-pack JSON file that survives a restart.",
    "stores": "The experience's shared store: versioned facts, blobs and leases across every server.",
    "http": "HTTP requests from the pack, with caching.",
    "network": "WebSockets out and listening sockets, for multiplayer-scale IO.",
    "shop": "Minefort's Gem shop: prompts, ownership and paid delivery.",
    "hub": "The Minefort hub: servers, experiences and portals.",
    "rooms": "Making and destroying rooms — isolated worlds with their own tables.",
    "fx": "Particles: `fx.particle` with count, spread, velocity and dust colour.",
    "sound": "Sound by name from the resource pack, or streamed through Simple Voice Chat.",
    "message": "A chat line to everyone in the main room.",
    "tween": "Any live field eased over time — numbers, vec3 and color values.",
    "camera": "Camera paths and modes per player.",
    "color": "Colour helpers: hsv, gradients and nearest-map-colour.",
    "colors": "The named colour table: Minecraft's sixteen and more.",
    "noise": "Smooth random numbers for a generator, made by the engine.",
    "models": "The models this pack makes, for `world.display{ kind = \"model\" }`.",
    "parts": "Named parts of a stored world and the generators that build them.",
    "routes": "How players get between the worlds of the group.",
    "data": "Helpers for persistent data views — `data.copy`, `data.insert`, `data.remove`.",
    "fields": "Recipes for numbers over the world, for `world.generate`.",
    "citadel": "The engine itself: the log, versions, environment and the tick budget.",
    "vec3": "Positions and directions with `x`, `y`, `z` — plus `lerp`, `distance` and friends.",
    "task": "The scheduler: `spawn`, `delay`, `defer`, `wait` and `cancel`.",
}

# canonical type for each global
GLOBAL_TYPE = {}
all_globals = [g for _, _, gs in REF_DOMAINS for g in gs]
for t in DATASET["reference_parents"]:
    if t[0].islower():
        GLOBAL_TYPE[t] = t  # lowercase global pages exist as their own refs
# map lowercase -> PascalCase type where both exist
for low in list(GLOBAL_TYPE):
    for casing in (low.capitalize(), low.upper(), low):
        if casing in DATASET["reference_parents"] and casing != low:
            GLOBAL_TYPE[low] = casing
            break

def redirect_href(href):
    """Map an original docs URL into a new wiki/ref route."""
    if not href or not href.startswith("/docs/citadel"):
        return None
    rest = href[len("/docs/citadel"):].strip("/")
    if not rest:
        return "#/"
    parts = rest.split("/")
    if parts[0] == "guides" and len(parts) > 1:
        return redirects.get(f"/docs/citadel/guides/{parts[1]}")
    if parts[0] == "reference":
        if len(parts) == 1:
            return "#/ref"
        if len(parts) == 2:
            return f"#/ref/{parts[1]}"
        return f"#/ref/{parts[1]}/{parts[2]}"
    return redirects.get(f"/docs/citadel/{parts[0]}")

# build ref pages (type pages + member pages)
ref_pages = {}
search_entries = []

def members_sig(pdata):
    return json.dumps([
        pdata.get("lead", ""), pdata.get("typedef", ""),
        [(m["name"], m.get("section"), m.get("signature"))
         for m in pdata.get("members", [])],
    ], sort_keys=True)

# Detect lowercase globals whose PascalCase twin is an identical page:
# emit only the PascalCase page; the loader's case-insensitive fallback maps
# /ref/world -> World. Genuinely different pairs keep both pages.
drop_lower = set()
for name in list(DATASET["reference_parents"]):
    if name[0].islower():
        for cand in (name.capitalize(), name[:1].upper() + name[1:]):
            twin = DATASET["reference_parents"].get(cand)
            if twin and members_sig(twin) == members_sig(DATASET["reference_parents"][name]):
                drop_lower.add(name)
                break

for name, pdata in DATASET["reference_parents"].items():
    if name in drop_lower:
        continue
    is_global = name[0].islower()
    assoc = GLOBAL_TYPE.get(name, name) if is_global else name
    members = pdata.get("members", [])
    funcs = [m for m in members if m.get("section") == "functions"]
    fields = [m for m in members if m.get("section") == "fields"]
    others = [m for m in members if m.get("section") not in ("functions", "fields")]
    for m in members:
        m["href2"] = redirect_href(m.get("href", ""))
    lead = MODULE_LEADS.get(name, "") if is_global else ""
    if not lead:
        lead = pdata.get("lead", "")
    dl = pdata.get("docs_link") or None
    ref_pages[name] = {
        "type": "ref", "name": name,
        "kind": "global" if is_global else "type",
        "assocType": assoc if is_global and assoc != name else "",
        "lead": lead,
        "typedef": pdata.get("typedef", ""),
        "docsLink": ({"title": dl["title"], "href": redirect_href(dl["href"])}
                     if dl else None),
        "functions": funcs, "fields": fields, "others": others,
        "title": pdata.get("title", name),
    }

for parent, mems in DATASET["reference_members"].items():
    for mname, m in mems.items():
        used = m.get("used_in", [])
        used2 = [{"quote": u.get("quote", ""), "source": u.get("source", ""),
                  "href": redirect_href(u.get("href", "")) or "#/ref"}
                 for u in used]
        ref_pages[f"{parent}.{mname}"] = {
            "type": "refmember", "parent": parent, "name": mname,
            "title": m.get("title", mname), "kind": m.get("kind", ""),
            "lead": m.get("lead", ""), "signature": m.get("signature", ""),
            "params": m.get("params", []), "returns": m.get("returns", []),
            "usedIn": used2[:6],
        }

# ---------------------------------------------------------------- write pages
nav_sections = []
for sec_id, sec_title in SECTIONS:
    pages = [p for p in wiki_pages.values() if p["section"] == sec_id]
    pages.sort(key=lambda p: p["slug"])
    order = {}
    secdir = f"{SRC}/{sec_id}"
    if os.path.isdir(secdir):
        for fname in os.listdir(secdir):
            if fname.endswith(".md"):
                fm, _ = parse_page(f"{secdir}/{fname}")
                order[fname[:-3]] = int(fm.get("order", 99))
    if sec_id == "appendix":
        order["event-catalog"] = 1; order["client-versions"] = 2
        order["faq"] = 3; order["limits-table"] = 4
    pages.sort(key=lambda p: order.get(p["slug"], 99))
    if not pages:
        continue
    nav_sections.append({
        "id": sec_id, "title": sec_title,
        "pages": [{"slug": p["slug"], "title": p["title"],
                   "description": p["description"]} for p in pages],
    })

# nav reference section: domains with globals + count of types
ref_nav = {"domains": [], "types": []}
lower_pages = [n for n in DATASET["reference_parents"] if n[0].islower()]
upper_pages = sorted([n for n in DATASET["reference_parents"] if n[0].isupper()])
for dom_id, dom_title, globals_ in REF_DOMAINS:
    types = [g for g in globals_ if g in DATASET["reference_parents"]]
    ref_nav["domains"].append({
        "id": dom_id, "title": dom_title,
        "globals": types,
    })
ref_nav["types"] = upper_pages

nav = {"sections": nav_sections, "reference": ref_nav}

# search index
for slug, p in wiki_pages.items():
    text = re.sub(r"```.*?```", " ", p["markdown"], flags=re.S)
    text = re.sub(r"[#*`>\|\-]", " ", text)
    search_entries.append({
        "t": "page", "title": p["title"], "section": p["section"],
        "route": f"#/wiki/{slug}", "text": (p["description"] + " " + text)[:400],
        "keywords": " ".join(p.get("tags", [])),
    })
for name, p in ref_pages.items():
    if p["type"] == "ref":
        text = p["lead"]
        for m in p["functions"] + p["fields"]:
            text += " " + m.get("signature", "") + " " + m.get("description", "")
        search_entries.append({
            "t": "ref", "title": name,
            "section": "API" if p["kind"] == "global" else "Type",
            "route": f"#/ref/{name}",
            "text": text[:400], "keywords": "",
        })
    else:
        text = p["lead"] + " " + p["signature"]
        for prm in p["params"]:
            text += " " + prm["name"]
        search_entries.append({
            "t": "refmember", "title": f"{p['parent']}.{p['name']}",
            "section": p["parent"],
            "route": f"#/ref/{p['parent']}/{p['name']}",
            "text": text[:400], "keywords": "",
        })

# write everything
count = {"wiki": 0, "ref": 0, "refmember": 0}
loaders = []
for slug, p in wiki_pages.items():
    with open(f"{DATA}/pages/wiki-{slug}.json", "w") as f:
        json.dump(p, f, ensure_ascii=False)
    loaders.append((f"wiki:{slug}", f"wiki-{slug}"))
    count["wiki"] += 1
for key, p in ref_pages.items():
    if p["type"] == "ref":
        # lowercase globals that share a name (mod case) with a kept type page
        # get a distinct filename to avoid TS casing collisions
        twin = key.capitalize() if len(key) > 1 else key.upper()
        has_twin = twin in ref_pages and twin != key
        fn = f"ref-g-{key}" if (p["kind"] == "global" and has_twin) else f"ref-{key}"
        with open(f"{DATA}/pages/{fn}.json", "w") as f:
            json.dump(p, f, ensure_ascii=False)
        loaders.append((key, fn))
        count["ref"] += 1
    else:
        fn = f"refm-{p['parent']}-{p['name']}"
        # sanitize filename
        fn = re.sub(r"[^A-Za-z0-9_.-]", "_", fn)
        with open(f"{DATA}/pages/{fn}.json", "w") as f:
            json.dump(p, f, ensure_ascii=False)
        loaders.append((f"{p['parent']}.{p['name']}", fn))
        count["refmember"] += 1

with open(f"{DATA}/nav.json", "w") as f:
    json.dump(nav, f, ensure_ascii=False, indent=1)
with open(f"{DATA}/redirects.json", "w") as f:
    json.dump(redirects, f, ensure_ascii=False, indent=1)
with open(f"{DATA}/search.json", "w") as f:
    json.dump(search_entries, f, ensure_ascii=False)

# generated loaders
lines = [
    "// AUTO-GENERATED by scripts/build_wiki.py — do not edit.",
    "",
    "export interface PageLoader { key: string; load: () => Promise<unknown> }",
    "",
    "export const pageLoaders: PageLoader[] = [",
]
for key, fn in loaders:
    lines.append(f'  {{ key: {json.dumps(key)}, load: () => import("./pages/{fn}.json") }},')
lines.append("];")
lines.append("")
with open(f"{DATA}/page-loaders.generated.ts", "w") as f:
    f.write("\n".join(lines))

print(f"wiki pages: {count['wiki']}")
print(f"ref pages:  {count['ref']}")
print(f"members:    {count['refmember']}")
print(f"search:     {len(search_entries)} entries")
print(f"nav:        {len(nav_sections)} sections")
