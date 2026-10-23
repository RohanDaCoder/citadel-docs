#!/usr/bin/env python3
"""Crawl Minefort Citadel docs: discover all pages and save raw HTML."""
import subprocess
import re
import os
import json
import time

BASE = "https://minefort.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
OUT_DIR = "/home/z/my-project/scripts/crawl_html"
os.makedirs(OUT_DIR, exist_ok=True)

SEEDS = [
    "/docs/citadel",
    "/docs/citadel/guides",
    "/docs/citadel/packs",
    "/docs/citadel/blocks-and-terrain",
    "/docs/citadel/players",
    "/docs/citadel/titles-and-bars",
    "/docs/citadel/sound",
    "/docs/citadel/displays",
    "/docs/citadel/rooms",
    "/docs/citadel/storage",
    "/docs/citadel/your-first-pack",
    "/docs/citadel/reference",
]

def fetch(url_path):
    """Fetch a URL path, return (status, html)."""
    out_file = os.path.join(OUT_DIR, url_path.strip("/").replace("/", "_") + ".html")
    if os.path.exists(out_file) and os.path.getsize(out_file) > 5000:
        with open(out_file, "r", encoding="utf-8", errors="ignore") as f:
            return 200, f.read()
    cmd = [
        "curl", "-sL", BASE + url_path,
        "-H", f"User-Agent: {UA}",
        "--compressed",
        "-o", out_file,
        "-w", "%{http_code}",
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        status = r.stdout.strip()
        with open(out_file, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()
        return status, html
    except Exception as e:
        return 0, str(e)

def extract_links(html):
    """Extract all /docs/citadel links from html."""
    return sorted(set(re.findall(r'href="(/docs/citadel[^"#]*)"', html)))

def main():
    visited = set()
    queue = list(SEEDS)
    all_urls = set()
    status_log = {}

    while queue:
        path = queue.pop(0)
        if path in visited:
            continue
        visited.add(path)
        status, html = fetch(path)
        status_log[path] = status
        if status != "200" or len(html) < 2000:
            print(f"[{status}] SKIP {path} ({len(html)}b)")
            continue
        links = extract_links(html)
        new = [l for l in links if l not in visited and l not in queue]
        queue.extend(new)
        all_urls.add(path)
        all_urls.update(links)
        print(f"[{status}] OK {path} -> {len(new)} new links (total known: {len(all_urls)})")
        time.sleep(0.3)

    # Save discovered URL list
    with open("/home/z/my-project/scripts/all_urls.json", "w") as f:
        json.dump(sorted(all_urls), f, indent=2)
    print(f"\nTotal discovered URLs: {len(all_urls)}")
    print("Saved to all_urls.json")

if __name__ == "__main__":
    main()
