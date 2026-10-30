#!/usr/bin/env python3
"""Batch-download / upload files between a Minefort workload and this container.

Usage:
  onix_fetch.py download <workload_id> <remote_path> <local_path> [<r,l> ...]
  onix_fetch.py upload   <workload_id> <local_path> <remote_path> [<l,r> ...]

Gets a fresh 60s file-transfer token per batch (auto-renews if it expires
mid-batch). Bytes go over HTTPS directly, never through the conversation.
"""
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

MCP = "/home/z/my-project/scripts/minefort_mcp.py"
BASE = "https://files.minefort.com/v1/workloads"


def get_token(workload: str, scope: str = "write") -> str:
    out = subprocess.run(
        [sys.executable, MCP, "call", "file_transfer",
         "--arg", f"workload={workload}"],
        capture_output=True, text=True, timeout=60,
    )
    m = re.search(r"MINEFORT_TOKEN='([^']+)'", out.stdout)
    if not m:
        raise RuntimeError(f"no token in file_transfer output: {out.stdout[:300]} {out.stderr[:300]}")
    tok = m.group(1)
    if scope not in out.stdout.splitlines()[0].lower():
        # token line looks like "Token (write, valid 60s):" — always write scope
        pass
    return tok


def fetch(workload: str, remote: str, local: str, token: str) -> None:
    url = f"{BASE}/{workload}/files/content?path={urllib.parse.quote(remote)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    with open(local, "wb") as f:
        f.write(data)
    print(f"[ok] {remote} -> {local} ({len(data)} bytes)")


def push(workload: str, remote: str, local: str, token: str) -> None:
    url = f"{BASE}/{workload}/files/content?path={urllib.parse.quote(remote)}"
    with open(local, "rb") as f:
        data = f.read()
    req = urllib.request.Request(
        url, data=data, method="PUT",
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/octet-stream"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        r.read()
    print(f"[ok] {local} -> {remote} ({len(data)} bytes)")


def main() -> int:
    if len(sys.argv) < 5:
        print(__doc__)
        return 2
    mode, workload = sys.argv[1], sys.argv[2]
    pairs = sys.argv[3:]
    if mode == "download":
        pairs = [(pairs[i], pairs[i + 1]) for i in range(0, len(pairs), 2)]
    elif mode == "upload":
        pairs = [(pairs[i + 1], pairs[i]) for i in range(0, len(pairs), 2)]
    else:
        print(__doc__)
        return 2
    token = get_token(workload)
    t0 = time.time()
    for remote, local in pairs:
        if time.time() - t0 > 50:  # renew before the 60s window closes
            token = get_token(workload)
            t0 = time.time()
        op = fetch if mode == "download" else push
        op(workload, remote, local, token)
    return 0


if __name__ == "__main__":
    sys.exit(main())
