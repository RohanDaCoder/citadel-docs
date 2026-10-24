---
title: "chunk:fill_biome"
description: "Sets the biome of every column in a box, clipped to the chunk."
---

Part of [`Chunk`](/ref/Chunk/).

```luau
chunk:fill_biome(from: Vec3, to: Vec3, biome: string)
```

Sets the biome of every column in a box, clipped to the chunk.

## Parameters

| Name    | Type                 | Required |
| ------- | -------------------- | -------- |
| `from`  | [`Vec3`](/ref/Vec3/) | yes      |
| `to`    | [`Vec3`](/ref/Vec3/) | yes      |
| `biome` | `string`             | yes      |

## Used in

> "-- chunk:fill_biome(from, to, biome) the biome of each column in a box" — [Blocks and terrain](/world/terrain-generation/)
> "chunk:fill_biome(chunk.min, chunk.max, "jungle") -- each column of a box, clipped to the chunk" — [Blocks and terrain](/world/terrain-generation/)
