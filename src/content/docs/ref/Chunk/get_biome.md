---
title: 'chunk:get_biome'
description: 'Returns the biome of the column at pos, by name; nil outside the chunk'
---

Part of [`Chunk`](/ref/Chunk/).

```luau
chunk:get_biome(pos: Vec3) → string ?
```

Returns the biome of the column at `pos`, by name; `nil` outside the chunk. A biome belongs to a column, so `pos.y` is not read.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `pos` | [`Vec3`](/ref/Vec3/) | yes |

## Returns

- `string ?`

## Used in

> "--   chunk:get_biome(pos)      the biome name there; nil outside the chunk" — [Blocks and terrain](/world/terrain-generation/)
> "chunk:get_biome(pos)                                -- "jungle"; nil outside the chunk" — [Blocks and terrain](/world/terrain-generation/)
