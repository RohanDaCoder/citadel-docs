#!/usr/bin/env python3
"""Sweep the built dist/ output: every internal link in every HTML page
(excluding redirect stubs under /docs/) must resolve to a real file.
Also verifies anchor targets exist in the linked page."""
import os
import re
import sys
from html.parser import HTMLParser

DIST = "/home/z/my-project/dist"

href_re = re.compile(r'href="(/[^"#]*)(#[^"]*)?"')


def github_slug(text):
    text = re.sub(r"[*`]", "", text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_]+", "-", text).strip("-")


class HeadingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.headings = set()
        self._in_heading = None

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k == "id" and v:
                self.ids.add(v)
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._in_heading = tag

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._in_heading = None

    def handle_data(self, data):
        if self._in_heading:
            self.headings.add(github_slug(data.strip()))


def resolve(route):
    """Map a URL path to a dist file."""
    route = route.split("?")[0]
    rel = route.lstrip("/")
    if not rel:
        return os.path.join(DIST, "index.html")
    if os.path.isfile(f"{DIST}/{rel}"):
        return f"{DIST}/{rel}"
    if os.path.isfile(f"{DIST}/{rel}/index.html"):
        return f"{DIST}/{rel}/index.html"
    if os.path.isfile(f"{DIST}/{rel}.html"):
        return f"{DIST}/{rel}.html"
    return None


pages = []
for root, _, files in os.walk(DIST):
    for fn in files:
        if fn.endswith(".html"):
            pages.append(os.path.join(root, fn))

errors = []
anchor_misses = []
checked = 0
anchor_cache = {}

for page in pages:
    rel = os.path.relpath(page, DIST)
    if rel.startswith("docs/"):  # redirect stubs
        continue
    html = open(page, encoding="utf-8").read()
    for m in href_re.finditer(html):
        route, anchor = m.group(1), m.group(2)
        if not route.startswith("/"):
            continue
        checked += 1
        target = resolve(route)
        if target is None:
            errors.append(f"{rel}: {route}")
            continue
        if anchor:
            a = anchor[1:]
            if target not in anchor_cache:
                p = HeadingParser()
                try:
                    p.feed(open(target, encoding="utf-8").read())
                except Exception:
                    p.ids = None
                anchor_cache[target] = p.ids | p.headings if p.ids else set()
            if anchor_cache[target] and a not in anchor_cache[target]:
                anchor_misses.append(f"{rel}: {route}{anchor}")

print(f"pages swept:      {len(pages)}")
print(f"links checked:    {checked}")
print(f"broken links:     {len(errors)}")
for e in errors[:30]:
    print("  ERROR", e)
print(f"anchor misses:    {len(anchor_misses)}")
for a in anchor_misses[:30]:
    print("  anchor", a)

sys.exit(1 if errors else 0)
