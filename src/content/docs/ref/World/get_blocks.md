---
title: "world.get_blocks"
description: "A box, in x, then z, then y order."
---

Part of [`world`](/ref/World/).

```luau
world.get_blocks(from: Vec3, to: Vec3) → { string ? }
```

A box, in x, then z, then y order.

## Parameters

| Name   | Type                 | Required |
| ------ | -------------------- | -------- |
| `from` | [`Vec3`](/ref/Vec3/) | yes      |
| `to`   | [`Vec3`](/ref/Vec3/) | yes      |

## Returns

- `{ string ? }`

## Used in

> "world.get_blocks(from, to) -- a box of names in one pass" — [Blocks and terrain](/world/terrain-generation/)
> "local box = world.get_blocks(vec3(0, 64, 0), vec3(15, 64, 15)) -- 256 names" — [Blocks and terrain](/world/terrain-generation/)
