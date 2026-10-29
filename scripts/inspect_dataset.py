#!/usr/bin/env python3
"""Print the schema of scripts/dataset.json — the structured crawl extraction.

Shows top-level keys, per-kind counts, and one truncated sample entry of each
page kind, so the dataset shape is self-documenting.

Run:  python3 scripts/inspect_dataset.py
"""
import json

ROOT = "/home/z/my-project"
ds = json.load(open(f"{ROOT}/scripts/dataset.json"))

print("top-level keys:", list(ds.keys()))
for key, val in ds.items():
    if isinstance(val, dict):
        print(f"\n== {key}: dict with {len(val)} entries; sample keys: {list(val)[:8]}")
        sample_key = next(iter(val))
        sample = val[sample_key]
        print(f"-- sample ['{sample_key}'] keys:", list(sample.keys()) if isinstance(sample, dict) else type(sample))
        print(json.dumps(sample, indent=2)[:1400])
    elif isinstance(val, list):
        print(f"\n== {key}: list with {len(val)} entries")
        if val:
            print("-- sample [0]:", json.dumps(val[0], indent=2)[:1400])
    else:
        print(f"\n== {key}: {type(val).__name__} = {str(val)[:200]}")
