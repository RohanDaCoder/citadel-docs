#!/usr/bin/env python3
"""Dump the block column under each live Skript spawn point, exact coords.

For each map: the live spawn (x, y, z, yaw) straight from the Paper Skript,
the schematic (Offset, no SHIFT -> live world), block column = floor of the
coords, blocks from feet+6 down to feet-8. Also shows what the Citadel
coords would be (SHIFT +5,+117,-35) and where the floor-snap Y (arena.luau
`floor`) sits relative to the exact spawn Y.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schem_parse import load, grid, block_at

REF = "/home/z/my-project/scripts/onixmg_citadel/pack/builds"
SHIFT = (5, 117, -35)

# exact live Skript spawns: (map, x, y, z, yaw)  — 1_Spawn.sk / 1_CoreSystem.sk
SPAWNS = [
    ("lobby",     -46.5, -18.0, 38.5, -90),
    ("spleef",      1.5, -20.0, 35.5,  90),
    ("tntrun",    -23.5, -20.0, 38.5,  90),
    ("hotpotato",   1.5, -20.0, 35.5,  90),
    ("sumo",        4.5, -15.0, 33.5,  90),
]

# arena.luau `floor` values (Citadel feet y) for comparison
FLOOR = {"lobby": 97, "spleef": 86, "tntrun": 85, "hotpotato": 67, "sumo": 94}

for name, x, y, z, yaw in SPAWNS:
    path = f"{REF}/OnixMG_state_{name}.schem"
    root = load(path)
    s = root.get("Schematic", root)
    w, h, l, inv, bd = grid(root)
    off = s["Offset"]
    # schematic local (0,0,0) sits at live Offset; local = world - Offset
    bx, bz = math.floor(x) - off[0], math.floor(z) - off[2]
    fy = math.floor(y)
    print(f"=== {name}: live spawn ({x}, {y}, {z}) yaw {yaw}"
          f"  -> Citadel ({x + SHIFT[0]}, {y + SHIFT[1]}, {z + SHIFT[2]})")
    print(f"    arena.luau floor-snap = Citadel y {FLOOR[name]}"
          f"  (exact = {y + SHIFT[1]}, delta {FLOOR[name] - (y + SHIFT[1]):+g})")
    print(f"    column block live x={math.floor(x)} z={math.floor(z)}"
          f"  local({bx},*,{bz})   [player body: feet {fy}, head {fy+1}]")
    nonsolid = ("minecraft:light[", "minecraft:air", "minecraft:structure_void")
    first_solid = None
    for ly in range(fy + 6 - off[1], -1, -1):
        b = block_at(w, h, l, inv, bd, bx, ly, bz)
        solid = b is not None and not b.startswith(nonsolid)
        mark = ""
        if solid and first_solid is None and ly + off[1] < fy:
            first_solid = ly + off[1]      # live block y of landing surface
            mark = "  <- FIRST SOLID (lands on top)"
        if ly + off[1] in range(fy + 6, fy - 9, -1) or mark:
            tag = {fy: "  <- feet", fy - 1: "  <- under feet"}.get(ly + off[1], "")
            print(f"    live y={ly + off[1]:>4}  local y={ly:>3}"
                  f"  citadel y={ly + off[1] + SHIFT[1]:>4}"
                  f"  {(b if b else '(outside)'):40s}{mark}{tag}")
    if first_solid is not None:
        fall = fy - (first_solid + 1)      # feet travel to the top of that block
        print(f"    fall from exact feet y={fy} to {first_solid + 1}:"
              f" {fall} blocks -> {(fall - 3) if fall > 3 else 0} dmg on live")
    else:
        print("    !! no solid block below the spawn in this column")
    print()
