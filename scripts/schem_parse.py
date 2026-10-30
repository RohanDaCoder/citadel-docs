#!/usr/bin/env python3
"""Parse Sponge .schem (gzipped NBT) files: header + palette + block grid.

Usage:
  schem_parse.py info <file.schem> [more files...]
  schem_parse.py at <file.schem> <ox> <oy> <oz>   # block at schem-local coords
  schem_parse.py under <file.schem> <ox> <oy> <oz> <shift_x> <shift_y> <shift_z>
      # world (x,y,z) = live coords; prints the block columns near the point,
      # given the schematic's own Offset and a world SHIFT, exactly the way
      # arena.luau places maps (origin = Offset + SHIFT, local = world - origin)
"""
import gzip
import io
import struct
import sys
from collections import Counter

TAG_END, TAG_BYTE, TAG_SHORT, TAG_INT, TAG_LONG, TAG_FLOAT, TAG_DOUBLE = 0, 1, 2, 3, 4, 5, 6
TAG_BYTE_ARRAY, TAG_STRING, TAG_LIST, TAG_COMPOUND, TAG_INT_ARRAY = 7, 8, 9, 10, 11
TAG_LONG_ARRAY = 12


def _payload(tag, data, little):
    end = "<" if little else ">"

    def fmt(n):
        return struct.unpack(end + fmts[tag][0], data.read(fmts[tag][1]))[0] if tag in fmts else None

    if tag == TAG_BYTE:
        return struct.unpack(end + "b", data.read(1))[0]
    if tag == TAG_SHORT:
        return struct.unpack(end + "h", data.read(2))[0]
    if tag == TAG_INT:
        return struct.unpack(end + "i", data.read(4))[0]
    if tag == TAG_LONG:
        return struct.unpack(end + "q", data.read(8))[0]
    if tag == TAG_FLOAT:
        return struct.unpack(end + "f", data.read(4))[0]
    if tag == TAG_DOUBLE:
        return struct.unpack(end + "d", data.read(8))[0]
    if tag == TAG_BYTE_ARRAY:
        n = struct.unpack(end + "i", data.read(4))[0]
        return data.read(n)
    if tag == TAG_STRING:
        n = struct.unpack(end + "H", data.read(2))[0]
        return data.read(n).decode("utf-8", "replace")
    if tag == TAG_LIST:
        t = struct.unpack(end + "B", data.read(1))[0]
        n = struct.unpack(end + "i", data.read(4))[0]
        return [_payload(t, data, little) for _ in range(n)]
    if tag == TAG_COMPOUND:
        out = {}
        while True:
            t = struct.unpack(end + "B", data.read(1))[0]
            if t == TAG_END:
                return out
            n = struct.unpack(end + "H", data.read(2))[0]
            name = data.read(n).decode("utf-8", "replace")
            out[name] = _payload(t, data, little)
    if tag == TAG_INT_ARRAY:
        n = struct.unpack(end + "i", data.read(4))[0]
        return list(struct.unpack(end + f"{n}i", data.read(4 * n)))
    if tag == TAG_LONG_ARRAY:
        n = struct.unpack(end + "i", data.read(4))[0]
        return list(struct.unpack(end + f"{n}q", data.read(8 * n)))
    raise ValueError(f"tag {tag}")


fmts = {}


def load(path):
    raw = open(path, "rb").read()
    data = io.BytesIO(gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw)
    # detect endianness: FAWE/Sponge uses big-endian; some tools little.
    big = data.read(1)[0]
    if big != TAG_COMPOUND:
        raise ValueError("not NBT")
    data.seek(0)
    t = data.read(1)[0]
    n = struct.unpack(">H", data.read(2))[0]
    data.read(n)
    return _payload(t, data, False)


def grid(root):
    """Return (width, height, length, palette list, blockdata byte string)."""
    root = root.get("Schematic", root)
    w, h, l = root["Width"], root["Height"], root["Length"]
    pal = root["Palette"]
    inv = {v: k for k, v in pal.items()}
    bd = root["BlockData"]
    return w, h, l, inv, bd


def block_at(w, h, l, inv, bd, x, y, z):
    if not (0 <= x < w and 0 <= y < h and 0 <= z < l):
        return None
    idx = (y * l + z) * w + x
    # varint scan from 0 to idx
    i, val, shift = 0, 0, 0
    pos = 0
    while True:
        b = bd[pos]
        val |= (b & 0x7F) << shift
        pos += 1
        if not (b & 0x80):
            if i == idx:
                return inv.get(val, f"?{val}")
            i += 1
            val, shift = 0, 0
        else:
            shift += 7


def info(path):
    root = load(path)
    s = root.get("Schematic", root)
    w, h, l, inv, bd = grid(root)
    off = s.get("Offset", [0, 0, 0])
    meta = s.get("Metadata", {}) or {}
    cnt = Counter()
    i, val, shift, pos = 0, 0, 0, 0
    total = w * h * l
    while i < total:
        b = bd[pos]
        val |= (b & 0x7F) << shift
        pos += 1
        if not (b & 0x80):
            cnt[inv.get(val, f"?{val}")] += 1
            i += 1
            val, shift = 0, 0
        else:
            shift += 7
    print(f"--- {path.split('/')[-1]}")
    print(f"  Sponge v{s.get('Version')}  size W{w} H{h} L{l}  offset {off}")
    print(f"  paste-offset meta: {meta.get('WEOffsetX')},{meta.get('WEOffsetY')},{meta.get('WEOffsetZ')}"
          if meta else "", end="")
    print(f"  total {total}")
    print("  blocks:")
    for name, c in sorted(cnt.items(), key=lambda kv: -kv[1])[:28]:
        print(f"    {c:>7}  {name}")
    return s, w, h, l, inv, bd, off


if __name__ == "__main__":
    if sys.argv[1] == "info":
        for p in sys.argv[2:]:
            info(p)
    elif sys.argv[1] in ("at", "under"):
        path = sys.argv[2]
        root = load(path)
        s = root.get("Schematic", root)
        w, h, l, inv, bd = grid(root)
        off = s.get("Offset", [0, 0, 0])
        if sys.argv[1] == "at":
            x, y, z = map(int, sys.argv[3:6])
            print(f"{path.split('/')[-1]} local({x},{y},{z}) = {block_at(w, h, l, inv, bd, x, y, z)}")
        else:
            # world coords + shift: origin = Offset + SHIFT ; local = world - origin
            x, y, z = map(float, sys.argv[3:6])
            sx, sy, sz = map(int, sys.argv[6:9])
            ox, oy, oz = off[0] + sx, off[1] + sy, off[2] + sz
            bx, bz = int(x) - ox, int(z) - oz
            for dy in range(4, -6, -1):
                by = int(y) - oy + dy
                b = block_at(w, h, l, inv, bd, bx, by, bz)
                print(f"  y={int(y)+dy:>4} local({bx},{by},{bz}) {b if b else '(outside)'}")
