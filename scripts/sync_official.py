#!/usr/bin/env python3
"""sync_official.py — one-command sync of scripts/dataset.json from the LIVE
official Citadel reference pages, so every generated artifact (Starlight
pages, llms.txt / llms-full.txt, citadel-ts/types/citadel.d.ts) refreshes from
the official source with nothing hand-typed.

Flow (the site's own HTML is the only source; no guessing):
  1. self-heal scripts/crawl_html/manifest.json from scripts/all_urls.json
     (forward map url -> filename; the file naming never needed a manifest
      when it was written, but extract_final.py needs one today)
  2. fetch every reference PARENT page (or --sections network,Commands)
  3. extract_parent() each; diff against dataset.json:
       member list changed  -> fetch each ADDED member page and extract it
                               (extract_final.extract_member);
                               HEAD-check each REMOVED member URL and prune
                               it only on a definitive 404;
                               refresh the parent entry
       entry otherwise moved on (lead / typedef / signatures) -> refresh
  4. save fetched HTML into scripts/crawl_html/ (existing naming convention)
     and update the manifest; new URLs are appended to all_urls.json
  5. --doc-pages a,b refreshes dataset["docs"] prose pages and the
     wiki_src/_sources/doc-<slug>.md provenance copies
  6. write dataset.json with a _meta provenance block, then print a report

Usage:
  python3 scripts/sync_official.py                          # all parents
  python3 scripts/sync_official.py --sections network,Commands
  python3 scripts/sync_official.py --dry-run                 # report only
  python3 scripts/sync_official.py --doc-pages network,commands
  python3 scripts/sync_official.py --deep                    # also re-fetch
                                       # every member page (slow, thorough)
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crawl_citadel import fetch as fetch_html            # noqa: E402
from extract_final import extract_member, extract_parent, article_markdown \
    # noqa: E402

ROOT = "/home/z/my-project"
DS_PATH = f"{ROOT}/scripts/dataset.json"
URLS_PATH = f"{ROOT}/scripts/all_urls.json"
CRAWL_DIR = f"{ROOT}/scripts/crawl_html"
MANIFEST_PATH = f"{CRAWL_DIR}/manifest.json"
REMOVED_DIR = f"{CRAWL_DIR}/removed"
REF_PREFIX = "/docs/citadel/reference/"
REF_INDEX = "/docs/citadel/reference"       # lists every parent page


# ------------------------------------------------------------------ helpers
def fname_for(url: str) -> str:
    """/docs/citadel/reference/network/start -> docs_citadel_reference_network_start.html
    (the exact naming convention of the existing crawl_html/ files)."""
    rest = url[len("/docs/citadel"):].strip("/")
    return ("docs_citadel_" + rest.replace("/", "_") + ".html") \
        if rest else "docs_citadel.html"


def status(path: str, retries: int = 3):
    """(http_code, effective_url) after redirects; retries transient codes."""
    for attempt in range(retries):
        out = subprocess.run(
            ["curl", "-sS", "-L", "-o", "/dev/null", "-w",
             "%{http_code} %{url_effective}",
             "-A", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
             "--max-time", "30", "https://minefort.com" + path],
            capture_output=True, text=True, timeout=60)
        if out.returncode == 0:
            code, eff = out.stdout.strip().split(" ", 1)
            code = int(code)
            if code in (403, 429, 500, 502, 503, 504):   # transient
                time.sleep(5 * (attempt + 1))
                continue
            return code, eff
        time.sleep(5 * (attempt + 1))
    return -1, path


def parent_member_links(html: str, parent_url: str) -> set:
    """Member hrefs under this parent's own path (exact case)."""
    prefix = parent_url + "/"
    rest = parent_url[len(REF_PREFIX):]
    pat = re.compile(rf"^/docs/citadel/reference/{re.escape(rest)}/"
                     rf"([A-Za-z0-9_().~-]+)$")
    found = set()
    for m in re.finditer(r'href="(/docs/citadel/[^"#]+)"', html):
        href = m.group(1)
        mm = pat.match(href)
        if mm:
            found.add(mm.group(1))
    return found


# --------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sections", default="",
                    help="comma-separated parent names (default: all)")
    ap.add_argument("--doc-pages", default="",
                    help="comma-separated doc slugs to refresh in dataset "
                         "+ wiki_src/_sources")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--deep", action="store_true",
                    help="also re-fetch every member page of every section")
    args = ap.parse_args()

    ds = json.load(open(DS_PATH))
    parents = ds["reference_parents"]
    members = ds["reference_members"]
    all_urls = json.load(open(URLS_PATH))
    all_urls = set(all_urls)

    # -- 1. self-heal the crawl manifest (url -> filename forward map)
    # crawl_html/ is a local cache, not tracked in git (215 MB, regenerable
    # via the cookbook in PIPELINE.md); a fresh clone starts without it, so
    # make sure it exists before the manifest write / save_html below.
    os.makedirs(CRAWL_DIR, exist_ok=True)
    manifest = {}
    missing_files = []
    for u in all_urls:
        f = fname_for(u)
        if os.path.exists(f"{CRAWL_DIR}/{f}"):
            manifest[u] = f
        else:
            missing_files.append(u)
    print(f"manifest self-heal: {len(manifest)} url->file pairs, "
          f"{len(missing_files)} urls without a file")

    # -- 1b. parent discovery: diff the live reference index vs the dataset.
    # A NEW parent (a fresh type/global page) is fetched, staged, and added
    # to the scan so all of its member pages are extracted; a parent that the
    # index no longer links is pruned only when its own page answers 404.
    staged = {}
    report = {"parents_scanned": 0, "parents_added": [], "parents_gone": [],
              "parents_refreshed": [], "members_added": [],
              "members_pruned": [], "members_refetched": [],
              "doc_pages_refreshed": []}
    idx_html = fetch_html(REF_INDEX)
    new_parents, gone_parents = [], []
    if idx_html:
        live_p = set()
        for m in re.finditer(r'href="(/docs/citadel/reference/'
                             r'[A-Za-z0-9_().\-]+)"', idx_html):
            rest = m.group(1)[len(REF_PREFIX):]
            if rest and "/" not in rest:
                live_p.add(rest)
        new_parents = sorted(live_p - set(parents))
        gone_parents = sorted(set(parents) - live_p)
        for np in new_parents:
            npurl = f"{REF_PREFIX}{np}"
            nhtml = fetch_html(npurl)
            time.sleep(0.25)
            if nhtml is None:
                print(f"  ! new parent page unreachable: {npurl}",
                      file=sys.stderr)
                continue
            staged[np] = extract_parent_from_html(nhtml, npurl)
            report["parents_added"].append(np)
            all_urls.add(npurl)
            if not args.dry_run:
                save_html(npurl, nhtml)
                manifest[npurl] = fname_for(npurl)
            print(f"  + parent {np} (new; "
                  f"{len(staged[np].get('members', []))} member cards)")
        for gp in gone_parents:
            gpurl = parents[gp]["url"]
            code, eff = status(gpurl)
            if code == 404:
                report["parents_gone"].append(gp)
                all_urls.discard(gpurl)
                if not args.dry_run:
                    parents.pop(gp, None)
                    members.pop(gp, None)
                    for murl in list(manifest):
                        if murl.startswith(gpurl + "/"):
                            all_urls.discard(murl)
                            dead = f"{CRAWL_DIR}/{manifest[murl]}"
                            if os.path.exists(dead):
                                os.rename(dead, f"{REMOVED_DIR}/{manifest[murl]}")
                            manifest.pop(murl, None)
                    dead = f"{CRAWL_DIR}/{fname_for(gpurl)}"
                    os.makedirs(REMOVED_DIR, exist_ok=True)
                    if os.path.exists(dead):
                        os.rename(dead, f"{REMOVED_DIR}/{fname_for(gpurl)}")
                    manifest.pop(gpurl, None)
                print(f"  - parent {gp} (404: pruned with its members)")
            else:
                print(f"  ? parent {gp} missing from the index but answers "
                      f"{code} — kept", file=sys.stderr)
    else:
        print("  ! reference index unreachable — parent discovery skipped",
              file=sys.stderr)

    wanted = [s.strip() for s in args.sections.split(",") if s.strip()] \
        or sorted(parents, key=str.lower)
    wanted += [p for p in new_parents if p not in wanted]

    for pname in wanted:
        pdata = parents.get(pname) or staged.get(pname)
        if not pdata:
            print(f"  ? parent {pname!r} not in dataset — skipped",
                  file=sys.stderr)
            continue
        purl = pdata["url"]
        html = fetch_html(purl)
        if html is None:
            print(f"  ! could not fetch parent {purl} — skipped",
                  file=sys.stderr)
            continue
        report["parents_scanned"] += 1
        live = extract_parent_from_html(html, purl)
        live_members = parent_member_links(html, purl)
        ds_members = set(members.get(pname, {}))
        added = sorted(live_members - ds_members)
        removed = sorted(ds_members - live_members)
        changed = pname in staged or live != pdata or added or removed

        # additions: fetch + extract each new member page
        for m in added:
            murl = f"{purl}/{m}"
            mhtml = fetch_html(murl)
            time.sleep(0.25)
            if mhtml is None:
                print(f"  ! member page unreachable: {murl} — NOT added",
                      file=sys.stderr)
                continue
            if not args.dry_run:
                save_html(murl, mhtml)
                manifest[murl] = fname_for(murl)
            all_urls.add(murl)
            entry = extract_member_from_html(mhtml, murl)
            if not entry.get("signature") or not entry.get("kind"):
                print(f"  ! thin extraction for {murl}: "
                      f"sig={entry.get('signature')!r} "
                      f"kind={entry.get('kind')!r}", file=sys.stderr)
            members.setdefault(pname, {})[m] = entry
            report["members_added"].append(f"{pname}.{m}")
            if not args.dry_run:
                print(f"  + {pname}.{m}")

        # removals: prune only on a definitive 404
        for m in removed:
            murl = f"{purl}/{m}"
            code, eff = status(murl)
            if code == 404:
                members[pname].pop(m, None)
                report["members_pruned"].append(f"{pname}.{m}")
                all_urls.discard(murl)
                dead = f"{CRAWL_DIR}/{fname_for(murl)}"
                if not args.dry_run:
                    os.makedirs(REMOVED_DIR, exist_ok=True)
                    if os.path.exists(dead):
                        os.rename(dead, f"{REMOVED_DIR}/{fname_for(murl)}")
                    manifest.pop(murl, None)
                print(f"  - {pname}.{m}  (404: pruned)")
            else:
                print(f"  ? {pname}.{m} missing from parent page but "
                      f"URL answers {code} ({eff}) — NOT pruned",
                      file=sys.stderr)

        # parent entry refresh when anything moved
        if changed:
            if removed:               # parent card list: only surviving members
                live["members"] = [mm for mm in live["members"]
                                    if mm["name"] in members.get(pname, {})]
            report["parents_refreshed"].append(pname)
            if not args.dry_run:
                parents[pname] = live
                save_html(purl, html)
                manifest[purl] = fname_for(purl)
            print(f"  ~ parent refreshed: {pname} "
                  f"(+{len(added)} -{len(removed)},"
                  f"{' content' if live != pdata else ' members only'})")

        # deep mode: re-fetch every member page of this section
        if args.deep:
            for m in sorted(members.get(pname, {})):
                murl = f"{purl}/{m}"
                mhtml = fetch_html(murl)
                time.sleep(0.25)
                if mhtml is None:
                    continue
                entry = extract_member_from_html(mhtml, murl)
                if entry != members[pname][m]:
                    if not args.dry_run:
                        members[pname][m] = entry
                        save_html(murl, mhtml)
                    report["members_refetched"].append(f"{pname}.{m}")
        time.sleep(0.25)

    # -- doc pages refresh (prose pages: dataset["docs"] + _sources copies)
    for slug in [s.strip() for s in args.doc_pages.split(",") if s.strip()]:
        durl = f"/docs/citadel/{slug}"
        html = fetch_html(durl)
        if html is None:
            print(f"  ! doc page unreachable: {durl}", file=sys.stderr)
            continue
        article = html_to_article(html)
        title = article.find("h1").get_text().strip()
        md = article_markdown(article)
        report["doc_pages_refreshed"].append(slug)
        if not args.dry_run:
            ds["docs"][slug] = {"title": title, "markdown": md}
            src_path = f"{ROOT}/scripts/wiki_src/_sources/doc-{slug}.md"
            with open(src_path, "w") as f:
                f.write(f"# SOURCE: {title}\n\n{md}")
            save_html(durl, html)
            manifest[durl] = fname_for(durl)
        print(f"  ~ doc page refreshed: {slug} ({title})")

    # -- write everything back
    if args.dry_run:
        print("\n--dry-run: nothing written")
    else:
        for pname in members:
            members[pname] = dict(sorted(members[pname].items()))
        ds["reference_members"] = dict(sorted(members.items()))
        rec = {
            "synced_at": datetime.now(timezone.utc).isoformat(),
            "source": "https://minefort.com/docs/citadel (live reference "
                      "pages, SSR HTML)",
            "official_llms": "https://minefort.com/docs/citadel/"
                             "llms-full.txt",
            "changes": {k: v for k, v in report.items() if v},
        }
        history = ds.get("_meta", {}).get("history", [])
        if isinstance(ds.get("_meta"), dict) and "history" not in ds["_meta"] \
                and ds["_meta"].get("changes"):
            history.append(ds["_meta"])          # migrate the first record
        history.append(rec)
        ds["_meta"] = {"history": history}
        with open(DS_PATH, "w") as f:
            json.dump(ds, f, indent=1)
        with open(MANIFEST_PATH, "w") as f:
            json.dump(dict(sorted(manifest.items())), f, indent=1)
        with open(URLS_PATH, "w") as f:
            json.dump(sorted(all_urls), f, indent=1)

    # -- report
    print("\n===== SYNC REPORT =====")
    print(f"parents scanned : {report['parents_scanned']}")
    print(f"parents added   : {len(report['parents_added'])} "
          f"{report['parents_added']}")
    print(f"parents gone    : {len(report['parents_gone'])} "
          f"{report['parents_gone']}")
    print(f"parents updated : {len(report['parents_refreshed'])} "
          f"{report['parents_refreshed']}")
    print(f"members added   : {len(report['members_added'])} "
          f"{report['members_added']}")
    print(f"members pruned  : {len(report['members_pruned'])} "
          f"{report['members_pruned']}")
    print(f"members refetch : {len(report['members_refetched'])}")
    print(f"doc pages       : {report['doc_pages_refreshed']}")
    total = sum(len(v) for v in ds["reference_members"].values())
    print(f"dataset members now: {total}")
    return 0


# ------------------------------------------------------------- glue helpers
from bs4 import BeautifulSoup    # noqa: E402


def html_to_article(html: str):
    return BeautifulSoup(html, "html.parser").find("article")


def extract_member_from_html(html: str, url: str):
    return extract_member(html_to_article(html), url)


def extract_parent_from_html(html: str, url: str):
    return extract_parent(html_to_article(html), url)


def save_html(url: str, html: str):
    with open(f"{CRAWL_DIR}/{fname_for(url)}", "w") as f:
        f.write(html)


if __name__ == "__main__":
    sys.exit(main())
