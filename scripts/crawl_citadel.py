#!/usr/bin/env python3
"""crawl_citadel.py — download every discovered Citadel docs page to disk.

Reads the URL list written by discover_all.py and saves each page's SSR HTML
to scripts/crawl_html/<flattened>.html, together with a manifest.json that
maps url -> filename (the pages carry no canonical/og:url tag, so the
manifest is the extractor's source of truth for a file's URL).

  url -> filename:  /docs/citadel                     -> index.html
                    /docs/citadel/packs                -> packs.html
                    /docs/citadel/reference/World      -> reference_World.html
                    /docs/citadel/reference/World/set_block
                                                       -> reference_World_set_block.html
  ('__' is the path separator; no page name contains '__')

  * resume: existing non-empty files are skipped (re-run after an interrupt)
  * polite: 0.25 s between requests, full browser UA (Cloudflare rejects
    short UAs with a "Just a moment..." challenge page), 3 retries with
    back-off; challenge pages are detected and never written to disk.

Usage:
  python3 scripts/crawl_citadel.py            # crawl everything in urls.txt
  python3 scripts/crawl_citadel.py --force    # re-download even if present
  python3 scripts/crawl_citadel.py --dir D --urls U   # custom locations
"""
import argparse
import json
import os
import subprocess
import sys
import time

BASE = "https://minefort.com"
OUT_DIR = "/home/z/my-project/scripts/crawl_html"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def flatten(url: str) -> str:
    rest = url[len("/docs/citadel"):].strip("/")
    return (rest.replace("/", "__") or "index") + ".html"


def fetch(url: str, retries: int = 3) -> str | None:
    for attempt in range(retries):
        try:
            out = subprocess.run(
                ["curl", "-sS", "-L", "-A", UA,
                 "-H", "Accept: text/html,application/xhtml+xml",
                 "--max-time", "30", "-w", "\n%{http_code}", BASE + url],
                capture_output=True, text=True, timeout=60)
            if out.returncode != 0:
                raise RuntimeError(f"curl exit {out.returncode}")
            html, _, code = out.stdout.rpartition("\n")
            if code.strip() == "200" and "Just a moment" not in html[:400] \
               and html.lstrip().startswith("<!DOCTYPE"):
                return html
            raise RuntimeError(f"HTTP {code.strip()} / challenge page")
        except Exception as e:
            wait = 5 * (attempt + 1)
            print(f"  {url}: {e}; retry in {wait}s", file=sys.stderr)
            time.sleep(wait)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="re-download files that already exist")
    ap.add_argument("--dir", default=OUT_DIR,
                    help="output directory for .html files + manifest.json")
    ap.add_argument("--urls", default=None,
                    help="URL list (default: <dir>/urls.txt)")
    args = ap.parse_args()

    urls_file = args.urls or f"{args.dir}/urls.txt"
    urls = [u for u in open(urls_file).read().splitlines() if u.strip()]
    manifest_path = f"{args.dir}/manifest.json"
    manifest = {}
    if os.path.exists(manifest_path):
        manifest = json.load(open(manifest_path))

    ok, skipped, failed = 0, 0, []
    for i, url in enumerate(urls, 1):
        fname = flatten(url)
        target = f"{args.dir}/{fname}"
        if not args.force and os.path.exists(target) and \
           os.path.getsize(target) > 1000:
            skipped += 1
            manifest[url] = fname
            continue
        html = fetch(url)
        if html is None:
            failed.append(url)
            continue
        with open(target, "w") as f:
            f.write(html)
        manifest[url] = fname
        ok += 1
        if i % 25 == 0 or i == len(urls):
            print(f"  {i}/{len(urls)} fetched ({ok} new, {skipped} kept)")
        time.sleep(0.25)                      # be polite

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
    print(f"done: {ok} downloaded, {skipped} already present, "
          f"{len(failed)} failed")
    for u in failed:
        print("  FAILED:", u, file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
