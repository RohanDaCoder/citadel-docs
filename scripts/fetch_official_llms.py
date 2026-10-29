#!/usr/bin/env python3
"""fetch_official_llms.py — snapshot the official llms files and cross-check
every API identifier they mention against dataset.json.

WHY THIS EXISTS (live-verified 2026-10-30):
minefort publishes /docs/citadel/llms.txt (index over the 55 prose pages)
and /docs/citadel/llms-full.txt (280 KB flattened markdown of those pages).
The reference layer — the 178 parents / 682 members that generate 850 of
the wiki's 915 pages and all of citadel.d.ts — is NOT in them: the index
has zero /reference/ URLs and the full file has zero Parameters/Returns
blocks. So the per-page HTML sync (sync_official.py) stays for the
reference layer; there is no markdown source for it. What the official
markdown IS good for is a one-request drift probe: every ns.member call
the official prose mentions, diffed against the dataset, surfaces NEW
members the reference-index diff could miss. (The 2026-10-29 sync caught
the network.* migration exactly this way — as a one-off manual pass;
this script automates it.)

Outputs (scripts/official_llms/, tracked):
  llms.txt                — official index snapshot
  minefort-llms-full.txt  — official full markdown snapshot (refreshed)
  official_calls.txt      — real-name ns.member( mentions, Lua stdlib filtered
  official_all_calls.txt  — all <var>:<method>( / ns.member( mentions, raw
  ours_identifiers.txt   — refreshed from dataset.json (parent.member /
                           parent:member by kind, lowercased)

Prints a drift report. Exits 0 when the dataset covers every official
mention, 1 when official mentions identifiers the dataset lacks (those
are fetch candidates for `sync_official.py --sections <ns>`).

Report buckets:
  matched       — dataset covers the call
  known gaps    — the wiki documents them from prose (PIPELINE.md Stage 7
                  gap-fills: task.*, camera.path); no reference page
                  exists, so the sync can never pick them up — allowlisted
  example-local — the namespace is defined INSIDE an official code sample
                  (`local dungeon = world.dimension(...)`,
                  `function steer.fly(...)`, `local kit = ui.kit(...)`),
                  so the call is example code, not the platform API
  candidates    — neither dataset nor known-gap nor example-local: worth
                  a human look and possibly `sync_official.py --sections`

Usage:
  python3 scripts/fetch_official_llms.py
"""
import json
import os
import re
import subprocess
import sys
import time

ROOT = "/home/z/my-project"
BASE = "https://minefort.com"
OUT_DIR = f"{ROOT}/scripts/official_llms"
DS_PATH = f"{ROOT}/scripts/dataset.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

LLMS_INDEX_URL = "/docs/citadel/llms.txt"
LLMS_FULL_URL = "/docs/citadel/llms-full.txt"

# Lua/Luau standard library namespaces: mentions like string.format(
# are the language, not the Citadel API.
LUA_STD = {
    "math", "string", "table", "os", "io", "coroutine", "utf8", "bit32",
    "debug", "pcall", "xpcall", "tostring", "tonumber", "pairs", "ipairs",
    "next", "select", "error", "assert", "print", "require", "type",
    "setmetatable", "getmetatable", "rawget", "rawset", "rawequal",
    "unpack", "loadstring", "collectgarbage", "dofile", "spawn", "wait",
}

# The wiki hand-documents these from the official prose because minefort
# publishes no reference pages for them (PIPELINE.md Stage 7 gap-fills;
# verified 2026-10-30: sync_official.py --sections hub confirmed hub.role
# has no reference page). Flagging them every run would be noise: they are
# known, documented, and unfixable until minefort adds reference pages.
# Coverage: task.* / camera.path -> ref/task, ref/camera;
# hub.role -> systems/hub; bank.* -> systems/commands; buffer.* -> systems/http.
KNOWN_GAPS = {
    "task.cancel", "task.defer", "task.delay", "task.spawn", "task.wait",
    "camera.path",
    "hub.role",
    "bank.bet", "bank.of",
    "buffer.readf64", "buffer.readu8", "buffer.writef64",
}


def fetch_text(url: str, retries: int = 3) -> str | None:
    """curl with a full browser UA (Cloudflare rejects short UAs) and
    retry/back-off, for plain-text endpoints (unlike crawl_citadel.fetch,
    which requires an HTML doctype)."""
    for attempt in range(retries):
        try:
            out = subprocess.run(
                ["curl", "-sS", "-L", "-A", UA,
                 "-H", "Accept: text/plain,text/*",
                 "--max-time", "60", "-w", "\n%{http_code}", BASE + url],
                capture_output=True, text=True, timeout=90)
            if out.returncode != 0:
                raise RuntimeError(f"curl exit {out.returncode}")
            body, _, code = out.stdout.rpartition("\n")
            if code.strip() == "200" and "Just a moment" not in body[:400]:
                return body
            raise RuntimeError(f"HTTP {code.strip()} / challenge page")
        except Exception as e:
            wait = 5 * (attempt + 1)
            print(f"  {url}: {e}; retry in {wait}s", file=sys.stderr)
            time.sleep(wait)
    return None


def extract_calls(md: str) -> tuple[set[str], set[str], set[str]]:
    """Return (real_name_calls, all_call_mentions, example_local_ns) from
    the markdown.

    Real names: lowercase ns.member( with ns >= 3 chars, Lua stdlib
    filtered — e.g. world.on_generate(, commands.add(.
    All mentions: any <var>:<method>( or <ns>.<member>( — includes the
    short example variables (a:cross, b:block) the official code samples
    use, matching the manual pass that produced official_all_calls.txt.
    Example-local namespaces: defined inside a code sample —
    `local dungeon = ...`, `function steer.fly(...)` — so their calls are
    example code, not platform API.
    """
    all_pat = re.compile(r"\b([A-Za-z][A-Za-z0-9_]*)[.:]([a-z_][a-z0-9_]*)\s*\(")
    real_pat = re.compile(r"\b([a-z][a-z0-9_]{2,})\.([a-z_][a-z0-9_]*)\s*\(")
    local_def = re.compile(
        r"\b(?:local\s+([a-z][a-z0-9_]*)\s*=|function\s+([a-z][a-z0-9_]*)\.)" )

    all_mentions = {f"{ns}.{mem}" for ns, mem in all_pat.findall(md)}
    real_calls = {f"{ns}.{mem}"
                  for ns, mem in real_pat.findall(md)
                  if ns not in LUA_STD}
    example_local_ns = {m.group(1) or m.group(2)
                        for m in local_def.finditer(md)}
    return real_calls, all_mentions, example_local_ns


def dataset_identifiers(ds: dict) -> set[str]:
    """One identifier per reference member, in Lua notation by kind:
    methods colon-joined (zone:contains), fields/functions dot-joined
    (world.time), lowercased — the convention of the manual pass."""
    ids = set()
    for parent, members in ds["reference_members"].items():
        p = parent.lower()
        for member, info in members.items():
            sep = ":" if info.get("kind") == "method" else "."
            ids.add(f"{p}{sep}{member}")
    return ids


def main() -> int:
    os.makedirs(OUT_DIR, exist_ok=True)

    index = fetch_text(LLMS_INDEX_URL)
    full = fetch_text(LLMS_FULL_URL)
    if index is None or full is None:
        print("[llms] fetch failed — see retries above")
        return 1

    old_full_path = f"{OUT_DIR}/minefort-llms-full.txt"
    unchanged = (os.path.exists(old_full_path)
                 and open(old_full_path, encoding="utf-8").read() == full)
    with open(f"{OUT_DIR}/llms.txt", "w", encoding="utf-8") as f:
        f.write(index)
    with open(old_full_path, "w", encoding="utf-8") as f:
        f.write(full)

    real_calls, all_mentions, example_local_ns = extract_calls(full)
    with open(f"{OUT_DIR}/official_calls.txt", "w") as f:
        f.write("\n".join(sorted(real_calls)) + "\n")
    with open(f"{OUT_DIR}/official_all_calls.txt", "w") as f:
        f.write("\n".join(sorted(all_mentions)) + "\n")

    ds = json.load(open(DS_PATH))
    ours = dataset_identifiers(ds)
    with open(f"{OUT_DIR}/ours_identifiers.txt", "w") as f:
        f.write("\n".join(sorted(ours)) + "\n")

    # Cross-check: does the dataset cover every real-name official call?
    # (Case-insensitive parent match — the docs use world./World. twins.)
    known = {}
    for ident in ours:
        ns, _, mem = ident.replace(":", ".").rpartition(".")
        known.setdefault(ns, set()).add(mem)
    matched, gaps, locals_, candidates = 0, [], [], []
    for call in sorted(real_calls):
        ns, _, mem = call.rpartition(".")
        if mem in known.get(ns, set()):
            matched += 1
        elif call in KNOWN_GAPS:
            gaps.append(call)
        elif ns in example_local_ns:
            locals_.append(call)
        else:
            candidates.append(call)

    prose_pages = len(re.findall(r"^- ", index, re.M))
    ibytes = len(index.encode())
    fbytes = len(full.encode())
    print(f"=== official llms snapshot ===")
    print(f"llms.txt: {ibytes:,} bytes ({prose_pages} prose entries)")
    print(f"llms-full.txt: {fbytes:,} bytes — "
          f"{'unchanged since last snapshot' if unchanged else 'REFRESHED'}")
    print()
    print(f"=== identifier cross-check ===")
    print(f"official real-name calls: {len(real_calls)} unique")
    print(f"  matched in dataset:     {matched}")
    print(f"  dataset members:        {len(ours)} across "
          f"{len(ds['reference_members'])} parents")
    if gaps:
        print(f"  known gap-fills ({len(gaps)}): "
              f"{', '.join(gaps)}  (documented in the wiki from prose)")
    if locals_:
        print(f"  example-local ({len(locals_)}): "
              f"{', '.join(locals_)}  (defined inside official code samples)")
    if candidates:
        print(f"  CANDIDATES ({len(candidates)}) — not in dataset, not known-gap, "
              f"not example-local:")
        for c in candidates:
            print(f"    {c}")
        print("  -> review; if a reference page exists: "
              "python3 scripts/sync_official.py --sections <ns>")
        return 1
    print("  no new identifiers — dataset covers every official mention")
    return 0


if __name__ == "__main__":
    sys.exit(main())
