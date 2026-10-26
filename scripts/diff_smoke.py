#!/usr/bin/env python3
"""diff_smoke.py — verify the reconstructed extractor against dataset.json.

Compares every entry the smoke crawl produced with the corresponding entry
in the original scripts/dataset.json, reporting exact-match / first
difference per entry.

Run:  python3 scripts/diff_smoke.py
"""
import json

ROOT = "/home/z/my-project"
real = json.load(open(f"{ROOT}/scripts/dataset.json"))
smoke = json.load(open(f"{ROOT}/scripts/crawl_html_smoke/dataset_smoke.json"))


def cmp(path, a, b, diffs):
    if type(a) is not type(b):
        diffs.append(f"{path}: type {type(a).__name__} != {type(b).__name__}")
        return
    if isinstance(a, dict):
        for k in set(a) | set(b):
            if k not in a:
                diffs.append(f"{path}.{k}: missing in reconstructed")
            elif k not in b:
                diffs.append(f"{path}.{k}: extra in reconstructed")
            else:
                cmp(f"{path}.{k}", a[k], b[k], diffs)
    elif isinstance(a, list):
        if len(a) != len(b):
            diffs.append(f"{path}: len {len(a)} != {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            cmp(f"{path}[{i}]", x, y, diffs)
    elif a != b:
        sa, sb = str(a), str(b)
        at = next((i for i in range(min(len(sa), len(sb)))
                   if sa[i] != sb[i]), min(len(sa), len(sb)))
        diffs.append(f"{path}:\n  real: {sa[max(0, at-40):at+60]!r}\n  new : {sb[max(0, at-40):at+60]!r}")


total, perfect = 0, 0
for kind in ("guides", "docs"):
    for slug in smoke[kind]:
        total += 1
        diffs = []
        cmp(f"{kind}.{slug}", real[kind][slug], smoke[kind][slug], diffs)
        status = "EXACT" if not diffs else f"{len(diffs)} diff(s)"
        if not diffs:
            perfect += 1
        print(f"{kind}.{slug:20s} {status}")
        for d in diffs[:4]:
            print("   ", d.replace("\n", "\n    "))

for name in smoke["reference_parents"]:
    total += 1
    diffs = []
    cmp(f"parents.{name}", real["reference_parents"][name],
        smoke["reference_parents"][name], diffs)
    if not diffs:
        perfect += 1
    print(f"parents.{name:20s} {'EXACT' if not diffs else str(len(diffs)) + ' diff(s)'}")
    for d in diffs[:4]:
        print("   ", d.replace("\n", "\n    "))

for parent, members in smoke["reference_members"].items():
    for member, entry in members.items():
        total += 1
        diffs = []
        cmp(f"members.{parent}.{member}", real["reference_members"][parent][member],
            entry, diffs)
        if not diffs:
            perfect += 1
        print(f"members.{parent}.{member:20s} "
              f"{'EXACT' if not diffs else str(len(diffs)) + ' diff(s)'}")
        for d in diffs[:4]:
            print("   ", d.replace("\n", "\n    "))

print(f"\n{perfect}/{total} entries byte-identical with the original dataset")
