#!/usr/bin/env python3
"""Generate the Starlight (Astro) content tree from wiki_src/ + dataset.json.

Outputs:
  src/content/docs/                     - all markdown pages
    <section>/<slug>.md                 - wiki pages (10 sections)
    appendix/event-catalog.md           - generated appendix (all on_* events)
    appendix/limits-table.md            - generated appendix (all numeric limits)
    ref/<Name>/index.md                 - API reference: global/type pages
    ref/<Name>/<member>.md              - API reference: member pages
  scripts/generated/starlight-manifest.json
    .sidebar                            - full Starlight sidebar (wiki + reference)
    .redirects                          - original minefort docs URLs -> new routes

Run:  python3 scripts/gen_starlight.py     (then: npm run build)
"""
import json
import os
import re
import shutil
from collections import OrderedDict

ROOT = "/home/z/my-project"
SRC = f"{ROOT}/scripts/wiki_src"
OUT = f"{ROOT}/src/content/docs"
GEN = f"{ROOT}/scripts/generated"
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

REF_DOMAINS = [
    ("World & game", ["world", "game", "models", "parts", "routes", "noise", "fields", "data"]),
    ("Players", ["players", "camera"]),
    ("Interface & media", ["ui", "fx", "sound", "message", "tween", "color", "colors"]),
    ("Systems", ["commands", "time", "task", "rooms", "storage", "stores", "http", "network", "shop", "hub"]),
    ("Engine", ["citadel", "vec3"]),
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
}

# original doc slug -> wiki slug (from the corpus analysis; "" = reference index)
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


def yaml_str(value):
    """Single-quoted YAML scalar."""
    return "'" + str(value).replace("'", "''").replace("\n", " ").strip() + "'"


def frontmatter(pairs):
    lines = ["---"]
    for k, v in pairs:
        lines.append(f"{k}: {yaml_str(v)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


# ------------------------------------------------------- case-twin analysis
def members_sig(pdata):
    return json.dumps([
        pdata.get("lead", ""), pdata.get("typedef", ""),
        [(m["name"], m.get("section"), m.get("signature"))
         for m in pdata.get("members", [])],
    ], sort_keys=True)


PARENTS = DATASET["reference_parents"]
MEMBERS = DATASET["reference_members"]

# lowercase globals whose PascalCase twin is an identical page: emit only one
CANON = {}          # lowercase name -> canonical page name (kept)
for name in list(PARENTS):
    if name[0].islower():
        for cand in (name.capitalize(), name[:1].upper() + name[1:]):
            if cand in PARENTS and cand != name and \
                    members_sig(PARENTS[cand]) == members_sig(PARENTS[name]):
                CANON[name] = cand
                break

def canon(name):
    return CANON.get(name, name)

KEPT = [n for n in PARENTS if n not in CANON]          # pages we emit
KEPT_SET = set(KEPT)
MEMBER_PARENTS = {p: m for p, m in MEMBERS.items() if canon(p) == p}


# ------------------------------------------------------------- link targets
SLUG2SECTION = {}    # wiki slug -> section id
WIKI_TITLES = {}     # wiki slug -> title
for sec_id, _ in SECTIONS:
    secdir = f"{SRC}/{sec_id}"
    if not os.path.isdir(secdir):
        continue
    for fname in os.listdir(secdir):
        if fname.endswith(".md"):
            slug = fname[:-3]
            SLUG2SECTION[slug] = sec_id
            fm, _ = parse_page(f"{secdir}/{fname}")
            WIKI_TITLES[slug] = fm.get("title", slug)
for extra in ("event-catalog", "limits-table"):        # generated appendix pages
    SLUG2SECTION[extra] = "appendix"


def wiki_route(slug):
    if slug in SLUG2SECTION:
        return f"/{SLUG2SECTION[slug]}/{slug}/"
    return None


def ref_route(parent, member=None):
    p = canon(parent)
    if p not in KEPT_SET:
        return None
    if member is None:
        return f"/ref/{p}/"
    if p in MEMBER_PARENTS and member in MEMBER_PARENTS[p]:
        return f"/ref/{p}/{member}/"
    return None


def original_url_to_route(href):
    """Map an original minefort docs URL to a new Starlight route."""
    if not href or not href.startswith("/docs/citadel"):
        return None
    rest = href[len("/docs/citadel"):].strip("/")
    if not rest:
        return "/"
    parts = rest.split("/")
    if parts[0] == "guides" and len(parts) > 1:
        g = parts[1]
        return wiki_route("quick-start" if g == "your-first-pack" else f"guide-{g}")
    if parts[0] == "reference":
        if len(parts) == 1:
            return "/ref/"
        if len(parts) == 2:
            return ref_route(parts[1])
        return ref_route(parts[1], parts[2])
    if parts[0] in DOC_TO_WIKI:
        w = DOC_TO_WIKI[parts[0]]
        return "/ref/" if w == "" else wiki_route(w)
    return None


# --------------------------------------------------------- body conversion
WIKI_LINK_RE = re.compile(r"\]\((/wiki/([^)#/]+?)(#[^)]*)?)\)")
APP_LINK_RE = re.compile(r"\]\((/appendix/([^)#/]+?)(#[^)]*)?)\)")
REF_LINK_RE = re.compile(r"\]\((/ref/([^)#/]+)(?:/([^)#/]+))?(#[^)]*)?)\)")

WARNINGS = []


def rewrite_links(body, ctx):
    def wiki_sub(m):
        slug, anchor = m.group(2), m.group(3) or ""
        route = wiki_route(slug)
        if route is None:
            WARNINGS.append(f"{ctx}: /wiki/{slug} has no target page")
            return m.group(0)
        return f"]({route}{anchor})"

    def app_sub(m):
        slug, anchor = m.group(2), m.group(3) or ""
        route = wiki_route(slug) if SLUG2SECTION.get(slug) == "appendix" else None
        if route is None:
            WARNINGS.append(f"{ctx}: /appendix/{slug} has no target page")
            return m.group(0)
        return f"]({route}{anchor})"

    def ref_sub(m):
        parent, member, anchor = m.group(2), m.group(3), m.group(4) or ""
        route = ref_route(parent, member)
        if route is None:
            WARNINGS.append(f"{ctx}: /ref/{parent}/{member or ''} has no target page")
            return m.group(0)
        return f"]({route}{anchor})"

    body = WIKI_LINK_RE.sub(wiki_sub, body)
    body = APP_LINK_RE.sub(app_sub, body)
    body = REF_LINK_RE.sub(ref_sub, body)
    body = body.replace("](/ref)", "](/ref/)")
    return body


CALLOUT_TYPES = {"In short": "note", "Note": "note", "Tip": "tip",
                 "Gotcha": "caution", "Warning": "danger"}
CALLOUT_RE = re.compile(r"^> \*\*(In short|Note|Gotcha|Tip|Warning):\*\*(.*)$")


def convert_callouts(body):
    """Convert `> **Type:** ...` blockquotes to Starlight ::: admonitions."""
    lines = body.split("\n")
    out = []
    i = 0
    while i < len(lines):
        m = CALLOUT_RE.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        ctype = CALLOUT_TYPES[m.group(1)]
        title = m.group(1) if m.group(1) in ("In short", "Gotcha") else None
        opener = f":::{ctype}" + (f"[{title}]" if title else "")
        block = [m.group(2).strip()]
        i += 1
        while i < len(lines) and lines[i].startswith(">"):
            block.append(re.sub(r"^> ?", "", lines[i]))
            i += 1
        # trim trailing blank lines inside the block
        while block and not block[-1].strip():
            block.pop()
        out.append(opener)
        out.extend(block)
        out.append(":::")
        if i < len(lines) and lines[i].strip():
            out.append("")
    return "\n".join(out)


def strip_h1(body, title):
    m = re.match(r"^# (.+)$", body, re.M)
    if m and m.group(1).strip() == title.strip():
        body = body[m.end():].lstrip("\n")
    return body


def convert_body(body, title, ctx):
    body = strip_h1(body, title)
    body = rewrite_links(body, ctx)
    body = convert_callouts(body)
    return body.strip() + "\n"


def esc_cell(text):
    """Escape pipes for use in a GFM table cell."""
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


# ================================================================ wiki pages
shutil.rmtree(OUT, ignore_errors=True)
shutil.rmtree(GEN, ignore_errors=True)
os.makedirs(OUT, exist_ok=True)
os.makedirs(GEN, exist_ok=True)

# root landing page (authored at wiki_src/index.md, links rewritten)
if os.path.isfile(f"{SRC}/index.md"):
    fm, body = parse_page(f"{SRC}/index.md")
    out_body = convert_body(body, fm.get("title", "Citadel Developer Wiki"), "wiki:index")
    with open(f"{OUT}/index.md", "w") as f:
        f.write(frontmatter([("title", fm.get("title", "Citadel Developer Wiki")),
                             ("description", fm.get("description", ""))]))
        f.write(out_body)

wiki_manifest = OrderedDict()   # (section) -> ordered [(slug, title)]
counts = {"wiki": 0, "appendix_gen": 0, "ref": 0, "refmember": 0}

for sec_id, _ in SECTIONS:
    secdir = f"{SRC}/{sec_id}"
    if not os.path.isdir(secdir):
        continue
    entries = []
    for fname in sorted(os.listdir(secdir)):
        if not fname.endswith(".md"):
            continue
        fm, body = parse_page(f"{secdir}/{fname}")
        slug = fname[:-3]
        entries.append((int(fm.get("order", 99)), slug, fm, body))
    entries.sort(key=lambda e: e[0])
    pages = []
    for order, slug, fm, body in entries:
        out_body = convert_body(body, fm.get("title", slug), f"wiki:{slug}")
        os.makedirs(f"{OUT}/{sec_id}", exist_ok=True)
        with open(f"{OUT}/{sec_id}/{slug}.md", "w") as f:
            f.write(frontmatter([
                ("title", fm.get("title", slug)),
                ("description", fm.get("description", "")),
            ]))
            f.write(out_body)
        pages.append({"slug": slug, "title": fm.get("title", slug)})
        counts["wiki"] += 1
    wiki_manifest[sec_id] = pages

# ====================================================== generated appendices
def gen_event_catalog():
    rows = []
    seen = set()
    for parent, mems in MEMBERS.items():
        for name, m in mems.items():
            if not name.startswith("on_"):
                continue
            key = f"{parent}.{name}"
            if key in seen:
                continue
            seen.add(key)
            lead = (m.get("lead", "") or "").strip()
            if not lead:
                p = PARENTS.get(parent)
                if p:
                    for mm in p.get("members", []):
                        if mm["name"] == name:
                            lead = mm.get("description", "")
                            break
            rows.append({"parent": canon(parent), "name": name,
                         "signature": m.get("signature", ""), "description": lead})
    rows.sort(key=lambda r: (r["parent"].lower(), r["name"]))
    lines = [
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
    byp = OrderedDict()
    for r in rows:
        byp.setdefault(r["parent"], []).append(r)
    for parent in sorted(byp, key=str.lower):
        lines.append(f"## `{parent}`")
        lines.append("")
        lines.append("| Event | Signature | Fires when |")
        lines.append("| --- | --- | --- |")
        for r in byp[parent]:
            desc = esc_cell(r["description"])
            if len(desc) > 160:
                desc = desc[:157] + "..."
            sig = esc_cell(r["signature"])
            lines.append(
                f"| [`{r['name']}`](/ref/{parent}/{r['name']}) | `{sig}` | {desc} |")
        lines.append("")
    lines += [
        "## See also",
        "",
        "- [The event model](/wiki/events) — subscriptions, asks, deadlines.",
        "- [Runtime](/wiki/runtime) — the event queue and its 4096 cap.",
        "",
    ]
    return ("\n".join(lines),
            "Every on_* event in the Citadel API in one table — what fires it, "
            "what the handler receives, and where the full treatment lives.")


def gen_limits_table():
    body = """# Limits

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
    return (body,
            "Every numeric limit in Citadel in one table — tick budgets, load "
            "times, event queues, stores, blobs, leases, builds and generation.")


GEN_APPENDIX = [
    ("event-catalog", "Event catalog", gen_event_catalog),
    ("limits-table", "Limits", gen_limits_table),
]
gen_pages = []
for slug, title, genfn in GEN_APPENDIX:
    body, desc = genfn()
    out_body = convert_body(body, title, f"appendix:{slug}")
    with open(f"{OUT}/appendix/{slug}.md", "w") as f:
        f.write(frontmatter([("title", title), ("description", desc)]))
        f.write(out_body)
    gen_pages.append({"slug": slug, "title": title})
    counts["appendix_gen"] += 1

# appendix section order: event-catalog, client-versions, faq, limits-table
app_pages = wiki_manifest["appendix"][:]
app_pages += [g for g in gen_pages]
app_pages.sort(key=lambda p: {"event-catalog": 1, "client-versions": 2,
                              "faq": 3, "limits-table": 4}.get(p["slug"], 9))
wiki_manifest["appendix"] = app_pages

# ============================================================== ref pages
def link_type(text):
    """Link a type name if it is exactly a kept reference parent."""
    t = (text or "").strip().rstrip("?").strip()
    if t in KEPT_SET:
        return f"[`{t}`]({ref_route(t)})"
    return f"`{text}`"


def linked_typedef(typedef):
    """Render a union typedef with each alternative linked when known."""
    parts = [p.strip() for p in typedef.split("|")]
    rendered = []
    for p in parts:
        p_clean = p.rstrip("?").strip()
        if p_clean in KEPT_SET:
            rendered.append(f"[`{p}`]({ref_route(p_clean)})")
        else:
            rendered.append(f"`{p}`")
    return " | ".join(rendered)


def member_exists(parent, member):
    return parent in MEMBER_PARENTS and member in MEMBER_PARENTS[parent]


for name in sorted(KEPT, key=str.lower):
    pdata = PARENTS[name]
    is_global = name[0].islower()
    label = name
    if not is_global:
        # if this PascalCase page is the canonical twin of a lowercase global,
        # present it under the global's lowercase name
        for low, can in CANON.items():
            if can == name:
                label = low
                break
    lead = MODULE_LEADS.get(name, "") if is_global else ""
    if not lead:
        lead = pdata.get("lead", "") or ""
    lead = lead.strip()

    lines = []
    if lead:
        lines.append(lead)
        lines.append("")

    typedef = (pdata.get("typedef") or "").strip()
    if typedef:
        lines.append(linked_typedef(typedef))
        lines.append("")

    dl = pdata.get("docs_link")
    if dl:
        target = original_url_to_route(dl.get("href", ""))
        if target and target != "/ref/":
            target_slug = target.rstrip("/").split("/")[-1]
            target_title = WIKI_TITLES.get(target_slug, dl.get("title", "docs"))
            lines.append(f"Part of the [{target_title}]({target}) article.")
            lines.append("")

    members = pdata.get("members", [])
    funcs = [m for m in members if m.get("section") == "functions"]
    fields = [m for m in members if m.get("section") == "fields"]
    others = [m for m in members if m.get("section") not in ("functions", "fields")]

    def member_table(mem_list, call_header):
        out = [f"| {call_header} | Purpose |", "| --- | --- |"]
        for m in mem_list:
            sig = m.get("signature", m["name"])
            # shorten function signatures to the call name for the index table
            call = m["name"] if m.get("section") == "functions" else sig
            if member_exists(name, m["name"]):
                cell = f"[`{esc_cell(call)}`]({ref_route(name, m['name'])})"
            else:
                cell = f"`{esc_cell(call)}`"
            out.append(f"| {cell} | {esc_cell(m.get('description', ''))} |")
        return out

    if funcs:
        lines.append("## Functions")
        lines.append("")
        lines.extend(member_table(funcs, "Call"))
        lines.append("")
    if fields:
        lines.append("## Fields")
        lines.append("")
        lines.extend(member_table(fields, "Field"))
        lines.append("")
    if others:
        lines.append("## Members")
        lines.append("")
        lines.extend(member_table(others, "Member"))
        lines.append("")

    if not members and not typedef and not lead:
        lines.append(f"`{name}` — see the members of this type.")

    body = rewrite_links("\n".join(lines).strip() + "\n", f"ref:{name}")
    desc = re.sub(r"[`*]", "", lead.split(". ")[0])[:200] if lead else \
        f"{name} reference — every call, field and type in one place."
    os.makedirs(f"{OUT}/ref/{name}", exist_ok=True)
    with open(f"{OUT}/ref/{name}/index.md", "w") as f:
        f.write(frontmatter([("title", pdata.get("title", name)),
                             ("description", desc)]))
        f.write(body)
    counts["ref"] += 1

# member pages
for parent in sorted(MEMBER_PARENTS, key=str.lower):
    for mname in sorted(MEMBER_PARENTS[parent]):
        m = MEMBER_PARENTS[parent][mname]
        lead = (m.get("lead", "") or "").strip()
        sig = (m.get("signature", "") or "").strip()
        kind = m.get("kind", "")
        lines = []

        display_parent = m.get("title", mname).split(".")[0] if "." in m.get("title", "") else parent
        lines.append(f"Part of [`{display_parent}`]({ref_route(parent)}).")
        lines.append("")

        if sig:
            lines.append("```luau")
            lines.append(sig)
            lines.append("```")
            lines.append("")

        if lead:
            lines.append(rewrite_links(lead, f"refmember:{parent}.{mname}"))
            lines.append("")

        params = m.get("params", [])
        if params:
            lines.append("## Parameters")
            lines.append("")
            lines.append("| Name | Type | Required |")
            lines.append("| --- | --- | --- |")
            for p in params:
                req = "yes" if p.get("required") else "no"
                lines.append(f"| `{esc_cell(p.get('name', ''))}` | "
                             f"{esc_cell(link_type(p.get('type', '')))} | {req} |")
            lines.append("")

        returns = m.get("returns", [])
        if returns:
            lines.append("## Returns")
            lines.append("")
            for r in returns:
                lines.append(f"- {link_type(r)}")
            lines.append("")

        used = m.get("used_in", [])[:6]
        if used:
            lines.append("## Used in")
            lines.append("")
            for u in used:
                quote = (u.get("quote", "") or "").strip()
                source = (u.get("source", "") or "").strip()
                route = original_url_to_route(u.get("href", ""))
                if route:
                    src = f"[{source}]({route})"
                else:
                    src = source
                if quote and src:
                    lines.append(f'> "{esc_cell(quote)}" — {src}')
                elif src:
                    lines.append(f"- {src}")
            lines.append("")

        body = "\n".join(lines).strip() + "\n"
        first_sentence = re.sub(r"[`*]", "", lead.split(". ")[0])[:200] if lead else \
            f"{m.get('title', mname)} — {kind}."
        with open(f"{OUT}/ref/{parent}/{mname}.md", "w") as f:
            f.write(frontmatter([("title", m.get("title", mname)),
                                 ("description", first_sentence)]))
            f.write(body)
        counts["refmember"] += 1

# reference domain groups (used by /ref/ overview page and the sidebar)
ref_domain_groups = []
domain_links = set()
for dom_title, globals_ in REF_DOMAINS:
    items = []
    for g in globals_:
        c = canon(g)
        if c not in KEPT_SET:
            continue
        link = f"/ref/{c}/"
        domain_links.add(link)
        items.append({"label": g, "link": link})
    if items:
        ref_domain_groups.append({"label": dom_title, "collapsed": True,
                                  "items": items})

type_names = sorted([n for n in KEPT if n[0].isupper()
                     and f"/ref/{n}/" not in domain_links], key=str.lower)
type_items = [{"label": t, "link": f"/ref/{t}/"} for t in type_names]
ref_domain_groups.append({"label": "Types A–Z", "collapsed": True,
                          "items": type_items})

# reference overview page (/ref/)
ref_lines = [
    "Every global, type and call in Citadel, one page each: the signature,",
    "the parameters, the returns, and the guides that use it. Pick a domain,",
    "or browse the types.",
    "",
]
for dom_title, globals_ in REF_DOMAINS:
    items = [(g, canon(g)) for g in globals_ if canon(g) in KEPT_SET]
    if not items:
        continue
    ref_lines.append(f"## {dom_title}")
    ref_lines.append("")
    ref_lines.append("| Global | What it is |")
    ref_lines.append("| --- | --- |")
    for g, c in items:
        lead = MODULE_LEADS.get(g, "") or PARENTS[c].get("lead", "") or PARENTS[g].get("lead", "")
        ref_lines.append(f"| [`{g}`](/ref/{c}/) | {esc_cell(lead)} |")
    ref_lines.append("")
ref_lines.append("## Types A–Z")
ref_lines.append("")
ref_lines.append(" · ".join(f"[`{t}`](/ref/{t}/)" for t in type_names))
ref_lines.append("")
ref_body = rewrite_links("\n".join(ref_lines).strip() + "\n", "ref:index")
with open(f"{OUT}/ref/index.md", "w") as f:
    f.write(frontmatter([
        ("title", "API reference"),
        ("description", "Every Citadel global, type and member — 29 globals in "
                        "five domains, 141 types, 674 documented members, each "
                        "with signature, parameters, returns and usage."),
    ]))
    f.write(ref_body)

# ============================================================ manifest: sidebar
sidebar = []
for sec_id, sec_title in SECTIONS:
    pages = wiki_manifest.get(sec_id, [])
    if not pages:
        continue
    sidebar.append({
        "label": sec_title,
        "items": [{"label": p["title"], "link": f"/{sec_id}/{p['slug']}/"}
                  for p in pages],
    })

sidebar.append({"label": "API reference", "items": [
    {"label": "Overview", "link": "/ref/"},
    *ref_domain_groups,
]})

# ============================================================ manifest: redirects
redirects = {
    "/docs/citadel": "/",
    "/docs/citadel/reference": "/ref/",
}
for doc, wiki_slug in DOC_TO_WIKI.items():
    if wiki_slug == "":
        continue
    route = wiki_route(wiki_slug)
    if route:
        redirects[f"/docs/citadel/{doc}"] = route
for g in DATASET.get("guides", {}):
    route = wiki_route("quick-start" if g == "your-first-pack" else f"guide-{g}")
    if route:
        redirects[f"/docs/citadel/guides/{g}"] = route

# Original reference URLs: emit redirects for every parent page and member page.
# A lowercase global whose PascalCase sibling also has a page (world/World,
# camera/Camera, ...) redirects only from the PascalCase URL — Astro's router
# treats case-variant redirect routes as collisions, and the PascalCase form
# is the canonical URL the original site linked with.
def has_pascal_sibling(name):
    return name[0].islower() and name.capitalize() in PARENTS and name.capitalize() != name

for name in PARENTS:
    if has_pascal_sibling(name):
        continue
    route = ref_route(name)
    if route:
        redirects[f"/docs/citadel/reference/{name}"] = route
for parent, mems in MEMBERS.items():
    if has_pascal_sibling(parent):
        continue
    for mname in mems:
        route = ref_route(parent, mname)
        if route:
            redirects[f"/docs/citadel/reference/{parent}/{mname}"] = route

with open(f"{GEN}/starlight-manifest.json", "w") as f:
    json.dump({"sidebar": sidebar, "redirects": redirects}, f, indent=1)

# ================================================================= validation
SLUGGER_STRIP = re.compile(r"[^\w\s-]", re.U)


def github_slug(text):
    """Match github-slugger: strip punctuation, each space/underscore -> one hyphen."""
    text = re.sub(r"[*`]", "", text).strip().lower()
    text = SLUGGER_STRIP.sub("", text)
    return re.sub(r"[\s_]", "-", text).strip("-")


def page_headings(path):
    heads = set()
    in_code = False
    for line in open(path):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            heads.add(github_slug(m.group(2)))
    return heads


md_files = []
for root, _, files in os.walk(OUT):
    for fn in files:
        if fn.endswith(".md"):
            md_files.append(os.path.join(root, fn))

link_re = re.compile(r"\]\((/[^)#]*)(#[^)]*)?\)")
errors, anchor_warns, checked = [], [], 0
cache = {}


def resolve(route):
    route = route.rstrip("/") or "/"
    rel = route.lstrip("/")
    if not rel:
        return f"{OUT}/index.md"
    if os.path.isfile(f"{OUT}/{rel}.md"):
        return f"{OUT}/{rel}.md"
    if os.path.isfile(f"{OUT}/{rel}/index.md"):
        return f"{OUT}/{rel}/index.md"
    return None


for path in md_files:
    content = open(path).read()
    # strip code fences so links inside code are not checked
    content_nf = re.sub(r"```.*?```", "", content, flags=re.S)
    for m in link_re.finditer(content_nf):
        route, anchor = m.group(1), m.group(2)
        checked += 1
        target = resolve(route)
        if target is None:
            errors.append(f"{path.replace(OUT, '')}: {route}")
            continue
        if anchor:
            a = anchor[1:]
            if target not in cache:
                cache[target] = page_headings(target)
            if a and a not in cache[target]:
                anchor_warns.append(f"{path.replace(OUT, '')}: {route}{anchor}")

# ---------------------------------------------------------------- report
print(f"wiki pages:        {counts['wiki']}")
print(f"generated appendix:{counts['appendix_gen']}")
print(f"ref type pages:    {counts['ref']}")
print(f"ref member pages:  {counts['refmember']}")
print(f"total md files:    {len(md_files)} (+ index.md static)")
print(f"sidebar entries:   wiki groups={len(sidebar) - 1}, "
      f"ref groups={len(ref_domain_groups)}, types={len(type_items)}")
print(f"redirects:         {len(redirects)}")
print(f"links checked:     {checked}")
print(f"broken links:      {len(errors)}")
for e in errors[:20]:
    print("  ERROR", e)
print(f"anchor misses:     {len(anchor_warns)}")
for w in anchor_warns[:20]:
    print("  anchor", w)
print(f"conversion warnings: {len(WARNINGS)}")
for w in WARNINGS[:20]:
    print("  warn", w)

if errors:
    raise SystemExit("BROKEN LINKS — fix before building")
