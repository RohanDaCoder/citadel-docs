---
title: "world.get_biome"
description: "Returns the biome name of the column at pos; nil where that chunk is not in memory."
---

Part of [`world`](/ref/World/).

```luau
world.get_biome(pos: Vec3) → string ?
```

Returns the biome name of the column at `pos`; `nil` where that chunk is not in memory.

## Parameters

| Name  | Type                 | Required |
| ----- | -------------------- | -------- |
| `pos` | [`Vec3`](/ref/Vec3/) | yes      |

## Returns

- `string ?`

## Used in

> "world.get_biome(pos) -- the biome name of a column, or nil (chunk not loaded)" — [Blocks and terrain](/world/terrain-generation/)
> "world.get_biome(pos) -- the same for a loaded chunk; nil when it is not loaded" — [Blocks and terrain](/world/terrain-generation/)
