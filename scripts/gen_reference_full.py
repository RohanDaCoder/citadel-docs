#!/usr/bin/env python3
"""gen_reference_full.py — regenerate wiki_src/_sources/reference-full.txt,
the human-readable provenance dump of the reference section of
scripts/dataset.json (one "===== REF: <name> =====" block per parent, JSON
indent=1, blocks separated by a blank line, file starts with a blank line).

Run after any scripts/sync_official.py run that changes reference data:

  python3 scripts/gen_reference_full.py
"""
import json

ROOT = "/home/z/my-project"
OUT = f"{ROOT}/scripts/wiki_src/_sources/reference-full.txt"

parents = json.load(open(f"{ROOT}/scripts/dataset.json"))["reference_parents"]

blocks = []
for name in parents:                      # dataset order (alphabetical)
    blocks.append(f"===== REF: {name} =====\n"
                  + json.dumps(parents[name], indent=1))

with open(OUT, "w") as f:
    f.write("\n\n".join(blocks) + "\n")

print(f"wrote {len(blocks)} REF blocks -> {OUT}")
