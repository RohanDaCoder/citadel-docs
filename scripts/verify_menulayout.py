#!/usr/bin/env python3
"""Mirror of ui/MenuKit.luau's layout engine, used to verify the slot
layout every menu's configuration produces before deployment."""
import math

def per_row(spacing):
    return math.floor((9 + spacing) / (spacing + 1))

def row_slots(row, k, spacing):
    if k <= 0:
        return []
    width = (k - 1) * (spacing + 1) + 1
    col = math.floor((9 - width) / 2) + 1
    base = (row - 1) * 9
    return [base + col + (i - 1) * (spacing + 1) for i in range(1, k + 1)]

def menu(name, rows, content, nav_count=0, note=""):
    """content: list of (k_items, spacing); returns the slot map."""
    layout = []
    for entry in content:
        k, spacing = entry
        size = per_row(spacing)
        i = 1
        while i <= k:
            chunk = min(size, k - i + 1)
            layout.append((chunk, spacing))
            i += chunk
    if rows is None:
        rows = len(layout) + (1 if nav_count else 0)
    rows = max(1, min(6, rows))
    first = max(1, math.ceil((rows - nav_count - len(layout)) / 2) + 1)
    placed = {}
    for ri, (k, spacing) in enumerate(layout):
        for i, s in enumerate(row_slots(first + ri, k, spacing)):
            placed[s] = f"item{sum(l[0] for l in layout[:ri]) + i + 1}"
    if nav_count:
        for i, s in enumerate(row_slots(rows, nav_count, 1)):
            placed[s] = "nav" + ("back" if i == 0 and nav_count == 1 else str(i + 1))
    # render as chest rows
    print(f"--- {name} (rows={rows}) {note}")
    for r in range(1, rows + 1):
        cells = []
        for c in range(1, 10):
            s = (r - 1) * 9 + c
            v = placed.get(s)
            cells.append(f"{v:>7}" if v else "   .   ")
        print(f"  row {r}: " + " ".join(cells))
    return placed

# AdminMenu: rows=3, one row of 7 buttons spacing 0, close
menu("AdminMenu", 3, [(7, 0)], nav_count=1)
# VoteMenu: auto, 2 votable cards spacing 1
menu("VoteMenu", None, [(2, 1)])
# GameListMenu: rows=3, 4 game cards spacing 1, back
menu("GameListMenu", 3, [(4, 1)], nav_count=1)
# GameStatMenu: rows=3, 3 cards (+ optional 4th) spacing 1, back
menu("GameStatMenu (3 cards)", 3, [(3, 1)], nav_count=1)
menu("GameStatMenu (4 cards)", 3, [(4, 1)], nav_count=1)
# PlayersMenu: auto, grid of 19 heads in cols of 7, back
menu("PlayersMenu (19 heads)", None, [(7, 0), (7, 0), (5, 0)], nav_count=1)
menu("PlayersMenu (4 heads)", None, [(4, 0)], nav_count=1)
# PlayerCardMenu: rows=3, 3 items spacing 1, back
menu("PlayerCardMenu", 3, [(3, 1)], nav_count=1)
# ProfileMenu: rows=3, 3 items spacing 1, close
menu("ProfileMenu", 3, [(3, 1)], nav_count=1)
# AnnounceMenu: rows=3, 3 items spacing 1, back
menu("AnnounceMenu", 3, [(3, 1)], nav_count=1)
# MapStatesMenu: rows=5, absolute slots (Skript 0-based +1)
print("--- MapStatesMenu (rows=5, absolute slots)")
for r in range(1, 6):
    cells = []
    for c in range(1, 10):
        s = (r - 1) * 9 + c
        labels = {11: "lobby", 13: "spleef", 15: "tntrun", 17: "sumo",
                  29: "potato", 31: "soon", 33: "soon", 35: "soon"}
        v = labels.get(s)
        cells.append(f"{v:>7}" if v else "   .   ")
    print(f"  row {r}: " + " ".join(cells))
