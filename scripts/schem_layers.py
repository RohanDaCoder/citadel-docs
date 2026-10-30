#!/usr/bin/env python3
"""Solid-layer histogram for each live OnixMG schematic (fast single pass)."""
import sys
sys.path.insert(0, '/home/z/my-project/scripts')
from schem_parse import load, grid
from collections import Counter

OPEN = {"light", "air", "end_portal", "barrier", "fire"}

for state in ["hotpotato", "spleef", "tntrun", "sumo", "lobby"]:
    p = f'/home/z/my-project/scripts/onixmg_citadel/reference/fawe/OnixMG_state_{state}.schem'
    root = load(p)
    s = root.get("Schematic", root)
    w, h, l, inv, bd = grid(root)
    off = s.get("Offset")
    hist = Counter()
    pos, i, total = 0, 0, w * h * l
    # single pass in order y, z, x
    x = y = z = 0
    val, shift = 0, 0
    while i < total:
        b = bd[pos]
        val |= (b & 0x7F) << shift
        pos += 1
        if not (b & 0x80):
            name = inv.get(val, "?")
            base = name.split('[')[0].replace('minecraft:', '')
            if base not in OPEN:
                hist[y] += 1
            i += 1
            x += 1
            if x >= w:
                x = 0
                z += 1
                if z >= l:
                    z = 0
                    y += 1
            val, shift = 0, 0
        else:
            shift += 7
    print(f"{state}: offset_y={off[1]}  thick solid layers (local y -> world y -> count):")
    for y in sorted(hist):
        if hist[y] > 200:
            print(f"    local {y:>3} world {y+off[1]:>4}  solid {hist[y]}")
