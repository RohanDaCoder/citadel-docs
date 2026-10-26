#!/usr/bin/env python3
"""discover_all.py — discover every Citadel docs URL on minefort.com.

The docs are a Next.js app with server-side rendering: every page's HTML
contains the full sidebar/nav as plain <a href> links, so a BFS crawl over
the SSR HTML finds every page without any JS execution.

  start:  /docs/citadel          (landing)
  walk:   fetch page -> collect hrefs matching /docs/citadel/... -> queue new
  out:    scripts/crawl_html/urls.txt (one URL per line, sorted)

Site notes (observed 2025-10):
  * The reference index page lists all ~177 type/global parents; each parent
    page lists its member pages, so BFS reaches all ~900 pages in 2-3 levels.
  * The site links BOTH letter-case variants of some pages (world/World,
    camera/Camera, color/Color, ...).  The server is case-insensitive for the
    first group but serves genuinely different pages for the second group, so
    URLs are kept EXACTLY as linked - never case-normalised.
  * /docs/citadel/llms.txt and /docs/citadel/llms-full.txt are linked but 404;
    they are skipped here.

Usage:
  python3 scripts/discover_all.py            # full discovery (~900 pages)
  python3 scripts/discover_all.py --limit 5  # stop after N fetches (test)
"""
import argparse
import os
import re
import subprocess
import sys
import time
from collections import deque

BASE = "https://minefort.com"
START = "/docs/citadel"
OUT_DIR = "/home/z/my-project/scripts/crawl_html"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

# /docs/citadel followed by any number of path segments (letters, digits,
# _ - . ( ) ~).  Query strings, fragments and files like llms.txt are dropped.
URL_RE = re.compile(r"^/docs/citadel(/[A-Za-z0-9_().~-]+)*$")
SKIP_EXT = (".txt", ".luau", ".json", ".xml", ".png", ".svg")


def fetch(path: str, retries: int = 3) -> str:
    """Fetch a page with curl and a full browser UA (Cloudflare needs it)."""
    for attempt in range(retries):
        try:
            out = subprocess.run(
                ["curl", "-sS", "-L", "-A", UA,
                 "-H", "Accept: text/html,application/xhtml+xml",
                 "--max-time", "30", BASE + path],
                capture_output=True, text=True, timeout=60)
            html = out.stdout
            if out.returncode == 0 and "Just a moment" not in html[:400]:
                return html
        except subprocess.TimeoutExpired:
            pass
        # Cloudflare challenge or transient error: back off and retry
        wait = 5 * (attempt + 1)
        print(f"  retry {path} in {wait}s (attempt {attempt + 1})",
              file=sys.stderr)
        time.sleep(wait)
    raise RuntimeError(f"could not fetch {path} after {retries} tries")


def extract_links(html: str):
    """All /docs/citadel hrefs in the SSR HTML (bs4 keeps it dependency-light)."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].split("#")[0]
        if URL_RE.match(href) and not href.endswith(SKIP_EXT):
            seen.add(href)
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0,
                    help="stop after fetching this many pages (0 = all)")
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    visited = set()
    queue = deque([START])
    all_urls = set([START])

    while queue:
        path = queue.popleft()
        if path in visited:
            continue
        visited.add(path)
        links = extract_links(fetch(path))
        new = links - all_urls
        all_urls |= links
        queue.extend(sorted(new))
        print(f"{len(visited):4d} fetched  {path}  (+{len(new)} new, "
              f"{len(all_urls)} total so far)", file=sys.stderr)
        time.sleep(0.2)                       # be polite
        if args.limit and len(visited) >= args.limit:
            print(f"--limit {args.limit}: stopping early", file=sys.stderr)
            break

    urls = sorted(all_urls)
    with open(f"{OUT_DIR}/urls.txt", "w") as f:
        f.write("\n".join(urls) + "\n")

    # report by category
    cats = {"index": 0, "guides": 0, "docs": 0, "parents": 0, "members": 0}
    for u in urls:
        rest = u[len("/docs/citadel"):]
        if not rest or rest == "/":
            cats["index"] += 1
        elif rest.startswith("/guides/"):
            cats["guides"] += 1
        elif rest.startswith("/reference/"):
            segs = rest.split("/")[1:]
            if len(segs) == 2 and segs[1]:
                cats["members"] += 1
            else:
                cats["parents"] += 1
        else:
            cats["docs"] += 1
    print("\ndiscovered:", len(urls), "pages ->", f"{OUT_DIR}/urls.txt")
    for k, v in cats.items():
        print(f"  {k:8s} {v}")


if __name__ == "__main__":
    main()
