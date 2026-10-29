#!/usr/bin/env python3
"""Check every internal link in wiki markdown + redirects actually resolves."""
import json, os, re, glob

ROOT = "/home/z/my-project"
DATA = f"{ROOT}/src/data"

pages = {}
for f in glob.glob(f"{DATA}/pages/wiki-*.json"):
    p = json.load(open(f))
    pages[p["slug"]] = p

ref_names = set()
member_keys = set()
for f in glob.glob(f"{DATA}/pages/ref-*.json") + glob.glob(f"{DATA}/pages/ref-g-*.json"):
    p = json.load(open(f))
    if p.get("type") == "ref":
        ref_names.add(p["name"])
for f in glob.glob(f"{DATA}/pages/refm-*.json"):
    p = json.load(open(f))
    if p.get("type") == "refmember":
        member_keys.add(f"{p['parent']}.{p['name']}")

# case-insensitive resolution maps
ref_lower = {n.lower(): n for n in ref_names}
member_lower = {k.lower(): k for k in member_keys}
slug_lower = {s.lower(): s for s in pages}

bad = []
counts = {"wiki": 0, "ref": 0, "refmember": 0, "anchor": 0, "external": 0}

def check_link(href, ctx):
    if href.startswith("http"):
        counts["external"] += 1
        return
    if href.startswith("#") and not href.startswith("#/"):
        counts["anchor"] += 1
        return
    if href.startswith("/appendix/"):
        href = "/wiki/" + href[len("/appendix/"):]
    if href == "/ref":
        counts["ref"] += 1
        return
    if href.startswith("/wiki/"):
        rest = href[len("/wiki/"):]
        slug, _, anchor = rest.partition("#")
        target = pages.get(slug) or pages.get(slug_lower.get(slug.lower(), ""))
        if target:
            counts["wiki"] += 1
            if anchor:
                ids = {t["id"] for t in target["toc"]}
                if anchor not in ids:
                    bad.append((ctx, href, f"anchor '#{anchor}' not a heading of {slug}"))
        else:
            bad.append((ctx, href, "no such wiki page"))
        return
    if href.startswith("/ref/"):
        parts = href[len("/ref/"):].split("/")
        name = parts[0]
        if len(parts) == 1:
            if name in ref_names or name in ref_lower:
                counts["ref"] += 1
            else:
                bad.append((ctx, href, "no such ref page"))
        else:
            key = f"{parts[0]}.{parts[1]}"
            if key in member_keys or key.lower() in member_lower:
                counts["refmember"] += 1
            else:
                bad.append((ctx, href, "no such member"))
        return
    bad.append((ctx, href, "unrecognized form"))

for slug, p in pages.items():
    body = p["markdown"]
    # strip code blocks
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    for m in re.finditer(r"\]\(([^)]+)\)", body):
        check_link(m.group(1), slug)

# also check redirects target existing pages
redirects = json.load(open(f"{DATA}/redirects.json"))
for src, dst in redirects.items():
    if dst.startswith("#/wiki/"):
        slug = dst[len("#/wiki/"):]
        if slug and slug not in pages and slug not in slug_lower:
            bad.append(("redirect", src, f"-> {dst} missing"))
    elif dst.startswith("#/ref"):
        pass

print(f"pages: {len(pages)}, refs: {len(ref_names)}, members: {len(member_keys)}")
print(f"link counts: {counts}")
print(f"BROKEN ({len(bad)}):")
for b in bad[:60]:
    print("  ", b)
