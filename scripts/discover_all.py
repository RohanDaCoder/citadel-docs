#!/usr/bin/env python3
"""Extract all links from cached HTML files, find missing pages, download them."""
import subprocess
import re
import os
import json
import time

BASE = "https://minefort.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
OUT_DIR = "/home/z/my-project/scripts/crawl_html"
os.makedirs(OUT_DIR, exist_ok=True)

def path_to_file(url_path):
    return os.path.join(OUT_DIR, url_path.strip("/").replace("/", "_") + ".html")

def extract_links(html):
    return sorted(set(re.findall(r'href="(/docs/citadel[^"#]*)"', html)))

# Step 1: gather all links from cached files
all_urls = set()
for fname in os.listdir(OUT_DIR):
    if not fname.endswith(".html"):
        continue
    with open(os.path.join(OUT_DIR, fname), "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    all_urls.update(extract_links(html))

print(f"Discovered {len(all_urls)} URLs from cache")

# Step 2: download missing ones
missing = [u for u in sorted(all_urls) if not os.path.exists(path_to_file(u)) or os.path.getsize(path_to_file(u)) < 5000]
print(f"Missing/empty: {len(missing)}")

for i, url_path in enumerate(missing):
    out_file = path_to_file(url_path)
    cmd = ["curl", "-sL", BASE + url_path, "-H", f"User-Agent: {UA}", "--compressed",
           "-o", out_file, "-w", "%{http_code}"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        status = r.stdout.strip()
        size = os.path.getsize(out_file) if os.path.exists(out_file) else 0
        print(f"[{status}] {url_path} ({size}b)")
        if status == "200" and size > 5000:
            with open(out_file, "r", encoding="utf-8", errors="ignore") as f:
                html = f.read()
            new_links = extract_links(html)
            before = len(all_urls)
            all_urls.update(new_links)
            if len(all_urls) > before:
                print(f"   +{len(all_urls)-before} new links discovered")
    except Exception as e:
        print(f"[ERR] {url_path}: {e}")
    time.sleep(0.2)

# Step 3: loop until stable (max 3 more passes)
for _ in range(3):
    new_missing = [u for u in sorted(all_urls) if not os.path.exists(path_to_file(u)) or os.path.getsize(path_to_file(u)) < 5000]
    if not new_missing:
        break
    print(f"\nSecond pass: {len(new_missing)} still missing")
    for url_path in new_missing:
        out_file = path_to_file(url_path)
        cmd = ["curl", "-sL", BASE + url_path, "-H", f"User-Agent: {UA}", "--compressed",
               "-o", out_file, "-w", "%{http_code}"]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            status = r.stdout.strip()
            print(f"[{status}] {url_path}")
            if status == "200":
                with open(out_file, "r", encoding="utf-8", errors="ignore") as f:
                    html = f.read()
                all_urls.update(extract_links(html))
        except Exception as e:
            print(f"[ERR] {url_path}: {e}")
        time.sleep(0.2)

with open("/home/z/my-project/scripts/all_urls.json", "w") as f:
    json.dump(sorted(all_urls), f, indent=2)
print(f"\nFinal: {len(all_urls)} URLs total")

# Categorize
guides = [u for u in all_urls if "/guides/" in u]
reference = [u for u in all_urls if "/reference/" in u]
docs = [u for u in all_urls if u not in guides and u not in reference and u != "/docs/citadel"]
print(f"Guide pages: {len(guides)}")
print(f"Reference pages: {len(reference)}")
print(f"Doc pages: {len(docs)}")
